from odoo import models, fields

class project_create_sale_order(models.TransientModel):
    # _inherit="mail.email_compose_message_wizard_form"
    # _inherit="sale.order"
    # email=fields.Char("email",related='partner_id.email',readonly=False)
    _inherit = 'project.create.sale.order'
    