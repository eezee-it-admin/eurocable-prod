# Copyright 2022 Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import models, api


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.onchange('product_id', 'product_uom_id')
    def _onchange_product_id(self):
        super(StockMoveLine, self)._onchange_product_id()
        if self.product_id:
            if self.picking_id:
                product = self.product_id.with_context(lang=self.picking_id.partner_id.lang or self.env.user.lang)
                self.description_picking = product.get_product_multiline_description_sale()

    @api.model
    def create(self, vals):
        res = super(StockMoveLine, self).create(vals)
        if res.move_id:
            res.description_picking = res.move_id.description_picking
        return res