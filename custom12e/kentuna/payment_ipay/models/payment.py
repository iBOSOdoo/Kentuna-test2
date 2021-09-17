# -*- coding: utf-8 -*-

from hashlib import sha1
import hmac

import json
from werkzeug import urls
from datetime import datetime
import requests
from urllib.parse import parse_qsl
from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.tools.float_utils import float_compare

import logging
_logger = logging.getLogger(__name__)

class PaymentAcquirerPayWeb(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('ipay', 'iPay')])
    ipay_vendor_id = fields.Char(string='Vendor ID', required_if_provider='ipay', groups='base.group_user')
    ipay_hash_key = fields.Char(string='Hash Key', required_if_provider='ipay', groups='base.group_user')

    def _get_ipay_urls(self, environment):
#         print('_get_payweb_urls')
        """ iPay URLs"""
        return {'ipay_form_url': 'https://payments.ipayafrica.com/v3/ke',
                'ipay_ipn_url': 'https://www.ipayafrica.com/ipn'}

    def _ipay_generate_sign(self, inout, values):
#         print ("_iPay_generate_sign")
        """ Generate the shasign for incoming or outgoing communications.
        :param self: the self browse record. It should have a shakey in shakey out
        :param string inout: 'in' (odoo contacting iPay) or 'out' (iPay
                             contacting odoo).
        :param dict values: transaction values

        :return string: shasign
        """
        if inout not in ('in', 'out'):
            raise Exception("Type must be 'in' or 'out'")

        if inout == 'in':
            keys = "live,oid,inv,ttl,tel,eml,vid,curr,p1,p2,p3,p4,cbk,cst,crl".split(',')
            sign = ''.join('%s' % (values.get(k) or '') for k in keys)
        else:
            keys = "live,oid,inv,ttl,tel,eml,vid,curr,p1,p2,p3,p4,cbk,cst,crl".split(',')
            sign = ''.join('%s' % (values.get(k) or '') for k in keys)

        hashed = hmac.HMAC(self.ipay_hash_key.encode(), sign.encode('utf-8'), sha1)
        return hashed.hexdigest()


    @api.multi
    def ipay_form_generate_values(self, values):
#         print('ipay_form_generate_values')
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

#         initate_url = 'https://secure.paygate.co.za/payweb3/initiate.trans'
#         payload = dict(PAYGATE_ID=self.payweb_paygate_id, REFERENCE=values['reference'],
#                        AMOUNT=int(values['amount'] * 100), CURRENCY='ZAR',
#                        RETURN_URL=urls.url_join(base_url, '/payment/payweb/return'),
#                        TRANSACTION_DATE=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), LOCALE='en-za', COUNTRY='ZAF',
#                        EMAIL=values.get('partner_email'),
#                        NOTIFY_URL=urls.url_join(base_url, '/payment/payweb/notify'),)

        payload = dict(
                live="0" if self.environment == 'test' else "1",
                creditcard="1",
                oid=values['reference'],
                inv=values['reference'],
                ttl=values['amount'],
                tel=values.get('partner_phone'),
                eml=values.get('partner_email'),
                vid=self.ipay_vendor_id,
                curr='KES',
                p1=values['reference'],
                p2=values['amount'],
                p3="vc",
                p4="vc",
                cbk=urls.url_join(base_url, '/payment/ipay/return'),
                lbk=urls.url_join(base_url, '/payment/ipay/error'),
                cst="1",
                crl="0"
            )

        payload['hsh'] = self._ipay_generate_sign('in', payload)

        return payload

    @api.multi
    def ipay_get_form_action_url(self):
#         print('ipay_get_form_action_url')
        self.ensure_one()
        return self._get_ipay_urls(self.environment)['ipay_form_url']

    def ipay_payment_ipn(self, data):
        query_url = self._get_ipay_urls(self.environment)['ipay_ipn_url']
        
        payload = dict(
            vendor=self.ipay_vendor_id,
            id=data.get('id'),
            ivm=data.get('ivm'),
            qwh=data.get('qwh'),
            afd=data.get('afd'),
            poi=data.get('poi'),
            uyt=data.get('uyt'),
            ifd=data.get('ifd'),
            )
        print ("payload>>>>>.", payload)
        response = requests.request('GET', query_url, headers={}, data=payload, 
                                    files={}, allow_redirects=False, timeout=None)
        return response.text


class PaymentTransactionPayweb(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _ipay_form_get_tx_from_data(self, data):
#         print('_iPay_form_get_tx_from_data',data)
        """ Given a data dict coming from iPay, verify it and find the related
        transaction record. """
        reference = data.get('id')

        transaction = self.search([('reference', '=', reference)])
#         transaction.sale_order_ids.write({'reference':reference})
        if not transaction:
            error_msg = (_('iPay: received data for reference %s; no order found') % (reference))
            raise ValidationError(error_msg)
        elif len(transaction) > 1:
            error_msg = (_('iPay: received data for reference %s; multiple orders found') % (reference))
            raise ValidationError(error_msg)
        return transaction

    @api.multi
    def _ipay_form_get_invalid_parameters(self, data):
#         print('_iPay_form_get_invalid_parameters')
        invalid_parameters = []
        if float_compare(float(data.get('mc', '0.0')), self.amount, 2) != 0:
            invalid_parameters.append(
                ('Amount', data.get('mc'), '%.2f' % self.amount))
        return invalid_parameters

    @api.multi
    def _ipay_form_validate(self, data):
#         print('_iPay_form_validate')


        acq = self.env['payment.acquirer'].sudo().search([('provider', '=', 'ipay')])[0]
        ipn_status = acq.sudo().ipay_payment_ipn(data)
        status = data.get('status')
#         print (status, "ipn_status>>>>>>", ipn_status)

        if ipn_status != status:
            _logger.warning(
            'iPay: %s Return Status not match with IPN Status %s', status, ipn_status)
#             print (">>>>>>>>>> Status not match with IPN!")

        result = self.write({
            'acquirer_reference': data.get('txncd'),
            'date': fields.Datetime.now(),
        })
        if status == 'bdi6p2yy76etrs':
            self._set_transaction_pending()
        elif status == 'aei7p7yrx4ae34':
            self._set_transaction_done()
#         elif status == 2:
#             self._set_transaction_cancel()
# #             self._set_transaction_error(data.get('RESULT_DESC'))
#         elif status == 3:
#             self._set_transaction_cancel()
        else:
            self._set_transaction_cancel()
#             self._set_transaction_error(data.get('RESULT_DESC'))

        return result

