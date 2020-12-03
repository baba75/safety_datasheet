# -*- coding: utf-8 -*-

from odoo import models, fields

class SdsChemicalProperty(models.Model):
    _name = "sds.chemical.property"
    _description = "Physical and chemical properties"

    name = fields.Char('Property name', translate=True)


class SdsChemicalPropertyLine(models.Model):
    """
    This class is for physical properties in section 9.1
    """
    _name = "sds.chemical.property.line"
    _description = "Physical and chemical properties line"

    name_id = fields.Many2one('sds.chemical.property', 'Property', copy=True)
    value = fields.Char('Property value', translate=True)
