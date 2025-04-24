# Copyright 2025 Alberto Carollo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade

def _link_datasheet_field_to_sentences_table(env, old_column, new_column, category):
    """Update column with the ID of the corresponding sentence value
    """
    openupgrade.logged_query(
        env.cr,
        f"""
        WITH link AS (
            SELECT datasheet."{old_column}" as name, sentences.id as linkid from sds_datasheet as datasheet
            INNER JOIN sds_sentences as sentences
            ON datasheet."{old_column}" = sentences.name
            WHERE sentences.category = '{category}'
        )
        UPDATE sds_datasheet
        SET "{new_column}" = link.linkid
        FROM link     
        """,
    )
    

@openupgrade.migrate()
def migrate(env, version):
    
    _link_datasheet_field_to_sentences_table(env, openupgrade.get_legacy_name("section_2_3_PBT"), "section_2_3_PBT", "pbtvpvb")
    _link_datasheet_field_to_sentences_table(env, openupgrade.get_legacy_name("section_2_3_vPvB"), "section_2_3_vPvB", "pbtvpvb")
    _link_datasheet_field_to_sentences_table(env, openupgrade.get_legacy_name("section_2_3_endocrine"), "section_2_3_endocrine", "endocrine")
    _link_datasheet_field_to_sentences_table(env, openupgrade.get_legacy_name("section_6_4"), "section_6_4", "ref_section")
    _link_datasheet_field_to_sentences_table(env, openupgrade.get_legacy_name("section_7_3"), "section_7_3", "end_use")
    _link_datasheet_field_to_sentences_table(env, openupgrade.get_legacy_name("section_9_2"), "section_9_2", "other_info")
    _link_datasheet_field_to_sentences_table(env, openupgrade.get_legacy_name("section_11_2_2"), "section_11_2_2", "other_info")
    _link_datasheet_field_to_sentences_table(env, openupgrade.get_legacy_name("section_14_1"), "section_14_1", "transport")
    _link_datasheet_field_to_sentences_table(env, openupgrade.get_legacy_name("section_14_4"), "section_14_4", "transport")
    _link_datasheet_field_to_sentences_table(env, openupgrade.get_legacy_name("section_14_5"), "section_14_5", "transport")
    _link_datasheet_field_to_sentences_table(env, openupgrade.get_legacy_name("section_14_6"), "section_14_6", "transport")
    _link_datasheet_field_to_sentences_table(env, openupgrade.get_legacy_name("section_14_7"), "section_14_7", "transport")
    _link_datasheet_field_to_sentences_table(env, openupgrade.get_legacy_name("section_15_2"), "section_15_2", "assessment")
    _link_datasheet_field_to_sentences_table(env, openupgrade.get_legacy_name("section_16_classification_procedure"), "section_16_classification_procedure", "classification")
    _link_datasheet_field_to_sentences_table(env, openupgrade.get_legacy_name("section_16_note"), "section_16_note", "disclaimer")
    
    
    
    