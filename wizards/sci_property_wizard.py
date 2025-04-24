# -*- coding: utf-8 -*-
# Copyright 2023 Alberto Carollo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

class SciPropertyDnelWizard(models.TransientModel):
    _name = "sci.property.dnel.wizard"
    _description = "Insert scientific DNEL properties"

    # chem_dnel_list = _get_available_dnel()

    @api.model
    def insert_dnel(self):
        
        return 

   

 #   lang = fields.Selection(_get_languages, string='Language', required=True, default='en_US')


