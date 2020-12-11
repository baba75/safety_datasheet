# -*- coding: utf-8 -*-

from odoo import models, fields, _


class SdsRegulation(models.Model):
    """
    This class contains the regulation on the substance or mixture
    that is not already provided in the safety data sheet  - for section 15
    """
    _name = "sds.regulation"
    _description = "Regulations"

    name = fields.Char('Regulation', required="True", translate=True)
    url = fields.Char('Link URL', translate=True)


class SdsRegulatoryInformation(models.Model):
    """
    This class contains the regulatory information on the substance or mixture
    that is not already provided in the safety data sheet  - for section 15
    """
    _name = "sds.regulatory.information"
    _description = "Regulatory information"

    regulation = fields.Many2one('sds.regulation', 'Regulation', copy=True)
    text = fields.Html(string="Relevant information",
                       default = lambda s: _("Not applicable."),
                       translate=True)
