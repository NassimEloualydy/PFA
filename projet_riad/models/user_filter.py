from odoo import models,fields,api,_
from datetime import datetime,timedelta
import re
class user_filter(models.Model):
    _name = "user.filter"  # Nom du modèle (table dans la base de données)
    user_id = fields.Many2one("res.users", string="Responsable")    
    
    # _inherit est une liste de modèles dont ce modèle hérite
