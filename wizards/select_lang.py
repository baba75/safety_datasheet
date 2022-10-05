# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SelectLangReportWizard(models.TransientModel):
    _name = "select.lang.report.wizard"
    _description = "Select SDS language for printing"

    @api.model
    def _get_languages(self):
        langs = self.env['res.lang'].search([('translatable', '=', True)])
        return [(lang.code, lang.name) for lang in langs]

    def get_report(self):
        """Call when button 'Print' clicked.
               """
        data = {
            'ids': self.env.context.get('active_ids'),
            'model': self._name,
            'form': {
                'lang': self.lang,
            },
        }
        # use `module_name.report_id` as reference.
        # `report_action()` will call `_get_report_values()` and pass `data` automatically.
        return self.env.ref('safety_datasheet.safety_sds_report').report_action(self, data=data)

    lang = fields.Selection(_get_languages, string='Language', required=True, default='en_US')

class SelectLangRecap(models.AbstractModel):
    """Abstract Model for report template.
    for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
    """

    _name = 'report.safety_datasheet.report_safety_datasheet'
    _description = 'Abstract model for custom SDS report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data:
            lang = data['form']['lang'] if data['form'] else 'en_US'
        else:
            lang = 'en_US'
        datasheets = self.env['sds.datasheet'].search([('id','in',data['ids'])])

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'doc_lang': lang,
            'docs': datasheets,
        }

