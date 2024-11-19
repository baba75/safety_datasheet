# -*- coding: utf-8 -*-
# Copyright 2023 Alberto Carollo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from ..models import datasheet

class SelectLangReportWizard(models.TransientModel):
    _name = "select.lang.report.wizard"
    _description = "Select SDS language for printing"

    @api.model
    def _get_languages(self):
        langs = self.env['res.lang'].search([('active', '=', True)])
        return [(lang.code, lang.name) for lang in langs]

    def get_report(self):
        """Called when button 'Print' is clicked.
               """
        data = {
            'ids': self.env.context.get('active_ids'),
            'model': self._name,
            'form': {
                'lang': self.lang,
                'country': self.country
            },
        }
        # use `module_name.report_id` as reference.
        # `report_action()` will call `_get_report_values()` and pass `data` automatically.
        return self.env.ref('safety_datasheet.safety_sds_report').report_action(self, data=data)

    lang = fields.Selection(_get_languages, string='Language', required=True, default='en_US')
    country = fields.Selection(datasheet.COUNTRY, string='Country', required=True, default='Italy')

class SelectLangRecap(models.AbstractModel):
    """Abstract Model for report template.
    for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
    """

    _name = 'report.safety_datasheet.report_safety_datasheet'
    _description = 'Abstract model for custom SDS report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data:
            if "form" in data:
                lang = data['form']['lang']
                country = data['form']['country']
            else:
                lang = 'en_US'
                country = 'Italy'
        if type(data['ids']) == str:
            # I'm probably call it from the url :-)
            # you can see html version using:
            # https://<yourserver>/report/html/safety_datasheet.report_safety_datasheet?ids=<your_id>&model=sds.datasheet
            data['ids'] = [data['ids']]
            if data['lang']:
                lang = data['lang']
            if data['country']:
                country = data['country']
        
        datasheets = self.env['sds.datasheet'].search([('id','in',data['ids'])])
        
        # Here we inject the emergency telephone number (point 1.4) specific for the country
        pcenter = self.env['sds.poison.centre'].search([('country','=',country)])
        if pcenter:
            doc_et = pcenter[0].name
        else:
            company = self.env.company
            doc_et = '<p>' + company.name + ' : ' + company.phone + '</p>'   
        
        # Here we inject the National Distributor
        distributor = self.env['sds.distributor'].search([('country','=',country)])
        if distributor:
            doc_dist = distributor[0].name
        else:
            company = self.env.company
            if(company.street and company.zip and company.city):
                doc_dist = '<p>' + company.name + '<br/>' + company.street
                doc_dist += '<br/>' + company.zip + ' ' + company.city + ' ' + company.state_id.name
                doc_dist += '<br/>' + company.country_id.name 
                doc_dist += '<br/> Phone: ' + company.phone
                doc_dist += '<br/> Email: ' + company.email
                doc_dist += '</p>'
            else:
                doc_dist = '<p><br/></p>'

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'doc_lang': lang,
            'doc_et': doc_et,
            'doc_dist': doc_dist,
            'docs': datasheets,
        }

