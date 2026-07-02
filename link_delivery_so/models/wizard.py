from odoo import models, fields
from odoo.exceptions import UserError


class LinkDeliveryWizard(models.TransientModel):
    _name = 'link.delivery.so.wizard'
    _description = 'Link Delivery to Sales Order'

    sale_id = fields.Many2one('sale.order', string='Sales Order', required=True)

    def action_link(self):
        self.ensure_one()
        pickings = self.env['stock.picking'].browse(
            self.env.context.get('active_ids', []))
        if not pickings:
            raise UserError("No delivery to process.")
        so = self.sale_id
        linked = 0
        for picking in pickings:
            for move in picking.move_ids_without_package:
                if move.sale_line_id:
                    continue
                candidates = so.order_line.filtered(
                    lambda l: l.product_id == move.product_id
                              and l.qty_delivered < l.product_uom_qty
                )
                line = candidates[:1] or so.order_line.filtered(
                    lambda l: l.product_id == move.product_id
                )[:1]
                if line:
                    move.sale_line_id = line.id
                    linked += 1
            if not picking.origin:
                picking.origin = so.name
            if so.procurement_group_id and not picking.group_id:
                picking.group_id = so.procurement_group_id.id
        if not linked:
            raise UserError(
                "No move could be linked: the delivery products do not match "
                "any line on sales order %s." % so.name)
        return {'type': 'ir.actions.act_window_close'}
