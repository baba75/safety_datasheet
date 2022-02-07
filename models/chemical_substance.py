# -*- coding: utf-8 -*-

from odoo import models, fields, _

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
    last_update = fields.Date(string="Revision date", default=fields.Date.today(), required=True)
    wrk_exp_limit = fields.Boolean('Workplace exposure limit', defalt=False)
    wrk_exp_tlv = fields.Html(string="TLV details",
                                      default=lambda s: _(
                                          '<table class="table table-bordered"><thead class="table-columns">'
                                          '<tr><th rowspan="2">Region</th><th rowspan="2">Legislation</th>'
                                          '<th colspan="3">Long-term Exposure Limit (LTEL) Values</th>'
                                          '<th colspan="3">Short-term Exposure Limit (STEL) Values</th>'
                                          '<th rowspan="2">Skin Designation</th>'
                                          '<th rowspan="2">Dermal Sensitization</th>'
                                          '<th rowspan="2">Respiratory Sensitization</th>'
                                          '<th rowspan="2">Work Sector</th>'
                                          '<th rowspan="2">Effective Date</th>'
                                          '<th rowspan="2">Expiration Date</th>'
                                          '<th rowspan="2">Miscellaneous Notes</th></tr>'
                                          '<tr><th>mg/m<sup>3</sup></th><th>ppm</th><th>f/ml</th><th>mg/m<sup>3</sup></th>'
                                          '<th>ppm</th><th>f/ml</th></tr></thead>'
                                          '<tbody class="table-data"><tr><td><br></td><td><br></td><td><br></td>'
                                          '<td><br></td><td><br></td><td><br></td><td><br></td><td><br></td>'
                                          '<td><br></td><td><br></td><td><br></td><td><br></td><td><br></td>'
                                          '<td><br></td><td><br></td></tr></tbody></table>'),
                                      translate=True, sanitize=False)
    Classification = fields.Many2many('sds.chemical.classification', string="EU Chemical Classification")
    reactivity = fields.Many2many('sds.sentences', relation="sds_substance_reactivity_rel",
                                    domain="[('category', '=', 'reactivity')]",
                                    string='Reactivity',
                                    context={'default_category': 'reactivity'})


class SdsChemicalMixture(models.Model):
    """
    This class is for table in section 3.2
    """
    _name = "sds.chemical.mixture"
    _description = "Chemical Mixture"

    datasheet_id = fields.Many2one('sds.datasheet', 'Related Datasheet', copy=True)
    substance = fields.Many2one('sds.chemical.substance', 'Chemical name')
    concentration = fields.Char('Concentration Range', translate=True)