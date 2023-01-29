
from blog.models import *
from tablib import Dataset
from django.db.models.functions import Left
from datetime import date


def import_with_worker(resource, dataset, user_id, task):

	#Run a dry run of the import to see if any errors pop up
	result = resource.import_data(dataset=dataset, dry_run=True, raise_errors=False, collect_failed_rows = True, user_id=user_id)

	# print(dir(result))
	# print(result.invalid_rows)
	# print(result.invalid_rows[0].error)
	# print(result.invalid_rows[0].error_dict)
	# print(result.invalid_rows[0].non_field_specific_errors)
	# print(result.invalid_rows[0].number)
	# print(result.invalid_rows[0].values)

	if not result.has_errors() and not result.has_validation_errors(): #import the data and save the task record
		resource.import_data(dataset=dataset, dry_run=False, user_id=user_id)
		task.complete = 1
		task.save()
			
	else: # Result has errors
		#Update the new task record and save it
		task.failed = 1
		task.complete = 1
		task.save()
		# Code added to view any row level errors that were returned. 
		errors = result.row_errors()[:5] #LIMIT to only 5 rows
		import_error_list = {} # {row_num:'error', row_num:'error', ...}

		for row_errors in errors: # row_errors = [row, {'list', 'of', 'errors'}]
			row_number = row_errors[0] # 123
			# print('Error occured at row number: ', row_number, 'in the import file')

			for row_error in row_errors[1]: # row_error = {'dict','of','errors'}
				# print("Error description", row_error.error)
				import_error_list[row_number+1] = row_error.error
		
		#Save error row numbers and messages
		for key, value in import_error_list.items():
			tt = ImportTaskError(importtask_id=task.id, row_number = key, message = value)
			tt.save()

		#Save validation errors
		for row in result.invalid_rows[:5]:
			row_number = row.number+1
			for key, error_list in row.error_dict.items():
				message = error_list[0]
				tt = ImportTaskError(importtask_id=task.id, row_number=row_number, message=message)
				tt.save()		

def migrate_masterloans():
	#Need to add platplan_id
	mls = MasterLoan.objects.all()

	for row in mls:
		phaseplan_id = row.phaseplan.id
		platplan_id = PlatPlan.objects.filter(phase_plan_id=phaseplan_id).first().id

		row.platplan_id = platplan_id

		row.save()

def import_cost_codes(community_id):
	"""take a community_id and build a file that will import cost codes to the PHI accounting database"""

	jobs = Job.objects.filter(actual_closing_date__isnull=True).filter(plat__community__id=community_id)
	today_date = date.today()
	today_str = today_date.strftime('%m%d%Y')

	prefixes = ['3-','4-','5-','7-','8-']

	codes = CostCode.objects.annotate(
	    prefix=Left('number', 2)).filter(prefix__in=prefixes).filter(is_group=False).filter(is_active=True)

	data = []

	for job in jobs:
		for i, code in enumerate(codes):
			if i == 0:
				data.append(('*', job.number,'','','')) #add job header
			data.append(("P",code.number,'','',today_str)) #add cost code
			data.append(("C",code.number,'','O',today_str)) #add zero budget line item

	return Dataset(*data)













