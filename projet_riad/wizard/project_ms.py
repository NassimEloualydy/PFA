from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _
import base64
import xml.etree.ElementTree as ET,xmltodict
from xml.dom import minidom
from collections import OrderedDict
from datetime import datetime
import base64


class project_ms(models.TransientModel):

    _name="project.ms"

    projet_id=fields.Many2one("project.project",required=True)

    ms_project_file=fields.Binary("ms_project_file",required=True)



    def import_data(self):
        base64_data = self.ms_project_file
        
        xml_content = base64.b64decode(base64_data).decode('utf-8')
        
        # Analyser le contenu XML en un dictionnaire
        root = xmltodict.parse(xml_content)
        
        # Extraire les données du dictionnaire
        data = root
        
        # Parcourir les éléments 'Task' dans les données
        print(len(data['Project']['Tasks']['Task']))
        print("-------------")
        nbr_item_added=False
        for item in data['Project']['Tasks']['Task']:
            nbr_item_added=False
            if 'Name' in item and 'Start' in item and 'Finish' in item:
                # Extraire le nom de la tâche
                print(item['Name'])
                
                # Formater la date au format 'YYYY-MM-DD'
                date_format = '%Y-%m-%d'
                date_debut = datetime.strptime(item['Start'][:10], date_format)
                date_fin = datetime.strptime(item['Finish'][:10], date_format)
                
                # Diviser le nom de la tâche en parties
                parts = item['Name'].split(":", 1)
                
                # if len(parts) == 2:
                #     # Obtenir l'ID du tag 'Admin' s'il existe, sinon le créer
                #     tage_id = parts[0]
                #     the_name = parts[1]
                #     is_tag_admin = self.env["project.tags"].search([("name", "=", "Admin")])
                #     is_tag_chantier = self.env["project.tags"].search([("name", "=", "Installation")])
                    
                #     if not is_tag_chantier:
                #         self.env["project.tags"].create({
                #             "name": "Installation",
                #         })
                    
                #     if not is_tag_admin:
                #         self.env["project.tags"].create({
                #             "name": "Admin",
                #         })
                    
                #     id_tag_admin = self.env["project.tags"].search([("name", "=", "Admin")], limit=1).id
                #     id_tag_chantier = self.env["project.tags"].search([("name", "=", "Installation")], limit=1).id
                    
                #     user = self.env.user
                    
                #     is_exist = self.env["project.task"].search([('name', '=', the_name), ('project_id', '=', self.projet_id.id)])
                    
                #     if not is_exist:
                #         # Créer une nouvelle tâche
                #         nbr_item_added=True

                #         self.env["project.task"].create({
                #             "date_debut": str(item['Start'][:10]),
                #             "date_fin_project": str(item['Finish'][:10]),
                #             "name": the_name,
                #             "project_id": self.projet_id.id,
                #             "user_ids": [[6, False, [user.id]]],
                #             "tag_ids": [[6, False, [id_tag_admin]]] if tage_id == "Admin" else [[6, False, [id_tag_chantier]]],
                #             "stage_id": self.env["project.task.type"].search([("name", "=", "Nouvelle Tâche")], limit=1).id
                #         })
                # else:
                user = self.env.user
                is_exist = self.env["project.task"].search([('name', '=', item['Name']), ('project_id', '=', self.projet_id.id)])
                
                if not is_exist:
                    # Obtenir l'ID du tag 'Travaux' s'il existe, sinon le le créer
                    id_tag_travaux = self.env["project.tags"].search([("name", "=", "Travaux")])
                    
                    if not id_tag_travaux:
                        self.env["project.tags"].create({
                            "name": "Travaux"
                        })
                    
                    id_tag_travaux = self.env["project.tags"].search([("name", "=", "Travaux")], limit=1).id
                    #the nbrrrr
                    nbr_item_added=True
                    self.env["project.task"].create({
                        "date_debut": str(item['Start'][:10]),
                        "date_fin_project": str(item['Finish'][:10]),
                        "name": item['Name'],
                        "project_id": self.projet_id.id,
                        "user_ids": [[6, False, [user.id]]],
                        "tag_ids": [[6, False, [id_tag_travaux]]],
                        "stage_id": self.env["project.task.type"].search([("name", "=", "Nouvelle Tâche")], limit=1).id
                    })







