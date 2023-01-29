# Generated by Django 3.1.3 on 2021-09-10 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0199_tieouttask_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='tieouttask',
            name='flag',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='tieouttask',
            name='name',
            field=models.CharField(choices=[('review_standard', 'Review Standard'), ('review_sqft', 'Review Sqft'), ('review_levels', 'Review Level'), ('review_start_date', 'Review Start Date'), ('review_plan_name', 'Review Plan Name'), ('review_revenue', 'Review Revenue'), ('review_base_price', 'Review Base Price'), ('review_lot_premium', 'Review Lot Premium'), ('review_plan_width', 'Review Plan Width'), ('review_completion_date', 'Review Completion Date'), ('review_sale_date', 'Review Sale Date'), ('review_close_date', 'Review Close Date'), ('review_upgrades', 'Review Upgrades'), ('review_upgrades_credits', 'Review Upgrades Credits'), ('review_concessions', 'Review Concessions'), ('review_lot_cost', 'Review Lot Cost'), ('review_lot_fmv', 'Review Lot FMV'), ('review_permit', 'Review Permit'), ('review_hard_cost', 'Review Hard Cost'), ('review_hard_cost_variance', 'Review Hard Cost Variance'), ('review_upgrade_cost', 'Review Upgrade Cost'), ('review_state_taxes', 'Review State Taxes'), ('review_project_management', 'Review Project Management'), ('review_subdivision', 'Review Subdivision'), ('review_warranty', 'Review Warranty'), ('review_marketing', 'Review Marketing'), ('review_sales_commissions', 'Review Sales Commissions'), ('review_financing', 'Review Financing'), ('sales_concessions_match', 'Sales Concessions Match'), ('review_open_pos', 'Review Open POs')], default=None, max_length=100),
        ),
    ]
