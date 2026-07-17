from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char("Typname", required=True)
    sequence = fields.Integer("Sequence", default=1)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "Name must be unique.")
    ]