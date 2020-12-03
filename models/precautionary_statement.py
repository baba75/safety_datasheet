# -*- coding: utf-8 -*-

from odoo import models, fields

class SdsPrecautionaryStatement(models.Model):
    """
        This class contains the P statement
        See ANNEX IV - List of precautionary statements of REGULATION (EC) No 1272/2008.
        Translations in major languages are already defined in the norm.
        (http://data.europa.eu/eli/reg/2008/1272/2018-03-01)
    """
    _name = "sds.precautionary.statement"
    _description = "Precautionary Statement"
    _order = "name"

    name = fields.Char('Prevention Code', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    description = fields.Char('Description', required=True, translate=True)
    MODE = [('P2', 'Prevention'),
            ('P3', 'Response'),
            ('P4', 'Storage'),
            ('P5', 'Disposal')]
    mode = fields.Selection(MODE)