from odoo import models,fields,api,_
from datetime import datetime,timedelta,time
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

class account_move_line(models.Model):
    _inherit="account.move.line"
    type_account_move_line=fields.Char("type")
    id_base_12=fields.Char("id_base_12")
    
@api.model
def create(self, vals):
    # Recherche de l'ID du projet lié à la facture
    project_id = self.env['account.move'].search([('id', '=', vals['move_id'])], limit=1).project_id

    # Si un projet est trouvé
    if project_id:
        # Calcul du total des factures liées à ce projet
        total_invoice_amount = sum(self.env['account.move'].search([('project_id', '=', int(project_id))]).mapped('amount_total_signed'))

        # Récupération du montant du marché pour ce projet
        contract_amount = self.env["project.project"].search([('id', '=', int(project_id))], limit=1).montant_marche    

        # Vérification si le montant du marché est supérieur au total des factures
        if float(contract_amount) > float(total_invoice_amount):
            return super(account_move_line, self).create(vals)
        else:
            raise ValidationError(_("Vous avez dépassé le montant du marché pour ce projet"))
    else:
        return super(account_move_line, self).create(vals)
