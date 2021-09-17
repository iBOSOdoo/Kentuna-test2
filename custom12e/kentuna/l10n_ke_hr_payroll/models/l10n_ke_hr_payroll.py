# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError
import logging
import string
import re


_logger = logging.getLogger(__name__)
try:
    import vatnumber
except ImportError:
    _logger.warning("PIN validation partially unavailable because the `pinnumber` Python library cannot be found. "
                    "Install it to support more countries, for example with `easy_install vatnumber`.")
    vatnumber = None

_ref_vat = {
    'ke': 'A012345678S'
}



class HrKeEmployee(models.Model):
    _inherit = 'hr.employee'

    kra_pin = fields.Char(string='KRA PIN', size=12)
    nhif_no = fields.Char("NHIF No.")
    nssf_no = fields.Char("NSSF No.")

    @api.model
    def simple_vat_check(self, pin_number):

        check_func_name = 'check_pin_ke'
        check_func = getattr(self, check_func_name, None) or getattr(vatnumber, check_func_name, None)
        if not check_func:
            # No VAT validation available, default to check that the country code exists
            return bool(self.env['res.country'].search([('code', '=ilike', 'KE')]))
        return check_func(pin_number)

    @api.constrains("kra_pin")
    def check_pin(self):
        # quick and partial off-line checksum validation
        check_func = self.simple_vat_check

        for partner in self:
            if not partner.kra_pin:
                continue
            pin_number = partner.kra_pin
            if not check_func(pin_number):
                _logger.info("Importing PIN Number [%s] is not valid !" % pin_number)
                msg = partner._construct_constraint_msg()
                raise ValidationError(msg)

    def _construct_constraint_msg(self):
        self.ensure_one()

        def default_pin_check(pn):
            # by default, in Kenya, a PIN number is valid if:
            #  it starts with a letter and P for company with A for individuals
            #  followed by 9 digits
            #  ends with an alphabetic letter.
            return pn[0] in string.ascii_lowercase and pn[10] in string.ascii_lowercase

        pin_number = self.kra_pin
        pin_no = "'C##D' (C=Alphabet Letter, ##=9 Numerics, D=Alphabet Letter)\n First letter starts with A"
        return '\n' + _('The PIN number [%s] for employee [%s] does not seem to be valid. \nNote: the expected format is %s') % (self.kra_pin, self.name, pin_no)

    def check_pin_ke(self, pin):
        KENYAN_PIN_REGEX=re.compile(r"\d?[A]\d[0-9]\d[0-9]\d[0-9]\d[0-9]\d?[A-Z]")

        if not KENYAN_PIN_REGEX.match(pin):
            return False

        return True


class HrKeContract(models.Model):
    _inherit = "hr.contract"

    deduct_nssf = fields.Boolean('Deduct NSSF')
    deduct_nhif = fields.Boolean('Deduct NHIF')
    monthly_relief = fields.Float('Monthly Relief')
    life_insurance_relief = fields.Float('Life Insurance Relief')
    h_bonus = fields.Float('H-Bonus')
    fixed_monthly_advance = fields.Float('Fixed Monthly Advance')
    motor_vehicle = fields.Float('Motor Vehicle Benefit')
    # commission = fields.Float('Commission')
    # overtime_amount = fields.Float('Overtime (Amount)')
    stipend_pay = fields.Float('Stipend Pay')
    stipend_adv = fields.Float('Stipend Advance')

    employee_cpf = fields.Float('Employee Pension Amount')
    employee_cpt_per = fields.Float('Employee Pension %')
    stima_sacco = fields.Float('Stima Sacco')
    welfare_deduct = fields.Float('Staff Welfare')
    deduct_cotu = fields.Boolean('Deduct COTU')
    deduct_union_dues = fields.Boolean('Deduct Union Dues')
    employee_loan_deduct = fields.Float('Employee Loan')
    motor_vehicle_benefit_deduct = fields.Float('Motor Vehicle Benefit Deduction')

    employer_cpf = fields.Float('Employer Pension Amount')
    employer_cpf_per = fields.Float('Employer Pension %')
    house_allowance = fields.Float('House Allowance')
    travel_allowance = fields.Float('Travel Allowance')
    other_allowance = fields.Float('Other Allowance')
    compute_hse_allowance = fields.Boolean('House Allowance')
    annual_leave_pay = fields.Boolean('Annual Leave Pay')
