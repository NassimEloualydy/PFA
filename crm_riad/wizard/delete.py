from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class deletePiste(models.TransientModel):
     _name="wizard.piste.delete"

     def delete_piste(self):
       
        crm_lead_model = self.env["crm.lead"]
        
        # Assurez-vous d'ajuster le code en fonction de votre modèle réel et de la manière dont vous souhaitez le supprimer
        crm_lead_model.browse(self.env.context.get('active_id')).unlink()
        view_id= self.env.ref('crm.crm_case_kanban_view_leads').id
       
        return {
            'type': 'ir.actions.act_window_close',
            'res_model': 'crm.lead',
            'view_mode':'kanban',
            'view_id': view_id,  # Utilisez False pour que le système choisisse la vue appropriée
            'target':'main',
            
        }

    