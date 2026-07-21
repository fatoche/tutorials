from odoo import api, fields, models
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection(string="Status", selection=[("accepted", "Accepted"), ("refused", "Refused")])
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    _sql_constraints = [
        ("check_price", 'CHECK(price > 0)', "The offer- price must be strictly positive"),
    ]

    @api.model
    def create(self, vals):
        new_price = vals['price']
        for property in self.env['estate.property'].browse(vals['property_id']):
            max_offer = max(offer.price for offer in property.offer_ids)
            if new_price < max_offer:
                raise UserError(f"The offer must be higher than {max_offer}")
            
            property.state = "offer_received"

        return super().create(vals)

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(create_date, days=record.validity)

    
    def _inverse_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - create_date).days


    def action_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"


    def action_refuse(self):
        for record in self:
            record.status = "refused"
