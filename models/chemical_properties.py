# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SdsChemicalProperties(models.Model):
    _name = "sds.chemical.properties"
    _description = "Physical and chemical properties"

    name = fields.Char('Property name', translate=True)


class SdsChemicalPropertiesLine(models.Model):
    """
    This class is for physical properties in section 9.1
    """
    _name = "sds.chemical.properties.line"
    _description = "Physical and chemical properties line"

    name_id = fields.Many2one('sds.chemical.properties', 'Property', copy=True)
    value = fields.Char('Property value', translate=True)
