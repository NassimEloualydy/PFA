from odoo import models,fields,api,_
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta


class resource_calendar(models.Model):
    _inherit="resource.calendar"
    
    # Définition d'un champ One2many pour établir une relation avec le modèle resource.calendar.leaves.
    resource_calendar_leaves_ids = fields.One2many(
        comodel_name='resource.calendar.leaves',  # Nom du modèle lié
        inverse_name='calendar_id',  # Champ sur le modèle lié pour la relation inverse
        string='Les Tâches'  # Étiquette du champ affichée dans l'interface utilisateur
    )
