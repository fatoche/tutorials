from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"

    name = fields.Char("Property name")