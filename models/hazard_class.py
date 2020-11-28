# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SdsHazardClass(models.Model):
    """
    This class contains the Hazard Classes (like 'Expl. 1.1','Flam. Liq. 1',...)
    See point 1.1.2.1.1. Hazard class and category codes of REGULATION (EC) No 1272/2008
    (http://data.europa.eu/eli/reg/2008/1272/2018-03-01)
    the name should not be translated
    """
    _name = "sds.hazard.class"
    _description = "Hazard Classification"

    name = fields.Char('Category Code', required="True")
    h_class = fields.Char('Hazard Class', required="True", translate=True)