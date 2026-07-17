from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "Name must be unique.")
    ]