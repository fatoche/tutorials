from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"

    name = fields.Char("Typname", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "Name must be unique.")
    ]