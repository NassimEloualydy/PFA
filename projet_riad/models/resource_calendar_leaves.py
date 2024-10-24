from odoo import models,fields,api,_
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta


class resource_calendar_leaves(models.Model):
    _inherit="resource.calendar.leaves"
    # Champ personnalisé pour stocker le total des arrêts (en heures)
    totale_des_arret = fields.Integer(string="Totale des arrêts", compute="_get_hours_between_date_from_then_date_to")
    
    # Champ pour le fishier d'order de arrêt
    order_arret_file = fields.Binary("order_arret_file")

    # Champ pour le fishier d'order de service
    order_reprise_file = fields.Binary("order_reprise_file")

    @api.depends('date_from', 'date_to')
    def _get_hours_between_date_from_then_date_to(self):
        for rec in self:
            if rec.date_from and rec.date_to:
                # Calculer la durée en jours entre les dates date_from et date_to
                rec.totale_des_arret = int((rec.date_to - rec.date_from).days)
            else:
                rec.totale_des_arret = 0  # Aucune durée si l'une des dates est manquante

