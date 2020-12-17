# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.osv import expression

class SdsHazardStatement(models.Model):
    """
    This class contains the H and EUH statement, with their pictograms
    See ANNEX III of REGULATION (EC) No 1272/2008. Translations in major languages are already
    defined in the norm.
    (http://data.europa.eu/eli/reg/2008/1272/2018-03-01)
    """
    _name = "sds.hazard.statement"
    _description = "Hazard Statements"
    _order = "code"

    pictogram_ids = fields.Many2many('sds.pictogram',
                                     string="GHS pictograms",
                                     copy=True)
    code = fields.Char('Hazard Code', required=True)
    name = fields.Char('Description', required=True, translate=True)

    @api.multi
    def name_get(self):
        """
        Display Hazard Code + Hazard name
        if context 'show_only_code' in defined in view display only the code (e.g. H200)
        :return: name
        """
        if self._context.get('show_only_code'):
            res = []
            for hazard in self:
                name = hazard.code + ' ' + hazard.name
                res.append((hazard.id, name))
            return res
        else:
            res = []
            for hazard in self:
                name = hazard.code
                res.append((hazard.id, name))
            return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):

        if self._context.get('show_only_code') == True:
            if operator == 'ilike' and not (name or '').strip():
                return super(SdsHazardStatement, self)._name_search(name, args=args, operator=operator, limit=limit,
                                                                 name_get_uid=name_get_uid)
            elif operator in ('ilike', 'like', '=', '=like', '=ilike'):
                domain = expression.AND([
                    args or [],
                    ['|', ('name', operator, name), ('code', operator, name)]
                ])
                hazard_ids = self._search(domain, limit=limit, access_rights_uid=name_get_uid)
                return self.browse(hazard_ids).name_get()
        else:
            return super(SdsHazardStatement, self)._name_search(name, args=args, operator=operator, limit=limit,
                                                             name_get_uid=name_get_uid)