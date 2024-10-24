from odoo import api, fields, models


class res_partner(models.Model):
    _inherit = 'res.partner'


    convention_achat = fields.Selection(
    [('60 jours', '60 Jours'),
     ('90 jours', '90 Jours'),
     ('120 jours', '120 Jours')],
    string="Convention",
    default="60 jours")

    fichier = fields.Binary(string="Fichier")
    second_email = fields.Char(string="second_email")