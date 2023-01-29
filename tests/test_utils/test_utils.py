from blog.utils import *
from blog.models import *
from blog.resources import ProformaMilestoneDetailResource
from blog.mixins import import_with_worker
from django.test import TestCase

from datetime import date
import django_rq
from tablib import Dataset
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

#Run Tests with => sudo python3 manage.py test tests/test_utils --nomigrations
#Run Utils tests with => sudo python3 manage.py test tests.test_utils.test_utils.UtilsTest --nomigrations

class ImportTest(TestCase):
  @classmethod
  def setUp(self):
     #Create all parent records for proforma milestone detail and import task
    self.c = Community.objects.create(id=1,name='Biggies Pad')
    self.pl = Plan.objects.create(id=1,name='ABERDEEN',garage_count=3)
    self.cp = CommunityPlan.objects.create(id=1,plan_id=1, community_id=1, name='Biggies Pad | ABERDEEN 3 car')
    self.pm = ProformaMilestone.objects.create(name = 'Biggie Smalls', milestone = 'BusinessPlan',community_id = 1,date=date(2021,1,1))
    self.u = User.objects.create(username='biggie', id=1)

    #Get a list of the headers from the resource
    self.resource = ProformaMilestoneDetailResource()
    self.headers = self.resource.get_diff_headers()
    """
      'community_plan',
      'proformamilestone',
      'base_price',
      'lot_cost',
      'lot_fmv',
      'permit_cost',
      'hard_cost',
      'project_management_cost',
      'sales_commission_cost',
      'financing_cost'
    """

    #Get queue and set is_async to false in order to process on the same test thread
    self.q = django_rq.get_queue("low", is_async=False)

  def test_import_with_worker_errors(self):
    print('test_import_with_worker_errors')
    #Test the failure happens as expected and the importtask and errors objects are correctly updated

    #Create a mock data set
    import_data = [(self.cp.name+"yipes",self.pm.name,25,25,25,25,25,25,25,25,)]

    #Create a task
    task = ImportTask(user_id=self.u.id, complete=0)
    task.db_table = self.resource._meta.model._meta.db_table # gets associated model's table name 
    task.save()

    #Define variables and send to queue
    dataset = Dataset(*import_data,headers=self.headers)
    self.q.enqueue(import_with_worker, self.resource, dataset, self.u.id, task)

    #Verify that an import task was created, and that it has errors
    import_tasks = ImportTask.objects.filter(failed=True, complete=True)
    self.assertEqual(len(import_tasks),1)

    #Verify that the error has the correct row number and message
    err = ImportTaskError.objects.filter(importtask_id=import_tasks[0].id)[0]
    self.assertEqual(err.message, 'CommunityPlan matching query does not exist.')
    self.assertEqual(err.row_number, 2)

  def test_import_with_worker(self):
    print("test_import_with_worker")

    #Create a mock data set
    import_data = [(self.cp.name,self.pm.name,25,25,25,25,25,25,25,25,)]

    #Create a task
    task = ImportTask(user_id=self.u.id, complete=0)
    task.db_table = self.resource._meta.model._meta.db_table # gets associated model's table name 
    task.save()

    #Define variables and send to queue
    dataset = Dataset(*import_data,headers=self.headers)
    self.q.enqueue(import_with_worker, self.resource, dataset, self.u.id, task)

    #Verify that an import task was created, and that it has no errors
    import_tasks = ImportTask.objects.filter(failed=False, complete=True)
    self.assertEqual(len(import_tasks),1)

    #Verify that the proforma detail object was created and the data is accurate
    pmd = ProformaMilestoneDetail.objects.filter(proformamilestone__name=self.pm.name, communityplan_id=1)
    self.assertEqual(len(pmd),1)
    self.assertEqual(pmd[0].base_price, 25)

class UtilsTest(TestCase):

  def test_cost_code_import(self):
    print("test_cost_code_import")
    c1 = Community.objects.create(
      id=1,
      name='Commie'
      )

    pl1 = Plat.objects.create(
      id=1,
      community_id=1,
      name='Platty',
      )

    j1 = Job.objects.create(
      id=1,
      plat_id=1,
      number='123-00-001')

    j2 = Job.objects.create(
      id=2,
      plat_id=1,
      number='123-00-002')

    cc1 = CostCode.objects.create(
      id=1,
      is_active=True,
      is_group=False,
      description="Build Something else",
      number='3-01-0001')

    cc2 = CostCode.objects.create(
      id=2,
      is_active=True,
      is_group=False,
      description='Build Something',
      number='3-01-0002')

    dataset = import_cost_codes(c1.id)

    self.assertEqual(dataset.width,5, 'the dataset is not the required lengh')

    #Build a set of jobs, cost codes in the dataset
    jobs = set()
    codes = set()

    for row in dataset:
      if row[0] == '*':
        jobs.add(row[1])
      else:
        codes.add(row[1])

    self.assertEqual(jobs, {j1.number,j2.number})
    self.assertEqual(codes, {cc1.number, cc2.number})






