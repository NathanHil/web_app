import django_filters
from django import forms
from django_filters import DateFilter, CharFilter,ModelChoiceFilter, ModelMultipleChoiceFilter, ChoiceFilter
from .models import *

#============================#
#====== AJAX Completed ======#
#============================#
class CommunityFilter(django_filters.FilterSet):
	class Meta:
		model = Community
		fields = {
			'name': ['icontains',],
		}
class JobFilter(django_filters.FilterSet):
	plat = ModelMultipleChoiceFilter(
		queryset=Plat.objects.exclude(jobs=None),
		widget=forms.CheckboxSelectMultiple(attrs={'class':'plat checkItems'})
	)

	class Meta:
		model = Job
		fields = {
			'number': ['icontains']
		}
class LenderFilter(django_filters.FilterSet):
	class Meta:
		model = Lender
		fields = {
			'name':['icontains']
		}

STATUS_CHOICES = (
	('Construction', 'Construction'),
	('Due Diligence', 'Due Diligence'),
	('Engineering', 'Engineering'),
	('Entitlement', 'Entitlement'),
	('Future', 'Future'),
	('Warranty', 'Warranty'),
	('Closed', 'Closed')
)
class PlatFilter(django_filters.FilterSet):

	community = ModelMultipleChoiceFilter(
		queryset=Community.objects.exclude(plat=None).order_by('name'),
		widget=forms.CheckboxSelectMultiple(attrs={'class':'community checkItems'})
	)
	project_status = ChoiceFilter(choices=STATUS_CHOICES)
	class Meta:
		model = Plat
		fields = []
class PlanFilter(django_filters.FilterSet):
	class Meta:
		model = Plan
		fields = {
			'name' : ['icontains']
		}

class ProformaMilestoneFilter(django_filters.FilterSet):
	class Meta:
		model = ProformaMilestone
		fields = {
			'name' : ['icontains']
		}

class TrafficFilter(django_filters.FilterSet):
	class Meta:
		model = Traffic
		fields = {
			'community__name':['icontains']
		}

class CostCodeFilter(django_filters.FilterSet):
	class Meta:
		model = CostCode
		fields = {
			'number' : ['icontains'],
			'costcodecategory__name': ['icontains']
		}

STAGE_CHOICES = (
	('Not Started', 'Not Started'),
	('In Progress', 'In Progress'),
	('Analysis', 'Analysis'),
	('Complete', 'Complete')
)
class TieOutProgressFilter(django_filters.FilterSet):
	
	job_number = django_filters.CharFilter(field_name='job__number', lookup_expr='icontains',label='Job Number contains')
	community = django_filters.CharFilter(field_name='job__plat__community__name', lookup_expr='icontains',label='Community contains')
	stage = ChoiceFilter(choices=STAGE_CHOICES)

	class Meta:
		model = TieOut
		fields = []

