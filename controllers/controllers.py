# -*- coding: utf-8 -*-
from odoo import http

# class /users/baba/nuvola.ecobeton.it/amministrazione/odoo/moduliEcobeton/12.0/safetyDatasheet(http.Controller):
#     @http.route('//users/baba/nuvola.ecobeton.it/amministrazione/odoo/moduli_ecobeton/12.0/safety_datasheet//users/baba/nuvola.ecobeton.it/amministrazione/odoo/moduli_ecobeton/12.0/safety_datasheet/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//users/baba/nuvola.ecobeton.it/amministrazione/odoo/moduli_ecobeton/12.0/safety_datasheet//users/baba/nuvola.ecobeton.it/amministrazione/odoo/moduli_ecobeton/12.0/safety_datasheet/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/users/baba/nuvola.ecobeton.it/amministrazione/odoo/moduli_ecobeton/12.0/safety_datasheet.listing', {
#             'root': '//users/baba/nuvola.ecobeton.it/amministrazione/odoo/moduli_ecobeton/12.0/safety_datasheet//users/baba/nuvola.ecobeton.it/amministrazione/odoo/moduli_ecobeton/12.0/safety_datasheet',
#             'objects': http.request.env['/users/baba/nuvola.ecobeton.it/amministrazione/odoo/moduli_ecobeton/12.0/safety_datasheet./users/baba/nuvola.ecobeton.it/amministrazione/odoo/moduli_ecobeton/12.0/safety_datasheet'].search([]),
#         })

#     @http.route('//users/baba/nuvola.ecobeton.it/amministrazione/odoo/moduli_ecobeton/12.0/safety_datasheet//users/baba/nuvola.ecobeton.it/amministrazione/odoo/moduli_ecobeton/12.0/safety_datasheet/objects/<model("/users/baba/nuvola.ecobeton.it/amministrazione/odoo/moduli_ecobeton/12.0/safety_datasheet./users/baba/nuvola.ecobeton.it/amministrazione/odoo/moduli_ecobeton/12.0/safety_datasheet"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/users/baba/nuvola.ecobeton.it/amministrazione/odoo/moduli_ecobeton/12.0/safety_datasheet.object', {
#             'object': obj
#         })