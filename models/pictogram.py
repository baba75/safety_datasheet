# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SdsPictogram(models.Model):
    """
    Hazard pictograms (quick list and images here: https://en.wikipedia.org/wiki/GHS_hazard_pictograms)
    ADR pictograms (https://commons.wikimedia.org/wiki/ADR_labels_of_danger)
    """
    _name = "sds.pictogram"
    _description = "Pictogram"
    _order = "sequence"

    SECTION = [('hazard', 'Hazard Pictograms'), ('transport', 'ADR/Transport Pictograms')]

    name = fields.Char('Pictogram name', required=True, translate=False)
    description = fields.Char('Pictogram description', translate=True)
    pictogram = fields.Binary("GHS Pictogram", attachment=True)
    category = fields.Selection(SECTION)
    sequence = fields.Integer(string='Sequence', default=10)

    def name_get(self):
        if self._context.get('show_description'):
            res = []
            for pictogram in self:
                desc = pictogram.description
                res.append((pictogram.id, desc))
            return res
        else:
            res = []
            for pictogram in self:
                name = pictogram.name
                res.append((pictogram.id, name))
            return res
