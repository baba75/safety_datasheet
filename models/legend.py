# -*- coding: utf-8 -*-
# Copyright 2023 Alberto Carollo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields

class SdsLegend(models.Model):
    """
    This class contains the items for Legend needed in section 16
    """
    _name = "sds.legend"
    _description = "Legend entries"
    _order = "acronym"

    acronym = fields.Char('Acronym', required="True", translate=True)
    description = fields.Char('Extended description', required="True", translate=True)