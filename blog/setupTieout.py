from .models import *


class SetupTieout:

	TASKS = {
		
		'review_plan_name': {'category': 'job_detail','has_cc_mapping':False},
		'review_standard': {'category': 'job_detail','has_cc_mapping':False},
		'review_sqft': {'category': 'job_detail','has_cc_mapping':False},
		'review_levels': {'category': 'job_detail','has_cc_mapping':False},
		'review_start_date': {'category': 'job_detail','has_cc_mapping':False},
		'review_plan_width': {'category': 'job_detail','has_cc_mapping':False},
		'review_completion_date': {'category': 'job_detail','has_cc_mapping':False},
		'review_sale_date': {'category': 'job_detail','has_cc_mapping':False},
		'review_revenue': {'category': 'revenue','has_cc_mapping':True},
		'review_base_price': {'category': 'revenue','has_cc_mapping':False},
		'review_lot_premium': {'category': 'revenue','has_cc_mapping':False},
		'review_close_date': {'category': 'revenue','has_cc_mapping':False},
		'review_upgrades': {'category': 'revenue','has_cc_mapping':False},
		'review_upgrades_credits': {'category': 'revenue','has_cc_mapping':False},
		'review_concessions': {'category': 'revenue','has_cc_mapping':True},
		'review_price_incentive': {'category': 'revenue','has_cc_mapping':False},
		'review_unpriced_upgrades': {'category':'revenue','has_cc_mapping':False},
		'review_build_fee': {'category': 'cost','has_cc_mapping':True},
		'review_inside_sales': {'category': 'cost','has_cc_mapping':True},
		'review_outside_sales': {'category': 'cost','has_cc_mapping':False},
		'review_lot_cost': {'category': 'cost','has_cc_mapping':True},
		'review_lot_fmv': {'category': 'cost','has_cc_mapping':False},
		'review_permit': {'category': 'cost','has_cc_mapping':True},
		'review_hard_cost': {'category': 'cost','has_cc_mapping':True},
		'review_hard_cost_variance': {'category': 'cost','has_cc_mapping':False},
		'review_upgrade_cost': {'category': 'cost','has_cc_mapping':False},
		'review_upgrades_without_po': {'category': 'cost','has_cc_mapping':False},
		'review_state_taxes': {'category': 'cost','has_cc_mapping':True},
		'review_subdivision': {'category': 'cost','has_cc_mapping':True},
		'review_warranty': {'category': 'cost','has_cc_mapping':True},
		'review_marketing': {'category': 'cost','has_cc_mapping':True},
		'review_financing': {'category': 'cost','has_cc_mapping':True},
		'review_misc_closing': {'category': 'cost','has_cc_mapping':False},
		'review_open_pos': {'category': 'cost','has_cc_mapping':False},
		'review_zero_pos': {'category': 'cost','has_cc_mapping':False},
		'review_cancelled_pos': {'category': 'cost','has_cc_mapping':False},
		'review_flagged_variances': {'category': 'cost','has_cc_mapping':False},
		'review_unmapped_codes': {'category': 'cost', 'has_cc_mapping':False},
		'review_net_profit': {'category': 'analysis','has_cc_mapping':False},
		'review_lot_profit': {'category': 'analysis','has_cc_mapping':False},
		'review_home_profit': {'category': 'analysis','has_cc_mapping':False},
		'review_upgrade_profit': {'category': 'analysis','has_cc_mapping':False},
		'review_direct_cost_margin': {'category': 'analysis','has_cc_mapping':False},
		'review_gross_profit_margin': {'category': 'analysis','has_cc_mapping':False},
		'review_net_profit_margin': {'category': 'analysis','has_cc_mapping':False},
		'review_upgrade_margin': {'category': 'analysis','has_cc_mapping':False},
		'review_lot_cost_ratio': {'category': 'analysis','has_cc_mapping':False},
		'review_direct_cost_ratio': {'category': 'analysis','has_cc_mapping':False},
		'review_total_lot_and_directs': {'category': 'analysis','has_cc_mapping':False},
		'review_sales_and_marketing_ratio': {'category': 'analysis','has_cc_mapping':False},
		'review_indirect_cost_ratio': {'category': 'analysis','has_cc_mapping':False},
		'review_base_price_per_sqft': {'category': 'analysis','has_cc_mapping':False},
		'review_hard_cost_per_sqft': {'category': 'analysis','has_cc_mapping':False},
		'review_net_profit_per_sqft': {'category': 'analysis','has_cc_mapping':False}
		}

	def __init__(self, tieout_id=None):

		self.order = self.TASKS
		self.master_task_list = []
		#The order of the listing in the model's choices attribute will be imported here
		for i, choice in enumerate(self.order):
			self.order[choice].update({'value': '','table_name':'','disable_complete_field': False, 'error_msg':'','order':i})
			self.master_task_list.append(choice)

		self.master_task_list = set(self.master_task_list)

		if tieout_id is not None:
			self.tieout_id = tieout_id
			self.task_list = set(TieOutTask.objects.filter(tieout_id=self.tieout_id).values_list('name', flat=True))
			self.tasks_to_add = self.master_task_list-self.task_list
			self.tasks_to_update = self.master_task_list-self.tasks_to_add
			self.tasks_to_delete = self.task_list-self.master_task_list

	def create_tasks(self):

		create_list = []
		for task in self.tasks_to_add:
			create_list.append(TieOutTask(name=task,category=self.order[task].get('category'), tieout_id=self.tieout_id,form_order=self.order[task].get('order')))

		created = TieOutTask.objects.bulk_create(create_list)

		print("Single create: ", create_list)

	def delete_tasks(self):

		delete_list = TieOutTask.objects.filter(tieout_id=self.tieout_id, name__in=self.tasks_to_delete)
		print("Single delete: ",delete_list)
		delete_list.delete()

	def update_tasks(self):
		
		for task in self.tasks_to_update:
			t = TieOutTask.objects.get(name=task, tieout_id=self.tieout_id)
			t.update(form_order=self.order[task].get('order'), category=self.order[task].get('category'))
		
	def update_tasks_global(self):
		for task, value in self.order.items():
			t = TieOutTask.objects.filter(name = task)
			t.update(form_order=value['order'], category=self.order[task].get('category'))

	def delete_tasks_global(self):
		delete_list = TieOutTask.objects.exclude(name__in=self.master_task_list)
		print("Global delete list: ",delete_list)
		delete_list.delete()
		#Call update to fix the ordering
		self.update_tasks_global()

	def create_tasks_global(self):
		create_list = []
		for tieout in TieOut.objects.all():
			task_list = set(TieOutTask.objects.filter(tieout_id=tieout.id).values_list('name', flat=True))
			tasks_to_add = self.master_task_list-task_list
			for task in tasks_to_add:
				create_list.append(TieOutTask(name=task,category=self.order[task].get('category'), tieout_id=tieout.id,form_order=self.order[task].get('order')))

		created = TieOutTask.objects.bulk_create(create_list)

class CheckTieout:

	def __init__(self, tasksDict=None):

		self.tasksDict = tasksDict
		self.ready_for_analysis = False
		self.passed_concession_check = False
		self.passed_revenue_check = False
		self.passed_blank_check = False
		self.passed_count_check = True
		self.passed_open_po_check = True
		#run checks

		self.check_concessions()
		self.check_revenue()
		self.check_blanks()
		self.check_counts()
		self.check_open_pos()

		if self.passed_blank_check == True and self.passed_revenue_check==True and self.passed_concession_check==True and self.passed_count_check==True:
			self.ready_for_analysis = True

		self.check_analysis()

	def check_open_pos(self):
		error = 'Open POs need to be resolved'
		diff = True if self.tasksDict['review_open_pos']['value'] != 0 else False

		if diff == True:
			self.tasksDict['review_open_pos'].update({'disable_complete_field': True, 'error_msg': error})

	def check_counts(self):
		error = 'This items has errors that need to be resolved '
		tasks_to_check = ['review_zero_pos','review_unpriced_upgrades','review_upgrades_without_po','review_flagged_variances','review_unmapped_codes']

		for task in tasks_to_check:
			error_count = self.tasksDict[task]['value']
			if error_count > 0:
				self.passed_count_check = False
				self.tasksDict[task].update({'disable_complete_field':True, 'error_msg':error})

	def check_concessions(self):
		error = 'Concessions and price incentive have a difference of '
		diff_amount = self.tasksDict['review_concessions']['value'] - self.tasksDict['review_price_incentive']['value']
		diff = True if diff_amount != 0 else False

		if diff == True:
			error = error+str(diff_amount)
			self.tasksDict['review_concessions'].update({'disable_complete_field': True, 'error_msg': error})
			self.tasksDict['review_price_incentive'].update({'disable_complete_field': True, 'error_msg': error})

		else:
			self.passed_concession_check = True

	def check_revenue(self):
		error = 'The function (revenue = base price + lot premium + updgrades - credits) has a difference of '
		diff_amount = (
			self.tasksDict['review_revenue']['value']-
			self.tasksDict['review_lot_premium']['value']-
			self.tasksDict['review_base_price']['value']-
			self.tasksDict['review_upgrades']['value']+
			self.tasksDict['review_upgrades_credits']['value']
		)
		diff = True if diff_amount != 0 else False

		if diff == True:
			error = error+str(diff_amount)
			self.tasksDict['review_revenue'].update({'disable_complete_field':True,'error_msg':error})
			self.tasksDict['review_lot_premium'].update({'disable_complete_field':True,'error_msg':error})
			self.tasksDict['review_base_price'].update({'disable_complete_field':True,'error_msg':error})
			self.tasksDict['review_upgrades'].update({'disable_complete_field':True,'error_msg':error})
			self.tasksDict['review_upgrades_credits'].update({'disable_complete_field':True,'error_msg':error})
		else:
			self.passed_revenue_check = True

	def check_analysis(self):
		error = 'All warnings must be resolved before analysis tasks can be completed'

		analysis_tasks = [

			'review_net_profit',
			'review_lot_profit',
			'review_home_profit',
			'review_upgrade_profit',
			'review_direct_cost_margin',
			'review_gross_profit_margin',
			'review_net_profit_margin',
			'review_upgrade_margin',
			'review_lot_cost_ratio',
			'review_direct_cost_ratio',
			'review_total_lot_and_directs',
			'review_sales_and_marketing_ratio',
			'review_indirect_cost_ratio',
			'review_base_price_per_sqft',
			'review_hard_cost_per_sqft',
			'review_net_profit_per_sqft',
		]

		if self.ready_for_analysis == False:
			for task in analysis_tasks:
				self.tasksDict[task].update({'disable_complete_field':True,'error_msg':error})

	def check_blanks(self):
		error = 'This value is empty and needs to be populated at its source'
	
		blank_count = 0
		tasks_to_check = [
			'review_plan_name',
			'review_standard',
			'review_sqft',
			'review_levels',
			'review_start_date',
			'review_plan_width',
			'review_completion_date',
			'review_sale_date',
			'review_lot_fmv'
			]

		for task in tasks_to_check:
			if self.tasksDict[task]['value'] is None or self.tasksDict[task]['value']==0 or self.tasksDict[task]['value'] == '':
				print(task)
				blank_count +=1
				self.tasksDict[task].update({'disable_complete_field':True,'error_msg':error})

		if blank_count == 0:
			self.passed_blank_check = True






