from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone
import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

# Models that have been converted to AJAX pages
class Lender(models.Model):
	name = models.CharField(max_length=100, unique=True)
	sage_name = models.CharField(max_length=100)
	credit_limit = models.IntegerField(default=0)
	interest_rate = models.DecimalField(decimal_places =4, max_digits=10, default=0)
	points = models.DecimalField(decimal_places =4, max_digits=10, default=0)
	ltc_limit = models.DecimalField(decimal_places =4, max_digits=10, default=0)
	ltv_limit = models.DecimalField(decimal_places =4, max_digits=10, default=0)
	
	def __str__(self):
		return self.name
		
	def get_absolute_url(self):
		return reverse('lender-home')
	class Meta:
		ordering = ('name',)
		verbose_name = "lender"
		verbose_name_plural = "lenders"

class Partner(models.Model):
	name = models.CharField(verbose_name="partner name",max_length=100, unique=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('plat-home')

class Plan(models.Model):
	name = models.CharField(max_length=50)
	last_updated = models.DateTimeField(auto_now=True)
	size = models.IntegerField(default=0)
	garage_count = models.IntegerField(default=1)
	stories = models.IntegerField(default=0)
	bedroom_count = models.IntegerField(default=0)
	bath_count = models.DecimalField(decimal_places =1, max_digits=11, default=0)
	width = models.DecimalField(decimal_places =1, max_digits=10, default=0)
	is_active = models.BooleanField(default=1)
	is_attached = models.BooleanField(default=0)
	levels = models.IntegerField(default=1)
	master_on_main = models.BooleanField(default=0)

	#Calculated at save
	full_name = models.CharField(max_length=50, default = 'none', verbose_name='Plan name')

	CHOICES = [
		('Rear', 'Rear'),
		('Front', 'Front'),

	]
	load = models.CharField(
		max_length=5,
		choices=CHOICES,
		null=True,
		blank=True
	)	
	
	def __str__(self):
		return self.full_name
		
	def get_absolute_url(self):
		return reverse('plan-home')
		
	def save(self, *args, **kwargs):
		
		if self.is_attached == True:
			stuff = " TH"
		else:
			stuff = ""

		long_name =  self.name +" "+str(self.garage_count)+" car"+stuff
		self.full_name = long_name
		super(Plan, self).save(*args, **kwargs)

	class Meta:
		ordering = ('name',)

# Normal form models
class Community(models.Model):
	com_id = models.IntegerField(unique=True,blank=True,null=True)
	procore_id = models.BigIntegerField(unique=True, blank=True, null=True)
	name = models.CharField(max_length=100, unique=True)
	partner = models.ForeignKey(Partner, on_delete=models.PROTECT, null=True, blank=True)
	abbreviation = models.CharField(max_length=10,null=True,blank=True)
	excise_tax_rate = models.DecimalField(decimal_places=4, default = 0.00, max_digits = 5)
	sales_tax_rate = models.DecimalField(decimal_places=3, default = 0.00,max_digits =5)
	city = models.CharField(max_length=100, null=True,blank=True)
	zip_code = models.CharField(max_length=5, null=True, blank=True)	
	plans = models.ManyToManyField(Plan, through='communityplan', blank=True)

	STATE_CHOICES = [('WA','WA'),('OR','OR')]
	state = models.CharField(max_length=2, choices=STATE_CHOICES, default='WA')

	# Character field with choices defined with the above list of tuples
	REGION_CHOICES = [('CO', 'CO'),('PDX', 'PDX'),('TRI', 'TRI'),]
	region = models.CharField(max_length=10, choices=REGION_CHOICES, default='CO')
	
	def __str__(self):
		return self.name
		
	def get_absolute_url(self):
		return reverse('community-home')

	class Meta:
		ordering = ('name',)
		verbose_name = "community"
		verbose_name_plural = "communities"

class Owner(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Plat(models.Model):
	procore_id = models.BigIntegerField(unique=True,blank=True,null=True)
	owner = models.ForeignKey(Owner, on_delete=models.PROTECT, null=True, blank=True)
	project_lot_count = models.IntegerField(default=0,null=True,blank=True)
	pahlisch_lot_count = models.IntegerField(default=0,null=True,blank=True)
	project_status = models.CharField(max_length=40,null=True,blank=True)
	partner = models.ForeignKey(Partner, on_delete=models.PROTECT, blank=True, null =True) #Need to add logic so that this doesn't just error out for the user when deleted
	name = models.CharField(max_length=100, unique=True)
	build_order = models.IntegerField(default=0, null=True, blank=True)
	date_posted = models.DateTimeField(auto_now=False, blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	community = models.ForeignKey(Community, on_delete=models.PROTECT)
	schedule_found = models.BooleanField(default=False) #consider removing
	default_start_pace = models.IntegerField(default=0, null=True, blank=True)
	predecessor = models.ForeignKey("Plat", on_delete=models.CASCADE, null= True, blank=True) #consider removing
	est_vert_start_date = models.DateTimeField(auto_now=False, null=True)
	planned_vert_start_date = models.DateTimeField(auto_now=False, null=True) #consider removing
	active = models.BooleanField(default=False)
	project_type = models.CharField(max_length=50,null=True,blank=True)
	plans = models.ManyToManyField(Plan, through='platplan', blank=True)
	
	def __str__(self):
		return self.name
		
	CHOICES = [
		('LD Diligence', 'LD Diligence'),
		('LD Future', 'LD Future'),
		('LD Construction', 'LD Construction'),
		('LD Complete', 'LD Complete'),	
		('Recorded', 'Recorded'),		
		('Vertical', 'Vertical'),
		('Closed', 'Closed'),

	]
	status = models.CharField(max_length=30,choices=CHOICES,default='LD Future')
	
	def get_absolute_url(self):
		return reverse('plat-home')
						
	class Meta:
		ordering = ('name',)

class ProjectedStart(models.Model):
	plat = models.ForeignKey(Plat, on_delete=models.CASCADE)
	month  = models.DateTimeField(auto_now=False)
	count = models.IntegerField(default=0)
	source = models.CharField(max_length=15, null=True)

	def __str__(self):
		return self.plat

	def get_absolute_url(self):
		return reverse('partner-home')	

class Phase(models.Model):
	number = models.CharField(verbose_name="phase number", max_length=2, validators=[RegexValidator(regex='^.{2}$', message='Length has to be 2 characters', code='nomatch')])
	name = models.CharField(max_length=40, null=True, verbose_name='Phase Name')
	lot_count = models.IntegerField(default=0, null=True, blank=True)
	plat = models.ForeignKey(Plat, on_delete=models.PROTECT)
	owner = models.ForeignKey(Owner, on_delete=models.PROTECT, null=True, blank=True)
	plans = models.ManyToManyField(Plan, through='phaseplan', blank=True)
	active = models.BooleanField(default=True)
		
	def __str__(self):
		return str(self.name)
		
	def get_absolute_url(self):
		return reverse('plat-home')
	
	def save(self, *args, **kwargs):
		self.name = self.plat.name+" :PH "+self.number
		super(Phase, self).save(*args, **kwargs)

	class Meta:
		ordering = ('name',)
		
		constraints = [
			models.UniqueConstraint(
				fields=['number', 'plat'], 
				name='unique number'
				)
		]

		indexes = [models.Index(fields=['name']),]

class MasterPlan(models.Model):
	#Foreign keys
	phase = models.ForeignKey(Phase, on_delete=models.PROTECT)
	plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
	lender = models.ForeignKey(Lender, on_delete=models.CASCADE, null = True, blank = True)
	user = models.ForeignKey(User, on_delete=models.PROTECT, null = True, blank = True)

	#Values 
	base_price = models.IntegerField(default=0)
	lot_cost = models.IntegerField(default=0)
	lot_fmv = models.IntegerField(default=0)
	lot_release = models.IntegerField(default=0)
	approved_commitment = models.IntegerField(default=0)
	est_commitment = models.IntegerField(default=0)
	receive_cash_back = models.BooleanField(default=0)
	uses_master_appraisal = models.BooleanField(default=1)

	#Dates
	approval_date = models.DateTimeField(auto_now=False, null=True, blank = True)
	submission_date = models.DateTimeField(auto_now=False, null=True, blank = True)
	last_update_date = models.DateTimeField(auto_now=True, null=True, blank = True)

	#Status
	STATUS_CHOICES = [
		('Submitted', 'Submitted'),
		('Approved', 'Approved'),
		
	]
	status = models.CharField(
		max_length=100,
		choices=STATUS_CHOICES,
		null = True,
		blank = True
	)

	#Standard
	CHOICES = [
		('Prelude', 'Prelude'),
		('Classic', 'Classic'),
		('Modern', 'Modern'),
		('Signature', 'Signature'),
		
	]
	standard = models.CharField(
		max_length=100,
		choices=CHOICES,
		default=None,
		null=True,
		blank=True
	)

	def __str__(self):
		return str(self.id)
	
	def get_absolute_url(self):
		return reverse('masterplan-home')

	class Meta:
		unique_together = [['phase', 'plan']]
		ordering = ('phase','plan')

	def save(self, *args, **kwargs):
		super(MasterPlan, self).save(*args, **kwargs)
		print("Saving")

		print(self.phase_id, self.plan_id)

		#This is temporary. The purpose is to keep PhasePlan in line with masterplan and allow for a seamless transition

		try:
			phaseplan = PhasePlan.objects.get(phase_id = self.phase.id, plan_id = self.plan.id)
			phaseplan.base_price = self.base_price
			phaseplan.lot_cost = self.lot_cost
			phaseplan.lot_fmv = self.lot_fmv
			phaseplan.save()
		except:
			pass

	
class Goal(models.Model):
	plat = models.ForeignKey(Plat, on_delete=models.CASCADE)
	date = models.DateField(auto_now=False)
	count = models.IntegerField(default=0)

	sale = 'Sale'
	start = 'Start'
	closing = 'Closing'

	EVENT_CHOICES = [
		(sale,'Sale'),
		(start,'Start'),
		(closing, 'Closing')
	]

	event = models.CharField(
		max_length = 15,
		choices = EVENT_CHOICES,
		default = sale
	)

	GOAL_TYPE_CHOICES = [
		('Annual','Annual'),
		('Reforecast','Reforecast'),
	]
	goal_type = models.CharField(
		max_length = 15,
		choices = GOAL_TYPE_CHOICES,
		default = 'Annual',
		null=True
	)

class Investor(models.Model):
	name = models.CharField(max_length=100, unique=True)
	total_capacity = models.IntegerField(default=0)

	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('investor-home')


class CostCodeCategory(models.Model):
	name = models.CharField(max_length=30, unique=True)

	def __str__(self):
		return self.name

	class Meta:
		indexes = [models.Index(fields=['name',]),]


class CostCode(models.Model):
	costcodecategory = models.ForeignKey(CostCodeCategory, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='Cost Code Category')
	number = models.CharField(max_length=10, unique=True, verbose_name="Cost Code")
	is_hard = models.BooleanField(default=1)
	description = models.CharField(max_length=30)
	is_active = models.BooleanField(default=1)
	is_group = models.BooleanField(default=0)

	def __str__(self):
		return self.description

class PurchasingActivity(models.Model):
	wms_id = models.IntegerField(unique=True)
	name = models.CharField(max_length=100)
	costcode = models.ForeignKey(CostCode, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.name

class Job(models.Model):
	number = models.CharField(max_length=10, unique=True, verbose_name='Job Number')
	phase = models.ForeignKey(Phase, on_delete=models.PROTECT, null=True)
	plat = models.ForeignKey(Plat, on_delete=models.PROTECT, related_name='jobs')
	lot_number = models.CharField(max_length=3)
	sales_status = models.CharField(max_length=50, null=True, blank=True)
	construction_status = models.CharField(max_length=50, null=True, blank=True)
	category = models.CharField(max_length=50, null=True, blank=True)
	use = models.CharField(max_length=50, null=True, blank=True)
	plan = models.ForeignKey(Plan, on_delete=models.PROTECT, null=True, blank=True)
	actual_sale_date = models.DateField(auto_now=False, null=True)
	actual_start_date = models.DateField(auto_now=False, null = True, blank=True)
	actual_closing_date = models.DateField(auto_now=False, null = True, blank=True)
	actual_completion_date = models.DateField(auto_now=False, null = True, blank=True)
	projected_sale_date = models.DateField(auto_now=False, null=True)
	projected_start_date = models.DateField(auto_now=False, null = True, blank=True)
	projected_closing_date = models.DateField(auto_now=False, null = True, blank=True)
	projected_completion_date = models.DateField(auto_now=False, null = True, blank=True)
	scheduled_closing_date = models.DateField(auto_now=False, null = True, blank=True)
	elevation = models.CharField(max_length=5, null=True, blank=True)
	garage_orientation = models.CharField(max_length=15, null=True, blank=True)
	attached_count = models.IntegerField(default=0, null=True, blank=True)
	garage_add = models.CharField(max_length=5, null=True, blank=True)
	sales_price = models.DecimalField(decimal_places =2, max_digits=10, default=0, null=True, blank=True)
	lot_premium = models.IntegerField(default=0, null=True, blank=True)
	list_date = models.DateField(auto_now=False, null = True, blank=True)
	address = models.CharField(max_length=50, null=True, blank=True)
	contingency = models.CharField(max_length=100, null=True, blank=True)
	sales_commission = models.DecimalField(decimal_places =2, max_digits=10, default=0, null=True, blank=True)
	base_contract_price = models.DecimalField(decimal_places =2, max_digits=10, default=0, null=True, blank=True)
	list_price = models.DecimalField(decimal_places =2, max_digits=10, default=0, null=True, blank=True)
	original_base_list_price = models.DecimalField(decimal_places =2, max_digits=10, default=0, null=True, blank=True)
	upgrades_price = models.DecimalField(decimal_places =2, max_digits=10, default=0, null=True, blank=True)
	credits = models.DecimalField(decimal_places =2, max_digits=10, default=0, null=True, blank=True)
	concessions = models.DecimalField(decimal_places =2, max_digits=10, default=0, null=True, blank=True)
	fmv = models.DecimalField(decimal_places =2, max_digits=10, default=0)
	base_list_price = models.DecimalField(decimal_places =2, max_digits=10, default=0, null=True, blank=True)
	past_sheetrock = models.BooleanField(default=0)
	revenue = models.DecimalField(decimal_places =2, max_digits=10, default=0)
	lot_cost = models.DecimalField(decimal_places =2, max_digits=10, default=0)

	PRODUCT_CHOICES = [
		('DFL', 'DFL'),
		('DRL', 'DRL'),
		('AFL', 'AFL'),
		('ARL', 'ARL'),
		
	]
	product_type = models.CharField(
		max_length=100,
		choices=PRODUCT_CHOICES,
		default='DFL',
		null=True,
		blank=True
	)
	
	class Meta:
		ordering = ('number',)

	def __str__(self):
		return self.number
			
	def get_absolute_url(self):
		return reverse('job-home')

class Traffic(models.Model):
	community = models.ForeignKey(Community, on_delete=models.CASCADE, blank=True, null=True)
	count = models.IntegerField(default=0)
	be_back_count = models.IntegerField(default=0)
	date = models.DateField(auto_now=False)
	
	class Meta:
		ordering = ('-date',)

	def __str__(self):
		return str(self.id)
		
	def get_absolute_url(self):
		return reverse('traffic-home')

class BuildingPermit(models.Model):

	job = models.OneToOneField(Job, on_delete=models.CASCADE)
	submission_date = models.DateField(auto_now=False, blank=True, null=True)
	status = models.CharField(max_length=30, blank=True, null = True)
	number = models.CharField(max_length=30, blank=True, null = True)
	note = models.CharField(max_length=100, blank=True, null = True)

	def __str__(self):
		return str(self.id)

	
class Loan(models.Model):
	#For all vertical loans
	closing_date = models.DateField(auto_now=False, blank=True, null =True)
	docs_requested_date = models.DateField(auto_now=False, blank=True, null=True)
	job = models.OneToOneField(Job, on_delete=models.CASCADE)
	lender = models.ForeignKey(Lender, on_delete=models.PROTECT)
	number = models.BigIntegerField(default=0)
	maturity_date = models.DateField(auto_now=False, blank=True, null=True)
	appraisal_date = models.DateField(auto_now=False, null=True, blank = True)
	submission_date = models.DateField(auto_now=False, null=True, blank = True)
	receive_cash_back = models.BooleanField(default=0)
	lot_release = models.IntegerField(default=0)
	note = models.CharField(max_length=50, null=True, blank=True)
	individual_submission = models.BooleanField(default=0)

	def __str__(self):
		return str(self.id)

class DocumentType(models.Model):
	wms_id = models.IntegerField(unique=True)
	description = models.CharField(max_length=50)
	required_for_start = models.BooleanField(default=0)

	def __str__(self):
		return self.description

class JobAttachment(models.Model):
	wms_id = models.IntegerField(unique=True)
	job = models.ForeignKey(Job, on_delete=models.CASCADE)
	documenttype = models.ForeignKey(DocumentType, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.id)

class PhasePlan(models.Model):

	description = models.CharField(max_length=75)
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
	phase = models.ForeignKey(Phase, on_delete=models.CASCADE)

	#Values 
	base_price = models.IntegerField(default=0)
	lot_cost = models.IntegerField(default=0)
	lot_fmv = models.IntegerField(default=0)

	#Standard
	CHOICES = [
		('Prelude', 'Prelude'),
		('Classic', 'Classic'),
		('Modern', 'Modern'),
		('Signature', 'Signature'),
		
	]
	standard = models.CharField(
		max_length=100,
		choices=CHOICES,
		default='Classic'
	)
	
	class Meta:
		ordering = ('description',)
		indexes = [models.Index(fields=['description']),]

	def save(self, *args, **kwargs):

		description =  self.phase.name +" | "+self.plan.full_name
		self.description = description
		super(PhasePlan, self).save(*args, **kwargs)

	def __str__(self):
		return self.description

class PlatPlan(models.Model):
	description = models.CharField(max_length=75)
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
	plat = models.ForeignKey(Plat, on_delete=models.CASCADE)
	phase_plan_id = models.IntegerField(default=0)

	#Values 
	base_price = models.IntegerField(default=0)
	lot_cost = models.IntegerField(default=0)
	lot_fmv = models.IntegerField(default=0)

	#Standard
	CHOICES = [
		('Prelude', 'Prelude'),
		('Classic', 'Classic'),
		('Modern', 'Modern'),
		('Signature', 'Signature'),
		
	]
	standard = models.CharField(
		max_length=100,
		choices=CHOICES,
		default='Classic'
	)
	
	class Meta:
		ordering = ('description',)
		indexes = [models.Index(fields=['description']),]

	def save(self, *args, **kwargs):

		description =  self.plat.name +" | "+self.plan.full_name
		self.description = description
		super(PlatPlan, self).save(*args, **kwargs)

	def __str__(self):
		return self.description


class MasterLoanPackage(models.Model):
	#This simplifies the loan process
	description = models.CharField(max_length=50)
	community = models.ForeignKey(Community, on_delete=models.PROTECT, null=True)
	phaseplans = models.ManyToManyField(PhasePlan, through='masterloan', blank=True)
	platplans = models.ManyToManyField(PlatPlan, through='masterloan', blank=True)
	lender = models.ForeignKey(Lender, on_delete=models.CASCADE)	
	receive_cash_back = models.BooleanField(default=0)

	STATUS_CHOICES = [
		('gathering_loan_facts', 'Gathering Loan Facts'),
		('submitted','Submitted'),
		('appraised','Appraised')
		]

	status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=None, null=True, blank=True)

	#Status
	CHOICES = [
		('Prelude', 'Prelude'),
		('Classic', 'Classic'),
		('Modern', 'Modern'),
		('Signature', 'Signature'),
		
	]
	standard = models.CharField(
		max_length=100,
		choices=CHOICES,
		default='Classic'
	)

	#Dates
	appraisal_date = models.DateField(auto_now=False, null=True, blank = True)
	submission_date = models.DateField(auto_now=False, null=True, blank = True)
	expiration_date = models.DateField(auto_now=False, null=True, blank = True)

	def __str__(self):
		return self.description

	class Meta:
		ordering = ('description',)

	def save(self, *args, **kwargs):	
		if self.appraisal_date is not None:
			self.status = 'appraised'	
		elif self.submission_date is not None:
			self.status = 'submitted'
		elif self.status != 'gathering_loan_facts':
			self.status = None
		super(MasterLoanPackage, self).save(*args, **kwargs)

class MasterLoan(models.Model):
	phaseplan = models.ForeignKey(PhasePlan, on_delete=models.PROTECT, null=True)
	platplan = models.ForeignKey(PlatPlan, on_delete=models.PROTECT, null=True)
	masterloanpackage = models.ForeignKey(MasterLoanPackage, on_delete=models.PROTECT)
	est_commitment = models.IntegerField(default=0)
	appraised_value = models.IntegerField(default=0)
	lot_release = models.IntegerField(default=0)

class PurchaseOrder(models.Model):

	job = models.ForeignKey(Job, on_delete=models.PROTECT, null=True, blank=True)
	wms_id = models.IntegerField(unique=True)
	number = models.CharField(max_length=50, unique=True)
	description = models.CharField(max_length=50)
	vendor = models.CharField(max_length=50)
	date_issued = models.DateField(auto_now=False)
	issued_by = models.CharField(max_length=50)
	date_approved = models.DateField(auto_now=False, blank=True, null=True)
	total = models.DecimalField(decimal_places =2, max_digits=10, default=0)
	tax_amount = models.DecimalField(decimal_places =2, max_digits=10, default=0)
	status = models.IntegerField()
	vpo_number = models.IntegerField()

	def __str__(self):
		return self.number

class LoanTransaction(models.Model):
	costcode = models.ForeignKey(CostCode, on_delete=models.PROTECT, null=True)
	purchasingactivity = models.ForeignKey(PurchasingActivity, on_delete=models.PROTECT)
	masterplan = models.ForeignKey(MasterPlan, on_delete=models.CASCADE, null=True)
	platplan = models.ForeignKey(PlatPlan, on_delete=models.CASCADE)
	phaseplan = models.ForeignKey(PhasePlan, on_delete=models.PROTECT, null=True)
	amount = models.DecimalField(decimal_places =2, max_digits=10)
	date_stamp = models.DateField(auto_now=True, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return str(self.id)

class TieOut(models.Model):
	job = models.OneToOneField(Job,null=True, on_delete=models.CASCADE)
	date = models.DateField(auto_now=False, null=True, blank = True)
	complete = models.BooleanField(default=0)

class TieOutTask(models.Model):
	
	tieout = models.ForeignKey(TieOut, on_delete=models.CASCADE)

	CHOICES = [
		
		('review_plan_name', 'Review Plan Name'),
		('review_standard', 'Review Standard'),
		('review_sqft', 'Review Sqft'),
		('review_levels', 'Review Level'),
		('review_start_date', 'Review Start Date'),
		('review_plan_width', 'Review Plan Width'),
		('review_completion_date', 'Review Completion Date'),
		('review_sale_date', 'Review Sale Date'),		
		('review_revenue','Review Revenue'),
		('review_base_price', 'Review Base Price'),
		('review_lot_premium', 'Review Lot Premium'),
		('review_close_date', 'Review Close Date'),
		('review_upgrades', 'Review Upgrades'),
		('review_upgrades_credits', 'Review Upgrades Credits'),
		('review_concessions', 'Review Concessions'),
		('review_price_incentive','Review Price Incentive'),
		('review_build_fee', 'Review Build Fee'),
		('review_inside_sales','Review Inside Sales'),
		('review_outside_sales','Review Outside Sales'),
		('review_lot_cost', 'Review Lot Cost'),
		('review_lot_fmv', 'Review Lot FMV'),
		('review_permit', 'Review Permit'),
		('review_hard_cost', 'Review Hard Cost'),
		('review_hard_cost_variance', 'Review Hard Cost Variance'),
		('review_upgrade_cost', 'Review Upgrade Cost'),
		('review_state_taxes', 'Review State Taxes'),
		('review_subdivision', 'Review Subdivision'),
		('review_warranty', 'Review Warranty'),
		('review_marketing', 'Review Marketing'),
		('review_financing', 'Review Financing'),
		('review_misc_closing','Review Misc Closing'),
		('review_open_pos','Review Open POs'),
		('review_net_profit','Review Net Profit'),
		('review_lot_profit','Review Lot Profit'),
		('review_home_profit','Review Home Profit'),
		('review_upgrade_profit','Review Upgrade Profit'),
		('review_direct_cost_margin','Review Direct Cost Margin'),
		('review_gross_profit_margin','Review Gross Profit Margin'),
		('review_net_profit_margin','Review Net Profit Margin'),
		('review_upgrade_margin','Review Upgrade Margin'),
		('review_lot_cost_ratio','Review Lot Cost Ratio'),
		('review_direct_cost_ratio','Revuew Direct Cost Ratio'),
		('review_total_lot_and_directs','Review Total Lot and Directs'),
		('review_sales_and_marketing_ratio','Review Sales and Marketing Ratio'),
		('review_indirect_cost_ratio','Review Indirect Cost Ratio'),
		('review_base_price_per_sqft','Review Base Price per SQFT'),
		('review_hard_cost_per_sqft','Review Hard Cost per SQFT'),
		('review_net_profit_per_sqft','Review Net Profit per SQFT'),

	]

	category = models.CharField(max_length=50, blank=True, null=True)
	comment = models.CharField(max_length=50, blank=True, null=True)
	name = models.CharField(max_length=100, default=None, verbose_name='Task Name')
	complete = models.BooleanField(default=0)
	flag = models.BooleanField(default=0)
	last_update_date = models.DateTimeField(auto_now=True, null=True, blank = True)
	last_updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
	form_order = models.IntegerField(default=0)

	def __str__(self):
		return self.name

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=['name', 'tieout'], 
				name='unique name'
				)
		]

class SalesOption(models.Model):
	ss_id = models.IntegerField(unique=True)
	description = models.CharField(max_length=50, null=True)
	code = models.CharField(max_length=50, null=True)
	from_spec = models.IntegerField(default=0)
	price = models.DecimalField(decimal_places =2, max_digits=10, default=0)
	quantity = models.IntegerField(default=0)
	job = models.ForeignKey(Job, on_delete=models.DO_NOTHING, null=True)

	def __str__(self):
		return self.description

class AccountingTransaction(models.Model):

	job = models.ForeignKey(Job, null=True, blank=True, on_delete=models.DO_NOTHING)
	Tjob = models.CharField(max_length=10)
	Tphase = models.CharField(max_length=12,null=True, verbose_name='Cost Code')
	Trantyp = models.CharField(max_length=25,null=True)
	Trandat = models.DateField(auto_now=False,null=True, verbose_name='Tran Date')
	Tactdat = models.DateField(auto_now=False,null=True,verbose_name='Acctg Date')
	Tamount = models.DecimalField(decimal_places =2, max_digits=10, default=0,verbose_name='Amount')
	Tdracct = models.CharField(max_length=50,null=True,verbose_name='Debit Account')
	Tcracct = models.CharField(max_length=50,null=True) 
	Tcat = models.CharField(max_length=50,null=True)
	Extra = models.CharField(max_length=50,null=True)
	Commitment = models.CharField(max_length=50,null=True,verbose_name="PO")
	Vendor = models.CharField(max_length=50,null=True) 
	SOURCE = models.CharField(max_length=50,null=True)
	date_stamp = models.DateField(auto_now=False)
	sage_row_id = models.CharField(max_length=50, unique=True)
	Tinv = models.CharField(max_length=50,null=True)
	costcode = models.ForeignKey(CostCode, null=True, blank=True, on_delete=models.DO_NOTHING)
	purchaseorder = models.ForeignKey(PurchaseOrder, null=True, blank=True, on_delete=models.DO_NOTHING)
	is_upgrade = models.BooleanField(default=0)
	salesoption = models.ForeignKey(SalesOption, null=True, blank=True, on_delete=models.DO_NOTHING)

	def __str__(self):
		return self.sage_row_id

class AccountingOption(models.Model):
	job = models.ForeignKey(Job, on_delete=models.DO_NOTHING)
	code = models.CharField(max_length=50, null=True)
	sage_row_id = models.CharField(max_length=50, null=True)

	def __str__(self):
		return self.description

class ScheduleTask(models.Model):
	procore_id = models.BigIntegerField(unique=True)
	plat = models.ForeignKey(Plat, on_delete=models.PROTECT)
	name = models.CharField(max_length=100,null=True)
	percent_complete = models.IntegerField(default=0)
	start = models.DateField(auto_now=False, null=True, blank=True)
	finish = models.DateField(auto_now=False, null=True, blank=True)
	baseline_start = models.DateField(auto_now=False, null=True, blank=True)
	baseline_finish = models.DateField(auto_now=False, null=True, blank=True)
	milestone = models.BooleanField(default=0)
	resource_name = models.CharField(max_length=30,null=True, blank=True)

	def __str__(self):
		return self.name

#PROFORMA

class CommunityPlan(models.Model):
	name = models.CharField(max_length=50, unique=True, null=True)
	plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
	community = models.ForeignKey(Community, on_delete=models.PROTECT)

	def save(self, *args, **kwargs):
		self.name = self.community.name +" | "+self.plan.full_name
		super(CommunityPlan, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ('name',)

class ProformaMilestone(models.Model):
	name = models.CharField(max_length=50, unique=True)
	date = models.DateField(auto_now=False)
	MILESTONE_CHOICES = [('BusinessPlan','BusinessPlan'),('GoNoGo','GoNoGo'),('VerticalLaunch','VerticalLaunch')]
	milestone = models.CharField(choices=MILESTONE_CHOICES, default=None,max_length=50)
	community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True)
	communityplans = models.ManyToManyField(CommunityPlan, through='proformamilestonedetail', blank=True, verbose_name='Community Plans') #Instead of having the user select these. I could auto-select all plans
	plat = models.ForeignKey(Plat, on_delete=models.PROTECT, null=True, blank=True) #plat can be null
	is_complete = models.BooleanField(default=0)

	def __str__(self):
		return self.name	

	def clean(self):
		# Don't allow vertical launch milestones to have a null plat
		if self.milestone == 'VerticalLaunch' and self.plat is None:
			raise ValidationError(_('Plat cannot be none when VerticalLaunch is specified.'), code='noplat')

		elif self.milestone != 'VerticalLaunch' and self.plat is not None:
			raise ValidationError(_('Plat must be none when VerticalLaunch is not specified.'))


class ProformaMilestoneDetail(models.Model):
	proformamilestone = models.ForeignKey(ProformaMilestone, on_delete=models.CASCADE)
	communityplan = models.ForeignKey(CommunityPlan, on_delete=models.CASCADE)
	#Value fields
	base_price = models.IntegerField(default=0)
	lot_cost = models.IntegerField(default=0)
	lot_fmv = models.IntegerField(default=0)
	permit_cost = models.IntegerField(default=0)
	hard_cost = models.IntegerField(default=0)
	project_management_cost = models.IntegerField(default=0)
	sales_commission_cost = models.IntegerField(default=0)
	financing_cost = models.IntegerField(default=0)

class ImportTask(models.Model):
	failed = models.BooleanField(default=0)
	complete = models.BooleanField(default=0)
	db_table =  models.CharField(max_length=50, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	datetime = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-datetime',)

class ImportTaskError(models.Model):
	importtask = models.ForeignKey(ImportTask, on_delete=models.CASCADE)
	row_number = models.IntegerField(default=0, null=True)
	message = models.CharField(max_length=200)






