# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SdsSentences(models.Model):

    _name = "sds.sentences"
    _description = "Action Sentences"
    _order = "sequence"

    SECTION = [('general', 'General'), ('inhalation', 'Inhalation'), ('skin', 'Skin contact'),
               ('eye', 'Eye contact'), ('ingestion', 'Ingestion'), ('extinguishing', 'Extinguishing'),
               ('fire_hazards', 'Fire special hazards'), ('fire_fight_advice', 'Advice dor Firefighters'),
               ('protective', 'Personal equipment'), ('env_precaution', 'Environmental precautions'),
               ('env_exposure', 'Environmental exposure'), ('containment', 'Containment methods'),
               ('handling', 'Safe handling'), ('storage', 'Safe storage'), ('store_products', 'Store products'),
               ('engineer_control', 'Engineer control'), ('eye_protection', 'Eye/Face protection'),
               ('skin_protection', 'Skin protection'), ('respiratory', 'Respiratory protection'),
               ('thermal', 'Thermal hazards'), ('reactivity', 'Reactivity'), ('stability', 'Stability'),
               ('haz_reaction', 'Hazardous Reaction'), ('avoid_condition', 'Condition to avoid'),
               ('incompatible', 'Incompatible materials'), ('decomposition', 'Decomposition products'),
               ('toxicity', 'Acute toxicity'), ('skin_corrosion', 'Skin corrosion'), ('eye_damage', 'Eye Damage'),
               ('sensitization', 'Respiratory/Skin sensitization'), ('mutagenicity', 'Mutagenicity'),
               ('carcinogenicity', 'Carcinogenicity'), ('reproductive', 'Reproductive toxicity'),
               ('STOST', 'Specific Target Toxicity'), ('aspiration', 'Aspiration hazards'),
               ('disposal', 'Waste treatment'), ('ecotoxicity', 'Toxicity'), ('persistence', 'Persistence'),
               ('bioaccumulative', 'Bioaccumulative potential'), ('mobility', 'Mobility in soil'),
               ('pbtvpvb', 'PBT and vPvB assessment'), ('endocrine', 'Endocrine disruption'),
               ('adverse', 'Other adverse')
               ]

    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char('Statement', translate=True)
    category = fields.Selection(SECTION)
