""" 
    we inherit this model in order , to add a project to the ir_attachment 
    for access rules, also we create message in the channel if the file 
    is created in the taks or in the project    
"""
from odoo import models,fields,api,_,SUPERUSER_ID
from odoo.exceptions import ValidationError

from datetime import datetime,timedelta
import re
from odoo.exceptions import AccessError, MissingError, UserError
from odoo.tools import consteq

class ir_attachment(models.Model):
    _inherit="ir.attachment"
    
    documents_folder_id=fields.Many2one("documents.folder",store=True)
    projet_id = fields.Many2one("project.project")

    # if the user connected belong to the Project Admin Group 
    # then he had permession to delete otherwise no
    def unlink(self):
        if self.env.user.has_group('project.group_project_manager') or self.create_date==False:
            product=super(ir_attachment, self).unlink()        
            
            return product
        else:
            
            raise ValidationError(_("Vous n'êtes pas autorisé à supprimer des fichiers ?"))

    
    @api.model
    def create(self, vals):
        # Crée une pièce jointe en utilisant la méthode create de la classe parente (superclasse)
        attachment = super(ir_attachment, self).create(vals)
        # Obtient l'utilisateur actuel
        user = self.env.user
        # Vérifie si la clé "res_model" est présente dans les valeurs
        if "res_model" in vals:
            # Recherche du modèle associé à l'ID spécifié
            modele = self.env[vals["res_model"]].search([("id", "=", vals["res_id"])], limit=1)
            if modele:
                # Recherche du nom du modèle à partir de la table "ir.model"
                label_of_the_model = self.env["ir.model"].search([("model", "=", vals["res_model"])], limit=1)
                name_modele = ""
                # Détermine le nom du modèle en fonction de "res_model"
                if vals["res_model"] == "mail.compose.message":
                    name_modele = ""
                elif vals["res_model"] == "project.pv":
                    name_modele = modele.nom
                elif vals["res_model"] == "project.ms":
                    name_modele = "Tâche"
                elif vals["res_model"] != "mail.compose.message":
                    name_modele = modele.name
                if vals["res_model"] == "project.project":
                    # Recherche de l'ID du projet de la tâche
                    id_project_task = self.env["documents.document"].search([("attachment_id", "=", attachment.id)], order="id desc", limit=1).res_id
                    id_project_task = vals["res_id"] 
                    # Recherche du document associé à la pièce jointe
                    document = self.env["documents.document"].search([("attachment_id", "=", attachment.id)], order="id desc", limit=1)
                    if document:
                    # Obtient le projet
                        project = self.env["project.project"].search([("id", "=", id_project_task)], limit=1)
                        # Recherche de l'ID du dossier parent
                        # if project.documents_folder_id.id==False:
                        parent_folder = project.documents_folder_id
                        # Nom du sous-dossier : "Taches photos"
                        sub_folder = self.env["documents.folder"].search([("name", "like", "Photos et Taches%"), ("parent_folder_id", "=", parent_folder.id)], limit=1)
                        query="UPDATE documents_document set project_id=%s,folder_id=%s where id=%s"
                        self.env.cr.execute(query, (project.id,parent_folder.id, document.id))
                if vals["res_model"] == "project.task":
                    # Recherche de l'ID du projet de la tâche
                    id_project_task = self.env["documents.document"].search([("attachment_id", "=", attachment.id)], order="id desc", limit=1).res_id
                    # Recherche du document associé à la pièce jointe
                    document = self.env["documents.document"].search([("attachment_id", "=", attachment.id)], order="id desc", limit=1)
                    # Obtient le projet
                    task = self.env["project.task"].search([("id", "=", id_project_task)], limit=1)
                    query = "UPDATE PROJECT_TASK SET nbr_field_attached=%s WHERE ID=%s"
                    self.env.cr.execute(query, (self.env["ir.attachment"].sudo().search_count([('res_id', '=', task.id), ("res_model", "=", "project.task")]),task.id))
                    # Recherche de l'ID du dossier parent
                    parent_folder = self.env["documents.folder"].search([("name", "like", str(task.project_id.name)+'%')], limit=1)
                    # Nom du sous-dossier : "Taches photos"
                    sub_folder = self.env["documents.folder"].search([("name", "like", "Photos et Taches%"), ("parent_folder_id", "=", task.project_id.documents_folder_id.id)], limit=1)
                    # Obtenire le nombre de fishier 
                    number_of_files=self.env["documents.document"].search_count([("folder_id","=",sub_folder.id)])
                    attachment.write({
                        "documents_folder_id":sub_folder.id
                    })
                    document.write({
                        "folder_id": sub_folder.id,
                        "project_id":task.project_id.id

                    })
                    # parent_folder = self.env["documents.folder"].search([("id", "=", project.documents_folder_id.id)], limit=1)
                    sub_folder.write({
                        "name":"Photos et Taches "
                    })
                # Crée un message pour notifier l'ajout de fichier
                body_message = "Un nouveau fichier a été ajouté par <span class='fw-bolder'>"+str(self.env.user.partner_id.name)+"</span> sur le <span class='fw-bolder'>" + str(label_of_the_model.name) + "</span> : <span class='fw-bolder'>" + str(name_modele) + "</span>"
                if label_of_the_model.name=="project.pv":
                    body_message = "Un nouveau fichier a été ajouté par <span class='fw-bolder'>"+str(self.env.user.partner_id.name)+"</span> sur le <span class='fw-bolder'> PV </span> : <span class='fw-bolder'>" + str(name_modele) + "</span>"
                channel_id = None
                # Détermine le canal de messagerie en fonction de "res_model"
                if vals["res_model"] in ["project.task"]:
                    project_id=self.with_context(lang='fr_FR').env["project.task"].search([("id","=",vals["res_id"])],limit=1).project_id
                    channel_id = project_id.channel_id.id
                if vals["res_model"] in ["project.project"]:
                    project_id=self.with_context(lang='fr_FR').env["project.project"].search([("id","=",vals["res_id"])],limit=1)
                    if project_id:
                        channel_id =project_id.channel_id.id
                if vals["res_model"] in ["project.pv"]:
                    project_id=self.with_context(lang='fr_FR').env["project.project"].search([("id","=",self.env["project.pv"].search([("id","=",vals["res_id"])],limit=1).projet_id.id)],limit=1)
                    channel_id =project_id.channel_id.id 
                # Crée un message pour notifier l'ajout de fichier
                if channel_id:
                    self.env["mail.message"].create({
                    "body": body_message,
                    'email_from': '"' + user.partner_id.name + '" <' + user.login + '>',
                    'message_type': 'comment',
                    'subtype_id': 1,
                    'subject': False,
                    'model': 'mail.channel',
                    'attachment_ids': [[6, False, [attachment.id]]],
                    'res_id': channel_id,
                    'record_name': 'Chantier',
                })
        return attachment
