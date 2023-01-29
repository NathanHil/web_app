# Generated by Django 3.1.3 on 2021-09-15 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0209_tieouttask_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tieouttask',
            name='name',
            field=models.CharField(choices=[('review_standard', 'Review Standard'), ('review_sqft', 'Review Sqft'), ('review_levels', 'Review Level'), ('review_start_date', 'Review Start Date'), ('review_plan_name', 'Review Plan Name'), ('review_revenue', 'Review Revenue'), ('review_base_price', 'Review Base Price'), ('review_lot_premium', 'Review Lot Premium'), ('review_plan_width', 'Review Plan Width'), ('review_completion_date', 'Review Completion Date'), ('review_sale_date', 'Review Sale Date'), ('review_close_date', 'Review Close Date'), ('review_upgrades', 'Review Upgrades'), ('review_upgrades_credits', 'Review Upgrades Credits'), ('review_concessions', 'Review Concessions'), ('review_lot_cost', 'Review Lot Cost'), ('review_lot_fmv', 'Review Lot FMV'), ('review_permit', 'Review Permit'), ('review_hard_cost', 'Review Hard Cost'), ('review_hard_cost_variance', 'Review Hard Cost Variance'), ('review_upgrade_cost', 'Review Upgrade Cost'), ('review_state_taxes', 'Review State Taxes'), ('review_project_management', 'Review Project Management'), ('review_subdivision', 'Review Subdivision'), ('review_warranty', 'Review Warranty'), ('review_marketing', 'Review Marketing'), ('review_sales_commissions', 'Review Sales Commissions'), ('review_financing', 'Review Financing'), ('review_concessions', 'Review Concessions'), ('review_open_pos', 'Review Open POs'), ('review_price_incentive', 'Review Price Incentive'), ('review_net_profit', 'Review Net Profit'), ('review_lot_profit', 'Review Lot Profit'), ('review_home_profit', 'Review Home Profit'), ('review_upgrade_profit', 'Review Upgrade Profit'), ('review_direct_cost_margin', 'Review Direct Cost Margin'), ('review_gross_profit_margin', 'Review Gross Profit Margin'), ('review_net_profit_margin', 'Review Net Profit Margin'), ('review_upgrade_margin', 'Review Upgrade Margin'), ('review_lot_cost_ratio', 'Review Lot Cost Ratio'), ('review_direct_cost_ratio', 'Revuew Direct Cost Ratio'), ('review_total_lot_and_directs', 'Review Total Lot and Directs'), ('review_sales_and_marketing_ratio', 'Review Sales and Marketing Ratio'), ('review_indirect_cost_ratio', 'Review Indirect Cost Ratio'), ('review_base_price_per_sqft', 'Review Base Price per SQFT'), ('review_hard_cost_per_sqft', 'Review Hard Cost per SQFT'), ('review_net_profit_per_sqft', 'Review Net Profit per SQFT')], default=None, max_length=100),
        ),
        migrations.AddIndex(
            model_name='costcodecategory',
            index=models.Index(fields=['name'], name='blog_costco_name_f82a87_idx'),
        ),
    ]
