
from odoo import models,fields,api,_
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import ast

class account_bank_statement_line(models.Model):
    
    _inherit="account.bank.statement.line"

    def write(self,vals):
        bank_statement_line=super(account_bank_statement_line,self).write(vals)
        bill=self.env["account.move"].search([])
        # print("the bills of the id "+str(self.id)+" are")
        # print(self.is_reconciled)
        model_id=self.env["ir.model"].search([("model","=","account.move")],limit=1)
        activity_id=self.env["mail.activity.type"].with_context(lang='en_US').search([("name","=","To Do")],limit=1)
        for rec in bill:
                if rec.payment_state=="paid":
                    is_activity_created=self.env["mail.activity"].search(
                        [("activity_type_id","=",activity_id.id),
                         ("res_model_id","=",model_id.id),
                         ("res_id","=",rec.id)
                         ])
                    if is_activity_created:
                        for rec_a in is_activity_created:
                            self.env["mail.activity"].search([("id","=",rec_a.id)],limit=1).action_done()                
        return bank_statement_line
