from blog.procoreIntegration import ProcoreIntegration
from blog.models import Plat, Community, Phase
from django.test import TestCase
from django.db import IntegrityError
import logging

#Run Tests with => sudo python3 manage.py test tests/test_procoreintegration --nomigrations
#sudo python3 manage.py test tests.test_procoreIntegration --nomigrations

class ProcoreIntegrationTest(TestCase):
  @classmethod
  def setUp(self):
    # Don't show logging messages while testing
    logging.disable(logging.CRITICAL)
    self.p = ProcoreIntegration()
  def test_get_record(self):
    print("test_get_record")
    record_id = 562949953428851
    record = self.p.get_record('Programs',record_id)
    self.assertEqual(562949953428851, record['id'])
  def test_project_is_plat(self):
    print("test_project_is_plat")
    plat_type = 'Master Plan'
    non_plat_type = 'Doobie'
    self.assertEqual(self.p.project_is_plat(plat_type),True)
    self.assertEqual(self.p.project_is_plat(non_plat_type),False)
  def test_delete_community(self):
    print("test_delete_community")
    #Delete should pass
    Community.objects.create(name="Doobie Estates",procore_id=420)
    webhook_payload = {
      'event_type':'delete',
      'resource_name': 'Programs',
      'resource_id': 420
    }
    data = self.p.process_webhook(webhook_payload)
    self.assertEqual(data['status'],'deleted')

    #Delete should except to integrity error because a dependent plat exists
    c = Community.objects.create(name="Weed street",procore_id=421)
    Plat.objects.create(community_id=c.id, name='Weed street plat 1')
    webhook_payload = {
      'event_type':'delete',
      'resource_name': 'Programs',
      'resource_id': 421
    }
    data = self.p.process_webhook(webhook_payload)
    self.assertTrue(isinstance(data['status'],IntegrityError))

    #Delete should except to does not exist error
    webhook_payload = {
      'event_type':'delete',
      'resource_name': 'Programs',
      'resource_id': 1234
    }
    data = self.p.process_webhook(webhook_payload)
    self.assertEqual(data['status'].__str__(), 'Community matching query does not exist.')
  def test_delete_plat(self):
    print("test_delete_plat")
    #Delete should pass
    c = Community.objects.create(name='The parent',procore_id=120)
    Plat.objects.create(name="Doobie Estates",procore_id=320, community_id = c.id)
    webhook_payload = {
      'event_type':'delete',
      'resource_name': 'Projects',
      'resource_id': 320
    }
    data = self.p.process_webhook(webhook_payload)
    self.assertEqual(data['status'],'deleted')

    #Delete should except to integrity error because a dependent phase exists
    p = Plat.objects.create(name="Weed street",procore_id=421, community_id=c.id)
    ph = Phase.objects.create(number='01', plat_id=p.id)
    webhook_payload = {
      'event_type':'delete',
      'resource_name': 'Projects',
      'resource_id': 421
    }
    data = self.p.process_webhook(webhook_payload)
    self.assertTrue(isinstance(data['status'],IntegrityError))

    #Delete should except to does not exist error
    webhook_payload = {
      'event_type':'delete',
      'resource_name': 'Projects',
      'resource_id': 1234
    }
    data = self.p.process_webhook(webhook_payload)
    self.assertEqual(data['status'].__str__(), 'Plat matching query does not exist.')
  def test_create_plat(self):
    print("test_create_plat")
    #This should result in creating a plat
    c= Community.objects.create(name='Flamers block', procore_id=678)
    webhook_payload = {
      'event_type':'create',
      'resource_name': 'Projects',
      'resource_id': 922      
    } 

    mock_api_request = {
      'id': 922,
      'name': 'Front Street Greens',
      'project_type':{'name':'Master Plan'},
      'active': True,
      'project_stage': {'name': 'Future'},
      'program': {'id': 678},
      'custom_fields': {'custom_field_34770': {'value': 25},'custom_field_50531': {'value': 20}},
    }

    data = self.p.process_webhook(webhook_payload, mock_api_request=mock_api_request)
    self.assertEqual(data['status'],'created')
    #This should result in an integrity error when attempting to create a plat
    Plat.objects.create(procore_id=423, name='Flamers Block', community_id = c.id)
    webhook_payload = {
      'event_type':'create',
      'resource_name': 'Projects',
      'resource_id': 424      
    } 

    mock_api_request = {
      'id': 424,
      'name': 'Flamers Block',
      'project_type':{'name':'Master Plan'},
      'active': True,
      'project_stage': {'name': 'Future'},
      'program': {'id': 678},
      'custom_fields': {'custom_field_34770': {'value': 25},'custom_field_50531': {'value': 20}},
    }
    data = self.p.process_webhook(webhook_payload, mock_api_request=mock_api_request)
    self.assertTrue(isinstance(data['status'],IntegrityError))
  def test_create_community(self):
    print("test_create_community")
    #This should result in creating a community
    webhook_payload = {
      'event_type':'create',
      'resource_name': 'Programs',
      'resource_id': 422      
    } 

    mock_api_request = {
      'id': 422,
      'name': 'Front Street Greens'
    }

    data = self.p.process_webhook(webhook_payload, mock_api_request=mock_api_request)
    self.assertEqual(data['status'],'created')
    #This should result in an integrity error when attempting to create a community
    Community.objects.create(procore_id=423, name='Flamers Block')
    webhook_payload = {
      'event_type':'create',
      'resource_name': 'Programs',
      'resource_id': 423      
    } 

    mock_api_request = {
      'id': 423,
      'name': 'Flamers Block'
    }
    data = self.p.process_webhook(webhook_payload, mock_api_request=mock_api_request)
    self.assertTrue(isinstance(data['status'],IntegrityError))
  def test_update_community(self):
    print("test_update_community")
    #This should result in updating a community
    Community.objects.create(procore_id=450, name='Old program name')
    webhook_payload = {
      'event_type':'update',
      'resource_name': 'Programs',
      'resource_id': 450      
    } 

    mock_api_request = {
      'id': 450,
      'name': 'New Program Name'
    }

    data = self.p.process_webhook(webhook_payload, mock_api_request=mock_api_request)
    c = Community.objects.get(procore_id=mock_api_request['id'])
    self.assertEqual(data['status'],'updated') 
    self.assertEqual(mock_api_request['name'], c.name)

    #This should result in a does not exist error
    webhook_payload = {
      'event_type':'update',
      'resource_name': 'Programs',
      'resource_id': 451      
    } 

    mock_api_request = {
      'id': 451,
      'name': 'The fuzz'
    }

    data = self.p.process_webhook(webhook_payload, mock_api_request=mock_api_request)
    c = Community.objects.get(procore_id=mock_api_request['id'])
    self.assertEqual(data['status'],'updated') 
    self.assertEqual(mock_api_request['name'], c.name)

    #This should result in an integrity error
    Community.objects.create(procore_id=333,name='The fuzzies')
    Community.objects.create(procore_id=444,name='The funnies')
    webhook_payload = {
      'event_type':'update',
      'resource_name': 'Programs',
      'resource_id': 444      
    } 

    mock_api_request = {
      'id': 444,
      'name': 'The fuzzies'
    }

    data = self.p.process_webhook(webhook_payload, mock_api_request=mock_api_request)
    self.assertTrue(isinstance(data['status'],IntegrityError))
  def test_update_plat_without_type(self):
    print('test_update_plat_without_type')
    #This tests if the project type is correctly set to None when it is not included in the payload
    c=Community.objects.create(procore_id=590, name='Jacky Bradley Jr')
    Plat.objects.create(procore_id=650, name='Fishy jack', community_id=c.id)
    webhook_payload = {
      'event_type':'update',
      'resource_name': 'Projects',
      'resource_id': 650
    } 

    mock_api_request = {
      'id': 650,
      'name': 'New Program Name',
      'active': True,
      'project_stage': {'name': 'Future'},
      'program': {'id': 590},
      'custom_fields': {'custom_field_34770': {'value': 25},'custom_field_50531': {'value': 20}},
    }

    data = self.p.process_webhook(webhook_payload, mock_api_request=mock_api_request)
    self.assertEqual(data['status'],'updated') 
    p = Plat.objects.get(procore_id=mock_api_request['id'])
    self.assertEqual(None, p.project_type)

  def test_update_plat(self):
    print("test_update_plat")
    #This should result in updating a plat
    print("Test that renaming a plat works")
    c=Community.objects.create(procore_id=490, name='Football Pitch')
    Plat.objects.create(procore_id=550, name='Old project name', community_id=c.id)
    webhook_payload = {
      'event_type':'update',
      'resource_name': 'Projects',
      'resource_id': 550
    } 

    mock_api_request = {
      'id': 550,
      'name': 'New Program Name',
      'active': True,
      'project_type':{'name':'Master Plan'},
      'project_stage': {'name': 'Future'},
      'program': {'id': 490},
      'custom_fields': {'custom_field_34770': {'value': 25},'custom_field_50531': {'value': 20}},
    }

    data = self.p.process_webhook(webhook_payload, mock_api_request=mock_api_request)
    p = Plat.objects.get(procore_id=mock_api_request['id'])
    self.assertEqual(data['status'],'updated') 
    self.assertEqual(mock_api_request['name'], p.name)

    print("Test updating a project that doesn't exist yet")
    webhook_payload = {
      'event_type':'update',
      'resource_name': 'Projects',
      'resource_id': 451      
    } 

    mock_api_request = {
      'id': 451,
      'name': 'The fuzz',
      'stage': 'Future',
      'active': True,
      'project_type':{'name':'Master Plan'},
      'project_stage': {'name': 'Future'},
      'program': {'id': 490},
      'custom_fields': {'custom_field_34770': {'value': 25},'custom_field_50531': {'value': 20}},
    }

    data = self.p.process_webhook(webhook_payload, mock_api_request=mock_api_request)
    self.assertEqual(data['status'].__str__(), 'updated')

    #This should result in an integrity error
    print("Test that the plat update fails when trying to re-use name")
    Plat.objects.create(procore_id=3333,name='The fuzzies',community_id=c.id)
    Plat.objects.create(procore_id=3344,name='The funnies',community_id=c.id)
    webhook_payload = {
      'event_type':'update',
      'resource_name': 'Projects',
      'resource_id': 3344      
    } 

    mock_api_request = {
      'id': 3344,
      'name': 'The fuzzies',
      'active': True,
      'project_type':{'name':'Master Plan'},
      'project_stage': {'name': 'Future'},
      'program': {'id': 490},
      'custom_fields': {'custom_field_34770': {'value': 25},'custom_field_50531': {'value': 20}},
    }

    data = self.p.process_webhook(webhook_payload, mock_api_request=mock_api_request)
    self.assertTrue(isinstance(data['status'],IntegrityError))


