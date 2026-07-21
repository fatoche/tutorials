from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
import odoo.tools.float_utils as fu


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    active = fields.Boolean("Aktiv", default=True)
    state = fields.Selection(
        string="Status",
        selection=[("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")],
        default="new",
        required=True,
        copy=False,
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user.id)

    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Property Offers")

    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float("Best offer", compute="_compute_best_price")

    _sql_constraints = [
        ("check_expected_price", 'CHECK(expected_price > 0)', "The expected price must be strictly positive"),
        ("check_selling_price", 'CHECK(selling_price >= 0)', "The selling price must be positive")
    ]

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_at_least_90p_of_expected_price(self):
        for record in self:
            if fu.float_is_zero(record.selling_price, precision_digits=2):
                return
            if fu.float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0:
                raise ValidationError(
                    "The selling price mustn't be lower than 90% of the expected price. " \
                    "You must change the expected price if you want to accept this offer.")


    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max((offer.price for offer in record.offer_ids), default=0.0)


    @api.onchange('garden')
    def _onchange_garden(self):
        if (self.garden):
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False


    def set_as_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold.")
            else:
                record.state = "sold"


    def set_as_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be cancelled.")
            else:
                record.state = "cancelled"
    
