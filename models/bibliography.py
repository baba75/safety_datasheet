# -*- coding: utf-8 -*-

from odoo import models, fields

class SdsBibliography(models.Model):
    """
    This class contains the items for Bibliography needed in section 16
    """
    _name = "sds.bibliography"
    _description = "Bibliography entries"

    name = fields.Char('Title of the regulation', required="True", translate=True)
    url = fields.Char('Link URL', translate=True)