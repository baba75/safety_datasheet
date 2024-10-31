# -*- coding: utf-8 -*-
# Copyright 2024 Alberto Carollo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from . import datasheet

class SdsDistributor(models.Model):
    """
    This class contains the contact info of National Distributors
    """
    _name = "sds.distributor"
    _description = "National Distributors"
    _sql_constraints = [
                     ('country', 
                      'unique(country)',
                      'Only one National Distributor per country is allowed.')
                    ]
           
    active = fields.Boolean(default=True)
    
    def action_archive(self):
        self.active = False

    def action_unarchive(self):
        self.active = True 
        
    name = fields.Html(string="Contact details of the National Distributor", required="True", translate=False)
    country = fields.Selection(datasheet.COUNTRY, required="True")