# Copyright 2025 Alberto Carollo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

_logger = logging.getLogger(__name__)

# Older versions of security/ir.model.access.csv used ids with a dot
# (e.g. "access_sds.pictogram_user"): Odoo stored them under fake modules
# ("access_sds", "access_chemical", "access_sds_regulatory"), so they were never
# cleaned up on update. Some of them gave full rights to every employee.
FAKE_MODULES = ('access_sds', 'access_chemical', 'access_sds_regulatory')


def migrate(cr, version):
    cr.execute(
        """
        SELECT d.id, d.res_id, d.module || '.' || d.name
          FROM ir_model_data d
          JOIN ir_model_access a ON a.id = d.res_id
          JOIN ir_model m ON m.id = a.model_id
         WHERE d.model = 'ir.model.access'
           AND d.module IN %s
           AND m.model IN (SELECT im.model FROM ir_model im
                             JOIN ir_model_data imd ON imd.model = 'ir.model' AND imd.res_id = im.id
                            WHERE imd.module = 'safety_datasheet')
        """,
        (FAKE_MODULES,),
    )
    rows = cr.fetchall()
    if not rows:
        return
    _logger.info("safety_datasheet: removing %s stale access rules: %s", len(rows), ', '.join(r[2] for r in rows))
    cr.execute("DELETE FROM ir_model_access WHERE id IN %s", (tuple(r[1] for r in rows),))
    cr.execute("DELETE FROM ir_model_data WHERE id IN %s", (tuple(r[0] for r in rows),))
