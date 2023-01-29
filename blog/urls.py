import debug_toolbar
from django.conf import settings
from django.urls import path, include
from django.contrib.auth.views import *
from . import views
from .views import *
from .forms import UserLoginForm
# for AJAX forms
from django.conf.urls import url, include
from django.contrib import admin

# Error handlers
handler403 = views.handler_403
handler404 = views.handler_404
handler500 = views.handler_500

urlpatterns = [
# User authentication
    url(r'^login/$', user_login, name='login_user'),
    url(r'^logout/$', user_logout, name='logout_user'),
# Home page
    path('', Home,name = 'blog-home'),
# Cost Codes
    url(r'^costcode/$',CostCodeView.as_view(), name='costcode-home'),
    url(r'^costcode/(?P<pk>\d+)/update/$', CostCodeUpdateView.as_view(), name='costcode_update'),
    path('costcode/<int:pk>/sage_import/', ImportCostCodes.as_view(), name='costcode-sage_import'),
# AJAX forms
    url(r'^admin/', admin.site.urls),
    path('ajax/load-platplans/',  load_platplans, name='ajax_load_platplans'),
    path('ajax/load-communityplans/',  load_communityplans, name='ajax_load_communityplans'),
    path('ajax/load-communityplats/',  load_communityplats, name='ajax_load_communityplats'),
# Import / Export
    url(r'^(?P<page_name>\w+)/import/$', ImportItemsView.as_view(), name='items_import'),
    url(r'^(?P<page_name>\w+)/export/$', login_required(ExportItemsView.as_view()), name='items_export'),
    url(r'^(?P<page_name>\w+)/template/$', login_required(ExportTemplateView.as_view()), name='template_export'),
    url(r'^(?P<page_name>\w+)/import/template/$', login_required(ExportTemplateView.as_view()), name='template_export'),
# Global URLs
    url(r'^(?P<page_name>\w+)/(?P<pk>\d+)/delete/$', 
        permission_required([
                'blog.delete_community',
                'blog.delete_lender',
                'blog.delete_plat',
                'blog.delete_traffic',
                'blog.delete_plan',
                'blog.delete_masterloanpackage'
            ],
            raise_exception=True, 
            login_url='/login/'
        )(DeleteView.as_view()), 
        name='delete_view'
    ),
# Community
    url(r'^community/$', CommunityView.as_view(), name='community-home'),
    url(r'^community/create/$', CommunityCreateView.as_view(), name='community_create'),
    url(r'^community/(?P<pk>\d+)/update/$', CommunityUpdateView.as_view(), name='community_update'),
    url(r'^community/(?P<pk>\d+)/delete/$', CommunityDeleteView.as_view(), name='community_delete'),
    path('community/<int:pk>/detail/', CommunityDetailView.as_view(), name='community-detail'),
# Job
    url(r'^job/$', list_job, name='job-home'),
    url(r'^job/(?P<pk>\d+)/update/$', update_job, name='job_update'),
    url(r'^job/address/import/data/', login_required(JobAddressImportView.as_view()), name='jobaddress-import'),
    url(r'^job/import/data/', login_required(JobImportView.as_view()), name='job-import'),
# Lender
    url(r'^lender/$', list_lender, name='lender-home'),
    url(r'^lender/create/$', create_lender, name='lender_create'),
    url(r'^lender/(?P<pk>\d+)/update/$', update_lender, name='lender_update'),
# Plats
    url(r'^plat/$', list_plat, name='plat-home'),
    url(r'^plat/create/$', create_plat, name='plat_create'),
    url(r'^plat/(?P<pk>\d+)/update/$', update_plat, name='plat_update'),
    url(r'^plat/(?P<pk>\d+)/plans', get_plat_plans, name='plat_get_plans'),
# Plan
    url(r'^plan/$', list_plan, name='plan-home'),
    url(r'^plan/create/$', create_plan, name='plan_create'),
    url(r'^plan/(?P<pk>\d+)/update/$', update_plan, name='plan_update'),
    url(r'^plan/(?P<pk>\d+)/jobs', get_plan_jobs, name='plan_get_jobs'),
# Traffic
    url(r'^traffic/$', list_traffic, name='traffic-home'),
    url(r'^traffic/create/$', create_traffic, name='traffic_create'),
    url(r'^traffic/(?P<pk>\d+)/update/$', update_traffic, name='traffic_update'),
    path('taffic/import/data/', TrafficImportView.as_view(), name='traffic-import'),
# Master Loan Package
    url(r'^masterloanpackage/$', list_masterloanpackage, name='masterloanpackage_list'),
    url(r'^masterloanpackage/create/$', create_masterloanpackage, name='masterloanpackage_create'),
    url(r'^masterloanpackage/(?P<pk>\d+)/update/$', update_masterloanpackage, name='masterloanpackage_update'),
    url(r'^masterloan/(?P<pk>\d+)/update/$', update_masterloan, name='masterloan_update'),
    url(r'^masterloanpackage/(?P<pk>\d+)/masterloans/$', get_masterloanpackage_masterloans, name='masterloanpackage_get_masterloans'),
# Loan
    url(r'^loan/(?P<job_id>\d+)/update/$', update_loan, name='loan_update'),
    url(r'^loan/create/$', create_loan, name='loan_create'),
# Loan Transaction
    path('loantransaction/detail/<int:platplan>/',LoanTransactionDetailView.as_view(), name='loantransaction-detail'),
    path('loantransaction/import/data/', LoanTransactionImportView.as_view(), name='loantransaction-import'),
    path('loantransaction/detail/<int:platplan>/export/', LoanTransactionExportView.as_view(), name='loantransaction-export'),
# Plat Plan
    url(r'^platplan/(?P<pk>\d+)/update/$', update_platplan, name='platplan_update'),
# Partner
    path('partner/new/', PartnerCreateView.as_view(), name='partner-create'),
    path('partner/<int:pk>/update/', PartnerUpdateView, name='partner-update'),
# Procore
    path('procore', ProcoreView, name = 'procore-home'),
# Tieout
    url(r'^tieout/$',TieOutProgressView.as_view(), name='tieout_progress'),
    url(r'^tieout/(?P<pk>\d+)/$',TieoutView.as_view(), name='tieout_full'),
    url(r'^tieout/(?P<pk>\d+)/breakdown/$',TieoutBreakdown.as_view(), name='tieout_breakdown'),
    url(r'^tieout/(?P<pk>\d+)/cc_breakdown/$',TieoutCostCodeBreakdownView.as_view(), name='tieout_costcode_breakdown'),
    url(r'^tieout/progress/',TieOutProgressView.as_view(), name='tieout_progress'),
# Proforma Milestone
    url(r'^proformamilestone/$',ProformaMilestoneView.as_view(), name='proformamilestone-home'),
    path('proformamilestone/create/', ProformaMilestoneCreateView.as_view(), name='proformamilestone-create'),
    url(r'^proformamilestone/(?P<pk>\d+)/update/$', ProformaMilestoneUpdateView.as_view(), name='proformamilestone_update'),
    url(r'^proformamilestone/(?P<pk>\d+)/remove/$', ProformaMilestoneDeleteView.as_view(), name='proformamilestone_delete'),
    url(r'^proformamilestone/export/data/', login_required(ProformaMilestoneExportView.as_view()), name='proformamilestone-export'),
    url(r'^proformamilestone/import/data/', login_required(ProformaMilestoneImportView.as_view()), name='proformamilestone-import'),
# Proforma Milestone Detail
    url(r'^proformamilestonedetail/export/data/', login_required(ProformaMilestoneDetailExportView.as_view()), name='proformamilestonedetail-export'),
    url(r'^proformamilestonedetail/import/data/', login_required(ProformaMilestoneDetailImportView.as_view()), name='proformamilestonedetail-import'),
# Proforma View Details
    url(r'^proformamilestone/(?P<pk>\d+)/details/$', get_proformamilestone_details, name='proformamilestone_get_details'),
# Import Task
    url(r'^importtask/$',ImportTaskView.as_view(), name='importtask-home'),
    url(r'^importtask/(?P<pk>\d+)/$',ImportTaskErrorView.as_view(), name='importtaskerror-home'),
# Goal
    url(r'^goal/import/data/', login_required(GoalImportView.as_view()), name='goal-import'),
# Debug
    path('__debug__/', include(debug_toolbar.urls)),
# Django-rq
    url(r'^django-rq/', include('django_rq.urls')),

]