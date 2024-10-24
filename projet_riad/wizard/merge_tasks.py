from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _
import base64
import xml.etree.ElementTree as ET,xmltodict
from xml.dom import minidom
from collections import OrderedDict
from datetime import datetime
import base64
from odoo.exceptions import ValidationError


class merge_task(models.TransientModel):

    _name="merge.task"
    tasks = fields.Many2many(
    'project.task',
    string='Choisir Une Tâche',
    # domain=['|', ('active', '=', False), ('active', '=', True)],
    # default=lambda self: self._get_default_taxes_ids()
    # default=[[6,0,[104]]]
    )
    task_one=fields.Many2one("project.task","task_one")
    task_tow=fields.Many2one("project.task","task_tow")
    def merge(self):
        if len(self.tasks)==1:
            task_choosen=self.task_one if self.task_one in self.tasks else self.task_tow
            task_notchoosen=self.task_one if self.task_one not in self.tasks else self.task_tow
            users=task_choosen.user_ids.ids
            tags=task_choosen.tag_ids.ids

            self.env["ir.attachment"].search([("res_model","=","project.task"),("res_id","=",task_notchoosen.id)]).write({
                "res_id":task_choosen.id,                
            })
            for rec in task_notchoosen.user_ids.ids:
                if rec not in users:
                    users.append(rec)
            
            for rec in task_notchoosen.tag_ids.ids:
                if rec not in tags:
                    tags.append(rec)
            
            self.env["project.task"].sudo().search([("id","=",task_choosen.id)],limit=1).sudo().write({
                "user_ids":[[6,False,users]],
                "tag_ids":[[6,False,tags]],
                "nbr_field_attached":self.env["ir.attachment"].search_count([("res_id","=",task_choosen.id),("res_model","=","project.task")])
            })

            self.env["project.task"].sudo().search([("id","=",task_notchoosen.id)],limit=1).sudo().unlink()
            

        else:
            raise ValidationError(_("SVP Choisissez une seule tâche"))

        

