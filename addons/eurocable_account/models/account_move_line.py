# Copyright 2022 Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = "account.move.line"

    uom_id = fields.Many2one('uom.uom')
    uom_category_id = fields.Many2one('uom.category')
    factor = fields.Float()
    region_code = fields.Integer(default=1)
    intrastat_id = fields.Many2one(
        'account.intrastat.code',
        string="Commodity code",
        store=True
    )
    weight = fields.Float(
        store=True,
        default=0.0
    )
    intrastat_product_origin_country_name = fields.Char(
        related='product_id.intrastat_origin_country_id.name'
    )
    co_commd = fields.Char(
        related='product_id.intrastat_id.code',
        store=True
    )
    is_service = fields.Integer(compute='_compute_is_service',
                                store=1)

    show_in_report = fields.Boolean()

    def get_default_transaction(self):
        intrastat_transaction_id = self.env['account.intrastat.code'].search([('code', '=', 11)])
        return intrastat_transaction_id and intrastat_transaction_id[0] or False

    intrastat_transaction_id = fields.Many2one('account.intrastat.code',
                                               string='Intrastat',
                                               domain="[('type', '=', 'transaction')]",
                                               default=get_default_transaction)

    @api.depends('name')
    def _compute_is_service(self):
        for rec in self:
            if rec.product_id and rec.product_id.\
                    detailed_type == 'service':
                rec.is_service = 1
            else:
                rec.is_service = 0

    @api.onchange('product_id', 'name', 'tax_ids')
    def _onchange_show_in_report(self):
        for rec in self:
            line_to_show = rec.tax_ids.filtered(lambda tax: tax.show_intrastat)
            if ((rec.product_id and rec.product_id.detailed_type != 'service') or
                    (not rec.product_id and bool(line_to_show))):
                rec.show_in_report = True
            else:
                rec.show_in_report = False

    @api.onchange('product_id')
    def compute_intrastat_code(self):
        for rec in self:
            if rec.product_id:
                rec.intrastat_id = rec.product_id.intrastat_id
                rec.weight = rec.product_id.weight
                rec.uom_id = rec.product_id.uom_id
                rec.uom_category_id = rec.uom_id.category_id
                rec.factor = rec.uom_id.factor
