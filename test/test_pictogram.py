# Copyright 2023 Alberto Carollo - 
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase

class PictogramCase(TransactionCase):
    def test_create_pictogram(self):
        pictogram_model = self.env["sds.pictogram"]
        pictogram1 = pictogram_model.create(
            {
                "name": "Pictogram1",
                "description": "A test pictogram",
                "pictogram": "",
                "category": "",
                "sequence": "1",
            }
        )

        self.assertEqual(pictogram1.name, "Pictogram1")

