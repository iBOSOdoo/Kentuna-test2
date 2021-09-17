# coding: utf-8
{
    "name": "Ipay Payment Getway",
    "category": "Payment Acquirer",
    "version": "12.0.1.0.0",
    "category": "Payment Getway Modules",
    "license": "",
    "author": "TechUltra Solutions",
    "website": "https://www.techultrasolutions.com/",

    # any module necessary for this one to work correctly
    "depends": ['payment'],

    # always loaded
    "data": [
        'views/payment_views.xml',
        'views/payment_payweb_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    "qweb": [],
    "installable": True,
    "auto_install": False
}
