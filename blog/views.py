import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
import django
django.setup()
import django_rq
from django_rq import job
from django import template
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from tablib import Dataset
# Views
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django_tables2.export.views import ExportMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, FormView, TemplateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2 import SingleTableView, LazyPaginator
from django.core.paginator import Paginator
# Models
from .models import *
from django.db import models
from django.db.models import Sum, Count, IntegerField, F, Max, Aggregate, CharField, ProtectedError, Value, Case, When, FloatField, ExpressionWrapper,DecimalField
from django.db.models.functions import Round, Coalesce
from django.db.models.query_utils import Q
# Tables
import django_tables2 as tables
from .tables import *
from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport
from .filters import *
# Forms
from .forms import *
from django import forms
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
# Resources
from .resources import *
# Authentication
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
# Python 
import datetime
from datetime import date
import time, json

# Other Functions
from .setupTieout import *
from .procoreIntegration import ProcoreIntegration
from .utils import *
from .mixins import CreateUpdateMixin, DeleteMixin, ImportMixin, ExportMixin

#================================#
# G L O B A L  V A R I A B L E S #
#================================#
PAGE_DATA_LIST = {
	'traffic': {'name':'Traffic','resource':TrafficResource(),'model':Traffic,'get':'get_traffics'},
	'loantransaction': {'name':'Loan Transaction','resource':LoanTransactionResource(),'model':LoanTransaction},
	'community': {'name':'Community','resource':CommunityResource(),'model':Community,'get':'get_communities'},
	'lender': {'name':'Lender','resource':'','model':Lender,'get':'get_lenders'},
	'job': {'name':'Job','resource':JobResource(),'update_form':JobUpdateForm(),'model':Job,'get':'get_jobs'},
	'jobfmv': {'name':'Job Fair Market Value','resource':UpdateJobFMVResource(),'model':Job},
	'plan': {'name':'Plan','resource':PlanResource(),'model':Plan,'get':'get_plans'},
	'plat': {'name':'Plat','resource':PlatResource(),'model':Plat,'get':'get_plats'},
	'platplan': {'name':'Plat Plan','resource':'','model':PlatPlan,'get':'get_plans'},
	'baseprice': {'name':'Base Price','resource':UpdateBasePriceResource(),'model':PlatPlan},
	'masterloanpackage': {'name':'Master Loan Package','resource':'','model':MasterLoanPackage,'get':'get_masterloanpackages'},
	'masterloan': {'name':'Master Loan','resource':'','model':MasterLoan,'get':'get_masterloanpackages'},
	'loan': {'name':'Loan','resource':'','model':Loan,'get':'get_jobs'},
	'proformamilestone': {'name':'proformamilestone','resource':ProformaMilestoneResource(),'model':ProformaMilestone},
	'proformamilestonedetail': {'name':'proformamilestonedetail', 'resource':ProformaMilestoneDetailResource()},
	'address': {'name':'address', 'resource':UpdateJobAddressResource()},
	'goal': {'name':'goal', 'resource':GoalResource()},
}

#================================#
#========== M I X I N ===========#
#================================#
class PageTitleMixin(object):
	def get_page_title(self,
	 context):
		return getattr(self, "page_title", "Default Page Title")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["page_title"] = self.get_page_title(context)
		return context


#================================#
#======= U S E R   A U T H ======#
#================================#
def user_login(request):
	return render(request, "registration/login.html")

def user_logout(request):
	return render(request, "registration/logout.html")

#================================#
#=========== H O M E ============#
#================================#

def Home(request): 
	# render function takes argument - request - and returns HTML as response 
	return render(request, "blog/home.html") 


#================================#
#======== P R O C O R E =========#
#================================#

def procore_rq(data):
	p = ProcoreIntegration()
	p.process_webhook(data)

@csrf_exempt
def ProcoreView(request):
	#The request.body element will contain the payload from the webhook
	#Parse the string to a dictionary
	data = json.loads(request.body)

	#Add processing function to queue
	django_rq.enqueue(procore_rq, data)

	return HttpResponse(status=200)

#================================#
#========= E R R O R S ==========#
#================================#
def handler_403(request, exception):# Forbidden
	data = {}
	return render(request, '403.html', data)

def handler_404(request, exception):# Not found
	data = {}
	return render(request, '404.html', data)

def handler_500(request):# Server error
	data = {}
	return render(request, '500.html', data)

#================================#
#== C R U D  O P E R A T I O N ==#
#================================#
class DeleteView(DeleteView):
	def get(self, request, page_name, pk):
		data = dict()
		obj = get_object_or_404(PAGE_DATA_LIST[page_name]['model'], pk=pk)
		url = "/"+page_name+"/"+pk+"/delete/"
		context = {'url':url, 'page_name':page_name}

		data['msg'] = "Hello world!"
		data['html_form'] = render_to_string('forms/partial_delete_item.html', context, request=request)
		return JsonResponse(data)
	def post(self, request, page_name, pk):
		# data = dict()
		obj = get_object_or_404(PAGE_DATA_LIST[page_name]['model'], pk=pk)
		url = "/"+page_name+"/"+pk+"/delete/"

		# data['form_is_valid'] = True  # This is just to play along with the existing code
		# Get table and repopulate the page with updated data
		# table = getattr(PAGE_DATA_LIST[page_name], 'get')()
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
			return JsonResponse(data=data, status=500)

		itemData = globals()[PAGE_DATA_LIST[page_name]['get']](request)
		# table = get_lenders(request)
		context = {'url':url, 'page_name':page_name, 'table':itemData['table']}
		# data['html_item_list'] = render_to_string('forms/partial_list_items.html', context, request=request)
		data = {
			'form_is_valid':True, 
			'html_item_list':render_to_string('forms/partial_list_items.html', context, request=request), 
			'error': {
				'type':None,
				'message':'No errors'
			}
		}
		response = JsonResponse(data=data, status=200)
		
		return response


#================================#
#=== I M P O R T / E X P O R T ==#
#================================#
def run_import(request, context,  page_name, page_data_list):

	template = 'forms/import.html'
	file_format = request.POST['file-format']
	item_resource = page_data_list[page_name]['resource']
	dataset = Dataset()
	new_items = request.FILES['importData']
	imported_data = dataset.load(new_items.read().decode('utf-8'),format='csv')
	result = item_resource.import_data(dataset, dry_run=False, raise_errors=False, collect_failed_rows = True)

	if not result.has_errors():
		# print("No errors")
		valid_rows = result.valid_rows()

		# Build html table with data imported
		rows_diff_html = "<table class='paleblue'>"
		for header in result.diff_headers:
			rows_diff_html += "<th>"+header+"</th>"

		for row in valid_rows:
			rows_diff_html += "<tr class='new_item'>" if row.new_record else "<tr class='update_item'>"
			# print("New Row? ", row.new_record)
			for row_diff in row.diff:
				# print(row_diff)
				rows_diff_html += "<td>"+row_diff+"</td>"
		rows_diff_html += "</table>"

		# Add html table to context
		context.update({'rows_diff_html':rows_diff_html})

		# Finalize import as background rq task
		q = django_rq.get_queue("low")
		q.enqueue(item_resource.import_data, dataset=dataset, dry_run=True)
			
	else: # Result has errors
		# Code added to view any row level errors that were returned. We'll want to display this to the user.
		errors = result.row_errors()
		import_error_list = {} # {row_num:'error', row_num:'error', ...}

		for row_errors in errors: # row_errors = [row, {'list', 'of', 'errors'}]
			row_number = row_errors[0] # 123
			# print('Error occured at row number: ', row_number, 'in the import file')

			for row_error in row_errors[1]: # row_error = {'dict','of','errors'}
				# print("Error description", row_error.error)
				import_error_list[row_number+1] = row_error.error
		# print(import_error_list)
		context.update({'import_errors':import_error_list})
	return render(request, template, context)

class ImportItemsView(View):
	def get(self, request, page_name):
		perm_required = 'blog.add_'+page_name
		user_has_permission = request.user.has_perm(perm_required)
		# Universal import for csv's into the database
		# Define page-specific variables from url's page_name

		if page_name in PAGE_DATA_LIST and user_has_permission: # Page is enabled for imports and user has permission to make changes
			# Define universal variables
			data = dict()
			template = 'forms/import.html'
			context = {
				'page_name':PAGE_DATA_LIST[page_name]['name'], 
				'csv_template_url':'/'+page_name+'/template/'
			}
			data['html_data'] = render_to_string(template, context, request)
		else:
			data = dict()
			# Not found if bad URL, forbidden if user doesn't have permission
			template = '404.html' if user_has_permission else '403.html'
			context = {
				'page_name':'Not Found', 
			}
		return render(request, template, context)
	def post(self, request, page_name):
		perm_required = 'blog.add_'+page_name
		user_has_permission = request.user.has_perm(perm_required)
		if page_name in PAGE_DATA_LIST and user_has_permission:
			data = dict()
			template = 'forms/import.html'
			context = {
				'page_name':PAGE_DATA_LIST[page_name]['name'], 
				'csv_template_url':'/'+page_name+'/template/'
			}

			if request.FILES.get('importData', False) and ".csv" in request.FILES['importData'].name: 
				print("Proper file uploaded")
				print(request.FILES['importData'])
				# q = django_rq.get_queue("low")
				# q.enqueue(run_import, context=context, page_name=page_name, page_data_list=PAGE_DATA_LIST)
				run_import(request, context, page_name, PAGE_DATA_LIST)
				
			else: # Problem with file or no file
				context.update({'import_errors': True})
				context.update({'import_errors_message':"Please select a valid file to import<br/>Filetype must be .csv - Please double check your file and try again"})
		else:
			data = dict()
			# Not found if bad URL, forbidden if user doesn't have permission
			template = '404.html' if user_has_permission else '403.html'
			context = {
				'page_name':'Not Found', 
			}
		return render(request, template, context)

class ExportItemsView(View): #login_required
	def get(self, request, page_name):
		resource = PAGE_DATA_LIST[page_name]['resource']
		filename = page_name+'_export_'+date.today().strftime("%m%d%Y")+'.csv'
		dataset = resource.export()
		response = HttpResponse(dataset.csv, content_type='text/csv')
		responseString = 'attachment; filename='+filename
		response['Content-Disposition'] = responseString
		return response

class ExportTemplateView(View): #login_required
	def get(self, request, page_name):
		if page_name in PAGE_DATA_LIST:
			resource = PAGE_DATA_LIST[page_name]['resource']

			#Get the resource's headers and instantiate a tablib dateset with only the headers and no data
			resource_headers = resource.get_export_headers()
			dataset = Dataset(headers=resource_headers)

			response = HttpResponse(dataset.csv, content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="'+page_name+'_template.csv"'
		else:
			data = dict()
			# Not found if bad URL, forbidden if user doesn't have permission
			template = '404.html'# if user_has_permission else '403.html'
			context = {
				'page_name':'not found', 
			}
			response = render(request, template, context)

		return response

#================================#
#========== F O R M S ===========#
#================================#
def save_form(request, form, template_name, url, page_name):
	data = dict()
	page_data = PAGE_DATA_LIST[page_name]
	if request.method == 'POST': #Create, update, or delete request
		if form.is_valid(): #Validate through model definition
			form.save()
			data['form_is_valid'] = True
			# Get updated list of items with new changes
			itemData = globals()[page_data['get']](request)
			data['html_item_list'] = render_to_string('forms/partial_list_items.html', context = {'table':itemData['table']}, request=request)
		else: #Return invalid flag so form is not submitted
			data['form_is_valid'] = False
	context = {'form':form, 'page_name':page_name, 'url':url}
	data['html_form'] = render_to_string(template_name, context, request=request)
	return JsonResponse(data)

def save_platform(request, form, template_name, url, page_name):
	data = dict()
	page_data = PAGE_DATA_LIST[page_name]
	if request.method == 'POST': #Create, update, or delete request
		if form.is_valid(): #Validate through model definition
			data['form_is_valid'] = True
			form.save()
			plat_id = form.instance.id
			#Get platplans associated and save them
			pps = PlatPlan.objects.filter(plat_id=plat_id)
			for row in pps:
				row.save()
			itemData = globals()[page_data['get']](request)
			# Get updated list of items with new changes
			data['html_item_list'] = render_to_string('forms/partial_list_items.html', { 'table':itemData['table'] }, request=request)
		else: #Return invalid flag so form is not submitted
			data['form_is_valid'] = False
	context = {'form':form, 'page_name':page_name, 'url':url}
	data['html_form'] = render_to_string(template_name, context, request=request)
	return JsonResponse(data)

def Diff(li1, li2):
	return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

def save_masterloanpackageform(request, form, template_name, url, page_name):
	data = dict()
	page_data = PAGE_DATA_LIST[page_name]
	if request.method == 'POST': #Create, update, or delete request
		if form.is_valid(): #Validate through model definition
			data['form_is_valid'] = True
			form.save()

			mlp = form.instance

			#Initialize variables that will be written to multiple loan records
			submission_date = mlp.submission_date
			appraisal_date = mlp.appraisal_date
			lender = mlp.lender
			receive_cash_back = mlp.receive_cash_back

			platplans = mlp.platplans.all()
			plat_ids = set(platplans.values_list('plat_id',flat=True))

			stuff = dict()
			for row in plat_ids:
				stuff[row] = []

			for row in platplans:
				stuff[row.plat_id].append(row.plan_id)

			#Can only loop once for each plat
			for plat_id,plan_ids in stuff.items():

				jobs = Job.objects.filter(plat_id = plat_id).filter(plan_id__in = plan_ids)
				job_ids = list(jobs.values_list('pk',flat=True))
				existing_loans = Loan.objects.filter(job_id__in=job_ids)
				loan_job_ids = list(existing_loans.values_list('job_id',flat=True))
				create_loans = Job.objects.filter(id__in=Diff(job_ids,loan_job_ids))
				print("Showing existing loans to be updated",existing_loans)
				existing_loans.update(
					lender=lender,
					receive_cash_back=receive_cash_back,
					submission_date=submission_date,
					appraisal_date=appraisal_date,
					)
				create_list = []

				for job in create_loans:
					create_list.append(Loan(lender=lender, submission_date = submission_date, appraisal_date = appraisal_date, job=job, receive_cash_back=receive_cash_back))
	
			try:
				objs = Loan.objects.bulk_create(create_list)
			except:
				pass

			itemData = globals()[page_data['get']](request)
			# Get updated list of items with new changes
			data['html_item_list'] = render_to_string('forms/partial_list_items.html', { 'table':itemData['table'] }, request=request)
		else: #Return invalid flag so form is not submitted
			data['form_is_valid'] = False

	context = {'form':form, 'page_name':page_name, 'url':url}
	data['html_form'] = render_to_string(template_name, context, request=request)
	return JsonResponse(data)

#*** @login_required AND @permission_required('<permission>', raise_exception=True, login_url='/login/')***
# These decorators are included in front of any function definition that might view/manipulate data. "raise_exception=True, login_url='/login/'" returns the 403 (forbidden) page when a user tries to access something they're not allowed to.

@login_required
def list_item(request, page_name, enable_export):
	page_data = PAGE_DATA_LIST[page_name]
	itemData = globals()[page_data['get']](request)
	createURL = '/'+page_name+'/create/'
	context = {
		'page_title':page_data['name'],
		'table':itemData['table'],
		'filter':itemData['filter'],
		'create_url':createURL,
		'enable_export':enable_export
	}
	userGroup = request.user.groups.all()
	if (userGroup.filter(name='viewer').exists()):
		itemData['table'].exclude = ('delete', 'edit')
		context.update({'no_add':True})
	return render(request, 'blog/body.html', context)

#================================#
#============ J O B =============#
#================================#
def get_jobs(request):# Build low-impact query to list the jobs
	query = Job.objects.all().select_related('plat','plat__community','plan','loan')
	jobsFilter = JobFilter(request.GET, queryset=query)
	jobs = JobTable(data = jobsFilter.qs)
	RequestConfig(request).configure(jobs)
	data = {
		'table':jobs,
		'filter':jobsFilter
	}
	return data

@login_required
def list_job(request):# Create context for first draw of page
	jobsData = get_jobs(request)
	createURL = '/loan/create/'
	context = {
		'page_title': "Jobs",
		'add_btn_name' :"Loan",
		'table': jobsData['table'],
		'filter': jobsData['filter'],
		'create_url':createURL,
		'no_add': False, #Flag (True) to remove the "add" button from the page
		'enable_export':True,
		'enable_import':False
	}
	userGroup = request.user.groups.all()
	if (userGroup.filter(name='viewer').exists()):
		jobsData['table'].exclude = ('edit',)
	return render(request, 'blog/body.html', context)

@permission_required('blog.change_job', raise_exception=True, login_url='/login/')
def update_job(request, pk):# Get the specified item and save it with its new data
	job = get_object_or_404(Job, pk=pk)
	url = '/job/'+pk+'/update/'
	if request.method == 'POST': #Form submitted
		form = JobUpdateForm(request.POST, instance=job)
	else: #Request "update" form
		form = JobUpdateForm(instance=job)
	return save_form(request, form, 'forms/partial_update_item.html', url, page_name='job')

@login_required
class JobView(PageTitleMixin, SingleTableView): #Used for viewing plan's associated Jobs
	model = Job
	template_name = 'blog/simpletable.html'
	poage_title = "Jobs"
	   
	def get_queryset(self):
		context = {}
		self.plan = get_object_or_404(Plan, id=self.kwargs['plan'])
		query = Job.objects.select_related('plan').filter(plan=self.plan)
		return query

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		t = JobTable2(data = data['job_list'])
		RequestConfig(self.request).configure(t)
		data['table'] = t
		return data


#================================#
#========= L E N D E R ==========#
#================================#
def get_lenders(request):
	query = Lender.objects.all() 
	lendersFilter = LenderFilter(request.GET, queryset=query)
	lenders = LenderTable(data = lendersFilter.qs)
	RequestConfig(request).configure(lenders)
	data = {
		'table':lenders,
		'filter':lendersFilter
	}
	return data

@login_required
def list_lender(request):
	userGroup = request.user.groups.all()
	lenderData = get_lenders(request)
	createURL = '/lender/create/'
	context = {
		'page_title': "Lenders",
		'add_btn_name' :"Lender",
		'table': lenderData['table'],
		'filter': lenderData['filter'],
		'create_url':createURL
	}
	if (userGroup.filter(name='viewer').exists()):
		lenderData['table'].exclude = ('delete','edit',)
		context.update({'no_add':True})
	return render(request, 'blog/body.html', context)

@permission_required('blog.add_lender', raise_exception=True, login_url='/login/')
def create_lender(request):
	if request.method == 'POST': #Form submitted
		form = LenderForm(request.POST)
	else: #Request "create" form
		form = LenderForm()
	url = '/lender/create/'
	return save_form(request, form, 'forms/partial_create_item.html', url, page_name='lender')

@permission_required('blog.change_lender', raise_exception=True, login_url='/login/')
def update_lender(request, pk):
	lender = get_object_or_404(Lender, pk=pk)
	if request.method == 'POST': #Form submitted
		form = LenderForm(request.POST, instance=lender)
	else: #Request "update" form
		form = LenderForm(instance=lender)
	url = "/lender/"+pk+"/update/"
	return save_form(request, form, 'forms/partial_update_item.html', url, page_name='lender')

@permission_required('blog.delete_lender', raise_exception=True, login_url='/login/')
def delete_lender(request, pk):
	lender = get_object_or_404(Lender, pk=pk)
	data = dict()
	url = "/lender/"+pk+"/delete/"
	if request.method == 'POST': #Form submitted
		lender.delete()
		data['form_is_valid'] = True  # This is just to play along with the existing code
		lenderData = get_lenders(request)
		context = {'lender': lender, 'url':url, 'page_name':'lender', 'table':lenderData['table']}
		data['html_item_list'] = render_to_string('forms/partial_list_items.html', context, request=request)
	else: #Get "delete" form
		context = {'lender': lender, 'url':url, 'page_name':'lender'}
		data['html_form'] = render_to_string('forms/partial_delete_item.html', context, request=request)
	return JsonResponse(data)

#================================#
#=========== P L A T ============#
#================================#

def get_plats(request):# Build low-impact query to list the plats
	query = Plat.objects.select_related('community').annotate(from_procore=Case(When(procore_id=None, then=0), default=1))
	platsFilter = PlatFilter(request.GET, queryset=query)
	plats = PlatTable(data = platsFilter.qs)
	RequestConfig(request).configure(plats)
	data = {
		'table':plats,
		'filter':platsFilter
	}
	return data

@login_required
def list_plat(request):# Create context for first draw of page
	platData = get_plats(request)
	createURL = '/plat/create/'
	context = {
		'page_title': "Plats",
		'add_btn_name' :"Plat",
		'table': platData['table'],
		'filter': platData['filter'],
		'no_add':True,
		'create_url':createURL,
		'enable_export':True
	}
	userGroup = request.user.groups.all()
	if (userGroup.filter(name='viewer').exists()):
		platData['table'].exclude = ('delete','edit',)
		context.update({'no_add':True})
	return render(request, 'blog/body.html', context)

@permission_required('blog.add_plat', raise_exception=True, login_url='/login/')
def create_plat(request):# Create form and save it to db if valid
	url = '/plat/create/'
	if request.method == 'POST': #Form submitted
		form = PlatForm(request.POST)
	else: #Request "create" form
		form = PlatForm()
	return save_platform(request, form, 'forms/partial_create_item.html', url, page_name='plat')

@permission_required('blog.change_plat', raise_exception=True, login_url='/login/')
def update_plat(request, pk):# Get the specified item and save it with its new data
	plat = get_object_or_404(Plat, pk=pk)
	url = '/plat/'+pk+'/update/'
	if request.method == 'POST': #Form submitted
		form = PlatForm(request.POST, instance=plat)
	else: #Request "update" form
		form = PlatForm(instance=plat)
	return save_platform(request, form, 'forms/partial_update_item.html', url, page_name='plat')

@permission_required('blog.delete_plat', raise_exception=True, login_url='/login/')
def delete_plat(request, pk):# Get object by id, delete it, rebuild table without item
	plat = get_object_or_404(Plat, pk=pk)
	data = dict()
	url = '/plat/'+pk+'/delete/'
	if request.method == 'POST': #Form submitted
		try:
			plat.delete()
			data['form_is_valid'] = True  # This is just to play along with the existing code
			data['msg'] = "Successfully deleted Plat"
			# Get and rebuild the table when manipulation successfully occurred
			platData = get_plats(request)
			context = {'plats': platData['table'], 'url':url, 'page_name':'plat', 'table':platData['table']}
			data['html_item_list'] = render_to_string('forms/partial_list_items.html', context, request=request)
			response = JsonResponse(data)
		except ProtectedError:
			data['form_is_valid'] = False  # This is just to play along with the existing code
			data['msg'] = "Cannot delete <strong>plat (id: "+pk+")</strong> becuase there is one or more <strong>plan</strong> associated with it"
			response = JsonResponse(data)
			response.status_code = 403
	else: #Get "delete" form
		context = {'plat': plat, 'url':url, 'page_name':'plat'}
		data['html_form'] = render_to_string('forms/partial_delete_item.html',context,request=request)
		response = JsonResponse(data)
	return response

def get_plat_plans(request, pk):
	platplanquery = PlatPlan.objects.filter(plat=pk).annotate(budget=Sum('loantransaction__amount'))
	plat = Plat.objects.get(pk=pk)
	platplans = PlatPlanSubTable(data = platplanquery)
	context = {'id': pk, 'table':platplans, 'table_type':'subtable', 'parent': plat.name, 'table_title':'Plans', 'excluded':['plat','edit'],'page_name':'platplan'}
	userGroup = request.user.groups.all()
	if (userGroup.filter(name='viewer').exists()):
		platplans.exclude = ('edit',)
		context.update({'no_add':True})
	return render(request, 'forms/partial_list_items.html', context)

def update_platplan(request, pk):# Get the specified item and save it with its new data
	platplan = get_object_or_404(PlatPlan, pk=pk)
	plat = get_object_or_404(Plat, id = platplan.plat.id)
	platplans = PlatPlan.objects.select_related('plan').filter(plat_id = plat.id)
	plans = list(platplans.values_list('description',flat=True))
	url = '/platplan/'+pk+'/update/'
	if request.method == 'POST': #Form submitted
		form = PlatPlanFormset(request.POST,form_kwargs={'plans': plans})
	else: #Request "update" form
		form = PlatPlanFormset(queryset=platplans, form_kwargs={'plans': plans})
	return save_form(request, form, 'forms/platplan.html', url, page_name='platplan')


#================================#
#======== T R A F F I C =========#
#================================#
def get_traffics(request):
	query = Traffic.objects.all().select_related('community')
	trafficsFilter = TrafficFilter(request.GET, queryset=query)
	traffics = TrafficTable(data = trafficsFilter.qs)
	RequestConfig(request).configure(traffics)
	data = {
		'table':traffics,
		'filter':trafficsFilter
	}
	return data

@login_required
def list_traffic(request):
	trafficData = get_traffics(request)
	createURL = '/traffic/create/'
	context = {
		'page_title': "Traffic",
		'add_btn_name' :"Traffic",
		'table': trafficData['table'],
		'filter': trafficData['filter'],
		'create_url':createURL,
		'enable_import':False,
		'enable_export':True
	}
	userGroup = request.user.groups.all()
	if (userGroup.filter(name='viewer').exists()):
		trafficData['table'].exclude = ('delete','edit',)
		context.update({'no_add':True})
	return render(request, 'blog/body.html', context)

@permission_required('blog.add_traffic', raise_exception=True, login_url='/login/')
def create_traffic(request):
	url = '/traffic/create/'
	if request.method == 'POST': #Form submitted
		form = TrafficForm(request.POST)
	else: #Request "create" form
		form = TrafficForm()
	return save_form(request, form, 'forms/partial_create_item.html', url, page_name='traffic')

@permission_required('blog.change_traffic', raise_exception=True, login_url='/login/')
def update_traffic(request, pk):
	traffic = get_object_or_404(Traffic, pk=pk)
	url = "/traffic/"+pk+"/update/"
	if request.method == 'POST': #Form submitted
		form = TrafficForm(request.POST, instance=traffic)
	else: #Request "update" form
		form = TrafficForm(instance=traffic)
	return save_form(request, form, 'forms/partial_update_item.html', url, page_name='traffic')

@permission_required('blog.delete_traffic', raise_exception=True, login_url='/login/')
def delete_traffic(request, pk):
	traffic = get_object_or_404(Traffic, pk=pk)
	data = dict()
	url = '/traffic/'+pk+'/delete/'
	if request.method == 'POST': #Form submitted
		try:
			traffic.delete()
			data['form_is_valid'] = True  # This is just to play along with the existing code
			data['msg'] = "Successfully deleted Traffic"
			# Get and rebuild the table when manipulation successfully occurred
			trafficData = get_traffics(request)
			context = {'traffics': trafficData['table'], 'url':url, 'page_name':'traffic', 'table':trafficData['table']}
			data['html_item_list'] = render_to_string('forms/partial_list_items.html', context, request=request)
			response = JsonResponse(data)
		except ProtectedError:
			data['form_is_valid'] = False  # This is just to play along with the existing code
			data['msg'] = "Cannot delete <strong>traffic (id: "+pk+")</strong> becuase there is one or more <strong>community</strong> associated with it"
			response = JsonResponse(data)
			response.status_code = 403

	else: #Get "delete" form
		context = {'traffic': traffic, 'url':url, 'page_name':'traffic'}
		data['html_form'] = render_to_string('forms/partial_delete_item.html',context,request=request)
		response = JsonResponse(data)

	return response


#================================#
#========== P L A N S ===========#
#================================#
def get_plans(request):# Build low-impact query to list the plans
	query = Plan.objects.all()
	planFilter = PlanFilter(request.GET, queryset=query)
	plans = PlanTable(data = planFilter.qs)
	RequestConfig(request).configure(plans)
	data = {
		'table':plans,
		'filter':planFilter
	}
	return data

@login_required
def list_plan(request):# Create context for first draw of page
	platData = get_plans(request)
	createURL = '/plan/create/'
	context = {
		'page_title': "Plans",
		'add_btn_name' :"Plan",
		'table': platData['table'],
		'filter': platData['filter'],
		'create_url':createURL,
		'enable_import':False,
		'enable_export':True
	}
	userGroup = request.user.groups.all()
	if (userGroup.filter(name='viewer').exists()):
		platData['table'].exclude = ('delete','edit',)
		context.update({'no_add':True})
	return render(request, 'blog/body.html', context)

@permission_required('blog.add_plan', raise_exception=True, login_url='/login/')
def create_plan(request):# Create form and save it to db if valid
	url = '/plan/create/'
	if request.method == 'POST': #Form submitted
		form = PlanForm(request.POST)
	else: #Request "create" form
		form = PlanForm()
	return save_form(request, form, 'forms/partial_create_item.html', url, page_name='plan')

@permission_required('blog.change_plan', raise_exception=True, login_url='/login/')
def update_plan(request, pk):# Get the specified item and save it with its new data
	plan = get_object_or_404(Plan, pk=pk)
	url = '/plan/'+pk+'/update/'
	if request.method == 'POST': #Form submitted
		form = PlanForm(request.POST, instance=plan)
	else: #Request "update" form
		form = PlanForm(instance=plan)
	return save_form(request, form, 'forms/partial_update_item.html', url, page_name='plan')

@permission_required('blog.delete_plan', raise_exception=True, login_url='/login/')
def delete_plan(request, pk):# Get object by id, delete it, rebuild table without item
	plan = get_object_or_404(Plan, pk=pk)
	data = dict()
	url = '/plan/'+pk+'/delete/'
	if request.method == 'POST': #Form submitted

		try:
			plan.delete()
			data['form_is_valid'] = True  # This is just to play along with the existing code
			data['msg'] = "Successfully deleted Plan"
			# Get and rebuild the table when manipulation successfully occurred
			platData = get_plans(request)
			context = {'plans': platData['table'], 'url':url, 'page_name':'plan', 'table':platData['table']}
			data['html_item_list'] = render_to_string('forms/partial_list_items.html', context, request=request)
			response = JsonResponse(data)
		except ProtectedError:
			data['form_is_valid'] = False  # This is just to play along with the existing code
			data['msg'] = "Cannot delete <strong>plan (id: "+pk+")</strong> becuase there is one or more <strong>plat</strong> associated with it"
			response = JsonResponse(data)
			response.status_code = 403

	else: #Get "delete" form
		context = {'plan': plan, 'url':url, 'page_name':'plan'}
		data['html_form'] = render_to_string('forms/partial_delete_item.html',context,request=request)
		response = JsonResponse(data)

	return response

def get_plan_jobs(request, pk):
	# Return the html table of the jobs associated with the plan(pk)
	jobQuery = Job.objects.all().select_related('plat','plat__community').filter(plan=pk)
	plan = Plan.objects.get(pk=pk)
	jobs = PlanJobTable(data = jobQuery)
	context = {'id': pk, 'table':jobs, 'table_type':'subtable', 'parent':plan.name, 'table_title':'Jobs', 'excluded':'plan', 'page_name':'plan-job'}
	userGroup = request.user.groups.all()
	if (userGroup.filter(name='viewer').exists()):
		jobs.exclude = ('edit',)
		context.update({'no_add':True})
	return render(request, 'forms/partial_list_items.html', context)

#================================#
#======== P A R T N E R =========#
#================================#
class PartnerCreateView(LoginRequiredMixin, CreateView):
	model = Partner
	fields = ['name']

	def form_valid(self, form):
		return super().form_valid(form)

class PartnerUpdateView(LoginRequiredMixin, UpdateView):
	model = Partner
	fields = ['name']
	
	def form_valid(self, form):
		#form.instance.author = self.request.user #set the author
		return super().form_valid(form) #run form valid method on parent class
		
	def test_func(self):
		return True

#================================#
#====== P L A T   P L A N =======#
#================================#
@login_required
def load_platplans(request):
	community_id = request.GET.get('community')
	plat_list = list(Plat.objects.filter(community_id=community_id).values_list('pk',flat=True))
	platplans = PlatPlan.objects.filter(plat_id__in=plat_list)
	context = {'platplans':platplans}
	return render(request, 'forms/platplan_dropdown_list.html', context)

#================================#
#===== M A S T E R  L O A N =====#
#================================#
def get_masterloanpackages(request):# Build low-impact query to list the platplans
	query = MasterLoanPackage.objects.all().select_related('community','lender')
	masterloanpackages = MasterLoanPackageTable(data = query)
	RequestConfig(request).configure(masterloanpackages)
	data = {
		'table':masterloanpackages,
		'filter':None
	}
	return data

@login_required
def list_masterloanpackage(request):# Create context for first draw of page
	mlpData = get_masterloanpackages(request)
	createURL = '/masterloanpackage/create/'
	context = {
		'page_title': "Master Loan Package",
		'add_btn_name' :"Master Loan Package",
		'table': mlpData['table'],
		'filter': mlpData['filter'],
		'no_add':False,
		'create_url':createURL,
		'enable_import':False,
		'enable_export':False
	}
	userGroup = request.user.groups.all()
	if (userGroup.filter(name='viewer').exists()):
		mlpData['table'].exclude = ('delete','edit',)
		context.update({'no_add':True})
	return render(request, 'blog/body.html', context)

@permission_required('blog.add_masterloanpackage', raise_exception=True, login_url='/login/')
def create_masterloanpackage(request):# Create form and save it to db if valid
	url = '/masterloanpackage/create/'
	if request.method == 'POST': #Form submitted
		form = MasterLoanPackageForm(request.POST)
	else: #Request "create" form
		form = MasterLoanPackageForm()
	return save_masterloanpackageform(request, form, 'forms/create_masterloan.html', url, page_name='masterloanpackage')

@permission_required('blog.change_masterloanpackage', raise_exception=True, login_url='/login/')
def update_masterloanpackage(request, pk):# Get the specified item and save it with its new data
	masterloanpackage = get_object_or_404(MasterLoanPackage, pk=pk)
	url = '/masterloanpackage/'+pk+'/update/'
	if request.method == 'POST': #Form submitted
		form = MasterLoanPackageForm(request.POST,  instance=masterloanpackage)
	else: #Request "update" form
		form = MasterLoanPackageForm(instance=masterloanpackage)
	return save_masterloanpackageform(request, form, 'forms/partial_update_item.html', url, page_name='masterloanpackage')

@permission_required('blog.delete_masterloanpackage', raise_exception=True, login_url='/login/')
def delete_masterloanpackage(request, pk):
	# mlp = MasterLoanPackage.objects.get(pk=pk)
	mlp = get_object_or_404(MasterLoanPackage, pk=pk)
	data = dict()
	url = "/masterloanpackage/"+pk+"/delete/"
	if request.method == 'POST': #Form submitted
		mlp.delete()
		data['form_is_valid'] = True  # This is just to play along with the existing code
		mlpData = get_masterloanpackages(request)
		context = {'masterloanpackage': mlp, 'url':url, 'page_name':'master loan package', 'table':mlpData['table']}
		data['html_item_list'] = render_to_string('forms/partial_list_items.html', context, request=request)
	else: #Get "delete" form
		context = {'masterloanpackage': mlp, 'url':url, 'page_name':'master loan package'}
		data['html_form'] = render_to_string('forms/partial_delete_item.html', context, request=request)
	return JsonResponse(data)

@permission_required('blog.change_masterloan', raise_exception=True, login_url='/login/')
def update_masterloan(request, pk):# Get the specified item and save it with its new data
	masterloan = get_object_or_404(MasterLoan, pk=pk)
	masterloanpackage = get_object_or_404(MasterLoanPackage, id = masterloan.masterloanpackage.id)
	#The ordering by description ensures that the queryset passed to the formset will match the ordering of the "plans" list.
	masterloans = MasterLoan.objects.select_related('platplan').filter(masterloanpackage_id = masterloanpackage.id).order_by('platplan__description')
	plans = list(masterloans.values_list('platplan__description', flat=True))

	url = '/masterloan/'+pk+'/update/'
	if request.method == 'POST': #Form submitted
		form = MasterLoanFormset(request.POST, form_kwargs={'plans': plans})
	else: #Request "update" form
		form = MasterLoanFormset(queryset = masterloans, form_kwargs={'plans': plans})
	return save_form(request, form, 'forms/platplan.html', url, page_name='masterloan')

def get_masterloanpackage_masterloans(request, pk):
	# Return the html table of the masterloans associated with the plat(pk)
	masterloanQuery = MasterLoan.objects.filter(masterloanpackage=pk).select_related('platplan','masterloanpackage').annotate(budget=Sum('platplan__loantransaction__amount'))
	masterloanpackage = MasterLoanPackage.objects.get(pk=pk)
	masterloans = MasterLoanSubTable(data = masterloanQuery)
	context = {'id': pk, 'table':masterloans, 'table_type':'subtable', 'parent':masterloanpackage.lender.name+' - '+pk, 'table_title':'Master Loan', 'excluded':['masterloanpackage','edit'],'page_name':'masterloanpackage-masterloan'}
	userGroup = request.user.groups.all()
	if (userGroup.filter(name='viewer').exists()):
		individualmasterloan.exclude = ('edit',)
		context.update({'no_add':True})
	return render(request, 'forms/partial_list_items.html', context)


#================================#
#=========== L O A N ============#
#================================#
@permission_required('blog.add_loan', raise_exception=True, login_url='/login/')
def create_loan(request):
	if request.method == 'POST': #Form submitted
		formset = LoanForm(request.POST)
	else: #Request "create" form
		formset = LoanForm()
	url = '/loan/create/'
	return save_form(request, formset, 'forms/partial_create_item.html', url, page_name='loan')

@permission_required('blog.change_loan', raise_exception=True, login_url='/login/')
def update_loan(request, job_id):#
	#if the loan already exists, populate its instance in the form for update
	#if the loan does not exist yet, populate an empty form not tied to a loan instance
	loan = Loan.objects.filter(job_id=job_id).first() #this returns none if no loan is found
	url = '/loan/'+job_id+'/update/'
	template_name = 'forms/partial_update_item.html'
	if request.method == 'POST': #Form submitted
		if loan is None:
			#Post the loan that was just created
			formset = LoanForm(request.POST)
			template_name ='forms/partial_create_item.html'
		else:
			formset = LoanUpdateForm(request.POST, instance=loan)

	else: #Request "update" or "create" form
		if loan is None:
			#Initialize the create form and set an initial job id
			formset = LoanForm()
			formset.fields['job'].initial = job_id
			template_name ='forms/partial_create_item.html'
		else:
			formset = LoanUpdateForm(instance=loan)
	return save_form(request, formset, template_name, url, page_name='loan')


#================================#
#========= T I E O U T ==========#
#================================#
class TieoutView(LoginRequiredMixin,View):

	def get(self, request, pk):
		start = time.time() # For testing
		zero = Decimal(0) # Proper type required for Coalesce function
		#Get related objects
		tieout = TieOut.objects.get(id=pk)
		job = Job.objects.select_related('plat').get(id = tieout.job_id)
		job_id = job.id
		pp = PlatPlan.objects.select_related('plat','plan').get(plat_id = job.plat_id, plan_id = job.plan_id)
		plan = Plan.objects.get(id = job.plan_id)
		context = dict()
		context['subtables'] = dict()		
		context['job_number'] = job.number
		
		#Query for open POs
		open_po_query = PurchaseOrder.objects.filter(job_id=job_id).exclude(status=5).annotate(transaction_type=ExpressionWrapper(F('accountingtransaction__Trantyp'),output_field=DecimalField()),amount=ExpressionWrapper(F('accountingtransaction__Tamount'),output_field=DecimalField())
			).values('number','description','date_issued','status').annotate(
			Total_POs=Coalesce(Sum('accountingtransaction__Tamount',filter=Q(accountingtransaction__Trantyp__in=['Committed cost','Aprv cmmtt cst chng']), output_field=DecimalField()),zero),
			Total_Cost=Coalesce(Sum('accountingtransaction__Tamount',filter=Q(accountingtransaction__Trantyp__in=['AP cost']), output_field=DecimalField()),zero),
			Total_Open = Sum('accountingtransaction__Tamount',filter=Q(accountingtransaction__Trantyp__in=['Committed cost','Aprv cmmtt cst chng']), output_field=DecimalField())-Coalesce(Sum('accountingtransaction__Tamount',filter=Q(accountingtransaction__Trantyp__in=['AP cost']), output_field=DecimalField()),zero),
			).exclude(Total_Open=0)

		#SALES OPTION QUERIES
		base_so_query = SalesOption.objects.filter(job_id=job_id, from_spec=0)
		#Query Upgrades without PO
		upgrades_without_po = base_so_query.exclude(code=None, price=0).annotate(transaction_type=F('accountingtransaction__Trantyp'),amount=F('accountingtransaction__Tamount')).values(
				'code','description','price','quantity').annotate(
				po_amount=Coalesce(Sum('accountingtransaction__Tamount',filter=Q(accountingtransaction__Trantyp__in=['Committed cost','Aprv cmmtt cst chng'])),zero)).filter(
					po_amount=zero).aggregate(count=Count('code',distinct=True))['count']

		#Query for unpriced upgrades
		unpriced_upgrades = base_so_query.filter(price=0).count()

		#ACCOUNTING TRANSACTION QUERIES
		#Query the Transactions
		accTrans = AccountingTransaction.objects.select_related('job','costcode','costcode__costcodecategory','purchaseorder').filter(job_id=job_id)

		#Query for unnmapped transactions
		unmapped_count = accTrans.filter(costcode__costcodecategory_id=None, Trantyp__in=['JC cost','AP cost','Committed cost','Aprv cmmtt cst chng']).count()

		#Query for Zero POs & flagged variances
		query = accTrans.filter(
				Trantyp__in=['Committed cost','Aprvd cmmtt cst chng','Original estimate'],costcode__costcodecategory__name='Hard').values(
				'Tphase', 'costcode__description').annotate(
				po_amount=Coalesce(Sum('Tamount', filter=Q(Trantyp__in=['Committed cost','Aprvd cmmtt cst chng']),output_field=DecimalField()),zero),
				estimate_amount=Coalesce(Sum('Tamount', filter=Q(Trantyp__in=['Original estimate']),output_field=DecimalField()),zero),
				variance_amount=Coalesce(Sum('Tamount', filter=Q(Trantyp__in=['Committed cost','Aprvd cmmtt cst chng']) & Q(Tcat__startswith='V'),output_field=DecimalField()),zero),
				)

		zero_pos = query.filter(po_amount=zero).exclude(estimate_amount=zero).aggregate(count=Count('Tphase'))['count']

		flagged_variances = query.annotate(
			diff_amount=F('estimate_amount')-F('po_amount')+F('variance_amount')).exclude(
			Q(diff_amount=zero) | (Q(diff_amount__lt=0.02) & Q(diff_amount__gt=-0.02))).aggregate(
			count=Count('Tphase'))['count']

		aggrTransData = accTrans.aggregate(
			hard_cost=Coalesce(Sum('Tamount',filter=Q(costcode__costcodecategory__name='Hard') & Q(Trantyp__in=['JC cost','AP cost']), output_field=DecimalField()),zero),
			cancelled_pos = Count('purchaseorder_id', filter=Q(Trantyp__in=['Committed cost','Aprvd cmmtt cst chng']) & Q(purchaseorder__status=5), distinct=True),
			hard_budget = Coalesce(Sum('Tamount',filter=Q(costcode__costcodecategory__name='Hard') & Q(Trantyp__in=['Original estimate']), output_field=DecimalField()),zero),
			marketing=Coalesce(Sum('Tamount',filter=Q(costcode__costcodecategory__name='Marketing') & Q(Trantyp__in=['JC cost','AP cost']), output_field=DecimalField()),zero),
			lot_cost=Coalesce(Sum('Tamount',filter=Q(costcode__costcodecategory__name='Lot Cost') & Q(Trantyp__in=['JC cost','AP cost']), output_field=DecimalField()),zero),
			warranty=Coalesce(Sum('Tamount',filter=Q(costcode__costcodecategory__name='Warranty') & Q(Trantyp__in=['JC cost','AP cost']), output_field=DecimalField()),zero),
			financing=Coalesce(Sum('Tamount',filter=Q(costcode__costcodecategory__name__in=['Financing']) & Q(Trantyp__in=['JC cost','AP cost']), output_field=DecimalField()),zero),
			revenue=Coalesce(Sum('Tamount',filter=Q(costcode__costcodecategory__name='Revenue') & Q(Trantyp__in=['JC cost','AP cost']), output_field=DecimalField()),zero),
			permit=Coalesce(Sum('Tamount',filter=Q(costcode__costcodecategory__name='Permit') & Q(Trantyp__in=['JC cost','AP cost']), output_field=DecimalField()),zero),
			concession=Coalesce(Sum('Tamount',filter=Q(costcode__costcodecategory__name='Concessions') & Q(Trantyp__in=['JC cost','AP cost']), output_field=DecimalField()),zero),
			subdivision=Coalesce(Sum('Tamount',filter=Q(costcode__costcodecategory__name='Subdivision') & Q(Trantyp__in=['JC cost','AP cost']), output_field=DecimalField()),zero),
			upgrade_cost=Coalesce(Sum('Tamount',filter=Q(salesoption__from_spec=0) & Q(Trantyp__in=['Committed cost','Aprvd cmmtt cst  chng']), output_field=DecimalField()),zero),
			state_taxes=Coalesce(Sum('Tamount',filter=Q(costcode__costcodecategory__name='Tax') & Q(Trantyp__in=['JC cost','AP cost']),output_field=DecimalField()),zero),
			build_fee=Coalesce(Sum('Tamount',filter=Q(costcode__costcodecategory__name='Build Fee') & Q(Trantyp__in=['JC cost','AP cost']),output_field=DecimalField()),zero),
			inside_sales=Coalesce(Sum('Tamount',filter=Q(costcode__costcodecategory__name='Inside Sales') & Q(Trantyp__in=['JC cost','AP cost']),output_field=DecimalField()),zero),
			outside_sales=Coalesce(Sum('Tamount',filter=Q(costcode__costcodecategory__name='Outside Sales') & Q(Trantyp__in=['JC cost','AP cost']),output_field=DecimalField()),zero),
			misc_closing=Coalesce(Sum('Tamount',filter=Q(costcode__costcodecategory__name='Misc Closing') & Q(Trantyp__in=['JC cost','AP cost']),output_field=DecimalField()),zero),
			)
		   
		#Intialize variables to pass to value items, and use in formulas
		revenue = -aggrTransData['revenue']
		open_po_total = open_po_query.aggregate(total=Coalesce(Sum('Total_Open', output_field=DecimalField()),zero))['total']
		direct_cost = aggrTransData['state_taxes']+aggrTransData['hard_cost'] + open_po_total+ aggrTransData['permit']
		indirect_cost = aggrTransData['subdivision']+aggrTransData['warranty']+aggrTransData['marketing']+aggrTransData['financing']
		net_profit = revenue - direct_cost - indirect_cost - aggrTransData['lot_cost']
		gross_profit = revenue - direct_cost
		lot_profit = job.fmv - aggrTransData['lot_cost']

		#Create the task dictionary and put the items in the correct order
		tasksDict = SetupTieout().order

		#This is where we assign values, [table names]
		tasksDict['review_build_fee'].update({
			'value':aggrTransData['build_fee'],
			'table_name':'Build Fee'
		})
		tasksDict['review_inside_sales'].update({
			'value':aggrTransData['inside_sales'],
			'table_name':'Inside Sales'
		})
		tasksDict['review_outside_sales'].update({
			'value':aggrTransData['outside_sales'],
			'table_name':'Outside Sales'
		})
		tasksDict['review_misc_closing'].update({
			'value':aggrTransData['misc_closing'],
			'table_name':'Misc Closing'
		})
		tasksDict['review_base_price'].update({
			'value':job.base_contract_price,
		})
		tasksDict['review_close_date'].update({
			'value':job.projected_closing_date,
		})
		tasksDict['review_completion_date'].update({
			'value':job.actual_completion_date,
		})
		tasksDict['review_financing'].update({
			'value':aggrTransData['financing'],
			'table_name':'Financing'
		})
		tasksDict['review_hard_cost'].update({
			'value':aggrTransData['hard_cost'],
			'table_name':'Hard'
		})
		tasksDict['review_hard_cost_variance'].update({
			'value':aggrTransData['hard_cost']-aggrTransData['hard_budget'],
		})
		tasksDict['review_levels'].update({
			'value':plan.levels,
		})
		tasksDict['review_lot_cost'].update({
			'value':aggrTransData['lot_cost'],
			'table_name':'Lot Cost'
		})
		tasksDict['review_lot_fmv'].update({
			'value':job.fmv,
		})
		tasksDict['review_lot_premium'].update({
			'value':job.lot_premium,
		})
		tasksDict['review_marketing'].update({
			'value':aggrTransData['marketing'],
			'table_name':'Marketing'
		})
		tasksDict['review_open_pos'].update({
			'value':open_po_total,
			'table_name':'Open PO'
		})
		tasksDict['review_permit'].update({
			'value':aggrTransData['permit'],
			'table_name':'Permit'
		})
		tasksDict['review_plan_name'].update({
			'value':plan.name,
		})
		tasksDict['review_plan_width'].update({
			'value':plan.width,
		})
		tasksDict['review_price_incentive'].update({
			'value': job.concessions,
		})
		tasksDict['review_concessions'].update({
			'value': aggrTransData['concession'],	
			'table_name': 'Concessions'
		})
		tasksDict['review_revenue'].update({
			'value':revenue,
			'table_name':'Revenue'
		}),
		tasksDict['review_sale_date'].update({
			'value':job.actual_sale_date ,
		})
		tasksDict['review_sqft'].update({
			'value':plan.size,
		})
		tasksDict['review_standard'].update({
			'value':pp.standard,
		})
		tasksDict['review_start_date'].update({
			'value':job.actual_start_date,
		})
		tasksDict['review_state_taxes'].update({
			'value':aggrTransData['state_taxes'],
			'table_name': 'Tax'
		})
		tasksDict['review_subdivision'].update({
			'value':aggrTransData['subdivision'],
			'table_name':'Subdivision'
		})
		tasksDict['review_upgrades'].update({
			'value':job.upgrades_price,
			'table_name':'Upgrades'
		})
		tasksDict['review_upgrades_credits'].update({
			'value':job.credits,
		})
		tasksDict['review_upgrade_cost'].update({
			'value': aggrTransData['upgrade_cost'],
			'table_name':'Upgrade Cost'
		})
		tasksDict['review_warranty'].update({
			'value':aggrTransData['warranty'],
			'table_name':'Warranty'
		})
		tasksDict['review_home_profit'].update({
			'value': round(net_profit-lot_profit,2),
		})
		tasksDict['review_lot_profit'].update({
			'value':round(lot_profit,2),
		})
		tasksDict['review_net_profit'].update({
			'value':round(net_profit,2),
		})
		tasksDict['review_upgrade_margin'].update({'value':  None, })
		tasksDict['review_upgrade_profit'].update({'value':  None, })    
		tasksDict['review_cancelled_pos'].update({'value': aggrTransData['cancelled_pos'], 'table_name': 'Cancelled POs'})  
		tasksDict['review_zero_pos'].update({'value': zero_pos, 'table_name': 'Zero POs'})  
		tasksDict['review_unpriced_upgrades'].update({'value': unpriced_upgrades, 'table_name': 'Unpriced Upgrades'})   
		tasksDict['review_flagged_variances'].update({'value': flagged_variances, 'table_name': 'Flagged Variances'})   
		tasksDict['review_upgrades_without_po'].update({'value': upgrades_without_po, 'table_name': 'Upgrades Without PO'})      
		tasksDict['review_unmapped_codes'].update({'value':unmapped_count,'table_name':'Unmapped'})                                               

		if revenue != 0: #pass the item if revenue is zero
			tasksDict['review_direct_cost_margin'].update({'value':round((revenue-direct_cost)/revenue,2),})
			tasksDict['review_direct_cost_ratio'].update({'value':round(direct_cost/revenue,2),})
			tasksDict['review_gross_profit_margin'].update({'value':round((revenue-direct_cost-aggrTransData['lot_cost'])/revenue,2),})
			tasksDict['review_sales_and_marketing_ratio'].update({'value':round((aggrTransData['marketing']+aggrTransData['inside_sales']+aggrTransData['outside_sales'])/revenue,2),}	)
			tasksDict['review_total_lot_and_directs'].update({'value':round((direct_cost+aggrTransData['lot_cost'])/revenue,2),})
			tasksDict['review_indirect_cost_ratio'].update({'value':round(indirect_cost/revenue,2),})
			tasksDict['review_lot_cost_ratio'].update({'value':round(aggrTransData['lot_cost']/revenue,2),})
			tasksDict['review_net_profit_margin'].update({'value':round((net_profit/revenue),2),})

		if plan.size != 0: #pass the item if plan size is zero
			tasksDict['review_base_price_per_sqft'].update({'value':round(job.base_contract_price/plan.size,2),})
			tasksDict['review_hard_cost_per_sqft'].update({'value':round((aggrTransData['hard_cost'] + open_po_total)/plan.size,2),})
			tasksDict['review_net_profit_per_sqft'].update({'value':round(net_profit/plan.size,2),})

		#Run checks. Disable complete fields, add error messages.
		check = CheckTieout(tasksDict)
		tasksDict = check.tasksDict

		#Build kwarg lists
		tasksDictValues = []
		tasksDictNames = []
		tasksDictTableNames = []
		tasksDictDisableComplete = []
		tasksDictErrors = []
		tasksDictCCmapping = []
		for key, value in tasksDict.items():
			tasksDictValues.append(value['value'])
			tasksDictNames.append(key.replace("_"," ").title()) #replace underscores and capitalize the first letter of each word
			tasksDictTableNames.append(value['table_name'])
			tasksDictDisableComplete.append(value['disable_complete_field'])
			tasksDictErrors.append(value['error_msg'])
			tasksDictCCmapping.append(value['has_cc_mapping'])

		#Pass the user list as a kwarg to the formset in oder to avoid duplicate query problems
		tieoutTasks = TieOutTask.objects.select_related('last_updated_by').filter(tieout_id=tieout.id,name__in=list(tasksDict),category__in=['job_detail','revenue','cost']).order_by('form_order')
		user_list = list(tieoutTasks.values_list('last_updated_by__username',flat=True))

		#Populate a dictionary specifying the starting index of each category's set of forms and send to the context
		cat_indexes = {'job_detail':0,'revenue':0, 'cost':0, 'analysis': 0}
		current_cat = ''
		for key, cat in enumerate(tieoutTasks.values_list('category', flat=True)):
			if current_cat != cat:
				current_cat = cat
				cat_indexes[cat] = key
		context['cat_indexes'] = cat_indexes

		#Initialize the formset and add to conext
		context['form'] = TieOutTaskFormset(
			queryset = tieoutTasks, 
			form_kwargs={
				'updated_by':user_list, 
				'task_name': tasksDictNames,
				'value': tasksDictValues, 
				'disable_complete_field':tasksDictDisableComplete, 
				'table_name':tasksDictTableNames,
				'error_msg': tasksDictErrors,
				'has_cc_mapping': tasksDictCCmapping,
				}
		)
		
		context['url'] = '/tieout/'+pk+'/'
		context['page_name'] = str(job.number)+ ' | Tieout 3'

		return render(request, 'blog/tieout3.html', context)

	def post(self, request, pk):
		form = TieOutTaskFormset(request.POST)
		user = request.user
		start = time.time()
		instances = form.save(commit=False)
		for instance in instances:
			instance.last_updated_by = user
			instance.save()
		end = time.time()
		return redirect(self.request.path_info)

class TieoutBreakdown(LoginRequiredMixin,ListView):

	def get(self, request, pk):
		table_name = request.GET.get('table_name', '')
		tieout = TieOut.objects.get(id=pk)
		job = Job.objects.select_related('plat').get(id = tieout.job_id)
		job_id = job.id
		zero = Decimal(0) # Proper type required for Coalesce function

		base_query = AccountingTransaction.objects.select_related('job','costcode','salesoption').filter(job_id=job_id)

		if table_name == "Open PO":
			query = PurchaseOrder.objects.filter(job_id=job_id).exclude(status=5).annotate(transaction_type=F('accountingtransaction__Trantyp'),amount=F('accountingtransaction__Tamount'),
			).values('number','description','date_issued','status','issued_by','vendor').annotate(
			Total_POs=Coalesce(Sum('accountingtransaction__Tamount',filter=Q(accountingtransaction__Trantyp__in=['Committed cost','Aprv cmmtt cst chng']), output_field=DecimalField()),zero),
			Total_Cost=Coalesce(Sum('accountingtransaction__Tamount',filter=Q(accountingtransaction__Trantyp__in=['AP cost']), output_field=DecimalField()),zero),
			Total_Open = Sum('accountingtransaction__Tamount',filter=Q(accountingtransaction__Trantyp__in=['Committed cost','Aprv cmmtt cst chng']), output_field=DecimalField())-Coalesce(Sum('accountingtransaction__Tamount',filter=Q(accountingtransaction__Trantyp__in=['AP cost']), output_field=DecimalField()),zero),
			).exclude(Q(Total_Open=zero) | (Q(Total_Open__lt=0.02) & Q(Total_Open__gt=-0.02)))
			breakdownTable = PurchaseOrderTable(data=query, orderable=False)
		elif table_name == "Upgrades":
			query = SalesOption.objects.filter(job_id=job_id, from_spec=0).annotate(amount=Sum(F('price')*F('quantity')))
			breakdownTable = UpgradesTable(data=query, orderable=False)
		elif table_name == "Upgrade Cost":
			query = base_query.filter(job_id=job_id ,Trantyp__in=['Committed cost','Aprvd cmmtt cst chng'], salesoption__from_spec=0).exclude(salesoption=None)
			breakdownTable = TransactionTable(data=query, attrs={'class':table_name+' paleblue'}, orderable=False)
		elif table_name == "Cancelled POs":
			query = AccountingTransaction.objects.select_related('purchaseorder').filter(job_id=job_id, Trantyp__in=['Committed cost','Aprvd cmmtt cst chng'],purchaseorder__status=5).values('purchaseorder__number','purchaseorder__description').annotate(sage_balance=Sum('Tamount'))
			breakdownTable = CancelledPOTable(data=query, attrs={'class':table_name+' paleblue'}, orderable=False)
		elif table_name == 'Zero POs':
			query = base_query.filter(
				Trantyp__in=['Committed cost','Aprvd cmmtt cst chng','Original estimate','AP cost','JC cost'],costcode__costcodecategory__name='Hard').values(
				'Tphase', 'costcode__description').annotate(
				po_amount=Coalesce(Sum('Tamount', filter=Q(Trantyp__in=['Committed cost','Aprvd cmmtt cst chng']),output_field=DecimalField()),zero),
				estimate_amount=Coalesce(Sum('Tamount', filter=Q(Trantyp__in=['Original estimate']),output_field=DecimalField()),zero),
				cost_amount=Coalesce(Sum('Tamount', filter=Q(Trantyp__in=['AP cost','JC cost']),output_field=DecimalField()),zero),
				).filter(po_amount=zero).exclude(estimate_amount=zero)
			breakdownTable = ZeroPOTable(data=query, attrs={'class':table_name+' paleblue'}, orderable=False)		
		elif table_name == 'Flagged Variances':
			query = base_query.filter(
				Trantyp__in=['Committed cost','Aprvd cmmtt cst chng','Original estimate'], costcode__costcodecategory__name='Hard').values(
				'Tphase','costcode__description').annotate(
				po_amount=Coalesce(Sum('Tamount', filter=Q(Trantyp__in=['Committed cost','Aprvd cmmtt cst chng']),output_field=DecimalField()),zero),
				estimate_amount=Coalesce(Sum('Tamount', filter=Q(Trantyp__in=['Original estimate']),output_field=DecimalField()),zero),
				variance_amount=Coalesce(Sum('Tamount', filter=Q(Trantyp__in=['Committed cost','Aprvd cmmtt cst chng']) & Q(Tcat__startswith='V'),output_field=DecimalField()),zero),
				).annotate(error_amount=F('estimate_amount')-F('po_amount')+F('variance_amount')).exclude(
			Q(error_amount=zero) | (Q(error_amount__lt=0.02) & Q(error_amount__gt=-0.02)))
			breakdownTable = FlaggedVariancesTable(data=query, attrs={'class':table_name+' paleblue'}, orderable=False)
		elif table_name == 'Unpriced Upgrades':
			query = SalesOption.objects.filter(job_id=job_id, from_spec=0, price=0)
			breakdownTable = UnpricedUpgradesTable(data=query, attrs={'class':table_name+' paleblue'}, orderable=False)
		elif table_name == 'Unmapped':
			query = base_query.filter(costcode__costcodecategory_id=None,Trantyp__in=['JC cost','AP cost','Committed cost','Aprv cmmtt cst chng'])
			breakdownTable = TransactionTable(data=query, attrs={'class':table_name+' paleblue'}, orderable=False)
		elif table_name == 'Upgrades Without PO':
			query = SalesOption.objects.filter(job_id=job_id, from_spec=0).exclude(code=None, price=0).annotate(transaction_type=F('accountingtransaction__Trantyp'),amount=F('accountingtransaction__Tamount')).values(
				'code','description','price','quantity').annotate(
				po_amount=Coalesce(Sum('accountingtransaction__Tamount',filter=Q(accountingtransaction__Trantyp__in=['Committed cost','Aprv cmmtt cst chng'])),zero)).filter(
					po_amount=zero)
			breakdownTable = UpgradesWithoutPOTable(data=query, attrs={'class':table_name+' paleblue'}, orderable=False)
		else:
			query = base_query.filter(job_id=job_id ,costcode__costcodecategory__name__in=[table_name],Trantyp__in=['JC cost','AP cost']).order_by('Tphase')
			breakdownTable = TransactionTable(data=query, attrs={'class':table_name+' paleblue'}, orderable=False)

		data = {'html_form':render_to_string('blog/tieout_breakdown.html', {'breakdown':breakdownTable, 'page_name':table_name, 'job_number':job.number}, request=request)}
		return JsonResponse(data)

class TieOutProgressView(LoginRequiredMixin,ListView):
	
	model = TieOut
	table_class = TieOutProgressTable
	filter_class = TieOutProgressFilter
	template_name = 'blog/body.html'
	page_name = 'tieout_progress'
	page_title = 'Tieout 3'

	def get_queryset(self):

		oct_end = datetime.date(2021,10,31)

		query  = self.model.objects.select_related('job__plat__community').filter(
			job__actual_closing_date__gt=oct_end).annotate(
			total_tasks=Count('tieouttask'),
			completed_tasks=Count('tieouttask',filter=Q(tieouttask__complete=1)),
			flagged_tasks=Count('tieouttask',filter=Q(tieouttask__flag=1)),
			remaining_tasks = Count('tieouttask',filter=Q(tieouttask__complete=0)),
			remaining_non_analysis_tasks=Count('tieouttask',filter=Q(tieouttask__category__in=['job_detail','revenue','cost']) & Q(tieouttask__complete=0) ),
			last_update=Max(
				'tieouttask__last_update_date'
				),
			).annotate(
			stage=Case(
				When(remaining_tasks=0,then=Value('Complete')),
				When(remaining_non_analysis_tasks=0,then=Value('Analysis')),
				When(completed_tasks__gt=0, then=Value('In Progress')),
				default=Value('Not Started')

				)
			)
		return query

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		filt = self.filter_class(self.request.GET, queryset=context['object_list'])
		table = self.table_class(data = filt.qs)
		RequestConfig(self.request).configure(table)

		context.update({
			'page_title': self.page_title,
			'page_name': self.page_name,
			'filter': filt,
			'table': table,
			'no_add':True,
			'enable_import':False,
			'enable_export':False
		})

		return context	

class TieoutCostCodeBreakdownView(LoginRequiredMixin, View):
	"""To display cost code level detail for specific tieout task items"""
	model = CostCode
	table_class = CostCodeTable
	template_name = 'blog/tieout_breakdown.html'
	page_title = 'Cost Codes'

	def get(self, request, pk):
		mapping = request.GET.get('mapping','')
		query = self.model.objects.select_related('costcodecategory').filter(costcodecategory__name=mapping) 
		table = CostCodeBreakdownTable(data=query, orderable=False)
		data = {'html_form':render_to_string(self.template_name, {'breakdown':table, 'page_name':self.page_title}, request=request)}
		return JsonResponse(data)

#====================================#
#========= C O S T  C O D E =========#
#====================================#
class CostCodeView(LoginRequiredMixin, ListView):
	model = CostCode
	filter_class = CostCodeFilter
	table_class = CostCodeTable
	template_name = 'blog/body.html'
	page_title = 'Cost Codes'

	def get_queryset(self):
		return self.model.objects.select_related('costcodecategory').exclude(number__startswith='20-').order_by('number')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		filt = self.filter_class(self.request.GET, queryset=context['object_list'])
		table = self.table_class(data = filt.qs)
		RequestConfig(self.request).configure(table)

		context.update({
			'page_title': self.page_title,
			'filter': filt,
			'table': table,
			'no_add':True,
			'enable_import':False,
			'enable_export':False
		})

		return context

class CostCodeUpdateView(LoginRequiredMixin, CreateUpdateMixin, View):
	list_view_class = CostCodeView
	model = CostCode
	form_class = CostCodeForm
	page_name = 'costcode'
	response_data = dict()

	def get(self, request, pk):
		self.response_data['html_form'] = self.get_html_form_as_string()
		return JsonResponse(self.response_data)

	def post(self, request, pk):
		#Run mixin function to set url, form, template_name and form_is valid
		self.evaluate_posted_form()

		if self.form_is_valid == True: 
			#Save the form and re-draw the list view with the updated items.
			self.form.save()
			self.response_data['html_item_list'] = self.get_html_items_as_string()
		else: 
			#Reload the form with the applicable error messages.
			self.response_data['html_form'] = self.get_html_form_with_errors()
		return JsonResponse(self.response_data)

#================================#
#====== C O M M   P L A N =======#
#================================#
@login_required
def load_communityplans(request):
	community_id = request.GET.get('community')
	community_list = list(Community.objects.filter(id=community_id).values_list('pk',flat=True))
	communityplans = CommunityPlan.objects.filter(community_id__in=community_list)
	context = {'communityplans':communityplans}
	return render(request, 'forms/commplan_dropdown_list.html', context)

#================================#
#====== C O M M   P L A T =======#
#================================#
@login_required
def load_communityplats(request):
	community_id = request.GET.get('community')
	plats = Plat.objects.filter(community=community_id)
	context = {'plats':plats}
	return render(request, 'forms/commplat_dropdown_list.html', context)

#====================================#
#========= P R O F O R M A ==========#
#====================================#

class ProformaMilestoneView(LoginRequiredMixin, ListView):
	model = ProformaMilestone
	filter_class = ProformaMilestoneFilter
	table_class = ProformaMilestoneTable
	template_name = 'blog/body.html'
	page_title = 'Proforma Milestones'
	export_data = [
		{'name': 'Milestones','url': '/proformamilestone/export/data'},
		{'name': 'Milestone detail','url': '/proformamilestonedetail/export/data'},
		]

	def get_queryset(self):
		return self.model.objects.select_related('community')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		filt = self.filter_class(self.request.GET, queryset=context['object_list'])
		table = self.table_class(data = filt.qs)
		RequestConfig(self.request).configure(table)

		context.update({
			'page_title': self.page_title,
			'export_data': self.export_data,
			'create_url': 'create',
			'filter': filt,
			'table': table,
			'no_add':False,
		})

		return context

class ProformaMilestoneCreateView(LoginRequiredMixin,CreateUpdateMixin,View):
	list_view_class = ProformaMilestoneView
	model = ProformaMilestone
	form_class = ProformaMilestoneForm
	page_name = 'proformamilestone'
	response_data = dict()

	def get(self, request, pk=None):
		self.response_data['html_form'] = self.get_html_form_as_string()
		return JsonResponse(self.response_data)

	def post(self, request, pk=None):
		#Run mixin function to set url, form, template_name and form_is valid
		self.evaluate_posted_form()

		if self.form_is_valid == True: 
			#Save the form and re-draw the list view with the updated items.
			self.form.save()	
			self.response_data['html_item_list'] = self.get_html_items_as_string()
		else: 
			#Reload the form with the applicable error messages.
			self.response_data['html_form'] = self.get_html_form_with_errors()

		return JsonResponse(self.response_data)

class ProformaMilestoneUpdateView(LoginRequiredMixin,CreateUpdateMixin,View):
	list_view_class = ProformaMilestoneView
	model = ProformaMilestone
	form_class = ProformaMilestoneForm
	page_name = 'proformamilestone'
	response_data = dict()

	def get(self, request, pk):
		self.response_data['html_form'] = self.get_html_form_as_string()
		return JsonResponse(self.response_data)

	def post(self, request, pk):
		#Run mixin function to set url, form, template_name and form_is valid
		self.evaluate_posted_form()

		if self.form_is_valid == True: 
			#Save the form and re-draw the list view with the updated items.
			self.form.save()	
			self.response_data['html_item_list'] = self.get_html_items_as_string()
		else: 
			#Reload the form with the applicable error messages.
			self.response_data['html_form'] = self.get_html_form_with_errors()

		return JsonResponse(self.response_data)

class ProformaMilestoneDeleteView(LoginRequiredMixin,DeleteMixin, View):
	model = ProformaMilestone
	list_view_class = ProformaMilestoneView
	page_name = 'proformamilestone'
	data = dict()

	def get(self, request, pk):
		self.data['html_form'] = self.get_form_as_string()
		return JsonResponse(self.data)

	def post(self,request, pk):
		self.data, status = self.other_function()
		return JsonResponse(self.data, status=status)

class ProformaMilestoneExportView(View): 
	resource = ProformaMilestoneResource
	page_name = 'proformamilestone'

	def get(self, request):
		resource = self.resource()
		filename = self.page_name+'_export_'+date.today().strftime("%m%d%Y")+'.csv'
		dataset = resource.export()
		response = HttpResponse(dataset.csv, content_type='text/csv')
		responseString = 'attachment; filename='+filename
		response['Content-Disposition'] = responseString
		return response

class ProformaMilestoneImportView(ImportMixin, View):

	page_name = 'proformamilestone'
	template = 'forms/import.html'
	resource = ProformaMilestoneResource
	data = dict()

	def get(self, request):
		self.user_has_permission() #Mixin function
		self.data.update({'has_import_message':False})
		return render(request, self.template, self.data)

	def post(self, request):
		if self.user_has_permission(): # Mixin function
			if request.FILES.get('importData', False) and ".csv" in request.FILES['importData'].name: 
				self.run_import() #Mixin function		
		return render(request, self.template, self.data)

class ProformaMilestoneDetailExportView(View): 
	resource = ProformaMilestoneDetailResource
	page_name = 'proformamilestonedetail'

	def get(self, request):
		resource = self.resource()
		filename = self.page_name+'_export_'+date.today().strftime("%m%d%Y")+'.csv'
		dataset = resource.export()
		response = HttpResponse(dataset.csv, content_type='text/csv')
		responseString = 'attachment; filename='+filename
		response['Content-Disposition'] = responseString
		return response

class ProformaMilestoneDetailImportView(ImportMixin, View):

	page_name = 'proformamilestonedetail'
	template = 'forms/import.html'
	resource = ProformaMilestoneDetailResource
	data = dict()

	def get(self, request):
		self.user_has_permission() #Mixin function
		self.data.update({'has_import_message':False})
		return render(request, self.template, self.data)

	def post(self, request):
		if self.user_has_permission(): # Mixin function
			if request.FILES.get('importData', False) and ".csv" in request.FILES['importData'].name: 
				self.run_import() #Mixin function	
		return render(request, self.template, self.data)

def get_proformamilestone_details(request, pk):
	# Return the html table of the masterloans associated with the plat(pk)
	planQuery = ProformaMilestoneDetail.objects.select_related("proformamilestone", "communityplan").filter(proformamilestone=pk)
	proformaMilestone = ProformaMilestone.objects.get(pk=pk)
	proformaMilestoneTable = ProformaMilestoneSubtable(data = planQuery)
	context = {'id': pk, 'table':proformaMilestoneTable, 'table_type':'subtable', 'parent':proformaMilestone.name+' - '+pk, 'table_title':'Plans', 'excluded':['proformamilestone', 'communityplan'],'page_name':'proformamilestone-plans'}
	userGroup = request.user.groups.all()
	if (userGroup.filter(name='viewer').exists()):
		individualproformamilestone.exclude = ('edit',)
		context.update({'no_add':True})
	return render(request, 'forms/partial_list_items.html', context)

#================================#
#====== C O M M U N I T Y =======#
#================================#
class CommunityView(LoginRequiredMixin, ListView):
	model = Community
	filter_class = CommunityFilter
	table_class = CommunityTable
	template_name = 'blog/body.html'
	page_title = 'Communities'

	def get_queryset(self):
		return self.model.objects.all()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		filt = self.filter_class(self.request.GET, queryset=context['object_list'])
		table = self.table_class(data = filt.qs)
		RequestConfig(self.request).configure(table)

		context.update({
			'page_title': self.page_title,
			'create_url': 'create',
			'filter': filt,
			'table': table,
			'no_add':False,
			'enable_import':False,
			'enable_export':True
		})

		return context

class CommunityCreateView(LoginRequiredMixin,CreateUpdateMixin,View):
	list_view_class = CommunityView
	model = Community
	form_class = CommunityForm
	page_name = 'community'
	response_data = dict()

	def get(self, request, pk=None):
		self.response_data['html_form'] = self.get_html_form_as_string()
		return JsonResponse(self.response_data)

	def post(self, request, pk=None):
		#Run mixin function to set url, form, template_name and form_is valid
		self.evaluate_posted_form()

		if self.form_is_valid == True: 
			#Save the form and re-draw the list view with the updated items.
			self.form.save()
			community_id = self.form.instance.id
			#Get communityplans associated and save them
			cps = CommunityPlan.objects.select_related('community').filter(community_id=community_id)
			for row in cps:
				row.save()

			self.response_data['html_item_list'] = self.get_html_items_as_string()
		else: 
			#Reload the form with the applicable error messages.
			self.response_data['html_form'] = self.get_html_form_with_errors()

		return JsonResponse(self.response_data)

class CommunityUpdateView(LoginRequiredMixin,CreateUpdateMixin,View):
	list_view_class = CommunityView
	model = Community
	form_class = CommunityForm
	page_name = 'community'
	response_data = dict()

	def get(self, request, pk):
		self.response_data['html_form'] = self.get_html_form_as_string()
		return JsonResponse(self.response_data)

	def post(self, request, pk):
		#Run mixin function to set url, form, template_name and form_is valid
		self.evaluate_posted_form()

		if self.form_is_valid == True: 
			#Save the form and re-draw the list view with the updated items.
			self.form.save()
			community_id = self.form.instance.id
			#Get communityplans associated and save them
			cps = CommunityPlan.objects.select_related('community').filter(community_id=community_id)
			for row in cps:
				row.save()

			self.response_data['html_item_list'] = self.get_html_items_as_string()
		else: 
			#Reload the form with the applicable error messages.
			self.response_data['html_form'] = self.get_html_form_with_errors()

		return JsonResponse(self.response_data)

class CommunityDeleteView(LoginRequiredMixin,DeleteMixin, View):
	model = Community
	list_view_class = CommunityView
	page_name = 'community'
	data = dict()

	def get(self, request, pk):
		self.data['html_form'] = self.get_form_as_string()
		return JsonResponse(self.data)

	def post(self,request, pk):
		self.data, status = self.other_function()
		return JsonResponse(self.data, status=status)

class CommunityDetailView(LoginRequiredMixin, DetailView):
    model = Community
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        job_count = len(Job.objects.select_related('plat').filter(plat__community__id=self.object.id))
        plans = set(self.object.plans.all().values_list('full_name',flat=True))

        context.update({'job_count': job_count, 'plans': plans })
        return context

#===================================#
#====== I M P O R T  T A S K =======#
#===================================#
class ImportTaskView(LoginRequiredMixin, ListView):
	model = ImportTask
	# filter_class = ImportTaskFilter
	table_class = ImportTaskTable
	template_name = 'blog/body.html'
	page_title = 'Import task history'

	def get_queryset(self):
		return self.model.objects.select_related('user').filter(user_id=self.request.user.id)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# filt = self.filter_class(self.request.GET, queryset=context['object_list'])
		table = self.table_class(data = context['object_list'])
		RequestConfig(self.request).configure(table)

		context.update({
			'page_title': self.page_title,
			'create_url': 'create',
			# 'filter': filt,
			'table': table,
			'no_add':True,
		})

		return context

class ImportTaskErrorView(LoginRequiredMixin, ListView):
	model = ImportTaskError
	# filter_class = ImportTaskFilter
	table_class = ImportTaskErrorTable
	template_name = 'blog/body.html'
	page_title = 'Import task errors'

	def get_queryset(self):
		return self.model.objects.select_related('importtask').filter(importtask_id=self.kwargs['pk']).order_by('row_number')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# filt = self.filter_class(self.request.GET, queryset=context['object_list'])
		table = self.table_class(data = context['object_list'])
		RequestConfig(self.request).configure(table)

		context.update({
			'page_title': self.page_title,
			'create_url': 'create',
			# 'filter': filt,
			'table': table,
			'no_add':True,
		})

		return context


class JobAddressImportView(LoginRequiredMixin, ImportMixin, View):
	page_name = 'job'
	template = 'forms/import.html'
	resource = UpdateJobAddressResource
	data = dict()
	
	def get(self, request):
		self.user_has_permission() #Mixin function
		self.data.update({'has_import_message':False})
		return render(request, self.template, self.data)

	def post(self, request):
		if self.user_has_permission(): # Mixin function
			if request.FILES.get('importData', False) and ".csv" in request.FILES['importData'].name: 
				self.run_import() #Mixin function	
		return render(request, self.template, self.data)

class LoanTransactionImportView(LoginRequiredMixin, ImportMixin, View):
	page_name = 'loantransaction'
	template = 'forms/import.html'
	resource = LoanTransactionResource
	data = dict()

	def get(self, request):
		self.user_has_permission() #Mixin function
		self.data.update({'has_import_message':False})
		return render(request, self.template, self.data)

	def post(self, request):
		if self.user_has_permission(): # Mixin function
			if request.FILES.get('importData', False) and ".csv" in request.FILES['importData'].name: 
				self.run_import() #Mixin function	
		return render(request, self.template, self.data)

class ImportCostCodes(View, LoginRequiredMixin): #login_required
	def get(self, request, pk=None):

		dataset = import_cost_codes(pk)

		response = HttpResponse(dataset.csv, content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="'+'budget_import.csv"'
		return response

class GoalImportView(LoginRequiredMixin, ImportMixin, View):
	page_name = 'goal'
	template = 'forms/import.html'
	resource = GoalResource
	data = dict()

	def get(self, request):
		self.user_has_permission() #Mixin function
		self.data.update({'has_import_message':False})
		return render(request, self.template, self.data)

	def post(self, request):
		if self.user_has_permission(): # Mixin function
			if request.FILES.get('importData', False) and ".csv" in request.FILES['importData'].name: 
				self.run_import() #Mixin function	
		return render(request, self.template, self.data)

class TrafficImportView(LoginRequiredMixin, ImportMixin, View):
	page_name = 'traffic'
	template = 'forms/import.html'
	resource = TrafficResource
	data = dict()

	def get(self, request):
		self.user_has_permission() #Mixin function
		self.data.update({'has_import_message':False})
		return render(request, self.template, self.data)

	def post(self, request):
		if self.user_has_permission(): # Mixin function
			if request.FILES.get('importData', False) and ".csv" in request.FILES['importData'].name: 
				self.run_import() #Mixin function	
		return render(request, self.template, self.data)


class LoanTransactionDetailView(LoginRequiredMixin, ListView):
	model = LoanTransaction
	table_class = LoanTransactionDetailTable
	template_name = 'blog/loantransaction_detail.html'
	page_title = 'Plat Plan Budget'

	def get_queryset(self):
		platplan_id = self.kwargs.get('platplan')
		self.platplan_description = PlatPlan.objects.get(pk=platplan_id).description
		# queryset = self.model.objects.select_related('purchasingactivity','user').filter(platplan_id=platplan_id).values('purchasingactivity__name','purchasingactivity__costcode__number').annotate(amount=Sum('amount'), last_update=Max('date_stamp')).order_by('purchasingactivity__name')
		queryset = self.model.objects.select_related('purchasingactivity','user','purchasingactivity__costcode').filter(platplan_id=platplan_id).order_by('purchasingactivity__name','-date_stamp','-id')
		self.total_budget = queryset.aggregate(Sum('amount'))['amount__sum']
		return queryset
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		table = self.table_class(data = context['object_list'])

		context.update({
			'page_title': self.page_title,
			'platplan':self.platplan_description,
			'total_budget':self.total_budget,
			'table': table,
			'enable_export': True
		})

		return context

class LoanTransactionExportView(LoginRequiredMixin, ExportMixin, View):
	resource = LoanTransactionResource
	page_name = 'LoanTransactions'
	data = dict()
	queryset = None

	def get(self, request, platplan):
		platplan_id = self.kwargs.get('platplan')
		self.queryset = self.resource._meta.model.objects.select_related('platplan','purchasingactivity').filter(platplan_id=platplan_id).order_by('purchasingactivity')

		return self.run_export()

class JobImportView(LoginRequiredMixin, ImportMixin, View):
	page_name = 'job'
	template = 'forms/import.html'
	resource = JobResource
	data = dict()

	def get(self, request):
		self.user_has_permission() #Mixin function
		self.data.update({'has_import_message':False})
		return render(request, self.template, self.data)

	def post(self, request):
		if self.user_has_permission(): # Mixin function
			if request.FILES.get('importData', False) and ".csv" in request.FILES['importData'].name: 
				self.run_import() #Mixin function	
		return render(request, self.template, self.data)



