# -*- coding: utf-8 -*-
from odoo import models, api, _
from odoo.exceptions import UserError


class PayslipConfirm(models.TransientModel):
    """
    This wizard will confirm Payslips
    """

    _name = "hr.payslip.run.confirm"
    _description = "Confirm the selected Payslips"

    @api.multi
    def payslip_confirm(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []

        for record in self.env['hr.payslip.run'].browse(active_ids):
            for slip in record.slip_ids:
                if record.state == 'close':
                    raise UserError(_("Selected Payslip(s) cannot be confirmed as they are not in 'Draft' state."))
                slip.action_payslip_done()
        return {'type': 'ir.actions.act_window_close'}


class PayslipCompute(models.TransientModel):
    """
    This wizard will compute Payslips
    """

    _name = "hr.payslip.run.compute"
    _description = "Compute the selected Payslips"

    @api.multi
    def payslip_compute(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []

        for record in self.env['hr.payslip.run'].browse(active_ids):
            for slip in record.slip_ids:
                if record.state == 'close':
                    raise UserError(_("Selected Payslip(s) cannot be confirmed as they are not in 'Draft' state."))
                slip.compute_sheet()
        return {'type': 'ir.actions.act_window_close'}
