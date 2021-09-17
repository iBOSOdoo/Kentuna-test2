# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResLocalConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_l10n_ke_hr_payroll = fields.Boolean(string='Kenyan Payroll')
