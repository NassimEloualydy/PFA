from odoo import models,fields,api,_
from datetime import datetime,timedelta
from odoo.exceptions import ValidationError

class project_pv_type(models.Model):

    _name = "project.pv.type"  # Nom du modèle (table dans la base de données)
    
    _rec_name = "libelle"  # Champ qui sera utilisé comme nom enregistré (champ 'libelle' dans ce cas)
    
    libelle = fields.Char(string="Libelle", required=True, translate=True)
    # Champ 'libelle' de type texte (Char)
    # 'string' est le libellé du champ qui sera affiché dans l'interface utilisateur
    # 'required' indique que ce champ est obligatoire lors de la création d'un enregistrement
    # 'translate' indique que ce champ est traduisible (pour prendre en charge plusieurs langues)



