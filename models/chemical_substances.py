# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SdsChemicalSubstances(models.Model):
    """
    Find data about substances here https://echa.europa.eu/
    """
    _name = "sds.chemical.substances"
    _description = "Chemical Substances"

    name = fields.Char('Chemical Name', translate=True)
    IUPACname = fields.Char('IUPAC Name')
    CASno = fields.Char('CAS Number')
    ECno = fields.Char('EC Number')
    REACHno = fields.Char('REACH Number')
    Classification = fields.Many2many('sds.chemical.classification', string="EU Chemical Classification")

class SdsChemicalMixture(models.Model):
    """
    This class is for table in section 3.2
    """
    _name = "sds.chemical.mixture"
    _description = "Chemical Mixture"

    datasheet_id = fields.Many2one('sds.datasheet', 'Related Datasheet', copy=True)
    substance = fields.Many2one('sds.chemical.substances', 'Chemical name')
    concentration = fields.Char('Concentration Range', translate=True)