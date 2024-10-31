# -*- coding: utf-8 -*-
# Copyright 2023 Alberto Carollo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields

class SdsBibliography(models.Model):
    """
    This class contains the items for Bibliography needed in section 16
    """
    _name = "sds.bibliography"
    _description = "Bibliography entries"
    
    active = fields.Boolean(default=True)
    
    def action_archive(self):
        self.active = False

    def action_unarchive(self):
        self.active = True 

    name = fields.Char('Title of the regulation', required="True", translate=True)
    url = fields.Char('Link URL', translate=True)