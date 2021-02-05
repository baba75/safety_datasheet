# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SdsRegulationCriteria(models.Model):
    """
    See point 2.1.2. Classification criteria of REGULATION (EC) No 1272/2008.
    (http://data.europa.eu/eli/reg/2008/1272/2018-03-01)
    TODO: In the norm there is defined a connection also with Signal Words and Precautionary Statement,
    for each class (Explosive, Flammable gases, etc...)
    """
    _name = "sds.regulation.criteria"
    _description = "European Community Regulation Criteria"

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

class SdsDatasheet(models.Model):
    """
    See Amendement to ANNEX II of REACH:
    REQUIREMENTS FOR THE COMPILATION OF SAFETY DATA SHEETS
    Reference: http://data.europa.eu/eli/reg/2020/878/oj
    """
    _name = 'sds.datasheet'
    _description = 'Product Safety Datasheet'
    _order = "name"

    @api.model
    def _default_company(self):
        company = self.env['res.company']._company_default_get()
        if(company.street and company.zip and company.city):
            result = '<p>' + company.name + '<br/>' + company.street
            result += '<br/>' + company.zip + ' ' + company.city + ' ' + company.state_id.name
            result += '<br/>' + company.country_id.name + '</p>'
        else:
            result = '<p>' + company.name + '<br/>' + 'Insert you company full adrees here</p>'
        return result

    @api.model
    def _default_emergency_phone(self):
        return self.env['res.company']._company_default_get().phone

    name = fields.Char(string='Name', required=True, index=True, default=lambda self: _('New SDS'))
    product_id = fields.Many2one('product.template', 'Product', required=True, copy=True)
    revision_date = fields.Date(string="Revision date", default=fields.Date.today(), required=True)
    supersedes_date = fields.Char(string="Supersedes version/date", translate=True)

    # Section 1: Identification of the substance/mixture and of the company/undertaking
    section_1_1 = fields.Char(string="Product Identifier", required=True, translate=True)
    section_1_2 = fields.Text(
        string="Relevant identified uses of the substance or mixture and uses advised against recommended use",
        required=True, translate=True)
    section_1_3 = fields.Html(string="Detail of the supplier of the safety data sheet", default=_default_company,
                              required=True)
    section_1_4 = fields.Text(string="Emergency telephone number", default=_default_emergency_phone,
                              required=True, translate=True)
    section_1_note = fields.Html(string="Section 1 notes", translate=True)

    # Section 2: Hazards identification
    section_2_1_selector = fields.Boolean(string="Hazardous substance or mixture", default=False)
    section_2_1 = fields.One2many('sds.regulation.criteria', 'datasheet_id', string='EC regulation',
                                  help='Regulation (EC) No 1272/2008 - classification, labelling and packaging of substances and mixtures (CLP)')
    section_2_2_selector = fields.Boolean(string="GHS Labelling", default=False)
    section_2_2_pictograms = fields.Many2many('sds.pictogram', string="Label pictograms", copy=True)
    section_2_2_signal = fields.Selection([('danger', 'Danger'), ('warning', 'Warning')], string="SignalWords",
                                          default='warning')
    section_2_2_P = fields.Many2many('sds.precautionary.statement', string="Precautionary Statement", copy=True)
    section_2_2_Additional = fields.Html('Additional Labelling', translate=True)
    section_2_3_PBT = fields.Char(string="PBT",
                                  help="persistent, bioaccumulative and toxic substances (PBT substances)",
                                  default=lambda s: _('none'), required=True, translate=True)
    section_2_3_vPvB = fields.Char(string="vPvB",
                                   help="very persistent and very bioaccumulative substances (vPvB substances)",
                                   default=lambda s: _('none'), required=True, translate=True)
    section_2_3_OtherHazards = fields.Char(string="Other Hazards", default=lambda s: _("none"), required=True,
                                           translate=True)
    section_2_note = fields.Html(string="Section 2 notes", translate=True)

    # Section 3: Composition/information on ingredients
    # Hint: Look at https://www.echa.europa.eu/substance-information/
    # FIXME: only subsection 3.1 or subsection 3.2 needs to be included as appropriate
    section_3 = fields.Char(string="Chemical identity", translate=True)
    section_3_1 = fields.Html(string="Substances", default=lambda s: _("Not applicable."), required=True,
                              translate=True, sanitize=False)
    section_3_2_selector = fields.Boolean(string="Mixture", default=False)
    section_3_2 = fields.One2many('sds.chemical.mixture', 'datasheet_id', string='Mixture elements')
    section_3_note = fields.Html(string="Section 3 notes", translate=True)

    # FIXME: sds.sentences are not displaying in the right order on report.

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
    section_6_4 = fields.Html(string="Reference to other sections",
                              default=lambda s: _("See sections: 7, 8, 11, 12 and 13."),
                              translate=True, sanitize=False)
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
    section_7_3 = fields.Html(string="Specific end use",
                              default=lambda s: _(
                                  "See the technical data sheet on this product for further information."),
                              translate=True, sanitize=False)
    section_7_note = fields.Html(string="Section 7 notes", translate=True)

    # Section 8: Exposure controls/personal protection
    section_8_1_tlv_selector = fields.Boolean(string="Occupational exposure limit (TLV).", default=False)
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
    section_8_1_dnel_selector = fields.Boolean(string="Derived No Effect Level (DNEL)", default=False)
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
    section_8_1_pnec_selector = fields.Boolean(string="Predicted No Effect Concentration (PNEC)",
                                               default=False)
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
    section_9_2 = fields.Html(string="Other information", default=lambda s: _("No data available."),
                              translate=True, sanitize=False)

    section_9_note = fields.Html(string="Section 9 Notes", translate=True)

    # Section 10: Stability and reactivity
    section_10_1 = fields.Many2many('sds.sentences', relation="sds_reactivity_statement_rel",
                                    domain="[('category', '=', 'reactivity')]",
                                    string='Reactivity',
                                    context={'default_category': 'reactivity'})
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
    section_11_1_1_selector = fields.Boolean(string="Insert acute toxicity details", default=False)
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
    section_11_1_2_selector = fields.Boolean(string="Insert skin corrosion/irritation details", default=False)
    section_11_1_2_text = fields.Html(string="Skin corrosion/irritation details", translate=True, sanitize=False)
    section_11_1_3 = fields.Many2many('sds.sentences', relation="sds_eye_damage_statement_rel",
                                      domain="[('category', '=', 'eye_damage')]",
                                      string='Serious eye damage/eye irritation',
                                      context={'default_category': 'eye_damage'})
    section_11_1_3_selector = fields.Boolean(string="Insert eye damage corrosion/irritation details", default=False)
    section_11_1_3_text = fields.Html(string="Eye damage/irritation details", translate=True,sanitize=False)
    section_11_1_4 = fields.Many2many('sds.sentences', relation="sds_respiratory_skin_sensitization_statement_rel",
                                      domain="[('category', '=', 'sensitization')]",
                                      string='Respiratory or skin sensitization',
                                      context={'default_category': 'sensitization'})
    section_11_1_4_selector = fields.Boolean(string="Insert respiratory or skin sensitization details", default=False)
    section_11_1_4_text = fields.Html(string="Respiratory or skin sensitization details", translate=True,sanitize=False)
    section_11_1_5 = fields.Many2many('sds.sentences', relation="sds_mutagenicity_statement_rel",
                                      domain="[('category', '=', 'mutagenicity')]",
                                      string='Germ cell mutagenicity',
                                      context={'default_category': 'mutagenicity'})
    section_11_1_5_selector = fields.Boolean(string="Insert mutagenicity details", default=False)
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
    section_11_1_6_selector = fields.Boolean(string="Insert carcinogenicity details", default=False)
    section_11_1_6_text = fields.Html(string="Carcinogenicity details", translate=True,sanitize=False)
    section_11_1_7 = fields.Many2many('sds.sentences', relation="sds_reproductive_toxicity_statement_rel",
                                      domain="[('category', '=', 'reproductive')]",
                                      string='Reproductive toxicity',
                                      context={'default_category': 'reproductive'})
    section_11_1_7_selector = fields.Boolean(string="Insert reproductive toxicity details", default=False)
    section_11_1_7_text = fields.Html(string="Reproductive toxicity details", translate=True,sanitize=False)
    section_11_1_8 = fields.Many2many('sds.sentences', relation="sds_specific_target_single_statement_rel",
                                      domain="[('category', '=', 'STOST')]",
                                      string='Specific Target Organ Systemic Toxicity (Single Exposure)',
                                      context={'default_category': 'STOST'})
    section_11_1_8_selector = fields.Boolean(string="Insert STOST SE details", default=False)
    section_11_1_8_text = fields.Html(string="STOST SE details", translate=True,sanitize=False)
    section_11_1_9 = fields.Many2many('sds.sentences', relation="sds_specific_target_repeated_statement_rel",
                                      domain="[('category', '=', 'STOST')]",
                                      string='Specific Target Organ Systemic Toxicity (Repeated Exposure)',
                                      context={'default_category': 'STOST'})
    section_11_1_9_selector = fields.Boolean(string="Insert STOST RE details", default=False)
    section_11_1_9_text = fields.Html(string="STOST RE details", translate=True,sanitize=False)
    section_11_1_10 = fields.Many2many('sds.sentences', relation="sds_aspiration_hazard_products_statement_rel",
                                       domain="[('category', '=', 'aspiration')]",
                                       string='Aspiration Hazard',
                                       context={'default_category': 'aspiration'})
    section_11_1_10_selector = fields.Boolean(string="Insert aspiration Hazard details", default=False)
    section_11_1_10_text = fields.Html(string="Aspiration Hazard details", translate=True, sanitize=False)
    section_11_2 = fields.Html(string='Information on other hazards', default=lambda s: _("None available."),
                               translate=True,sanitize=False)

    section_11_note = fields.Html(string="Section 11 Notes", translate=True)

    # Section 12: Ecological information
    section_12_1 = fields.Many2many('sds.sentences', relation="sds_toxicity_statement_rel",
                                    domain="[('category', '=', 'ecotoxicity')]", string='Toxicity',
                                    context={'default_category': 'ecotoxicity'})
    section_12_1_selector = fields.Boolean(string="Insert toxicity details", default=False)
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
    section_12_2_selector = fields.Boolean(string="Insert degradability details", default=False)
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
    section_12_3_selector = fields.Boolean(string="Insert bioaccumulative details", default=False)
    section_12_3_text = fields.Html(string="Bioaccumulative potential details", translate=True, sanitize=False)
    section_12_4 = fields.Many2many('sds.sentences', relation="sds_mobility_soil_statement_rel",
                                    domain="[('category', '=', 'mobility')]", string='Mobility in soil',
                                    context={'default_category': 'mobility'})
    section_12_4_selector = fields.Boolean(string="Insert mobility details", default=False)
    section_12_4_text = fields.Html(string="Mobility in soil details", translate=True, sanitize=False)
    section_12_5 = fields.Many2many('sds.sentences', relation="sds_pbt_vpvb_statement_rel",
                                    domain="[('category', '=', 'pbtvpvb')]",
                                    string='Results of PBT and vPvB assessment',
                                    context={'default_category': 'pbtvpvb'})
    section_12_5_selector = fields.Boolean(string="Insert PBT and vPvB details", default=False)
    section_12_5_text = fields.Html(string="Results of PBT and vPvB assessment details", translate=True, sanitize=False)
    section_12_6 = fields.Many2many('sds.sentences', relation="sds_endocrine_disrupting_statement_rel",
                                    domain="[('category', '=', 'endocrine')]", string='Endocrine disrupting properties',
                                    context={'default_category': 'endocrine'})
    section_12_6_selector = fields.Boolean(string="Insert endocrine details", default=False)
    section_12_6_text = fields.Html(string="Endocrine disrupting properties details", translate=True, sanitize=False)
    section_12_7 = fields.Many2many('sds.sentences', relation="sds_other_adverse_statement_rel",
                                    domain="[('category', '=', 'adverse')]", string='Other adverse effects',
                                    context={'default_category': 'adverse'})
    section_12_7_selector = fields.Boolean(string="Insert adverse effects details", default=False)
    section_12_7_text = fields.Html(string="Other adverse effects details", translate=True, sanitize=False)
    section_12_note = fields.Html(string="Section 12 Notes", translate=True)

    # Section 13: Disposal considerations
    section_13_1 = fields.Many2many('sds.sentences', relation="sds_disposal_consideration_statement_rel",
                                    domain="[('category', '=', 'disposal')]",
                                    string='Waste treatment methods',
                                    context={'default_category': 'disposal'})
    section_13_note = fields.Html(string="Section 13 Notes", translate=True)

    # Section 14: Transport information
    section_14_1 = fields.Char('UN number', default=lambda s: _("Not regulated for transport."), translate=True)
    section_14_2 = fields.Char('UN proper shipping name', default=lambda s: _("Not regulated for transport."),
                               translate=True)
    section_14_3 = fields.Char('Transport hazard class(es)', default=lambda s: _("Not regulated for transport."),
                               translate=True)
    section_14_4 = fields.Char('Packing group', default=lambda s: _("Not regulated for transport."), translate=True)
    section_14_5 = fields.Char('Environmental hazards', default=lambda s: _("Not Hazardous to the environment."),
                               translate=True)
    section_14_6 = fields.Char('Special precautions for user',
                               default=lambda s: _("Relevant information in other sections has to be considered."),
                               translate=True)
    section_14_7 = fields.Char('Maritime transport in bulk according to IMO instruments',
                               default=lambda s: _("Bulk transport in tankers is not intended."), translate=True)
    section_14_note = fields.Html(string="Section 14 Notes", translate=True)

    # Section 15: Regulatory Information

    section_15_regulation = fields.Many2many('sds.regulatory.information', relation="sds_regulatory_information_rel",
                                   string="Regulatory Information")

    section_15_1 = fields.Html(
        string="Other regulations specific for the substance or mixture",
        default=lambda s: _('None available.'), translate=True, sanitize=False)
    section_15_2 = fields.Char('Chemical safety assessment',
                               default=lambda s: _(
                                   'No Chemical Safety Assessment has been carried out for this substance/mixture.'),
                               translate=True)
    section_15_note = fields.Html(string="Section 15 Notes", translate=True)

    # Section 16: Other information
    section_16_classification_procedure = fields.Html(
        string="Classification and procedure used to derive the classification for mixtures according to Regulation (EC) No 1272/2008",
        default=lambda s: _('<p>The information contained in this Safety Data Sheet is derived '
                            'from the data provided by the suppliers of the components of the mixture, '
                            'that we verified adequate and reliable by analogy with similar products '
                            'and with the information provided by ECHA.</p>'),
        translate=True, sanitize=False)

    # Only literal strings can be marked for exports, not expressions or variables.

    section_16_legend = fields.Many2many('sds.legend', relation="sds_legend_rel",
                                   string="Legend entries")
    section_16_bibliography_url = fields.Boolean(string="Bibliography URL in PDF", default=False)
    section_16_bibliography = fields.Many2many('sds.bibliography', relation="sds_bibliography_rel",
                                   string="Bibliography entries")

    section_16_changes = fields.Char('Changes made to the previous version', default=lambda s: _('Initial version'), translate=True)
    section_16_note = fields.Html(string="Section 16 Notes",
                                  default=lambda s: _('<p class="sds">'
                                                      'The information contained in this sheet is based on the knowledge available to us at the date '
                                                      'of the latest version. The user must ensure the suitability and completeness of the information '
                                                      'in relation to the specific use of the product.<br> This document should not be construed as a '
                                                      'guarantee of any specific property of the product.<br> Since the use of the product does not fall '
                                                      'under our direct control, it is the user s obligation to observe the laws and regulations in force '
                                                      'regarding hygiene and safety under his own responsibility. No responsibility is assumed for '
                                                      'improper use.<br> Provide adequate training to personnel assigned to the use of chemical products.'
                                                      '</p>'),
                                  translate=True, sanitize=False)


    @api.multi
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

    @api.multi
    @api.onchange('section_2_1_selector')
    def section_2_1_selector_change(self):
        """
        If not hazardous, then GHS Labelling should be not necessary
        :return:
        """
        vals = {}
        status_butt_1 = self.section_2_1_selector
        status_butt_2 = self.section_2_2_selector
        if status_butt_1 != status_butt_2:
            status_butt_2 = status_butt_1
        vals.update(section_2_1_selector=status_butt_1, section_2_2_selector=status_butt_2)
        result = self.update(vals)
        return result

    @api.multi
    def xlate_default(self,ids=False):
        """
        This function set the translation of default values.
        It is called by create function or by the specific button (last option is
        necessary when importing from csv, for example)
        TODO: disable the button once called with create function
        :return:
        """
        if self.ids:
            ids = self.ids

        xlat_obj = self.env['ir.translation']
        model = 'sds'
        my_fields = self.fields_get().keys()
        my_defaults = self.default_get(my_fields)

        for my_field in my_fields:
            fname = model + '.datasheet,' + my_field
            default_ids = xlat_obj._get_ids(fname, 'model', 'en_US', ids)
            # FIXME: I have some troubles with sanitization of HTML and translation of default values.
            # We do not want sanitization, because is splitting the translation into several pieces.
            # On the other hand, I do not know how to manage quotes (like in "... user's ...") or <br/>
            # that becomes magically <br>

            if my_field in my_defaults:
                xlat_src = my_defaults[my_field]
                # First we want to see if the user made a translation
                xlat_values = xlat_obj.search([('name','like',fname),
                                               ('src','like',xlat_src),
                                               ('state','like','translated')])
                if not xlat_values:
                    # Then we take the default
                    xlat_values = xlat_obj.search([('name','like','addons/safety_datasheet/models/models.py'),
                                               ('src','like',xlat_src)
                                               ])
                    # If even the default does not exists, give up
                    if not xlat_values:
                        continue
                xlat_dict = dict(zip(xlat_values.mapped('lang'),xlat_values.mapped('value')))
                for lang in xlat_values.mapped('lang'):
                    xlat_obj._set_ids(
                        fname,
                        'model',
                        lang,
                        default_ids,
                        xlat_dict[lang],
                        xlat_src,
                    )
        return

    @api.model
    def create(self, vals):
        result = super(SdsDatasheet, self).create(vals)
        self.xlate_default(result.ids)
        return result

    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if 'name' not in default:
            default['name'] = _("%s (copy)") % (self.name)
        # Retrieve properties values for copy (section 9.1)
        pvals = dict(zip(self.section_9_1.mapped('name_id.name'),self.section_9_1.mapped('value')))
        cvals = dict(zip(self.section_2_1.mapped('Classification'),self.section_2_1.mapped('HazardStatement')))
        mvals = dict(zip(self.section_3_2.mapped('substance'),self.section_3_2.mapped('concentration')))
        rec = super(SdsDatasheet, self).copy(default=default)
        rec.fill_properties(pvals)
        rec.fill_classification(cvals)
        rec.fill_mixture(mvals)
        return rec

    @api.multi
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

    @api.multi
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

    @api.multi
    def fill_properties(self, values=None):
        """
        Preload all the properties in the properties table (Section 9.1)
        # TODO: Translations of values are lost
        :return:
        """
        values = dict(values or {})
        props = {}
        prop_obj = self.env['sds.chemical.property'].search([])
        prop_ids = []

        for prop in prop_obj:
            if prop.name in values:
                props.update({prop.name: values[prop.name]})
            else:
                props.update({prop.name: _('n.a.')})
            prop_ids += self.env['sds.chemical.property.line'].create(
                {'name_id': prop.id , 'value': props[prop.name]}
            )

        vals = {}
        vals.update({'section_9_1': [(4, new_prop_id.id) for new_prop_id in prop_ids]})
        return self.update(vals)

