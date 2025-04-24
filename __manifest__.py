# -*- coding: utf-8 -*-
# Copyright 2023 Alberto Carollo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Safety Data Sheets",
    "version": "16.0.1.1.0",
    "category": "Specific Industry Applications",
    "summary": """
        Product Safety Data Sheets""",
    "author": "Alberto Carollo",    
    "website": "https://github.com/baba75/safety_datasheet",
    "license": "AGPL-3",
    "depends": ["base","product"],
    'description': """
        Help to compose multilanguage/multiversion Product Safety Data Sheets
    """,
    "data": [
        "views/bibliography_views.xml",
        "views/chemical_substance_views.xml",
        "views/distributor_views.xml",
        "views/hazard_classification_views.xml",
        "views/hazard_statement_views.xml",
        "views/legend_views.xml",
        "views/pictogram_views.xml",
        "views/poisoncentre_views.xml",
        "views/precautionary_statement_views.xml",
        "views/regulation_views.xml",
        "views/safety_datasheet_views.xml",
        "views/sentence_views.xml",
        "views/safety_datasheet_menus.xml",
        "wizards/select_lang.xml",
        "reports/safety_datasheet_report.xml",
        "data/pictogram_data.xml",
        "data/precautionary_statement_data.xml",
        "data/hazard_class_data.xml",
        "data/hazard_statement_data.xml",
        "data/sentences_data.xml",
        "data/chemical_property_data.xml",
        "data/chemical_substance_data.xml",
        "data/bibliography_data.xml",
        "data/legend_data.xml",
        "data/regulation_data.xml",
        "data/poisoncentre_data.xml",        
        "security/ir.model.access.csv",
    ],
    "assets": {
        "web.report_assets_common": ["/safety_datasheet/static/src/css/sds.css"],
    },
    "application": True,
    "development_status": "Beta",
}
