from odoo import models, fields


class DocumentType(models.Model):
    _name = "document.type"
    _description = "Type Document"

    name = fields.Char(required=True)
    text = fields.Html(translate=True)
