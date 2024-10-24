from odoo import models,fields,api,_
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta



class crossovered_budget(models.Model):
    # Héritage du modèle "crossovered.budget"
    _inherit = "crossovered.budget"
    
    # Ajout d'un champ "project_id" de type many2one (Many2one) lié au modèle "project.project"
    project_id = fields.Many2one("project.project")
    
    # Ajout d'un champ "budget_lines" de type one2many (One2many) lié au modèle "crossovered.budget.lines"
    # Ce champ permet d'établir une relation entre les budgets et les lignes de budget associées.
    budget_lines = fields.One2many(comodel_name="crossovered.budget.lines", inverse_name="crossovered_budget_id", string="budget_line_ids")


