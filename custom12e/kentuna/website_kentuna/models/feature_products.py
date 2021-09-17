from odoo import api, fields, models

class Websitefeature(models.Model):
    _name = "website.feature.products"

    name = fields.Char(string='Name')
    feature_product_ids = fields.Many2many('product.template','feature_product_id', string="Feature Products")



