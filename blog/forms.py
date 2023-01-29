from django.db import models
from django import forms
from .models import *
import decimal, datetime, time
from decimal import *
from datetime import date
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.forms.models import inlineformset_factory

#================================#
# ====== U S E R   A U T H ===== #
#================================#
class UserLoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(UserLoginForm, self).__init__(*args, **kwargs)

	username = forms.EmailField(widget=forms.TextInput(
		attrs={'class': 'form-control', 'placeholder': 'username/email', 'id': 'login-username'}))
	password = forms.CharField(widget=forms.PasswordInput(
		attrs={
			'class': 'form-control',
			'placeholder': 'password',
			'id': 'login-password',
		}
))

class DateInput(forms.DateInput):
	input_type = 'date'


#==============================#
#====== Email Validation ======#
#==============================#
class EmailValidationOnForgotPassword(PasswordResetForm):
	def clean_email(self):
		email = self.cleaned_data['email']
		if not User.objects.filter(email__iexact=email, is_active=True).exists():
			raise ValidationError("There is no user registered with the specified email address!")

		return email

#============================#
#========= MODELS ===========#
#============================#
class CommunityForm(forms.ModelForm):
	class Meta:
		model = Community
		fields = '__all__'
		widgets = {'plans': forms.CheckboxSelectMultiple()}

class JobUpdateForm(forms.ModelForm):
	class Meta:
		model = Job
		fields = ['number','address','plan','attached_count','elevation','garage_orientation','garage_add',]

	def __init__(self, *args, **kwargs):
		 super(JobUpdateForm, self).__init__(*args, **kwargs)
		 self.fields['number'].widget.attrs['readonly'] = True

class LoanForm(forms.ModelForm):
	class Meta:
		model = Loan
		fields = ['job','number','individual_submission','lender','receive_cash_back','lot_release','submission_date','appraisal_date','docs_requested_date','closing_date','maturity_date','note']
		widgets = {
			'closing_date': DateInput(),
			'docs_requested_date': DateInput(),
			'maturity_date': DateInput(),
			'submission_date': DateInput(),
			'appraisal_date': DateInput()
		}

	def __init__(self, *args, **kwargs):
		 super(LoanForm, self).__init__(*args, **kwargs)
		 self.fields['job'].queryset = self.fields['job'].queryset.select_related('loan').filter(loan=None)
		 self.fields['closing_date'].widget.attrs['readonly'] = True
		 self.fields['number'].widget.attrs['readonly'] = True
		 self.fields['maturity_date'].widget.attrs['readonly'] = True

class LoanUpdateForm(forms.ModelForm):
	class Meta:
		model = Loan
		fields = ['number','individual_submission','lender','receive_cash_back','lot_release','submission_date','appraisal_date','docs_requested_date','closing_date','maturity_date','note']
		widgets = {
			'closing_date': DateInput(),
			'docs_requested_date': DateInput(),
			'maturity_date': DateInput(),
			'submission_date': DateInput(),
			'appraisal_date': DateInput()
		}

	def __init__(self, *args, **kwargs):
		 super(LoanUpdateForm, self).__init__(*args, **kwargs)
		 self.fields['closing_date'].widget.attrs['readonly'] = True
		 self.fields['number'].widget.attrs['readonly'] = True
		 self.fields['maturity_date'].widget.attrs['readonly'] = True

class LenderForm(forms.ModelForm):
	class Meta:
		model = Lender
		fields = '__all__'
		exclude = ['id']

class LenderUpdateForm(forms.ModelForm):
	class Meta:
		model = Lender
		fields = '__all__'

class PlatForm(forms.ModelForm):
	class Meta:
		model = Plat
		fields = '__all__'
		exclude = ['author','schedule_found','predecessor','est_vert_start_date','date_posted','est_vert_start_date','planned_vert_start_date','partner','status']
		widgets = {
			'plans': forms.CheckboxSelectMultiple()
		}
	def __init__(self, *args, **kwargs):
		 super(PlatForm, self).__init__(*args, **kwargs)
		 if self.instance.procore_id is not None:
			 self.fields['procore_id'].widget.attrs['readonly'] = True
			 self.fields['project_lot_count'].widget.attrs['readonly'] = True
			 self.fields['name'].widget.attrs['readonly'] = True
			 self.fields['active'].widget.attrs['readonly'] = True
			 self.fields['project_status'].widget.attrs['readonly'] = True
			 self.fields['project_type'].widget.attrs['readonly'] = True
			 self.fields['community'].widget.attrs['readonly'] = True

class PlanForm(forms.ModelForm):
	class Meta:
		model = Plan
		fields = '__all__'
		exclude = ['last_updated', 'full_name','stories']

class PlanUpdateForm(forms.ModelForm):
	class Meta:
		model = Plan
		fields = '__all__'
		exclude = ['last_updated', 'full_name','stories']

class MasterLoanPackageForm(forms.ModelForm):
	class Meta:
		model = MasterLoanPackage
		fields = '__all__'
		exclude = ['user','standard','phaseplans']
		widgets = {
			'submission_date': DateInput(),
			'appraisal_date': DateInput(),
			'expiration_date': DateInput(),
			'platplans': forms.CheckboxSelectMultiple()
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['platplans'].queryset = PlatPlan.objects.none()

		if 'community' in self.data:
			try:
				community_id = int(self.data.get('community'))
				plat_list = list(Plat.objects.filter(community_id=community_id).values_list('pk',flat=True))
				self.fields['platplans'].queryset = PlatPlan.objects.filter(plat_id__in=plat_list)
			except (ValueError, TypeError):
				pass  # invalid input from the client; ignore and fallback to empty platplan queryset
		elif self.instance.pk:
			self.fields['community'].disabled = True
			community_id = self.instance.community.id
			plat_list = list(Plat.objects.filter(community_id=community_id).values_list('pk',flat=True))
			self.fields['platplans'].queryset = PlatPlan.objects.filter(plat_id__in=plat_list)


	def clean(self):
		cleaned_data = super().clean()
		mps = cleaned_data.get("platplans")

		if mps is not None:
			community_id = None
			
			for row in mps:
				temp_community_id = row.plat.community.id

				if community_id != temp_community_id and community_id is not None:
					msg = "Selections must all be from the same community"
					self.add_error('platplans', msg)
					break
				else:
					community_id = temp_community_id
		
class BaseMasterLoanFormSet(forms.BaseModelFormSet):
	def get_form_kwargs(self, index):
		kwargs = super().get_form_kwargs(index)
		kwargs['plans'] = kwargs['plans'][index]	
		return kwargs

class MasterLoanForm(forms.ModelForm):
	plan_name = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))

	class Meta:
		model = MasterLoan
		fields = ['plan_name','appraised_value','est_commitment','lot_release']
	
	def __init__(self, *args, plans, **kwargs):
		self.plans = plans
		super().__init__(*args, **kwargs)
		self.fields['plan_name'].initial = self.plans
		self.fields['plan_name'].disabled = True

MasterLoanFormset = forms.modelformset_factory(MasterLoan, form = MasterLoanForm, formset = BaseMasterLoanFormSet,
	extra=0, can_delete=False)

class BasePlatPlanFormSet(forms.BaseModelFormSet):
	def get_form_kwargs(self, index):
		kwargs = super().get_form_kwargs(index)
		kwargs['plans'] = kwargs['plans'][index]	
		return kwargs

class PlatPlanForm(forms.ModelForm):

	plan_name = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))

	class Meta:
		model = PlatPlan
		fields = '__all__'
		fields = ['plan_name','base_price','lot_cost','lot_fmv','standard']

	def __init__(self, *args, plans, **kwargs):
		self.plans = plans
		super().__init__(*args, **kwargs)
		self.fields['plan_name'].initial = self.plans
		self.fields['plan_name'].disabled = True

PlatPlanFormset = forms.modelformset_factory(PlatPlan, form=PlatPlanForm, formset=BasePlatPlanFormSet, extra=0)


class TrafficForm(forms.ModelForm):
	class Meta:
		model = Traffic
		fields = '__all__'
		exclude = [ 'plat']
		file = forms.FileField()
		widgets = {
			'date': DateInput()
		}

class TrafficUpdateForm(forms.ModelForm):
	class Meta:
		model = Traffic
		fields = '__all__'


#============================#
#========= TIEOUT ===========#
#============================#
class TieOutPlanForm(forms.ModelForm):
	class Meta:
		model = Plan
		fields = ['name','size','stories','width','is_attached','load']

class TieOutTaskFormSet(forms.BaseModelFormSet):
	def get_form_kwargs(self, index):
		kwargs = super().get_form_kwargs(index)

		if 'disable_complete_field' in kwargs:
			kwargs['disable_complete_field'] = kwargs['disable_complete_field'][index]

		if 'table_name' in kwargs:
			kwargs['table_name'] = kwargs['table_name'][index]

		if 'value' in kwargs:
			kwargs['value'] = kwargs['value'][index]

		if 'updated_by' in kwargs:
			kwargs['updated_by'] = kwargs['updated_by'][index]

		if 'error_msg' in kwargs:
			kwargs['error_msg'] = kwargs['error_msg'][index]

		if 'task_name' in kwargs:
			kwargs['task_name'] = kwargs['task_name'][index]

		if 'has_cc_mapping' in kwargs:
			kwargs['has_cc_mapping'] = kwargs['has_cc_mapping'][index]

		return kwargs

class TieOutTaskForm(forms.ModelForm):
	current_value = forms.CharField(required=False)
	task_name = forms.CharField(required=False)
	error_msg = forms.CharField(required=False)
	updated_by = forms.CharField(required=False)
	has_cc_mapping = forms.CharField(required=False)
	class Meta:
		model = TieOutTask
		fields = ['task_name','current_value','flag','complete','updated_by','error_msg','has_cc_mapping', 'comment']

	def __init__(self, *args, value=None, disable_complete_field=None, table_name=None,updated_by=None, error_msg=None,task_name=None,has_cc_mapping=None, **kwargs):

		super().__init__(*args, **kwargs)

		# print(vtype)
		# Ternary to set field class from data type
		field_class = 'decimal' if isinstance(value, decimal.Decimal) else 'string' if isinstance(value, str) else 'date' if isinstance(value, datetime.date) else 'integer' if isinstance(value, int) else 'float' if isinstance(value, float) else ''
		self.fields['current_value'].widget.attrs['class'] = field_class
		self.fields['error_msg'].widget.attrs['class'] = ' error_msg'
		if error_msg:
			if len(error_msg) > 0:
				self.fields['error_msg'].widget.attrs['class'] += ' active'
		if field_class == 'decimal' and 1 > value > 0:
			self.fields['current_value'].widget.attrs['class'] += ' percent'
			value *= 100
			value = str(value)+'%'

		self.fields['updated_by'].widget.attrs['class'] = 'last_updated_by'
		self.fields['updated_by'].initial = updated_by
		self.fields['updated_by'].disabled = True
		self.fields['task_name'].initial = task_name
		self.fields['task_name'].widget.attrs['class'] = table_name
		self.fields['task_name'].disabled = True
		self.fields['current_value'].initial = value
		self.fields['current_value'].disabled = True
		self.fields['error_msg'].initial = error_msg
		self.fields['error_msg'].disabled = True
		self.fields['has_cc_mapping'].initial = has_cc_mapping
		self.fields['has_cc_mapping'].disabled = True
		self.fields['comment'].widget = forms.Textarea(attrs={'placeholder':'Comment', 'rows':1})
		if disable_complete_field == True:
			self.fields['complete'].disabled = True

TieOutTaskFormset = forms.modelformset_factory(TieOutTask, form = TieOutTaskForm, formset=TieOutTaskFormSet,
	extra=0, can_delete=False)

class TieOutJobForm(forms.ModelForm):
	class Meta:
		model = Job
		fields = [
			'actual_start_date',
			'actual_completion_date',
			'actual_sale_date',
			'actual_closing_date',
			'base_contract_price',
			'upgrades_price',
			'credits',
			'concessions',
			'lot_premium',
			'fmv'
			]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['actual_start_date'].widget.attrs['readonly'] = True
		self.fields['actual_completion_date'].widget.attrs['readonly'] = True
		self.fields['actual_sale_date'].widget.attrs['readonly'] = True
		self.fields['actual_closing_date'].widget.attrs['readonly'] = True


class CostCodeForm(forms.ModelForm):
	class Meta:
		model = CostCode
		fields = ['number','description','costcodecategory','is_active']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['number'].widget.attrs['readonly'] = True
		self.fields['description'].widget.attrs['readonly'] = True

class ProformaMilestoneForm(forms.ModelForm):
	class Meta:
		model = ProformaMilestone
		fields = '__all__'

		widgets = {
			'date': DateInput(),
			'communityplans': forms.CheckboxSelectMultiple()
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Only display communities that have plans setup
		self.fields['community'].queryset = self.fields['community'].queryset.exclude(plans=None)
		self.fields['communityplans'].queryset = CommunityPlan.objects.none()
		self.fields['communityplans'].widget.attrs['name'] = 'Community Plan'

		if 'community' in self.data:
			try: # get the communityplans related to current community
				community_id = int(self.data.get('community'))
				community_plans = CommunityPlan.objects.filter(community=community_id)
				plats = Plat.objects.filter(community=community_id)
				self.fields['communityplans'].queryset = community_plans
				self.fields['plat'].queryset = plats
			except (ValueError, TypeError):
				pass # invalid input from the client; ignore and fallback to empty communityplan queryset
		elif self.instance.pk:
			self.fields['community'].disabled = True
			community_id = self.instance.community.id
			community_plans = CommunityPlan.objects.filter(community=community_id)
			plats = Plat.objects.filter(community=community_id)
			self.fields['communityplans'].queryset = community_plans
			self.fields['plat'].queryset = plats


	def clean(self):
		cleaned_data = super().clean()
		milestone = cleaned_data.get("milestone")
		plat = cleaned_data.get("plat")

		if plat is None and milestone == 'VerticalLaunch':
			msg = "Plat must be selected with a vertical launch milestone"
			self.add_error('plat', msg)

		elif plat is not None and milestone != 'VerticalLaunch':
			msg = "A plat can only be selected with a vertical launch milestone"
			self.add_error('plat', msg)


