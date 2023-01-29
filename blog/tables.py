
from django_tables2 import TemplateColumn, Column
import django_tables2 as tables
from .models import *
from django_tables2.utils import A
from django.db.models import Sum

class LenderTable(tables.Table):
	# Edit and delete columns must be defined here and not externally in order to retain the scope and usage of "record.id" within the template
	edit = TemplateColumn(
		template_code='''
			{% if user.is_authenticated %}
				<button type="button" 
					class="btn btn-warning btn-sm js-update-item" 
					id="{{record.id}}_edit_btn" 
					data-url="{% url 'lender_update' record.id %}">
				<i class="fas fa-pencil-alt"></i> Edit</button>
			{% endif %}''', 
		orderable=False, 
		attrs={
			"th": {"class": "edit-btn"},
			"td":{"class":"edit-btn"}
		})
	delete = TemplateColumn(
		template_code='''
			{% if user.is_authenticated %}
				<button type="button" 
					class="btn btn-danger btn-sm js-delete-item" 
					id="{{record.id}}_delete_btn" 
					data-url="{% url 'delete_view' 'lender' record.id %}">
				<i class="fas fa-trash"></i> DELETE</button>
			{% endif %}''', 
		orderable=False, 
		attrs={
			"th": {"class": "delete-btn"},
			"td":{"class":"delete-btn"}
		})
	
	class Meta:
		model = Lender
		template_name = "django_tables2/bootstrap4.html"
		fields = ("name","interest_rate","points","ltc_limit","ltv_limit")
		attrs = {'class': 'paleblue lender col-md-12', 'width':'100%','id': 'item-table'}
		ordering = 'name'

class TrafficTable(tables.Table):
	edit = TemplateColumn(template_code='''{% if user.is_authenticated %}<button type="button" class="btn btn-warning btn-sm js-update-item" id="{{record.id}}_edit_btn" data-url="{% url 'traffic_update' record.id %}"><i class="fas fa-pencil-alt"></i> Edit</button>{% endif %}''', orderable=False, attrs={"th": {"class": "edit-btn"},"td":{"class":"edit-btn"}})
	delete = TemplateColumn(template_code='''{% if user.is_authenticated %}<button type="button" class="btn btn-danger btn-sm js-delete-item" id="{{record.id}}_delete_btn" data-url="{% url 'delete_view' 'traffic' record.id %}"><i class="fas fa-trash"></i> DELETE</button>{% endif %}''', orderable=False, attrs={"th": {"class": "delete-btn"},"td":{"class":"delete-btn"}})
	
	class Meta:
		model = Traffic
		template_name = "django_tables2/bootstrap4.html"
		fields = ("community","count","be_back_count","date")
		attrs = {'class': 'paleblue traffic col-md-12', 'width':'100%','id': 'item-table'}
		ordering = 'plat'

class CommunityTable(tables.Table):	
	edit = TemplateColumn(template_code='''{% if user.is_authenticated %}<button type="button" class="btn btn-warning btn-sm js-update-item" id="{{record.id}}_edit_btn" data-url="{% url 'community_update' record.id %}"><i class="fas fa-pencil-alt"></i> Edit</button>{% endif %}''', orderable=False, attrs={"th": {"class": "edit-btn"},"td":{"class":"edit-btn"}})
	delete = TemplateColumn(template_code='''{% if user.is_authenticated %}<button type="button" class="btn btn-danger btn-sm js-delete-item" id="{{record.id}}_delete_btn" data-url="{% url 'delete_view' 'community' record.id %}"><i class="fas fa-trash"></i> DELETE</button>{% endif %}''', orderable=False, attrs={"th": {"class": "delete-btn"},"td":{"class":"delete-btn"}})
	name = tables.Column(linkify=("community-detail", [tables.A("pk")]))	

	class Meta:
		model = Community
		template_name = "django_tables2/bootstrap4.html"
		fields = ("com_id","name","region","abbreviation","partner","excise_tax_rate", "sales_tax_rate", "city","state", "zip_code" )
		attrs = {
			'class': 'paleblue community col-md-12', 
			'width':'100%',
			'id': 'item-table'
		}

class PlatTable(tables.Table):
	view_plans = tables.TemplateColumn(template_code='''<button type="button" class="btn btn-blue btn-sm js-view-accordion" id="{{record.id}}" action="/plat/{{record.id}}/plans" ><i class="fas fa-plus"></i>Plans</button>''', orderable=False)
	edit = TemplateColumn(template_code='''{% if user.is_authenticated %}<button type="button" class="btn btn-warning btn-sm js-update-item" id="{{record.id}}_edit_btn" data-url="{% url 'plat_update' record.id %}"><i class="fas fa-pencil-alt"></i> Edit</button>{% endif %}''', orderable=False, attrs={"th": {"class": "edit-btn"},"td":{"class":"edit-btn"}})
	delete = TemplateColumn(template_code='''{% if user.is_authenticated %}<button type="button" class="btn btn-danger btn-sm js-delete-item" id="{{record.id}}_delete_btn" data-url="{% url 'delete_view' 'plat' record.id %}"><i class="fas fa-trash"></i> DELETE</button>{% endif %}''', orderable=False, attrs={"th": {"class": "delete-btn"},"td":{"class":"delete-btn"}})
	community__name = tables.Column(verbose_name='Community')
	name = tables.Column(verbose_name='Plat Name')
	from_procore = tables.BooleanColumn()
	class Meta:
		model = Plat
		# template_name = 'blog/templates/tables/table-with-subs.html'
		order_by = ('community__name', 'name')
		template_name = "django_tables2/bootstrap4.html"
		fields = ("id","community__name","name","project_status","project_type","from_procore","active",'project_lot_count','build_order','default_start_pace')
		attrs = {
			'class': 'paleblue plat col-md-12', 
			'id': 'item-table',
			'width':'100%',
			'td': {"name": lambda bound_column: bound_column.verbose_name.lower().replace(" ", "_")}
		}
		row_attrs = {
			'id': lambda record: '{}'.format(record.pk)+"_row",
			'class':'parent'
		}

class PlatPlanSubTable(tables.Table):
	edit = TemplateColumn(template_code='''{% if user.is_authenticated %}<button type="button" class="btn btn-warning btn-sm js-update-item" id="{{record.id}}_edit_btn" data-url="{% url 'platplan_update' record.id %}"><i class="fas fa-pencil-alt"></i> Edit</button>{% endif %}''', orderable=False, attrs={"th": {"class": "edit-btn"},"td":{"class":"edit-btn"}})
	budget = tables.Column(linkify=("loantransaction-detail", [tables.A("pk")]))	
	class Meta:
		model = PlatPlan
		template_name = "django_tables2/bootstrap4.html"
		fields = ("id","description","base_price","lot_cost","lot_fmv","budget")
		attrs = {
			'class': 'paleblue plan col-md-12', 
			'width':'100%',
			'id': 'item-table',
			'td': {"name": lambda bound_column: bound_column.verbose_name.lower().replace(" ", "_")}
		}

class JobTable(tables.Table):
	edit = TemplateColumn(template_code='''{% if user.is_authenticated %}<button type="button" class="btn btn-warning btn-sm js-update-item" id="{{record.id}}_edit_btn" data-url="{% url 'job_update' record.id %}"><i class="fas fa-pencil-alt"></i> Edit</button>{% endif %}''', orderable=False, attrs={"th": {"class": "edit-btn"},"td":{"class":"edit-btn"}})
	edit_loan = TemplateColumn(template_code='''{% if user.is_authenticated %}<button type="button" class="btn btn-warning btn-sm js-update-item" id="{{record.id}}_edit_btn" data-url="{% url 'loan_update' record.id %}"><i class="fas fa-pencil-alt"></i> Edit</button>{% endif %}''', orderable=False, attrs={"th": {"class": "edit-btn"},"td":{"class":"edit-btn"}})
	
	class Meta:
		model = Job
		template_name = "django_tables2/bootstrap4.html"
		fields = ('plat__community','number','plan','construction_status','attached_count','elevation','garage_orientation','garage_add')
		attrs = {
			'class': 'paleblue job col-md-12', 
			'width':'100%',
			'id': 'item-table',
			'td': {"name": lambda bound_column: bound_column.verbose_name.lower().replace(" ", "_")}
		}

class PlanJobTable(tables.Table):
	edit = TemplateColumn(template_code='''{% if user.is_authenticated %}<button type="button" class="btn btn-warning btn-sm js-update-item" id="{{record.id}}_edit_btn" data-url="{% url 'job_update' record.id %}"><i class="fas fa-pencil-alt"></i> Edit</button>{% endif %}''', orderable=False, attrs={"th": {"class": "edit-btn"},"td":{"class":"edit-btn"}})
	class Meta:
		model = Job
		template_name = "django_tables2/bootstrap4.html"
		fields = ('plat__community','number','construction_status','attached_count','elevation','garage_orientation','garage_add','product_type')
		attrs = {
			'class': 'paleblue job col-md-12', 
			'width':'100%',
			'id': 'item-table',
			'td': {"name": lambda bound_column: bound_column.verbose_name.lower().replace(" ", "_")}
		}
	
class JobTable2(tables.Table):	
	class Meta:
		model = Job
		order_by = model._meta.ordering
		template_name = "django_tables2/bootstrap4.html"
		fields = ('number','sales_status','actual_closing_date','plan__full_name','attached_count','elevation','garage_orientation','garage_add','sales_price')
		attrs = {'class': 'paleblue job col-md-12', 'width':'100%'}

class PlanTable(tables.Table):	
	view_jobs = tables.TemplateColumn(template_code='''<button type="button" class="btn btn-blue btn-sm js-view-accordion" id="{{record.id}}" action="/plan/{{record.id}}/jobs/" ><i class="fas fa-plus"></i>Jobs</button>''', orderable=False)
	edit = TemplateColumn(template_code='''{% if user.is_authenticated %}<button type="button" class="btn btn-warning btn-sm js-update-item" id="{{record.id}}_edit_btn" data-url="{% url 'plan_update' record.id %}"><i class="fas fa-pencil-alt"></i> Edit</button>{% endif %}''', orderable=False, attrs={"th": {"class": "edit-btn"},"td":{"class":"edit-btn"}})
	delete = TemplateColumn(template_code='''{% if user.is_authenticated %}<button type="button" class="btn btn-danger btn-sm js-delete-item" id="{{record.id}}_delete_btn" data-url="{% url 'delete_view' 'plan' record.id %}"><i class="fas fa-trash"></i> DELETE</button>{% endif %}''', orderable=False, attrs={"th": {"class": "delete-btn"},"td":{"class":"delete-btn"}})
		
	class Meta:
		model = Plan
		template_name = "django_tables2/bootstrap4.html"
		fields = ("id","full_name","size","garage_count",'bedroom_count','bath_count','width','load',"is_active","is_attached","levels","master_on_main")
		attrs = {
			'class': 'paleblue plan col-md-12',
			'width':'100%',
			'id': 'item-table'
		}
		row_attrs = {
			'id': lambda record: '{}'.format(record.pk)+"_row",
			'class':'parent'
		}
		
class MasterLoanPackageTable(tables.Table):
	view_masterloans = tables.TemplateColumn(template_code='''<button type="button" class="btn btn-blue btn-sm js-view-accordion" id="{{record.id}}" action="/masterloanpackage/{{record.id}}/masterloans" ><i class="fas fa-plus"></i>View Master Loans</button>''', orderable=False)
	edit = TemplateColumn(template_code='''{% if user.is_authenticated %}<button type="button" class="btn btn-warning btn-sm js-update-item" id="{{record.id}}_edit_btn" data-url="{% url 'masterloanpackage_update' record.id %}"><i class="fas fa-pencil-alt"></i> Edit</button>{% endif %}''', orderable=False, attrs={"th": {"class": "edit-btn"},"td":{"class":"edit-btn"}})
	delete = TemplateColumn(template_code='''{% if user.is_authenticated %}<button type="button" class="btn btn-danger btn-sm js-delete-item" id="{{record.id}}_delete_btn" data-url="{% url 'delete_view' 'masterloanpackage' record.id %}"><i class="fas fa-trash"></i> DELETE</button>{% endif %}''', orderable=False, attrs={"th": {"class": "delete-btn"},"td":{"class":"delete-btn"}})
	
	class Meta:
		model = MasterLoanPackage
		template_name = "django_tables2/bootstrap4.html"
		fields = ('community','description','lender','submission_date','appraisal_date','expiration_date','status')
		order_by = model._meta.ordering
		# exclude = ('standard','receive_cash_back','uses_master_appraisal')
		attrs = {
			'class': 'paleblue masterloanpackage col-md-12',
			'width':'100%',
			'id': 'item-table'
		}
		row_attrs = {
			'id': lambda record: '{}'.format(record.pk)+"_row",
			'class':'parent'
		}
		
class MasterLoanSubTable(tables.Table):
	edit = TemplateColumn(template_code='''{% if user.is_authenticated %}<button type="button" class="btn btn-warning btn-sm js-update-item" id="{{record.id}}_edit_btn" data-url="{% url 'masterloan_update' record.id %}"><i class="fas fa-pencil-alt"></i> Edit</button>{% endif %}''', orderable=False, attrs={"th": {"class": "edit-btn"},"td":{"class":"edit-btn"}})
	budget = tables.Column(linkify=("loantransaction-detail", [tables.A("platplan__id")]))
	class Meta:
		model = MasterLoan
		template_name = "django_tables2/bootstrap4.html"
		fields = ("platplan__id","platplan__description","platplan__base_price","platplan__lot_cost","platplan__lot_fmv","appraised_value",'lot_release', 'budget')
		order_by = ("platplan__description",)
		attrs = {
			'class': 'paleblue plan col-md-12', 
			'width':'100%',
			'id': 'item-table',
			'td': {"name": lambda bound_column: bound_column.verbose_name.lower().replace(" ", "_")}
		}

class InvestorTable(tables.Table):	
	edit = tables.LinkColumn('investor-update',text='Edit', args=[A("pk")])
	delete = tables.LinkColumn('investor-delete',text='Delete', args=[A("pk")])
		
	class Meta:
		model = Investor
		template_name = "django_tables2/bootstrap4.html"
		fields = ('name','total_capacity', )

class PurchaseOrderTable(tables.Table):	
	
	class Meta:
		model = AccountingTransaction
		template_name = "django_tables2/bootstrap4.html"
		fields = ('number','description','vendor','status','date_issued','issued_by','Total_POs','Total_Cost','Total_Open',)


class TransactionTable(tables.Table):
	Tamount = Column(attrs={'td':{'class':'dollar'}})
	class Meta:
		model = AccountingTransaction
		template_name = "django_tables2/bootstrap4.html"
		fields = ('Tphase','Commitment','Extra','costcode__description','Tamount','Trandat','Tactdat','SOURCE','Tdracct')

class UpgradesTable(tables.Table):

	class Meta:
		model = SalesOption
		template_name = "django_tables2/bootstrap4.html"
		fields = ('description','quantity','price','amount')

class CancelledPOTable(tables.Table):
	class Meta:
		model = AccountingTransaction
		template_name = "django_tables2/bootstrap4.html"
		fields = ('purchaseorder__number','purchaseorder__description','sage_balance')

class ZeroPOTable(tables.Table):
	class Meta:
		model = AccountingTransaction
		template_name = "django_tables2/bootstrap4.html"
		fields = ('Tphase','costcode__description','estimate_amount','po_amount','cost_amount')	

class UnpricedUpgradesTable(tables.Table):
	class Meta:
		model = SalesOption
		template_name = "django_tables2/bootstrap4.html"
		fields = ('code','description','quantity','price')	

class FlaggedVariancesTable(tables.Table):
	class Meta:
		model = SalesOption
		template_name = "django_tables2/bootstrap4.html"
		fields = ('Tphase','costcode__description','estimate_amount','po_amount','variance_amount','error_amount')	

class UpgradesWithoutPOTable(tables.Table):
	class Meta:
		model = SalesOption
		template_name = "django_tables2/bootstrap4.html"
		fields = ('code','description','quantity','price','po_amount')	

class TieOutProgressTable(tables.Table):
	job__number = tables.Column(linkify=("tieout_full", [tables.A("pk")])) 
	progress = tables.TemplateColumn(template_code='''<div class="tieout_progress" id="progress_{{record.id}}"><div class="progress_bar"><div class="complete"></div></div><div class="total"></div></div>''', orderable=False, attrs={"th":{'class':'progress_bar'}})
	completed_tasks = tables.Column(attrs={"td": {"class": "completed_tasks"}})
	total_tasks = tables.Column(attrs={"th":{"class":"total_tasks"},"td": {"class": "total_tasks"}})

	class Meta:
		model = TieOut
		template_name = "django_tables2/bootstrap4.html"
		fields = ('job__number','job__plat__community','job__actual_closing_date','stage','flagged_tasks','completed_tasks','progress','total_tasks','last_update')
		attrs = {'class': 'paleblue tieout_progress_table col-md-12', 'width':'100%','id': 'item-table tieout_progress_table'}
		order_by = ("-job__actual_closing_date",)

class CostCodeTable(tables.Table):
	# number = tables.Column(linkify=("costcode_update", [tables.A("pk")]))
	edit = TemplateColumn(template_code='''{% if user.is_authenticated %}<button type="button" class="btn btn-warning btn-sm js-update-item" id="{{record.id}}_edit_btn" data-url="{% url 'costcode_update' record.id %}"><i class="fas fa-pencil-alt"></i> Edit</button>{% endif %}''', orderable=False, attrs={"th": {"class": "edit-btn"},"td":{"class":"edit-btn"}})
	
	class Meta:
		model = CostCode
		template_name = "django_tables2/bootstrap4.html"
		fields = ('number','description','costcodecategory','is_active')
		attrs = {
			'class': 'paleblue costcode col-md-12', 
			'width':'100%',
			'id': 'item-table',
			}
		row_attrs = {
			'id': lambda record: '{}'.format(record.pk)+"_row",
			'class':'parent'
			}

class CostCodeBreakdownTable(tables.Table):
	# number = tables.Column(linkify=("costcode_update", [tables.A("pk")]))
	class Meta:
		model = CostCode
		template_name = "django_tables2/bootstrap4.html"
		fields = ('number','description','costcodecategory','is_active')
		attrs = {
			'class': 'paleblue costcode col-md-12', 
			'width':'100%',
			'id': 'item-table',
			}
		row_attrs = {
			'id': lambda record: '{}'.format(record.pk)+"_row",
			'class':'parent'
			}

class ProformaMilestoneTable(tables.Table):
	view_plans = tables.TemplateColumn(template_code='''<button type="button" class="btn btn-blue btn-sm js-view-accordion" id="{{record.id}}" action="/proformamilestone/{{record.id}}/details" ><i class="fas fa-plus"></i>View Details</button>''', orderable=False)
	edit = TemplateColumn(template_code='''{% if user.is_authenticated %}<button type="button" class="btn btn-warning btn-sm js-update-item" id="{{record.id}}_edit_btn" data-url="{% url 'proformamilestone_update' record.id %}"><i class="fas fa-pencil-alt"></i> Edit</button>{% endif %}''', orderable=False, attrs={"th": {"class": "edit-btn"},"td":{"class":"edit-btn"}})
	delete = TemplateColumn(template_code='''{% if user.is_authenticated %}<button type="button" class="btn btn-danger btn-sm js-delete-item" id="{{record.id}}_delete_btn" data-url="{% url 'proformamilestone_delete' record.id %}"><i class="fas fa-trash"></i> DELETE</button>{% endif %}''', orderable=False, attrs={"th": {"class": "delete-btn"},"td":{"class":"delete-btn"}})
	
	class Meta:
		model = ProformaMilestone
		template_name = "django_tables2/bootstrap4.html"
		fields = ('community','name','plat','milestone','date','is_complete')
		attrs = {
			'class': 'paleblue proformamilestone col-md-12', 
			'width':'100%',
			'id': 'item-table',
			}
		row_attrs = {
			'id': lambda record: '{}'.format(record.pk)+"_row",
			'class':'parent'
			}

class ProformaMilestoneSubtable(tables.Table):
	edit = TemplateColumn(template_code='''{% if user.is_authenticated %}<button type="button" class="btn btn-warning btn-sm js-update-item" id="{{record.id}}_edit_btn" data-url="{% url 'proformamilestonedetail_update' record.id %}"><i class="fas fa-pencil-alt"></i>Edit</button>{% endif %}''', orderable=False, attrs={"th": {"class": "edit-btn"},"td":{"class":"edit-btn"}})
	class Meta:
		model = ProformaMilestoneDetail
		template_name = "django_tables2/bootstrap4.html"
		order_by = ("communityplan",)
		exclude = ('proformamilestone', 'edit','id')
		attrs = {
			'class': 'paleblue plan col-md-12', 
			'width':'100%',
			'id': 'item-table',
			'td': {"name": lambda bound_column: bound_column.verbose_name.lower().replace(" ", "_")}
		}

class ImportTaskTable(tables.Table):

	failed = tables.Column(linkify=("importtaskerror-home", [tables.A("pk")]), verbose_name='Has Errors') 
	user__profile__full_name = tables.Column(verbose_name='User')

	class Meta:
		model = ImportTask
		order_by = model._meta.ordering
		template_name = "django_tables2/bootstrap4.html"
		fields = ('db_table','user__profile__full_name','datetime','complete','failed')
		attrs = {
			'class': 'paleblue importtask col-md-12', 
			'width':'100%',
			'id': 'item-table',
			}

class ImportTaskErrorTable(tables.Table):

	class Meta:
		model = ImportTaskError
		template_name = "django_tables2/bootstrap4.html"
		fields = ('row_number','message')
		attrs = {
			'class': 'paleblue importtaskerror col-md-12', 
			'width':'100%',
			'id': 'item-table',
			}

class LoanTransactionDetailTable(tables.Table):	
	user__profile__full_name = tables.Column(verbose_name='User')
	
	class Meta:
		model = LoanTransaction
		template_name = "django_tables2/bootstrap4.html"
		fields = ('purchasingactivity__name','purchasingactivity__costcode__number','date_stamp','user__profile__full_name','amount')
		attrs = {
			'class': 'paleblue plan col-md-12', 
			'width':'100%',
			'id': 'item-table',
			'td': {"name": lambda bound_column: bound_column.verbose_name.lower().replace(" ", "_")}
		}