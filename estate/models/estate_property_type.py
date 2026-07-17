from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char("Typname", required=True)

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "Name must be unique.")
    ]