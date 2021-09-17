# -*- coding: utf-8 -*-

import logging
import pprint
import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class PayWebController(http.Controller):

    @http.route(['/payment/ipay/return', '/payment/ipay/cancel', '/payment/ipay/error'], type='http', auth='public', csrf=False)
    def payweb_return(self, **post):
        print('RETURNING-------------------------------', post)
        
#         {'p2': '170.0', 'p3': 'vc', 'qwh': '1100406167', 'uyt': '104013111', 'agt': '246398279', 'ivm': 'SO081-33', 
#          'id': 'SO081-33', 'afd': '1481328537', 'status': 'aei7p7yrx4ae34', 'poi': '1370791762', 'mc': '170.00', 
#          'p1': 'SO081-33', 'msisdn_id': 'JOHN DOE', 'txncd': '177153297981', 'channel': 'MPESA', 'p4': 'vc', 
#          'ifd': '186835014', 'msisdn_idnum': '08347087049'}

        tx_obj = request.env['payment.transaction'].sudo()
        tx = tx_obj.search([('reference', '=', post.get('id'))])

        if post and tx.state in ['draft', 'pending', 'authorized']:
            tx_obj.form_feedback(post, 'ipay')
            request.session["__payment_tx_ids__"] = [tx.id]

        return werkzeug.utils.redirect('/payment/process')

#     @http.route(['/payment/payweb/notify'], type='http', auth='public', csrf=False)
#     def payweb_notify(self, **post):
#         print("Notifying=====================================")
# #         print ("p tx ids>>", request.session.get("__payment_tx_ids__", []))
# 
#         """ PayWeb."""
#         _logger.info(
#             'PayWeb: entering form_feedback with post data %s', pprint.pformat(post))
#         tx_obj = request.env['payment.transaction'].sudo()
#         tx = tx_obj.search([('reference', '=', post.get('REFERENCE'))])
# 
#         if post and tx.state in ['draft', 'pending', 'authorized']:
#             tx_obj.form_feedback(post, 'payweb')
#             request.session["__payment_tx_ids__"] = [tx.id]
# #             print ("p tx ids>>", request.session.get("__payment_tx_ids__"))
#         return 'OK'