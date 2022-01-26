# -*- coding: utf-8 -*-

from odoo import models, fields

class SdsChemicalClassification(models.Model):
    """
    This class is necessary for correct classification of chemical substances, i.e. in section 3.2 od the SDS (Mixtures)
    The relation between classification and hazard statement is not always unique, for example:
    Acute Tox. - 3 - H301
    Acute Tox. - 3 - H331
    Acute Tox. - 3 - H311
    """
    _name = "sds.chemical.classification"
    _description = "Chemical Classification"

    HazardCategories = fields.Many2one('sds.hazard.class', 'Hazard Categories')
    HazardStatement = fields.Many2one('sds.hazard.statement', 'Hazard Statement')

class SdsChemicalSubstance(models.Model):
    """
    Find data about substances here https://echa.europa.eu/
    """
    _name = "sds.chemical.substance"
    _description = "Chemical Substances"

    name = fields.Char('Chemical Name', translate=True)
    IUPACname = fields.Char('IUPAC Name')
    CASno = fields.Char('CAS Number')
    ECno = fields.Char('EC Number')
    REACHno = fields.Char('REACH Number')
    wrk_exp_limit = fields.Boolean('Workplace exposure limit', defalt=False)
    Classification = fields.Many2many('sds.chemical.classification', string="EU Chemical Classification")

class SdsChemicalMixture(models.Model):
    """
    This class is for table in section 3.2
    """
    _name = "sds.chemical.mixture"
    _description = "Chemical Mixture"

    datasheet_id = fields.Many2one('sds.datasheet', 'Related Datasheet', copy=True)
    substance = fields.Many2one('sds.chemical.substance', 'Chemical name')
    concentration = fields.Char('Concentration Range', translate=True)