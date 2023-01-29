#================================#
#====== C O M M U N I T Y =======#
#================================#
def get_communities(request):
	query = Community.objects.all()
	communitiesFilter = CommunityFilter(request.GET, queryset=query)
	communities = CommunityTable(data = communitiesFilter.qs)
	RequestConfig(request).configure(communities)
	data = {
		'table':communities,
		'filter':communitiesFilter
	}
	return data

@login_required
def list_community(request):
	communitiesData = get_communities(request)
	createURL = '/community/create/'
	context = {
		'page_title': "Communities",
		'add_btn_name' :"Community",
		'table': communitiesData['table'],
		'filter': communitiesData['filter'],
		'create_url':createURL,
		'enable_export':True
	}
	userGroup = request.user.groups.all()
	if (userGroup.filter(name='viewer').exists()):
		communitiesData['table'].exclude = ('delete','edit',)
		context.update({'no_add':True})
	return render(request, 'blog/body.html', context)

@permission_required('blog.add_community', raise_exception=True, login_url='/login/')
def create_community(request):
	if request.method == 'POST': #Form submitted
		form = CommunityForm(request.POST)
	else: #Request "create" form
		form = CommunityForm()
	url = '/community/create/'
	return save_form(request, form, 'forms/partial_create_item.html', url, page_name='community')

@permission_required('blog.change_community', raise_exception=True, login_url='/login/')
def update_community(request, pk):
	community = get_object_or_404(Community, pk=pk)
	if request.method == 'POST': #Form submitted
		form = CommunityForm(request.POST, instance=community)
	else: #Request "update" form
		form = CommunityForm(instance=community)
	url = "/community/"+pk+"/update/"
	return save_form(request, form, 'forms/partial_update_item.html', url, page_name="community")

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

#==================================#
#====== C L A S S B A S E D =======#
#==================================#

class CommunityView(LoginRequiredMixin, ListView):
	model = Community
	filter_class = CommunityFilter
	table_class = CommunityTable
	template_name = 'blog/body.html'
	page_title = 'Commities'

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
			'enable_export':False
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

		#Intialize variables
		self.url = ''
		self.form = ''
		self.template_name = ''
		self.form_is_valid = False

		#Run mixin function to set url, form, template_name and form_is valid
		self.evaluate_posted_form()

		if self.form_is_valid == True: 
			#Save the form and re-draw the list view with the updated items.
			self.form.save()	
			self.response_data['html_item_list'] = self.get_html_items_as_string()
		else: 
			#Reload the form with the applicable error messages.
			self.response_data['html_form'] = render_to_string(
				self.template_name, 
					{'url': self.url, 
					'page_name':self.page_name, 
					'form': self.form
					}, 
				request=request
				)
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

		#Intialize variables
		self.url = ''
		self.form = ''
		self.template_name = ''
		self.form_is_valid = False

		#Run mixin function to set url, form, template_name and form_is valid
		self.evaluate_posted_form()

		if self.form_is_valid == True: 
			#Save the form and re-draw the list view with the updated items.
			self.form.save()	
			self.response_data['html_item_list'] = self.get_html_items_as_string()
		else: 
			#Reload the form with the applicable error messages.
			self.response_data['html_form'] = render_to_string(
				self.template_name, 
					{'url': self.url, 
					'page_name':self.page_name, 
					'form': self.form
					}, 
				request=request
				)
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