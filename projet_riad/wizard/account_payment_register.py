from odoo import models, fields,api

class AccountPaymentRegister(models.TransientModel):
    # Héritage du modèle "account.payment.register"
    _inherit = "account.payment.register"
    
    # Ajout d'un champ "payment_subtype" de type sélection (Selection)
    payment_subtype = fields.Selection([
        ('payment', 'Paiement'),
        ('adc', 'A.D.C'),
        ('pre', 'Pré-financement')],
        string="Payment Subtype"
    )
    communication=fields.Char(string="Numéro de chèque",compute='_default_value_for_communication',store=True)

    move_id=fields.Many2one("account.move",string="Facture")
    # Ajout d'un champ "date_echeance" de type date (Date)
    date_echeance = fields.Date(string="Date d'échéance")
    @api.onchange("payment_method_line_id")
    @api.depends("payment_method_line_id")
    def _default_value_for_communication(self):
        print("the paument method is ")
        print(self.payment_method_line_id.name)
        if self.payment_method_line_id.name in ["Prélèvement","Effet"]:
            self.communication=self.payment_method_line_id.name
        else: 
            self.communication=""

    # def action_create_payments(self):
    #     active_ids=self._context.get('active_ids')
    #     active_model=self._context.get('active_model')
    #     if active_model=="account.move":
    #         self.env["account.move"].search([("id","=",active_ids[0])],limit=1).write({
    #             "invoice_date_due":self.date_echeance
    #         })
    #         query="update account_move set invoice_date_due=%s where id=%s"
    #         self.env.cr.execute(query, (self.date_echeance,active_ids[0]))                                                                   
    #         self.move_id=active_ids[0]
    #     res=super(AccountPaymentRegister,self).action_create_payments()
    #     return res
        # print("the date echenace is")
        # print(self.date_echeance)
        # return self.action_create_payments()
        # # return super.(self)