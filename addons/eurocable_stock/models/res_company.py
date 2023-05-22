# Copyright 2023 Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    logo_zpl = fields.Binary(string="Logo ZPL",
                             help="This logo is used in ZPL type report "
                                  "print.")
