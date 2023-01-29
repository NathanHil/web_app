import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
import django
django.setup()

from django_tables2.config import RequestConfig
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.shortcuts import render
from tablib import Dataset
import django_rq
from blog.models import ImportTask, ImportTaskError
from blog.utils import import_with_worker
from datetime import date
from django.http import HttpResponse

class ImportMixin(object):

	def user_has_permission(self):
		"""set the parent class' data attribute with the relevant page name and template url"""
		perm_required = 'blog.add_'+self.page_name
		has_perm = self.request.user.has_perm(perm_required)

		if has_perm:
			self.data.update({
				'page_name': self.page_name, 
				'csv_template_url':'/'+self.page_name+'/template/'
			})
		else:
			self.template = '403.html'
			self.data.update({
				'page_name':'Not Found', 
			})

		return has_perm

	def run_import(self):
		"""Extract info from the request object (which can't be serialized) and send to worker for import"""
		file_format = self.request.POST['file-format']
		resource = self.resource()
		dataset = Dataset() #tablib dateset
		new_items = self.request.FILES['importData']
		dataset.load(new_items.read().decode('utf-8'),format='csv')
		user_id = self.request.user.id

		#Inititalize and save the import task so that it shows up as Pending
		task = ImportTask(user_id=user_id, complete=0)
		task.db_table = resource._meta.model._meta.db_table.replace("blog_", "") # gets associated model's table name 
		task.save()

		# Finalize import as background rq task
		q = django_rq.get_queue("default")
		q.enqueue(import_with_worker, resource, dataset, user_id, task)

		self.data.update({'has_import_message':True})
		self.data.update({'import_message':"<h3>Submitted to server</h3><h5>Please allow a few minutes for the database to update with new imported data</br>Thank you</h5>"})

class ExportMixin(object):
	"""Mix-in to export all entries of the specified object as CSV file"""
	def user_has_permission(self):
		"""set the parent class' data attribute with the relevant page name and template url"""
		has_perm = self.request.user.has_perm('blog.view_'+self.page_name)

		if has_perm:
			self.data.update({
				'page_name': self.page_name, 
				'csv_template_url':'/'+self.page_name+'/template/'
			})
		else:
			self.template = '403.html'
			self.data.update({
				'page_name':'Not Found', 
			})

		return has_perm

	def run_export(self):
		resource = self.resource()
		page_name = self.page_name
		filename = page_name+'_export_'+date.today().strftime("%m%d%Y")+'.csv'
		dataset = resource.export(self.queryset)
		response = HttpResponse(dataset.csv, content_type='text/csv')
		responseString = 'attachment; filename='+filename
		response['Content-Disposition'] = responseString
		return response

	def export_template(self):
		resource = self.resource()
		resource_headers = resource.get_export_headers()
		dataset = Dataset(headers=resource_headers)
		response = HttpResponse(dataset.csv, content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="'+self.page_name+'_template.csv"'
		return response

class CreateUpdateMixin(object):
	"""Mix in to create and update views"""	
	def evaluate_posted_form(self):
		"""Get the posted create or update form. Return the form, url and template name."""
		pk = self.kwargs.get('pk')
		obj = None
		if pk is not None:
			obj = get_object_or_404(self.model, pk=pk)
			self.url = "/"+self.page_name+"/"+pk+"/update/"
			self.form = self.form_class(self.request.POST, instance=obj)
			self.template_name = 'forms/partial_update_item.html'
		else:
			self.url =  "/"+self.page_name+"/create/"
			self.form = self.form_class(self.request.POST)
			self.template_name = 'forms/partial_create_item.html'
		is_valid = self.form.is_valid()
		self.form_is_valid = is_valid
		self.response_data['form_is_valid'] = is_valid
	def get_html_form_with_errors(self):
		"""If the form was not valid, call this function to reload the form with associated errors"""
		return render_to_string(self.template_name, {'url': self.url, 'page_name':self.page_name, 'form': self.form}, request=self.request)
	def get_html_form_as_string(self):
		"""Get the create or update form as a string"""
		pk = self.kwargs.get('pk')
		obj = None
		if pk is not None: #use the update url pattern and template
			obj = get_object_or_404(self.model, pk=pk)
			url = "/"+self.page_name+"/"+pk+"/update/"
			form_template = 'forms/partial_update_item.html'
		else: #use the create url pattern and template
			url = "/"+self.page_name+"/create/"
			form_template = 'forms/partial_create_item.html'
		form = self.form_class(instance=obj)
		return render_to_string(form_template, {'url':url, 'page_name':self.page_name, 'form': form}, request=self.request)	
	def get_html_items_as_string(self):
		"""On succesful post, redraw the parent list view's queryset and pass to its table class. Render template as string"""
		lvc = self.list_view_class()
		query = lvc.get_queryset()
		table = lvc.table_class(data=query)
		RequestConfig(self.request).configure(table)
		return render_to_string('forms/partial_list_items.html', context = {'table':table}, request=self.request)

class DeleteMixin(object):
	def get_form_as_string(self):
		pk = self.kwargs.get('pk')
		obj = get_object_or_404(self.model, pk=pk).__str__()
		url = "/"+self.page_name+"/"+pk+"/remove/"
		return render_to_string('forms/partial_delete_item_v2.html', {'url':url, 'page_name':self.page_name,'obj': obj}, request=self.request)
	def other_function(self):
		data = {}
		status = None
		pk = self.kwargs.get('pk')
		obj = get_object_or_404(self.model, pk=pk)
		url = "/"+self.page_name+"/"+pk+"/delete/"
		try:
			obj.delete()
		except ProtectedError as e:
			data = {
				'code': 'server_error',
				'message': ('Internal server error.'),
				'error': {
					'type': str(type(e)),
					'message': str(e)
				}
			}
			status = 500
			return data, status

		lvc = self.list_view_class()
		query = lvc.get_queryset()
		table = lvc.table_class(data=query)
		RequestConfig(self.request).configure(table)

		context = {'url':url, 'page_name':self.page_name, 'table':table}
		data = {
			'form_is_valid':True, 
			'html_item_list':render_to_string('forms/partial_list_items.html', context, request=self.request), 
			'error': {
				'type':None,
				'message':'No errors'
			}
		}

		status = 200
		return data, status