# -*- coding: utf-8 -*-
# Copyright 2023 Alberto Carollo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

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
                                     relation="sds_pictogram_ghs_rel",
                                     domain="[('category', '=', 'hazard')]",
                                     context={'default_category': 'hazard'},
                                     copy=True)
    code = fields.Char('Hazard Code', required=True)
    name = fields.Char('Description', required=True, translate=True)
    
    _rec_names_search = ['name', 'code']

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
