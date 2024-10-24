from odoo import models,fields,api,_
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

class purchase_order(models.Model):
    _inherit = "purchase.order"  # Héritage du modèle "purchase.order"

    # Champ personnalisé pour stocker l'email du projet
    email_project = fields.Char(string="Choisissez l'email du projet")
    