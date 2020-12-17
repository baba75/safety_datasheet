# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SdsPictogram(models.Model):
    """
    Hazard pictograms (quick list and images here: https://en.wikipedia.org/wiki/GHS_hazard_pictograms)
    """
    _name = "sds.pictogram"
    _description = "GHS Pictogram"
    _order = "sequence"

    name = fields.Char('Pictogram name', required=True, translate=False)
    description = fields.Char('Pictogram description', translate=True)
    pictogram = fields.Binary("GHS Pictogram", attachment=True)
    sequence = fields.Integer(string='Sequence', default=10)

    @api.multi
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
