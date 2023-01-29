import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, DateWidget
from .models import *
from .tables import *

class TrafficResource(resources.ModelResource):
	community = fields.Field(
		column_name='community',
		attribute='community',
		widget=ForeignKeyWidget(Community, 'name'))
	class Meta:
		model = Traffic
		fields = ('community','count','be_back_count','date')
		export_order = ('community','count','be_back_count','date')
		force_init_instance = True
	def get_queryset(self):
		return self._meta.model.objects.select_related('community')

class LoanTransactionResource(resources.ModelResource):
	platplan = fields.Field(
		column_name='platplan_id',
		attribute='platplan',
		widget=ForeignKeyWidget(PlatPlan, 'id'))
	purchasingactivity = fields.Field(
		column_name='purchasingactivity',
		attribute='purchasingactivity',
		widget=ForeignKeyWidget(PurchasingActivity, 'name'))
	class Meta:
		model = LoanTransaction
		fields = ('purchasingactivity','platplan_id','amount')
		force_init_instance = True
	def get_queryset(self):
		return self._meta.model.objects.select_related('purchasingactivity','platplan')

	def before_import_row(self, row, row_number=None, **kwargs):
		if type(row['amount']) == str:
			row['amount'] = float(row['amount'].replace(',',''))

	def before_save_instance(self, instance, using_transactions, dry_run):
		instance.user_id = self.user_id

	def import_data(self, *args, **kwargs):
		self.user_id = kwargs.get("user_id") # Here, we are assigning the requested user to the `ModelResource` object.
		return super().import_data(*args, **kwargs)

class JobResource(resources.ModelResource):
	plan = fields.Field(
		column_name='plan_id',
		attribute='plan',
		widget=ForeignKeyWidget(Plan, 'id'))
	plat = fields.Field(
		column_name='plat_id',
		attribute='plat',
		widget=ForeignKeyWidget(Plat, 'id'))
	class Meta:
		model = Job
		fields = ('number','plat','plan','attached_count','elevation','garage_orientation','garage_add')
		export_order = ('number','plat','plan','attached_count','elevation','garage_orientation','garage_add')
		import_id_fields = ('number',)
		force_init_instance = True
		# skip_unchanged = True
	def get_queryset(self):
		return self._meta.model.objects.select_related('plat','plan')

class UpdateJobFMVResource(resources.ModelResource):
	"""Used to update fair market values of a Job."""
	class Meta:
		model = Job
		fields = ('number','fmv')
		import_id_fields = ('number',)

class UpdateJobAddressResource(resources.ModelResource):
	"""Used to update a job's address"""
	class Meta:
		model = Job
		fields = ('number','address')
		import_id_fields = ('number',)

class PlanResource(resources.ModelResource):	
	class Meta:
		model = Plan

class CommunityResource(resources.ModelResource):	
	class Meta:
		model = Community
		exclude = ('id',)

	def get_queryset(self):
		return self._meta.model.objects.select_related('partner')

class PlatResource(resources.ModelResource):
	community = fields.Field(
		column_name='community',
		attribute='community',
		widget=ForeignKeyWidget(Community, 'name'))
	partner = fields.Field(
		column_name = 'partner',
		attribute = 'partner',
		widget=ForeignKeyWidget(Partner,'name'))
	class Meta:
		model = Plat
		import_id_fields = ('name',)
		exclude = ('id','date_posted','author','predecessor','est_vert_start_date','planned_vert_start_date')
		export_order = ('name','status','schedule_found','build_order','default_start_pace','partner','community')
	def get_queryset(self):
		return self._meta.model.objects.select_related('community')

class UpdateBasePriceResource(resources.ModelResource):
	"""Used to update base price values of a PlatPlan."""
	plan = fields.Field(
		column_name='plan',
		attribute='plan',
		widget=ForeignKeyWidget(Plan, 'full_name'))
	plat = fields.Field(
		column_name='plat',
		attribute='plat',
		widget=ForeignKeyWidget(Phase, 'name'))
	class Meta:
		model = PlatPlan
		fields = ('plan','plat','base_price')
		import_id_fields = ('plan','plat',)
	def get_queryset(self):
		return self._meta.model.objects.select_related('plat','plan')

class CostCodeResource(resources.ModelResource):	
	class Meta:
		model = CostCode
		exclude = ('id',)

class ProformaMilestoneDetailResource(resources.ModelResource):
	communityplan = fields.Field(
		column_name='community_plan',
		attribute='communityplan',
		widget=ForeignKeyWidget(CommunityPlan, 'name'))
	proformamilestone = fields.Field(
		column_name='proformamilestone',
		attribute='proformamilestone',
		widget=ForeignKeyWidget(ProformaMilestone, 'name'))
	class Meta:
		model = ProformaMilestoneDetail
		fields = (
			'proformamilestone',
			'communityplan',
			'base_price',
			'lot_cost',
			'lot_fmv',
			'permit_cost',
			'hard_cost',
			'project_management_cost',
			'sales_commission_cost',
			'financing_cost'
			)

		import_id_fields = ('communityplan','proformamilestone',)
	def get_queryset(self):
		return self._meta.model.objects.select_related('proformamilestone','communityplan')

class ProformaMilestoneResource(resources.ModelResource):
	community = fields.Field(
		column_name='community',
		attribute='community',
		widget=ForeignKeyWidget(Community, 'name'))
	plat = fields.Field(
		column_name='plat',
		attribute='plat',
		widget=ForeignKeyWidget(Plat, 'name'))
	class Meta:
		model = ProformaMilestone
		clean_model_instances= True
		fields = (
			'name',
			'date',
			'milestone',
			'community',
			'plat'
			'is_complete',
			)
		import_id_fields = ('name',)
	def get_queryset(self):
		return self._meta.model.objects.select_related('community','plat')

class GoalResource(resources.ModelResource):
	plat = fields.Field(
		column_name='plat',
		attribute='plat',
		widget=ForeignKeyWidget(Plat, 'name'))
	class Meta:
		model = Goal
		force_init_instance = True
		clean_model_instances= True
		fields = (
			'plat',
			'date',
			'count',
			'event',
			'goal_type'
			)
	def get_queryset(self):
		return self._meta.model.objects.select_related('plat')




