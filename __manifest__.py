# -*- coding: utf-8 -*-
{
    'name': "Safety Data Sheets",

    'summary': """
        Product Safety Data Sheets""",

    'description': """
        Help to compose multilanguage/multiversion Product Safety Data Sheets
    """,

    'author': "Alberto Carollo",
    'website': "https://github.com/baba75",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Specific Industry Applications',
    'version': '12.2',

    # any module necessary for this one to work correctly
    'depends': ['base','product','web_tree_image_tooltip'],

    # always loaded
    'data': [
        'views/templates.xml',
        'wizards/select_lang.xml',
        'views/views.xml',
        'reports/report_sds.xml',
        'data/pictogram.xml',
        'data/precautionary_statement.xml',
        'data/hazard_class.xml',
        'data/hazard_statement.xml',
        'data/sentences.xml',
        'data/chemical_property.xml',
        'data/chemical_substance.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'css': ['static/src/css/sds.css'],
}
