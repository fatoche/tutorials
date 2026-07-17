from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char("Name", required=True)

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "Name must be unique.")
    ]