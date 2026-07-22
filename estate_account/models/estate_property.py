from odoo import Command, models

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def set_as_sold(self):
        for record in self:
            invoice_vals = {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': 'Percent of selling price',
                        'quantity': 0.06,
                        'price_unit': record.selling_price,
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100.0,
                    }),
                ]
            }
            self.env['account.move'].create(invoice_vals)
        return super().set_as_sold()