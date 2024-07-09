from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    weight = fields.Float(compute="_compute_weight", store=True, readonly=False)
    weight_total = fields.Float(compute="_compute_total_weight", store=True)

    def _compute_weight(self):
        for rec in self:
            # Loop instead of .filtered() to get rid of pre-commit error
            # B023 Function definition does not bind loop variable `rec`
            production = self.env["mrp.production"]
            for mo in rec.order_id.mrp_production_ids:
                if mo.product_id == rec.product_id:
                    production |= mo
            rec.weight = production.xx_weight if len(production) == 1 else 0

    @api.depends("product_uom_qty", "weight")
    def _compute_total_weight(self):
        for rec in self:
            rec.weight_total = rec.weight * rec.product_uom_qty if rec.weight else 0.0

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        res.update({"weight": self.weight})
        return res
