# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Kenyan Payroll',
    'author': 'iBos',
    'website': 'https://www.ibos.co.ke',
    'category': 'Localization',
    'depends': ['hr_payroll','hr_payroll_account'],
    'description': """
Kenyan Payroll Salary Rules.
============================

    -Configuration of hr_payroll for Kenyan localization
    * Employee Contracts
    * Allow to configure Basic / Gross / Net Salary
    * Employee PaySlip
    * Allowance / Deduction
    * Integrated with Leaves Management
    * Medical Allowance, Travel Allowance, ...
    """,
    'data': [
         'views/l10n_ke_hr_payroll_view.xml', 'views/res_config_setting_view.xml',
         'data/l10n_ke_hr_payroll_data.xml',
         'data/pay_input_data.xml',
         'data/stipend_data.xml',
         'report/payroll_detail_report_view.xml',
         'wizard/confirm_run_payroll_view.xml'
     ],
}
