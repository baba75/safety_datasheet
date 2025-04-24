# -*- coding: utf-8 -*-
# Copyright 2023 Alberto Carollo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

COUNTRY = [('Austria','Austria'),('Belgium','Belgium'),('Bulgaria','Bulgaria'),
               ('Croatia','Croatia'),('Cyprus','Cyprus'),('Czech Republic','Czech Republic'),
               ('Denmark','Denmark'),('Estonia','Estonia'),('Finland','Finland'),
               ('France','France'),('Germany','Germany'),('Greece','Greece'),
               ('Hungary','Hungary'),('Iceland','Iceland'),('Ireland','Ireland'),
               ('Italy','Italy'),('Latvia','Latvia'),('Liechtenstein','Liechtenstein'),
               ('Lithuania','Lithuania'),('Luxembourg','Luxembourg'),('Malta','Malta'),
               ('Netherlands','Netherlands'),('Norway','Norway'),('Poland','Poland'),
               ('Portugal','Portugal'),('Romania','Romania'),('Slovakia','Slovakia'),
               ('Slovenia','Slovenia'),('Spain','Spain'),('Sweden','Sweden'),
               ('United Kingdom','United Kingdom')]

class SdsRegulationCriteria(models.Model):
    """
    See point 2.1.2. Classification criteria of REGULATION (EC) No 1272/2008.
    (http://data.europa.eu/eli/reg/2008/1272/2018-03-01)
    TODO: In the norm there is defined a connection also with Signal Words and Precautionary Statement,
    for each class (Explosive, Flammable gases, etc...)
    """
    _name = "sds.regulation.criteria"
    _description = "European Community Regulation Criteria"
    _order = "sequence"

    sequence = fields.Integer(string='Sequence', default=10)
    datasheet_id = fields.Many2one('sds.datasheet', 'Related Datasheet', copy=True)
    Classification = fields.Many2one('sds.hazard.class', 'Hazard Class', copy=True)
    HazardStatement = fields.Many2one('sds.hazard.statement', 'Hazard Statement', copy=True)


class SdsChemicalClassification(models.Model):
    """
    This class is necessary for correct classification of chemical substances, i.e. in section 3.2 od the SDS (Mixtures)
    The relation between classification and hazard statement is not always unique, for example:
    Acute Tox. - 3 - H301
    Acute Tox. - 3 - H331
    Acute Tox. - 3 - H311
    """
    _name = "sds.chemical.classification"
    _description = "Chemical Classification"

    HazardCategories = fields.Many2one('sds.hazard.class', 'Hazard Categories')
    HazardStatement = fields.Many2one('sds.hazard.statement', 'Hazard Statement')

# TODO: Datasheet => Data Sheet
# add a state field for published SDS in Submission portal
# add submission information (no, date, ecc)

class SdsDatasheet(models.Model):
    """
    See Amendement to ANNEX II of REACH:
    REQUIREMENTS FOR THE COMPILATION OF SAFETY DATA SHEETS
    Reference: http://data.europa.eu/eli/reg/2020/878/oj
    """
    _name = 'sds.datasheet'
    _description = 'Product Safety Datasheet'
    _order = "name"
    
    active = fields.Boolean(default=True)
    
    def action_archive(self):
        self.active = False

    def action_unarchive(self):
        self.active = True 

    @api.model
    def _default_company(self):
        company = self.env.company
        if(company.street and company.zip and company.city):
            result = '<p>' + company.name + '<br/>' + company.street
            result += '<br/>' + company.zip + ' ' + company.city + ' ' + company.state_id.name
            result += '<br/>' + company.country_id.name 
            result += '<br/> Phone: ' + company.phone
            result += '<br/> Email: ' + company.email
            result += '</p>'
        else:
            result = '<p>' + company.name + '<br/>' + 'Insert you company full adrees here</p>'
        return result

    name = fields.Char(string='Name', required=True, index=True, default=lambda self: _('New SDS'))
    product_id = fields.Many2one('product.template', 'Product', required=True, copy=True)
    revision_date = fields.Date(string="Revision date", default=fields.Date.today(), required=True)
    supersedes_date = fields.Char(string="Supersedes version/date", translate=True)

    # Section 1: Identification of the substance/mixture and of the company/undertaking
    section_1_1 = fields.Char(string="Product Identifier", required=True, translate=True)
    section_1_1_UFI = fields.Char(string="UFI", help="Unique Formula Identifier")
    section_1_2 = fields.Text(
        string="Relevant identified uses of the substance or mixture and uses advised against recommended use",
        required=True, translate=True)
    section_1_3 = fields.Html(string="Detail of the supplier of the safety data sheet", default=_default_company,
                              required=True, translate=True, sanitize=False)
    section_1_3_info = fields.Char(string="Email of the person responsible for the safety data sheet")
    section_1_3_distributor_selector = fields.Boolean(string="Insert National Distributor contact", default=False)
    section_1_note = fields.Html(string="Section 1 notes", translate=True)

    # Section 2: Hazards identification
    section_2_1_selector = fields.Boolean(string="Hazardous substance or mixture", default=False)
    section_2_1_b_selector = fields.Boolean(string="Non Hazardous mixture with hazardous components", default=False)
    section_2_1 = fields.One2many('sds.regulation.criteria', 'datasheet_id', string='EC regulation',
                                  help='Regulation (EC) No 1272/2008 - classification, labelling and packaging of substances and mixtures (CLP)')
    section_2_2_selector = fields.Boolean(string="GHS Labelling", default=False)
    section_2_2_pictograms = fields.Many2many('sds.pictogram', string="Label pictograms", 
                                     relation="sds_pictogram_hazard_rel",
                                     domain="[('category', '=', 'hazard')]",
                                     context={'default_category': 'hazard'},copy=True)
    section_2_2_signal = fields.Selection([('danger', 'Danger'), ('warning', 'Warning')], string="SignalWords",
                                          default='warning')
    section_2_2_P = fields.Many2many('sds.precautionary.statement', string="Precautionary Statement", copy=True)
    section_2_2_Additional = fields.Html('Additional Labelling', translate=True)
   
    """
    At first look, the following three fields may be confused with the corresponding fields in section 11. 
    Here, we should declare *IF* those properties are verified or listed; in section 11, we give the information 
    on adverse health effects caused by. We will use the same sentence category.
    """ 
    section_2_3_PBT = fields.Many2one('sds.sentences', 
                                       domain="[('category', '=', 'pbtvpvb')]", 
                                       string='is PBT ?',
                                       help="Persistent, Bioaccumulative and Toxic substances (PBT substances)",
                                       context={'default_category': 'pbtvpvb',},
                                       required=True,
                                       copy=True)
    section_2_3_vPvB = fields.Many2one('sds.sentences', 
                                       domain="[('category', '=', 'pbtvpvb')]", 
                                       string='is vPvB ?',
                                       help="very persistent and very bioaccumulative substances (vPvB substances)",
                                       context={'default_category': 'pbtvpvb',},
                                       required=True,
                                       copy=True)
    section_2_3_endocrine = fields.Many2one('sds.sentences', 
                                       domain="[('category', '=', 'endocrine')]", 
                                       string='is endocrine disrupting ?',
                                       help="Endocrine disrupting properties",
                                       context={'default_category': 'endocrine',},
                                       required=True,
                                       copy=True)
    
 
    section_2_3_OtherHazards = fields.Char(string="Other Hazards", default=lambda s: _('none'), required=True,
                                           translate=True)
    section_2_note = fields.Html(string="Section 2 notes", translate=True)

    # Section 3: Composition/information on ingredients
    # Hint: Look at https://www.echa.europa.eu/substance-information/
    section_3 = fields.Char(string="Chemical identity", translate=True)
    section_3_type = fields.Selection([('substance', 'Substance'), ('mixture', 'Mixture')],
                                              string="Product type",
                                              default='mixture')
    section_3_1 = fields.Html(string="Substances",  required=False, translate=True, sanitize=False)
    section_3_2_selector = fields.Boolean(string="Mixture", default=False)
    section_3_2 = fields.One2many('sds.chemical.mixture', 'datasheet_id', string='Mixture elements')
    section_3_note = fields.Html(string="Section 3 notes", translate=True)

    # Section 4: First aid measures
    section_4_1_general = fields.Many2many('sds.sentences', relation="sds_general_firstaid_statement_rel",
                                           domain="[('category', '=', 'general')]", string='General advice',
                                           context={'default_category': 'general'})
    section_4_1_inhalation = fields.Many2many('sds.sentences', relation="sds_inhalation_firstaid_statement_rel",
                                              domain="[('category', '=', 'inhalation')]", string='Inhalation',
                                              context={'default_category': 'inhalation'})
    section_4_1_skin = fields.Many2many('sds.sentences', relation="sds_skin_firstaid_statement_rel",
                                        domain="[('category', '=', 'skin')]", string='Skin contact',
                                        context={'default_category': 'skin'})
    section_4_1_eye = fields.Many2many('sds.sentences', relation="sds_eye_firstaid_statement_rel",
                                       domain="[('category', '=', 'eye')]", string='Eye contact',
                                       context={'default_category': 'eye'})
    section_4_1_ingestion = fields.Many2many('sds.sentences', relation="sds_ingestion_firstaid_statement_rel",
                                             domain="[('category', '=', 'ingestion')]", string='Ingestion',
                                             context={'default_category': 'ingestion'})
    section_4_2 = fields.Html(string="Most important symptoms and effects, both acute and delayed",
                              default=lambda s: _(
                                  "Specific information on symptoms and effects caused by the product are unknown."),
                              required=True, translate=True, sanitize=False)
    section_4_3 = fields.Html(string="Indication of any immediate medical attention and special treatment needed",
                              default=lambda s: _("Not available."), required=True, translate=True,
                              sanitize=False)
    section_4_note = fields.Html(string="Section 4 notes", translate=True)

    # Section 5: Firefighting measures
    section_5_1_1 = fields.Many2many('sds.sentences', relation="sds_extinguishing_statement_rel",
                                     domain="[('category', '=', 'extinguishing')]", string='Extinguishing media',
                                     context={'default_category': 'extinguishing'})
    section_5_1_2 = fields.Many2many('sds.sentences', relation="sds_non_suitable_extinguishing_statement_rel",
                                     domain="[('category', '=', 'extinguishing')]",
                                     string='Unsuitable extinguishing media',
                                     context={'default_category': 'extinguishing'})
    section_5_2 = fields.Many2many('sds.sentences', relation="sds_combustion_products_statement_rel",
                                   domain="[('category', '=', 'fire_hazards')]",
                                   string='Special hazards arising from the substance or mixture',
                                   context={'default_category': 'fire_hazards'})
    section_5_3 = fields.Many2many('sds.sentences', relation="sds_fire_fighting_statement_rel",
                                   domain="[('category', '=', 'fire_fight_advice')]",
                                   string='Advice for firefighters',
                                   context={'default_category': 'fire_fight_advice'})
    section_5_note = fields.Html(string="Section 5 notes", translate=True)

    # Section 6: Accidental release measures

    section_6_1_1 = fields.Many2many('sds.sentences', relation="sds_protective_equipment_statement_rel",
                                     domain="[('category', '=', 'protective')]",
                                     string='Personal precautions for non-emergency personnel',
                                     context={'default_category': 'protective'})
    section_6_1_2 = fields.Many2many('sds.sentences', relation="sds_protective_responders_equipment_statement_rel",
                                     domain="[('category', '=', 'protective')]",
                                     string='Personal precautions for emergency responders',
                                     context={'default_category': 'protective'})
    section_6_2 = fields.Many2many('sds.sentences', relation="sds_env_precaution_statement_rel",
                                   domain="[('category', '=', 'env_precaution')]",
                                   string='Environmental precautions',
                                   context={'default_category': 'env_precaution'})
    section_6_3 = fields.Many2many('sds.sentences', relation="sds_containment_methods_statement_rel",
                                   domain="[('category', '=', 'containment')]",
                                   string='Methods and materials for containment and cleaning up',
                                   context={'default_category': 'containment'})
    section_6_4 = fields.Many2one('sds.sentences', 
                                       domain="[('category', '=', 'ref_section')]", 
                                       string='Reference to other sections',
                                       context={'default_category': 'ref_section',},
                                       required=True,
                                       copy=True)
    section_6_note = fields.Html(string="Section 6 notes", translate=True)

    # Section 7: Handling and storage
    section_7_1 = fields.Many2many('sds.sentences', relation="sds_safe_handling_statement_rel",
                                   domain="[('category', '=', 'handling')]",
                                   string='Precautions for safe handling',
                                   context={'default_category': 'handling'})
    section_7_2_1 = fields.Many2many('sds.sentences', relation="sds_safe_storage_statement_rel",
                                     domain="[('category', '=', 'storage')]",
                                     string='Conditions for safe storage, including any incompatibilities',
                                     context={'default_category': 'storage'})
    section_7_2_2 = fields.Many2many('sds.sentences', relation="sds_not_store_with_statement_rel",
                                     domain="[('category', '=', 'store_products')]",
                                     string='Do not store with the following product types',
                                     context={'default_category': 'store_products'})
    section_7_2_3 = fields.Many2many('sds.sentences', relation="sds_unsuitable_containers_statement_rel",
                                     domain="[('category', '=', 'store_products')]",
                                     string='Unsuitable materials for containers',
                                     context={'default_category': 'store_products'})
    section_7_3 = fields.Many2one('sds.sentences', 
                                       domain="[('category', '=', 'end_use')]", 
                                       string='Specific end use',
                                       context={'default_category': 'end_use',},
                                       required=True,
                                       copy=True)
    section_7_note = fields.Html(string="Section 7 notes", translate=True)

    # Section 8: Exposure controls/personal protection
    section_8_1_tlv_selector = fields.Boolean(string="TLV of the mixture",help="Occupational exposure limit of the entire mixture (TLV).", default=False)
    section_8_1_tlv_selector_ing = fields.Boolean(string="TLV of the ingredients",help="Occupational exposure limit of the ingredients (TLV).", default=False)
    section_8_1_tlv = fields.Html(string='TLV',
                                  default=lambda s: _('<table class="table table-bordered">'
                                       '<thead class="table-columns">' 
                                       '<tr><th rowspan="2">Region</th>'
                                            '<th rowspan="2">Legislation</th>' 
                                            '<th colspan="3">Long-term Exposure Limit (LTEL) Values</th>' 
                                            '<th colspan="3">Short-term Exposure Limit (STEL) Values</th>' 
                                            '<th rowspan="2">Skin Designation</th>' 
                                            '<th rowspan="2">Dermal Sensitization</th>' 
                                            '<th rowspan="2">Respiratory Sensitization</th>' 
                                            '<th rowspan="2">Work Sector</th>' 
                                            '<th rowspan="2">Effective Date</th>' 
                                            '<th rowspan="2">Expiration Date</th>' 
                                            '<th rowspan="2">Miscellaneous Notes</th></tr>' 
                                        '<tr><th>mg/m<sup>3</sup></th>' 
                                            '<th>ppm</th><th>f/ml</th>' 
                                            '<th>mg/m<sup>3</sup></th>' 
                                            '<th>ppm</th><th>f/ml</th></tr>'
                                      '</thead>' 
                                      '<tbody class="table-data">' 
                                        '<tr><td><br></td><td><br></td><td><br></td><td><br></td><td><br></td>'
                                            '<td><br></td><td><br></td><td><br></td><td><br></td><td><br></td>' 
                                            '<td><br></td><td><br></td><td><br></td><td><br></td><td><br></td>'
                                        '</tr></tbody></table>'),
                                  translate=True,sanitize=False)
    section_8_1_dnel_selector = fields.Boolean(string="DNEL of the mixture",help="Derived No Effect Level (DNEL) of the mixture", default=False)
    section_8_1_dnel_selector_ing = fields.Boolean(string="DNEL of ingredients", help="Show DNEL of ingredients", default=False)
    section_8_1_dnel = fields.Html(string='DNEL',
                                   default=lambda s: _(
                                       '<p><b>Derived No Effect Level<br>'
                                    '</b>Name of the substance here</p>'
                                    '<p>Workers</p>'
                                    '<table class="table table-bordered">'
                                        '<thead><tr>'
                                                '<th colspan="2">Acute systemic effects</th>'
                                                '<th colspan="2">Acute local effects</th>'
                                                '<th colspan="2">Long-term systemic effects</th>'
                                                '<th colspan="2">Long-term local effects</th></tr>'
                                        '</thead>'
                                        '<tbody><tr>'
                                                '<td>Dermal</td><td>Inhalation</td>'
                                                '<td>Dermal</td><td>Inhalation</td>'
                                                '<td>Dermal</td><td>Inhalation</td>'
                                                '<td>Dermal</td><td>Inhalation</td></tr>'
                                            '<tr><td><br></td><td><br></td><td><br></td><td><br></td>'
                                                '<td><br></td><td><br></td><td><br></td><td><br></td>'
                                            '</tr></tbody>'
                                    '</table>'
                                    '<p>Consumers</p>'
                                    '<table class="table table-bordered">'
                                        '<thead><tr>'
                                                '<th colspan="3">Acute systemic effects</th>'
                                                '<th colspan="2">Acute local effects</th>'
                                                '<th colspan="3">Long-term systemic effects</th>'
                                                '<th colspan="2">Long-term local effects</th></tr>'
                                        '</thead>'
                                        '<tbody><tr>'
                                                '<td>Dermal</td><td>Inhalation</td><td>Oral</td>'
                                                '<td>Dermal</td><td>Inhalation</td>'
                                                '<td>Dermal</td><td>Inhalation</td><td>Oral</td>'
                                                '<td>Dermal</td><td>Inhalation</td></tr>'
                                            '<tr><td><br></td><td><br></td><td><br></td>'
                                                '<td><br></td><td><br></td>'
                                                '<td><br><br></td><td><br></td><td><br></td>'
                                                '<td><br></td><td><br></td></tr>'
                                        '</tbody>'
                                    '</table>'),
                                   translate=True, sanitize=False)
    section_8_1_pnec_selector = fields.Boolean(string="PNEC of the mixture",help="Predicted No Effect Concentration (PNEC) of the mixture",
                                               default=False)
    section_8_1_pnec_selector_ing = fields.Boolean(string="PNEC of ingredients", help="Show PNEC of ingredients", default=False)
    section_8_1_pnec = fields.Html(string='PNEC',
                                   default=lambda s: _(
                                       '<p><b>Predicted No Effect Concentration</b><br>'
                                    'Name of the component here</p>'
                                '<div class="row mt16">'
                                    '<div class="col-6">'
                                        '<table class="table table-bordered">'
                                            '<thead><tr><th colspan="2">Hazard for Aquatic Organisms</th></tr></thead>'
                                            '<tbody>'
                                                '<tr><td>Freshwater</td><td>-</td></tr>'
                                                '<tr><td>Intermittent releases (freshwater)</td><td>-</td></tr>'
                                                '<tr><td>Marine water</td><td>-</td></tr>'
                                                '<tr><td>Intermittent releases (marine water)</td><td>-</td></tr>'
                                                '<tr><td>Sewage treatment plant (STP)</td><td>-</td></tr>'
                                                '<tr><td>Sediment (freshwater)</td><td>-</td></tr>'
                                                '<tr><td>Sediment (marine water)</td><td>-</td></tr>'
                                            '</tbody>'
                                        '</table>'
                                    '</div><div class="col-6">'
                                        '<table class="table table-bordered">'
                                            '<thead><tr><th colspan="2">Hazard for Air</th></tr></thead>'
                                            '<tbody><tr><td>Air</td><td>-</td></tr></tbody>'
                                        '</table>'
                                        '<table class="table table-bordered">'
                                            '<thead><tr><th colspan="2">Hazard for Terrestrial Organism</th></tr></thead>'
                                            '<tbody><tr><td>Soil</td><td>-</td></tr></tbody>'
                                        '</table>'
                                        '<table class="table table-bordered">'
                                            '<thead><tr><th colspan="2">Hazard for Predators</th></tr></thead>'
                                            '<tbody><tr><td>Secondary poisoning</td><td>-</td></tr></tbody>'
                                        '</table></div></div>'),
                                   translate=True, sanitize=False)
    section_8_2_1 = fields.Many2many('sds.sentences', relation="sds_engineer_control_statement_rel",
                                     domain="[('category', '=', 'engineer_control')]",
                                     string='Appropriate engineering controls',
                                     context={'default_category': 'engineer_control'})
    section_8_2_2 = fields.Many2many('sds.sentences', relation="sds_eye_protection_statement_rel",
                                     domain="[('category', '=', 'eye_protection')]",
                                     string='Eye/face protection',
                                     context={'default_category': 'eye_protection'})
    section_8_2_3_1 = fields.Many2many('sds.sentences', relation="sds_skin_hand_protection_statement_rel",
                                       domain="[('category', '=', 'skin_protection')]",
                                       string='Skin Protection - Hand',
                                       context={'default_category': 'skin_protection'})
    section_8_2_3_2 = fields.Many2many('sds.sentences', relation="sds_skin_other_protection_statement_rel",
                                       domain="[('category', '=', 'skin_protection')]",
                                       string='Skin Protection - Other',
                                       context={'default_category': 'skin_protection'})
    section_8_2_4 = fields.Many2many('sds.sentences', relation="sds_respiratory_protection_statement_rel",
                                     domain="[('category', '=', 'respiratory')]",
                                     string='Respiratory protection',
                                     context={'default_category': 'respiratory'})
    section_8_2_5 = fields.Many2many('sds.sentences', relation="sds_thermal_hazards_statement_rel",
                                     domain="[('category', '=', 'thermal')]",
                                     string='Thermal hazards',
                                     context={'default_category': 'thermal'})
    section_8_3 = fields.Many2many('sds.sentences', relation="sds_env_exposure_statement_rel",
                                   domain="[('category', '=', 'env_exposure')]",
                                   string='Environmental exposure controls',
                                   context={'default_category': 'env_exposure'})
    section_8_note = fields.Html(string="Section 8 notes", translate=True)

    # Section 9: Physical and chemical properties
    section_9_1 = fields.Many2many('sds.chemical.property.line', relation="sds_chemical_property_rel",
                                   string="Physical and chemical properties", copy=False)
    section_9_2 = fields.Many2one('sds.sentences', 
                                       domain="[('category', '=', 'other_info')]", 
                                       string='Other information',
                                       context={'default_category': 'other_info',},
                                       required=True,
                                       copy=True)
    section_9_note = fields.Html(string="Section 9 Notes", translate=True)

    # Section 10: Stability and reactivity
    section_10_1 = fields.Many2many('sds.sentences', relation="sds_reactivity_statement_rel",
                                    domain="[('category', '=', 'reactivity')]",
                                    string='Reactivity',
                                    context={'default_category': 'reactivity'})
    section_10_1_component = fields.Boolean('Insert reactivity of the components', default=False)
    section_10_2 = fields.Many2many('sds.sentences', relation="sds_stability_statement_rel",
                                    domain="[('category', '=', 'stability')]",
                                    string='Chemical stability',
                                    context={'default_category': 'stability'})
    section_10_3 = fields.Many2many('sds.sentences', relation="sds_hazardous_reaction_statement_rel",
                                    domain="[('category', '=', 'haz_reaction')]",
                                    string='Possibility of hazardous reactions',
                                    context={'default_category': 'haz_reaction'})
    section_10_4 = fields.Many2many('sds.sentences', relation="sds_avoid_condition_statement_rel",
                                    domain="[('category', '=', 'avoid_condition')]",
                                    string='Conditions to avoid',
                                    context={'default_category': 'avoid_condition'})
    section_10_5 = fields.Many2many('sds.sentences', relation="sds_incompatible_materials_statement_rel",
                                    domain="[('category', '=', 'incompatible')]",
                                    string='Incompatible materials',
                                    context={'default_category': 'incompatible'})
    section_10_6 = fields.Many2many('sds.sentences', relation="sds_decomposition_products_statement_rel",
                                    domain="[('category', '=', 'decomposition')]",
                                    string='Hazardous decomposition products',
                                    context={'default_category': 'decomposition'})
    section_10_note = fields.Html(string="Section 10 Notes")

    # Section 11: Toxicological information
    section_11_1_1_oral = fields.Many2many('sds.sentences', relation="sds_acute_oral_toxicity_statement_rel",
                                           domain="[('category', '=', 'toxicity')]",
                                           string='Acute oral toxicity',
                                           context={'default_category': 'toxicity'})
    section_11_1_1_dermal = fields.Many2many('sds.sentences', relation="sds_acute_dermal_toxicity_statement_rel",
                                             domain="[('category', '=', 'toxicity')]",
                                             string='Acute dermal toxicity',
                                             context={'default_category': 'toxicity'})
    section_11_1_1_inhalation = fields.Many2many('sds.sentences', relation="sds_acute_inhalation_toxicity_statement_rel",
                                                 domain="[('category', '=', 'toxicity')]",
                                                 string='Acute inhalation toxicity',
                                                 context={'default_category': 'toxicity'})
    section_11_1_1_selector = fields.Boolean(string="Acute toxicity details (mixture)", default=False)
    section_11_1_1_component = fields.Boolean(string="Acute toxicity details (ingredients)", default=False)
    section_11_1_1_text = fields.Html(string="Acute toxicity details",
                                      default=lambda s: _(
                                          '<table class="table table-bordered">'
                                            '<thead><tr><th>Route of exposure</th>'
                                                    '<th>Result/Effect</th>'
                                                    '<th>Species/Test system</th>'
                                                    '<th>Source</th></tr></thead>'
                                            '<tbody><tr><td>Ingestion</td><td><br></td><td><br></td><td><br></td></tr>'
                                                '<tr><td>Inhalation</td><td><br></td><td><br></td><td><br></td></tr>'
                                                '<tr><td>Dermal</td><td><br></td><td><br></td><td><br></td></tr>'
                                            '</tbody></table>'),
                                      translate=True, sanitize=False)
    section_11_1_2 = fields.Many2many('sds.sentences', relation="sds_skin_corrosion_statement_rel",
                                      domain="[('category', '=', 'skin_corrosion')]",
                                      string='Skin corrosion/irritation',
                                      context={'default_category': 'skin_corrosion'})
    section_11_1_2_selector = fields.Boolean(string="Skin cor/irr details (mixture)",        
                                      help="Insert skin corrosion/irritation details (mixture)", 
                                      default=False)
    section_11_1_2_component = fields.Boolean(string="Skin cor/irr det. (ingredients)",
                                              help="Insert skin corrosion/irritation details (ingredients)",
                                              default=False)
    section_11_1_2_text = fields.Html(string="Skin corrosion/irritation details", translate=True, sanitize=False)
    section_11_1_3 = fields.Many2many('sds.sentences', relation="sds_eye_damage_statement_rel",
                                      domain="[('category', '=', 'eye_damage')]",
                                      string='Serious eye damage/eye irritation',
                                      context={'default_category': 'eye_damage'})
    section_11_1_3_selector = fields.Boolean(string="Eye cor/irr details (mixture)",
                                             help="Insert eye damage corrosion/irritation details (mixture)",
                                             default=False)
    section_11_1_3_component = fields.Boolean(string="Eye cor/irr details (ingredients)",
                                              help="Insert eye damage corrosion/irritation details (ingredients)",
                                              default=False)
    section_11_1_3_text = fields.Html(string="Eye damage/irritation details", translate=True,sanitize=False)
    section_11_1_4 = fields.Many2many('sds.sentences', relation="sds_respiratory_skin_sensitization_statement_rel",
                                      domain="[('category', '=', 'sensitization')]",
                                      string='Respiratory or skin sensitization',
                                      context={'default_category': 'sensitization'})
    section_11_1_4_selector = fields.Boolean(string="Resp/skin sens. details (mixture)",
                                             help="Insert respiratory or skin sensitization details (mixture)",
                                             default=False)
    section_11_1_4_component = fields.Boolean(string="Resp/skin sens. details (ingredients)",
                                             help="Insert respiratory or skin sensitization details (ingredients)",
                                             default=False)
    section_11_1_4_text = fields.Html(string="Respiratory or skin sensitization details", translate=True,sanitize=False)
    section_11_1_5 = fields.Many2many('sds.sentences', relation="sds_mutagenicity_statement_rel",
                                      domain="[('category', '=', 'mutagenicity')]",
                                      string='Germ cell mutagenicity',
                                      context={'default_category': 'mutagenicity'})
    section_11_1_5_selector = fields.Boolean(string="Mutagenicity details (mixture)",
                                             help="Insert germ cell mutagenicity details (mixture)",
                                             default=False)
    section_11_1_5_component = fields.Boolean(string="Mutagenicity details (ingredients)",
                                             help="Insert germ cell mutagenicity details (ingredients)",
                                             default=False)
    section_11_1_5_text = fields.Html(string="Mutagenicity details",
                                      default=lambda s: _(
                                          '<table class="table table-bordered"><thead>'
                                          '<tr><th>Result/Effect</th><th>Species/Test system</th><th>Source</th></tr></thead>'
                                          '<tbody><tr><td><br></td><td><br></td><td><br></td></tr></tbody></table>'),
                                      translate=True,sanitize=False)
    section_11_1_6 = fields.Many2many('sds.sentences', relation="sds_carcinogenicity_statement_rel",
                                      domain="[('category', '=', 'carcinogenicity')]",
                                      string='Carcinogenicity',
                                      context={'default_category': 'carcinogenicity'})
    section_11_1_6_selector = fields.Boolean(string="Carcinogenicity details (mixture)",
                                             help="Insert carcinogenicity details (mixture)",
                                             default=False)
    section_11_1_6_component = fields.Boolean(string="Carcinogenicity details (ingredients)",
                                             help="Insert carcinogenicity details (ingredients)",
                                             default=False)
    section_11_1_6_text = fields.Html(string="Carcinogenicity details", translate=True,sanitize=False)
    section_11_1_7 = fields.Many2many('sds.sentences', relation="sds_reproductive_toxicity_statement_rel",
                                      domain="[('category', '=', 'reproductive')]",
                                      string='Reproductive toxicity',
                                      context={'default_category': 'reproductive'})
    section_11_1_7_selector = fields.Boolean(string="Reproductive tox. details (mixture)",
                                             help="Insert reproductive toxicity details (mixture)",
                                             default=False)
    section_11_1_7_component = fields.Boolean(string="Reproductive tox. details (ingredients)",
                                             help="Insert reproductive toxicity details (ingredients)",
                                             default=False)
    section_11_1_7_text = fields.Html(string="Reproductive toxicity details", translate=True,sanitize=False)
    section_11_1_8 = fields.Many2many('sds.sentences', relation="sds_specific_target_single_statement_rel",
                                      domain="[('category', '=', 'STOT')]",
                                      string='Specific Target Organ Systemic Toxicity (Single Exposure)',
                                      context={'default_category': 'STOT'})
    section_11_1_8_selector = fields.Boolean(string="STOT SE details (mixture)", 
                                             help="Insert pecific Target Organ Systemic Toxicity (Single Exposure) details (mixture)",
                                             default=False)
    section_11_1_8_component = fields.Boolean(string="STOT SE details (ingredients)", 
                                             help="Insert pecific Target Organ Systemic Toxicity (Single Exposure) details (ingredients)",
                                             default=False)
    section_11_1_8_text = fields.Html(string="STOT SE details", translate=True,sanitize=False)
    section_11_1_9 = fields.Many2many('sds.sentences', relation="sds_specific_target_repeated_statement_rel",
                                      domain="[('category', '=', 'STOT')]",
                                      string='Specific Target Organ Systemic Toxicity (Repeated Exposure)',
                                      context={'default_category': 'STOT'})
    section_11_1_9_selector = fields.Boolean(string="STOT RE details (mixture)",
                                             help="insert Specific Target Organ Systemic Toxicity (Repeated Exposure) details (mixture)",
                                             default=False)
    section_11_1_9_component = fields.Boolean(string="STOT RE details (ingredients)",
                                             help="insert Specific Target Organ Systemic Toxicity (Repeated Exposure) details (ingredients)",
                                             default=False)
    section_11_1_9_text = fields.Html(string="STOT RE details", translate=True,sanitize=False)
    section_11_1_10 = fields.Many2many('sds.sentences', relation="sds_aspiration_hazard_products_statement_rel",
                                       domain="[('category', '=', 'aspiration')]",
                                       string='Aspiration Hazard',
                                       context={'default_category': 'aspiration'})
    section_11_1_10_selector = fields.Boolean(string="Aspiration haz. details (mixture)",
                                              help="Insert aspiration hazard details (mixture)",
                                              default=False)
    section_11_1_10_component = fields.Boolean(string="Aspiration haz. details (ingredients)",
                                              help="Insert aspiration hazard details (ingredients)",
                                              default=False)
    section_11_1_10_text = fields.Html(string="Aspiration Hazard details", translate=True, sanitize=False)
    section_11_2_1 = fields.Many2many('sds.sentences', relation="sds_endocrine_disrupting_products_statement_rel",
                                       domain="[('category', '=', 'endocrine')]",
                                       string='Endocrine disrupting properties',
                                       context={'default_category': 'endocrine'})
    section_11_2_2 = fields.Many2one('sds.sentences', 
                                       domain="[('category', '=', 'other_info')]", 
                                       string='Other information',
                                       context={'default_category': 'other_info',},
                                       required=True,
                                       copy=True)
    section_11_note = fields.Html(string="Section 11 Notes", translate=True)

    # Section 12: Ecological information
    section_12_1 = fields.Many2many('sds.sentences', relation="sds_toxicity_statement_rel",
                                    domain="[('category', '=', 'ecotoxicity')]", string='Toxicity',
                                    context={'default_category': 'ecotoxicity'})
    section_12_1_selector = fields.Boolean(string="Toxicity details (mixture)", default=False)
    section_12_1_component = fields.Boolean(string="Toxicity details (ingredients)",
                                              help="Insert ingredients toxicity details",
                                              default=False)
    section_12_1_text = fields.Html(string="Toxicity details",
                                    default=lambda s:_(
                                        '<table class="table table-bordered"><thead>'
                                        '<tr><th>Result/Effect</th><th>Species/Test system</th><th>Source</th></tr></thead>'
                                        '<tbody><tr><td><br></td><td><br></td><td><br></td></tr></tbody></table>'
                                    ),
                                    translate=True, sanitize=False)
    section_12_2 = fields.Many2many('sds.sentences', relation="sds_persistence_statement_rel",
                                    domain="[('category', '=', 'persistence')]", string='Persistence and degradability',
                                    context={'default_category': 'persistence'})
    section_12_2_selector = fields.Boolean(string="Degradability details (mixture)", default=False)
    section_12_2_component = fields.Boolean(string="Degradability details (ingredients)",
                                              help="Insert ingredients degradability details",
                                              default=False)
    section_12_2_text = fields.Html(string="Persistence and degradability details",
                                    default=lambda s:_(
                                        '<table class="table table-bordered"><thead><tr>'
                                        '<th>Substance</th><th>Biodegradation in water</th>'
                                        '<th>Source</th></tr></thead><tbody><tr><td></td>'
                                        '<td></td><td></td></tr></tbody></table>'
                                    ),
                                    translate=True, sanitize=False)
    section_12_3 = fields.Many2many('sds.sentences', relation="sds_bioaccumulative_potential_statement_rel",
                                    domain="[('category', '=', 'bioaccumulative')]", string='Bioaccumulative potential',
                                    context={'default_category': 'bioaccumulative'})
    section_12_3_selector = fields.Boolean(string="Bioaccumulative details (mixture)", 
                                           help="Insert mixture bioaccumulative potential details",
                                           default=False)
    section_12_3_component = fields.Boolean(string="Bioaccumulative details (ingredients)",
                                              help="Insert ingredients bioaccumulative details",
                                              default=False)
    section_12_3_text = fields.Html(string="Bioaccumulative potential details", translate=True, sanitize=False)
    section_12_4 = fields.Many2many('sds.sentences', relation="sds_mobility_soil_statement_rel",
                                    domain="[('category', '=', 'mobility')]", string='Mobility in soil',
                                    context={'default_category': 'mobility'})
    section_12_4_selector = fields.Boolean(string="Mobility details (mixture)", 
                                           help="Insert mobility in soil details of the mixture",
                                           default=False)
    section_12_4_component = fields.Boolean(string="Mobility details (ingredients)",
                                              help="Insert ingredients mobility in soil details",
                                              default=False)
    section_12_4_text = fields.Html(string="Mobility in soil details", translate=True, sanitize=False)
    section_12_5 = fields.Many2many('sds.sentences', relation="sds_pbt_vpvb_statement_rel",
                                    domain="[('category', '=', 'pbtvpvb')]",
                                    string='Results of PBT and vPvB assessment',
                                    context={'default_category': 'pbtvpvb'})
    section_12_5_selector = fields.Boolean(string="PBT and vPvB details (mixture)", 
                                           help="Insert results of mixture PBT and vPvB assessment",
                                           default=False)
    section_12_5_component = fields.Boolean(string="PBT and vPvB details (ingredients)",
                                              help="Insert results of ingredients PBT and vPvB assessment",
                                              default=False)
    section_12_5_text = fields.Html(string="Results of PBT and vPvB assessment details", translate=True, sanitize=False)
    section_12_6 = fields.Many2many('sds.sentences', relation="sds_endocrine_disrupting_statement_rel",
                                    domain="[('category', '=', 'endocrine')]", string='Endocrine disrupting properties',
                                    context={'default_category': 'endocrine'})
    section_12_6_selector = fields.Boolean(string="Endocrine details (mixture)", 
                                           help="Insert endocrine disrupting properties details (mixture)",
                                           default=False)
    section_12_6_component = fields.Boolean(string="Endocrine details (ingredients)",
                                              help="Insert endocrine disrupting properties details (ingredients)",
                                              default=False)
    section_12_6_text = fields.Html(string="Endocrine disrupting properties details", translate=True, sanitize=False)
    section_12_7 = fields.Many2many('sds.sentences', relation="sds_other_adverse_statement_rel",
                                    domain="[('category', '=', 'adverse')]", string='Other adverse effects',
                                    context={'default_category': 'adverse'})
    section_12_7_selector = fields.Boolean(string="Adverse effects details (mixture)", default=False)
    section_12_7_component = fields.Boolean(string="Adverse effects details (ingredients)",
                                              help="Insert other adverse effects details (ingredients)",
                                              default=False)
    section_12_7_text = fields.Html(string="Other adverse effects details", translate=True, sanitize=False)
    section_12_note = fields.Html(string="Section 12 Notes", translate=True)

    # Section 13: Disposal considerations
    section_13_1 = fields.Many2many('sds.sentences', relation="sds_disposal_consideration_statement_rel",
                                    domain="[('category', '=', 'disposal')]",
                                    string='Waste treatment methods',
                                    context={'default_category': 'disposal'})
    section_13_note = fields.Html(string="Section 13 Notes", translate=True)

    # Section 14: Transport information
    """
    When not specifying the transport regulation, we prefer the Many2one approach to reduce the proliferation of translations.
    """ 
    section_14_selector = fields.Boolean(string="Specify ADR/RID/ADN/IMDG/IATA transport regulation", default=False)
    section_14_1 = fields.Many2one('sds.sentences', 
                                       domain="[('category', '=', 'transport')]", 
                                       string='UN number',
                                       context={'default_category': 'transport',},
                                       required=True,
                                       copy=True)
    # First part is for ADR/RID/ADN
    section_14_2 = fields.Char('Proper shipping name (ADR)', default=lambda s: _("Not regulated for transport."),
                               translate=True)
    section_14_3 = fields.Char('Transport hazard class(es) (ADR)', default=lambda s: _("Not regulated for transport."),
                               translate=True)
    section_14_3_adr_pictograms = fields.Many2many('sds.pictogram', string="Label pictograms (ADR)", 
                                     relation="sds_pictogram_adr_rel",
                                     domain="[('category', '=', 'transport')]",
                                     context={'default_category': 'transport'},copy=True)
    section_14_3_adr_notes = fields.Html(string="ADR/RID/ADN additional notes", translate=True)
    # Maritime Dangerous Goods (IMDG)    
    
    section_14_2_imdg = fields.Char('Proper shipping name (IMDG)', default=lambda s: _("Not regulated for transport."),
                               translate=True)
    section_14_3_imdg = fields.Char('Transport hazard class(es) (IMDG)', default=lambda s: _("Not regulated for transport."),
                               translate=True)
    section_14_3_imdg_pictograms = fields.Many2many('sds.pictogram', string="Label pictograms (IMDG)", 
                                     relation="sds_pictogram_imgd_rel",
                                     domain="[('category', '=', 'transport')]",
                                     context={'default_category': 'transport'},copy=True)
    section_14_3_imdg_notes = fields.Html(string="IMDG additional notes", translate=True)
    # Dangerous Goods by Air (ICAO) - IATA 
    section_14_2_iata = fields.Char('Proper shipping name (IATA)', default=lambda s: _("Not regulated for transport."),
                               translate=True)
    section_14_3_iata = fields.Char('Transport hazard class(es) (IATA)', default=lambda s: _("Not regulated for transport."),
                               translate=True)
    section_14_3_iata_pictograms = fields.Many2many('sds.pictogram', string="Label pictograms (IATA)", 
                                     relation="sds_pictogram_iata_rel",
                                     domain="[('category', '=', 'transport')]",
                                     context={'default_category': 'transport'},copy=True)
    section_14_3_iata_notes = fields.Html(string="ICAO - IATA additional notes", translate=True)

    section_14_4 = fields.Many2one('sds.sentences', 
                                       domain="[('category', '=', 'transport')]", 
                                       string='Packing group',
                                       context={'default_category': 'transport',},
                                       required=True,
                                       copy=True)
    section_14_5 = fields.Many2one('sds.sentences', 
                                       domain="[('category', '=', 'transport')]", 
                                       string='Environmental hazards',
                                       context={'default_category': 'transport',},
                                       required=True,
                                       copy=True)
    section_14_6 = fields.Many2one('sds.sentences', 
                                       domain="[('category', '=', 'transport')]", 
                                       string='Special precautions for user',
                                       context={'default_category': 'transport',},
                                       required=True,
                                       copy=True)
    section_14_7 = fields.Many2one('sds.sentences', 
                                       domain="[('category', '=', 'transport')]", 
                                       string='Maritime transport in bulk according to IMO instruments',
                                       context={'default_category': 'transport',},
                                       required=True,
                                       copy=True)
    section_14_note = fields.Html(string="Section 14 Notes", translate=True)

    # Section 15: Regulatory Information

    section_15_regulation = fields.Many2many('sds.regulatory.information', relation="sds_regulatory_information_rel",
                                   string="Regulatory Information")

    section_15_1 = fields.Html(
        string="Other regulations specific for the substance or mixture",
        default=lambda s: _('None available.'), translate=True, sanitize=False)
    section_15_2 = fields.Many2one('sds.sentences', 
                                       domain="[('category', '=', 'assessment')]", 
                                       string='Chemical safety assessment',
                                       context={'default_category': 'assessment',},
                                       required=True,
                                       copy=True)
    section_15_note = fields.Html(string="Section 15 Notes", translate=True)

    # Section 16: Other information
    section_16_classification_procedure = fields.Many2one('sds.sentences', 
                                       domain="[('category', '=', 'classification')]", 
                                       string='Classification and procedure used',
                                       context={'default_category': 'classification',},
                                       required=True,
                                       copy=True)

    # Only literal strings can be marked for exports, not expressions or variables.

    section_16_legend = fields.Many2many('sds.legend', relation="sds_legend_rel",
                                   string="Legend entries")
    section_16_bibliography_url = fields.Boolean(string="Bibliography URL in PDF", default=False)
    section_16_bibliography = fields.Many2many('sds.bibliography', relation="sds_bibliography_rel",
                                   string="Bibliography entries")

    section_16_changes = fields.Char('Changes made to the previous version', default=lambda s: _('Initial version'), translate=True)
    # FIXME: Change field name to 'section_16_disclaimer' or add a field
    section_16_note = fields.Many2one('sds.sentences', 
                                       domain="[('category', '=', 'disclaimer')]", 
                                       string='Section 16 Notes',
                                       context={'default_category': 'disclaimer',},
                                       required=True,
                                       copy=True)

    @api.onchange('product_id')
    def product_id_change(self):
        """
        Set the name of SDS according to product name
        :return:
        """
        vals = {}
        sds_name = 'New SDS'
        pname = self.product_id.name
        if pname:
            sds_name = pname + ' SDS'
        vals.update(section_1_1=pname, name=sds_name)
        result = self.update(vals)
        return result

    @api.onchange('section_2_1_selector')
    def section_2_1_selector_change(self):
        """
        If not hazardous, then GHS Labelling should be not necessary
        If hazardous, then the optional hazard in section 3 does not need to be explicitly declared here.
        :return:
        """
        vals = {}
        status_butt_1 = self.section_2_1_selector
        status_butt_2 = self.section_2_2_selector
        status_butt_3 = self.section_2_1_b_selector
        if status_butt_1 != status_butt_2:
            status_butt_2 = status_butt_1

        if status_butt_1 == True:
            status_butt_3 = False
        vals.update(section_2_1_selector=status_butt_1,
                    section_2_2_selector=status_butt_2,
                    section_2_1_b_selector=status_butt_3)
        result = self.update(vals)
        return result

    @api.onchange('section_2_1_b_selector')
    def section_2_1_b_selector_change(self):
        """
        If not hazardous, but with optional hazard in section 3 then remove GHS Labeling and hazard declaration here.
        :return:
        """
        vals = {}
        status_butt_1 = self.section_2_1_selector
        status_butt_2 = self.section_2_2_selector
        status_butt_3 = self.section_2_1_b_selector
        status_butt_4 = self.section_3_2_selector
        if status_butt_3 == True:
            status_butt_1 = False
            status_butt_2 = False
            status_butt_4 = True
            
        vals.update(section_2_1_selector=status_butt_1,
                    section_2_2_selector=status_butt_2,
                    section_2_1_b_selector=status_butt_3,
                    section_3_2_selector=status_butt_4)
        result = self.update(vals)
        return result

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if 'name' not in default:
            default['name'] = _("%s (copy)") % (self.name)
        # Retrieve properties values for copy (section 9.1)
        pvals = dict(zip(self.section_9_1.mapped('name_id.name'),self.section_9_1.mapped('value')))
        pids = dict(zip(self.section_9_1.mapped('name_id.name'),self.section_9_1.mapped('id')))
        cvals = dict(zip(self.section_2_1.mapped('Classification'),self.section_2_1.mapped('HazardStatement')))
        mvals = dict(zip(self.section_3_2.mapped('substance'),self.section_3_2.mapped('concentration')))
        rec = super(SdsDatasheet, self).copy(default=default)
        rec.fill_properties(pvals,pids)
        rec.fill_classification(cvals)
        rec.fill_mixture(mvals)
        return rec

    def fill_mixture(self, values=None):
        """
        This function helps the copy of section 3.2, a one2Many field
        :return:
        """
        values = dict(values or {})
        mixture_ids = []
        for sub, conc in values.items():
            mixture_ids += self.env['sds.chemical.mixture'].create({
                'datasheet_id': self._context.get('active_id'),
                'substance': sub.id,
                'concentration': conc,
            })
        vals = {}
        vals.update({'section_3_2': [(4, new_mixture.id) for new_mixture in mixture_ids]})
        return self.update(vals)

    def fill_classification(self, values=None):
        """
        This function helps the copy of section 2.1, a one2Many field
        :return:
        """
        values = dict(values or {})
        c_ids = []
        for classification, hazstat in values.items():
            c_ids += self.env['sds.regulation.criteria'].create({
                'datasheet_id': self._context.get('active_id'),
                'Classification': classification.id,
                'HazardStatement': hazstat.id ,
            })
        vals = {}
        vals.update({'section_2_1': [(4, new_classification_id.id) for new_classification_id in c_ids]})
        return self.update(vals)

    def fill_properties(self, values=None, pids=None):
        """
        Preload all the properties in the properties table (Section 9.1)
        :return:
        """
        values = dict(values or {})
        pids = dict(pids or {})
        props = {}
        prop_obj = self.env['sds.chemical.property'].search([])

        prop_ids = []

        for prop in prop_obj:
            if prop.name in values:
                props.update({prop.name: values[prop.name]})
            else:
                props.update({prop.name: _('n.a.')})
            prop_id = self.env['sds.chemical.property.line'].create(
                {'name_id': prop.id , 'value': props[prop.name]})
            prop_ids += prop_id

        vals = {}
        vals.update({'section_9_1': [(4, new_prop_id.id) for new_prop_id in prop_ids]})
        return self.update(vals)
    
    @api.model
    def _get_available_dnel(self):
        """
        This function looks at which substances are declared in section 3, 
        which ones have a DNEL section filled, and returns a dictionary 
        of DNEL descriptions.
        """
        chem_sub = {}

        # Check if this is a mixture
        status_butt = self.section_3_2_selector
        if status_butt == False:
            return chem_sub
        
        for chem in self.section_3_2:
            if chem.substance.dnel == True:
                chem_sub.update({chem.substance.name: chem.substance.wrk_aq_sys_dermal})

        return chem_sub

    def sds_preview(self):
        if self.id:
            return {
                'type': 'ir.actions.act_url',
                'url': '/report/html/safety_datasheet.report_safety_datasheet?ids=%s&model=sds.datasheet&lang=%s&country=%s' % (self.id,'en_US','Italy'),
                'target': 'new',
            }