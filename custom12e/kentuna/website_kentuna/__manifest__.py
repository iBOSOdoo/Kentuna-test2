# -*- coding: utf-8 -*-
{
    'name': "website_kentuna",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "TechUltra Solution",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['website','website_sale','website_crm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/cart.xml',
        'views/header_footer_view.xml',
        # 'security/ir.model.access.csv',
        # 'views/cart.xml',
        # 'views/templates.xml',
        'views/home_view.xml',
        'views/about_us.xml',
        'views/store.xml',
        'views/contact_us.xml',
        # 'views/my_account.xml',
        'views/my_account.xml',
        # 'views/lost_password.xml',
        # 'views/orders.xml',
        # 'views/downloads.xml',
        # 'views/address.xml',
        # 'views/send_message.xml',
        # 'views/register.xml',
        'views/feature_products_view.xml',
        # 'views/billing.xml',
        # 'views/shipping.xml',
        # 'views/account_details.xml',
        'static/src/xml/kentuna.xml',
        'static/src/xml/kentuna_js.xml',
        'templates/feature_products_template.xml',
    ],
    # only loaded in demonstodoo_kentunaration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}