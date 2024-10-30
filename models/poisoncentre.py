# -*- coding: utf-8 -*-
# Copyright 2024 Alberto Carollo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from . import datasheet


class SdsPoisonCentre(models.Model):
    """
    This class contains the country info about Poison Centres
    (national emergency phone numbers)
    see: https://echa.europa.eu/en/support/helpdesks
    """
    _name = "sds.poison.centre"
    _description = "Poison Centres"
    _sql_constraints = [
                     ('country', 
                      'unique(country)',
                      'Only one Poison Centre text per country is allowed. You can put multiple lines in this field')
                    ]

    @api.model
    def _default_emergency_phone(self):
        company = self.env.company
        default_phone = '<p>' + company.name + ' : ' + company.phone + '</p>'
        return default_phone
   
        
    # We use translation cause some countries are multilingual
    name = fields.Html(string="Contact details of the poison centres", default=_default_emergency_phone, required="True", 
                       translate=True, sanitize=False)
    country = fields.Selection(datasheet.COUNTRY, required="True")