import requests
from .models import Community, Plat
from django.db import IntegrityError
import pandas as pd
import logging

logger = logging.getLogger('rq.worker')

class ProcoreIntegration:
	#'web app field': 'procore field'
	plat_mapping = {
		'name': 'name',
		'project_status': 'stage',
		'procore_id': 'id',
	}
	community_mapping = {
		'name':'name',
		'procore_id':'id'
	}

	base_url = 'https://api.procore.com/rest/v1.0/'
	procore_company_id = '562949953434271'


	def __init__(self):
		self.bearer_code = ''
		#Get intial bearer token
		self.refresh_token()
		#Set required headers
		self.headers = {
			'Procore-Company-ID':self.procore_company_id,
			'Authorization': 'Bearer '+self.bearer_code
		}

	def token_is_ok(self):
		# Process request
		url= 'https://login.procore.com/oauth/token/info'
		r = requests.get(url, headers=self.headers)

		# Log the data received from the call (whether it's ok or not)
		logging.info("\nTOKEN STATUS")
		if r.ok:
			logging.info("Token Valid")
		else:
			logging.debug("Token invalid")

		return r.ok
		
	#Retrieves an access token
	def refresh_token(self):
		url = 'https://login.procore.com/oauth/token'
		data = {
			'grant_type': 'client_credentials',
			'client_id': '4bf2464567c5c8a4122e530d9fbc87f0533a089a0e31f38cd45438b082742b7b',
			'client_secret': '006b2a62d6f8a2dc45edab886b29345cbc1ae8e06db85d9394db6ef3968bad58'
		}
		r = requests.post(url, data=data)
		self.bearer_code = r.json()['access_token']
	
	#PLAT OPERATIONS
	def handle_plat(self, data, event_type):
		"""Attempts to create or update plat record. Returns 'created','updated' or error code"""	
		status = None
		try:		
			community = Community.objects.get(procore_id=data['program']['id'])	# this could fail if the program is not set up
			procore_id=data['id']
			name=data['name']
			project_status=data['project_stage']['name']
			active=data['active']
			#If project type isn't specified, it's not even shown in the endpoint JSON, unlike project lot count
			project_type_parent = data.get('project_type')	
			if project_type_parent is None:
				project_type = None
			else:
				project_type = project_type_parent.get('name')
			community_id=community.id
			project_lot_count=data['custom_fields']['custom_field_34770']['value']
			pahlisch_lot_count = data['custom_fields']['custom_field_50531']['value']

			if event_type == 'create':
				Plat.objects.create(
					procore_id=procore_id,
					name=name,
					project_status=project_status,
					active=active,
					project_type=project_type,
					community_id=community_id,
					project_lot_count=project_lot_count,
					pahlisch_lot_count = pahlisch_lot_count
					)	
				status = 'created'
			elif event_type == 'update':			
				p = Plat.objects.filter(procore_id=procore_id).first()		
				if p is None: #If the plat doesn't exist yet because it failed at the created stage, we need to create it here.
					Plat.objects.create(
						procore_id=procore_id,
						name=name,
						project_status=project_status,
						active=active,
						project_type=project_type,
						community_id=community_id,
						project_lot_count=project_lot_count,
						pahlisch_lot_count=pahlisch_lot_count
					)
				else:
					p.name = name
					p.project_status = project_status
					p.project_type = project_type
					p.active=active
					p.community_id = community_id
					p.project_lot_count=project_lot_count
					p.pahlisch_lot_count = pahlisch_lot_count
					p.save()
				status='updated'
		except Exception as e:
			print(e)
			logger.exception("Error occurred")
			status=e
		return status

	def delete_plat(self, record_id):
		"""Attempts to delete plat record. Returns 'deleted' or error code"""
		status = None
		try:
			p = Plat.objects.get(procore_id=record_id)
			p.delete()
			status = 'deleted'
		except Exception as e:
			logger.exception("Error occurred")
			status = e
		return status

	#COMMUNITY OPERATIONS
	def handle_community(self, data, event_type):
		"""Attempts to create or update community record. Returns 'created','updated' or error code"""
		status = None		
		try:
			if event_type == 'create':
				Community.objects.create(
				procore_id=data['id'],
				name=data['name'],
				)
				status = 'created'
			elif event_type == 'update':
				c = Community.objects.filter(procore_id=data['id']).first()
				if c is None:
					Community.objects.create(
					procore_id=data['id'],
					name=data['name'],
					)
				else:
					c.name = data[self.community_mapping['name']]
					c.save()
				status='updated'
		except Exception as e: #This could be raised if the community object is not found
			logger.exception("Error occurred")
			status = e
		return status

	def delete_community(self, record_id):
		"""Attempts to delete community record. Returns 'deleted' or error code"""
		status = None
		try:
			c = Community.objects.get(procore_id=record_id)
			c.delete()
			status = 'deleted'
		except Exception as e:
			logger.exception("Error occurred")
			status=e
		return status

	def get_hooks(self):
		url = 'https://api.procore.com/rest/v1.0/webhooks/hooks?company_id=562949953434271'
		r = requests.get(url, headers=self.headers)
		return r.json()

	def list_events(self):
		url = 'https://api.procore.com/rest/v1.0/webhooks/hooks/49395/deliveries?company_id=562949953434271'
		r = requests.get(url, headers=self.headers)
		return r.json()

	def process_webhook(self, data, mock_api_request=None):
		"""Direct an incoming webhook based on its resource name (eg. program, project) and event type (eg. create, update, delete)"""
		event_type = data['event_type']
		resource_name = data['resource_name']
		record_id = data['resource_id']
		context = dict()
		status=None

		#If the event type is delete, we don't need to query the record.
		#All we need is the id to delete it from the web app. Calling the record would result in an error because it doesn't exist anymore in Procore.
		if event_type == 'delete':
			if resource_name == 'Programs':
				status = self.delete_community(record_id)
			if resource_name == 'Projects':
				status = self.delete_plat(record_id)	
		else:
			if mock_api_request is None:
				record = self.get_record(resource_name, record_id)
			else:
				record = mock_api_request
			if record != {}:
				if resource_name == 'Projects':
					# if self.project_is_plat(record['project_type']['name']) == True:
					status = self.handle_plat(record, event_type)
				if resource_name == 'Programs':
					status = self.handle_community(record, event_type)
		context.update({'status': status})
		return context

	def project_is_plat(self, type_name):
		"""If project is a plat, return true"""
		return True if type_name in ['Master Plan','Phased Development','Subdivision'] else False

	def get_all_projects(self):
		"""Query projects and return them"""
		if self.token_is_ok() == False:
			self.refresh_token()
		url = self.base_url+'companies/'+self.procore_company_id+"/projects"
		r = requests.get(url, headers=self.headers)
		data = r.json()
		return data

	def get_all_programs(self):
		"""Query programs are return them"""
		if self.token_is_ok() == False:
			self.refresh_token()
		url = self.base_url+'companies/'+self.procore_company_id+"/programs"
		r = requests.get(url, headers=self.headers)
		data = r.json()
		return data

	
	def update_all_plats(self):
		status = None
		projects = self.get_all_projects()

		for row in projects:

			if self.project_is_plat(row['type_name']) and row['status_name']=='Active':
				record = self.get_record('Projects',row['id'])
				status = self.handle_plat(record,'update')
		return status

	def get_all_tasks(self):
		"""Query projects, append task data and return projects"""
		projects = self.get_all_projects()
		tasks = []
		for row in projects:
			try:
				if row['id'] ==562949953536286 and row['status_name']=='Active' and row['type_name'] in ['Master Plan','Subdivision','Phased Development']:
					url = self.base_url+'tasks?project_id='+str(row['id'])+'?company_id='+self.procore_company_id
					print(url)
					r = requests.get(url, headers=self.headers)
					tasks = tasks + r.json()
			except Exception as e:
				logger.exception("Error occurred")
		
		#Convert tasks list to DF
		tasks_df = pd.DataFrame(tasks)

		return tasks_df

	def clean_task_df(self, tasks_df):
		"""return a cleaned tasks data_frame"""
		#Filter by milestone
		filt = tasks_df['milestone'] == True
		df = tasks_df.loc[filt]
		#Exclude uneeded columns
		df = df[['id','name','key','start_datetime','finish_datetime','task_name','resource_name']]
		#Extract procore_id column from key
		df['key'] = df.key.str.split("|", expand=True)[0]

		return df

	def get_record(self, resource_name, record_id):
		"""Query a program or project endpoint and return the associated data"""
		if self.token_is_ok() == False:
			self.refresh_token()
		if resource_name == 'Programs':
			endpoint_suffix = 'companies/'+self.procore_company_id+"/programs/"+str(record_id)
		elif resource_name == 'Projects':
			endpoint_suffix = 'projects/'+str(record_id)+"?company_id="+self.procore_company_id
		url = self.base_url+endpoint_suffix
		r = requests.get(url, headers=self.headers)
		data = r.json()
		return data


#Get project https://api.procore.com/rest/v1.0/projects/562949953730780?company_id=562949953434271