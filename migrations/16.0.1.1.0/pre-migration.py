# Copyright 2025 Alberto Carollo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

_column_renames = {
    "sds_datasheet": [("section_2_3_PBT", None),
                      ("section_2_3_vPvB", None),
                      ("section_2_3_endocrine", None),
                      ("section_6_4", None),
                      ("section_7_3", None),
                      ("section_9_2", None),
                      ("section_11_2_2", None),
                      ("section_14_1", None),
                      ("section_14_4", None),
                      ("section_14_5", None),
                      ("section_14_6", None),
                      ("section_14_7", None),  
                      ("section_15_2", None), 
                      ("section_16_classification_procedure", None),
                      ("section_16_note", None),                     
                      ],
}

def _insert_sds_sentences_table(env, column, category):
    """Insert in the sds_sentences new values corresponding to distinct char values on the original column
    """
    openupgrade.logged_query(
        env.cr,
        f"""
        WITH sentences AS (
            SELECT DISTINCT "{column}" as name, '{category}' as category
            FROM sds_datasheet
        )
        INSERT INTO sds_sentences(
            sequence, create_uid, write_uid, category, name, active, create_date, write_date
        )
        SELECT '10','1','1',category, name, 'true', NOW(), NOW()
        FROM sentences
        WHERE NOT EXISTS (
            SELECT 1 FROM sds_sentences WHERE name = sentences.name AND category = '{category}'
        )
        """,
    )

@openupgrade.migrate()
def migrate(env, version):
    _insert_sds_sentences_table(env, 'section_2_3_PBT', 'pbtvpvb')
    _insert_sds_sentences_table(env, 'section_2_3_vPvB', 'pbtvpvb')
    _insert_sds_sentences_table(env, 'section_2_3_endocrine', 'endocrine')
    _insert_sds_sentences_table(env, 'section_6_4', 'ref_section')
    _insert_sds_sentences_table(env, 'section_7_3', 'end_use')
    _insert_sds_sentences_table(env, 'section_9_2', 'other_info')
    _insert_sds_sentences_table(env, 'section_11_2_2', 'other_info')
    _insert_sds_sentences_table(env, 'section_14_1', 'transport')
    _insert_sds_sentences_table(env, 'section_14_4', 'transport')
    _insert_sds_sentences_table(env, 'section_14_5', 'transport')
    _insert_sds_sentences_table(env, 'section_14_6', 'transport')
    _insert_sds_sentences_table(env, 'section_14_7', 'transport')
    _insert_sds_sentences_table(env, 'section_15_2', 'assessment')
    _insert_sds_sentences_table(env, 'section_16_classification_procedure', 'classification')
    _insert_sds_sentences_table(env, 'section_16_note', 'disclaimer')

    openupgrade.rename_columns(env.cr, _column_renames)
    
    openupgrade.drop_columns(env.cr, [("sds_datasheet", "section_2_3_PBT"),
                                      ("sds_datasheet", "section_2_3_vPvB"),
                                      ("sds_datasheet", "section_2_3_endocrine"),
                                      ("sds_datasheet", "section_6_4"),
                                      ("sds_datasheet", "section_7_3"),
                                      ("sds_datasheet", "section_9_2"),  
                                      ("sds_datasheet", "section_11_2_2"),   
                                      ("sds_datasheet", "section_14_1"),
                                      ("sds_datasheet", "section_14_4"), 
                                      ("sds_datasheet", "section_14_5"), 
                                      ("sds_datasheet", "section_14_6"), 
                                      ("sds_datasheet", "section_14_7"),  
                                      ("sds_datasheet", "section_15_2"),  
                                      ("sds_datasheet", "section_16_classification_procedure"),
                                      ("sds_datasheet", "section_16_note"),                                        
                                      ])

    openupgrade.add_columns(env, [("sds_datasheet", "section_2_3_PBT", "many2one"),
                                  ("sds_datasheet", "section_2_3_vPvB", "many2one"),
                                  ("sds_datasheet", "section_2_3_endocrine", "many2one"),
                                  ("sds_datasheet", "section_6_4", "many2one"),
                                  ("sds_datasheet", "section_7_3", "many2one"),
                                  ("sds_datasheet", "section_9_2", "many2one"),
                                  ("sds_datasheet", "section_11_2_2", "many2one"),
                                  ("sds_datasheet", "section_14_1", "many2one"),
                                  ("sds_datasheet", "section_14_4", "many2one"),
                                  ("sds_datasheet", "section_14_5", "many2one"),
                                  ("sds_datasheet", "section_14_6", "many2one"),
                                  ("sds_datasheet", "section_14_7", "many2one"),
                                  ("sds_datasheet", "section_15_2", "many2one"),
                                  ("sds_datasheet", "section_16_classification_procedure", "many2one"),
                                  ("sds_datasheet", "section_16_note", "many2one"),
                                  ])

