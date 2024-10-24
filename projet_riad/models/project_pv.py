from odoo import models,fields,api,_
from datetime import datetime,timedelta
from odoo.exceptions import ValidationError
import ast
class project_pv(models.Model):
    _name = "project.pv"  # Nom du modèle (table dans la base de données)
    _rec_name = "nom"  # Champ qui sera utilisé comme nom enregistré (champ 'nom' dans ce cas)

    # _inherit est une liste de modèles dont ce modèle hérite
    _inherit = ['portal.mixin', 'mail.alias.mixin', 'mail.thread', 'mail.activity.mixin', 'rating.parent.mixin']

    # Champs du modèle "project.pv"
    nom = fields.Char(string="Nom", required=True, track_visibility='always')
    # Champ 'nom' de type texte (Char)
    # 'string' est le libellé du champ qui sera affiché dans l'interface utilisateur
    # 'required' indique que ce champ est obligatoire lors de la création d'un enregistrement
    # 'track_visibility' indique que les modifications de ce champ seront suivies pour la visibilité

    user_id = fields.Many2one("res.users", string="Responsable", track_visibility='always')
    # Champ 'user_id' de type Many2one (relation à un utilisateur)
    # 'string' est le libellé du champ
    # 'track_visibility' indique que les modifications de ce champ seront suivies pour la visibilité

    date_pv = fields.Datetime("Date PV", default=fields.Date.today, track_visibility='always')
    # Champ 'date_pv' de type date
    # 'default' indique la valeur par défaut (la date d'aujourd'hui)
    # 'track_visibility' indique que les modifications de ce champ seront suivies pour la visibilité

    type_pv = fields.Many2one("project.pv.type", string="Type", track_visibility='always')
    # Champ 'type_pv' de type Many2one (relation à un type de PV)
    # 'string' est le libellé du champ
    # 'track_visibility' indique que les modifications de ce champ seront suivies pour la visibilité

    type_pv_libelle = fields.Char(string="Type", related='type_pv.libelle')
    # Champ 'type_pv_libelle' de type texte (Char)
    # Il est lié au champ 'libelle' du modèle 'project.pv.type'

    projet_id = fields.Many2one("project.project", required=False, track_visibility='always')
    # Champ 'projet_id' de type Many2one (relation à un projet)
    # 'required' indique que ce champ est obligatoire lors de la création d'un enregistrement
    # 'track_visibility' indique que les modifications de ce champ seront suivies pour la visibilité

    project_tasks_ids = fields.One2many(comodel_name='project.task', inverse_name='pv_id', string='Les Tache')
    # Champ 'project_tasks_ids' de type One2many (relation à plusieurs tâches)
    # Il est lié au modèle 'project.task'

    pj = fields.Integer(string='Nombre Des Fichier', compute='_compute_nbr_attached_file')
    # Champ 'pj' de type entier (Integer)
    # Il est calculé (compute='_compute_nbr_attached_file')

    is_project_readonly = fields.Boolean(string="", default=False)
    # Champ 'is_project_readonly' de type booléen (Boolean)
    # Il a une valeur par défaut de False
    active=fields.Boolean(string="Active",default=True)
    
    is_active = fields.Char("is_active", compute="_get_is_active")

        
    def cree_tach(self):
        view_id = self.env.ref('project.view_task_form2').id
        # Obtient l'ID de la vue du formulaire de tâche

        data = self.env["project.tags"].search([("name", "=", self.type_pv.libelle)])
        # Recherche un enregistrement de modèle 'project.tags' avec le nom du type de PV

        project_tag_id = None
        if not data:
            project_tag_id = self.env["project.tags"].create({
                "name": self.type_pv.libelle
            }).id
        else:
            project_tag_id = self.env["project.tags"].search([('name', '=', self.type_pv.libelle)], limit=1).id
        # Crée un enregistrement de modèle 'project.tags' si le type de PV n'existe pas, sinon, obtient son ID

        # Définit l'action pour créer une tâche avec des champs pré-remplis
        return {
            'name': _('Créer les tâches'),  # Nom de l'action
            'type': 'ir.actions.act_window',  # Type de l'action, ouvre une fenêtre
            'view_mode': 'form',  # Mode d'affichage de la vue (formulaire)
            'res_model': 'project.task',  # Modèle cible pour la création de tâches
            'view_id': view_id,  # ID de la vue du formulaire de tâche
            'views': [(view_id, 'form')],  # Spécifie la vue à utiliser (ici, la vue de formulaire)
            'target': 'new',  # Ouvre la fenêtre dans un nouvel onglet/fenêtre
            'context': {
                'default_pv_id': self.id,  # Pré-remplit le champ PV ID avec l'ID actuel
                'default_project_id': self.projet_id.id,  # Pré-remplit le champ Project ID avec l'ID du projet actuel
                'is_shown': True,  # Indicateur pour afficher certaines informations (non utilisé dans ce contexte)
                'default_tag_ids': [project_tag_id]  # Pré-remplit le champ Tag IDs avec l'ID du tag du projet associé au type de PV
            }
            # Contexte pour pré-remplir les champs de la tâche à créer
        }

    def _compute_nbr_attached_file(self):
        for record in self:
            nombre_de_fichiers_joints = self.env["ir.attachment"].search_count([('res_id', '=', record.id), ('res_model', '=', 'project.pv')])

            # Met à jour le champ 'pj' de l'enregistrement actuel (project.pv spécifique en cours de traitement)
            # avec le nombre de fichiers joints trouvés.
            record.pj = nombre_de_fichiers_joints
    
    def _alias_get_creation_values(self):
        # Appelle la méthode '_alias_get_creation_values' du modèle parent (superclasse) pour récupérer les valeurs par défaut.
        values = super(project_pv, self)._alias_get_creation_values()

        # Définit le modèle de l'alias en tant que modèle 'project.pv' en utilisant l'ID du modèle IR correspondant.
        values['alias_model_id'] = self.env['ir.model']._get('project.pv').id

        if self.id:
            # Si l'enregistrement actuel (project.pv) possède déjà un ID, prépare des valeurs par défaut pour l'alias.
            values['alias_defaults'] = defaults = ast.literal_eval(self.alias_defaults or "{}")

            # Associe l'enregistrement actuel (project.pv en cours de traitement) à l'alias en utilisant une clé 'project_pv'.
            defaults['project_pv'] = self.id

        # Retourne les valeurs mises à jour pour la création de l'alias.
        return values

    def write(self, vals):
        # Appelle la méthode 'write' du modèle parent (superclasse) pour effectuer la mise à jour de l'enregistrement.

        # Récupère l'ID du message le plus récent associé au modèle 'project.pv'.
        id_message_posted = self.env["mail.message"].search([("model", "=", "project.pv")], order='id desc', limit=1).id

        # Récupère les valeurs de suivi mises à jour associées au message.
        values_updated = self.env["mail.tracking.value"].search([("mail_message_id", "=", id_message_posted)])

        # Initialise le corps du message.
        body_message = "PV modifié Par : <span class='fw-bolder'>"+str(self.env.user.partner_id.name)+"</span><br/>"
        if "nom" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Nom : <span class='fw-bolder'>" + str(self.nom) + "</span> à <span class='fw-bolder'>" + str(vals["nom"]) + "</span> <br/> "

        # else:
        #     body_message += "&nbsp;&nbsp;&nbsp; Nom  :  <br/> "
        if "user_id" in vals:
            # body_message += "&nbsp;&nbsp;&nbsp; Responsable  : " + str(self.user_id.partner_id.name) + " <" + str(pv.user_id.login) + "> <br/> "
            body_message += "&nbsp;&nbsp;&nbsp; Responsable : <span class='fw-bolder'>" + str(self.user_id.partner_id.name) + "</span> à <span class='fw-bolder'>" + str(self.env["res.users"].search([("id","=",vals["user_id"])],limit=1).partner_id.name) + "</span> <br/> "

        # else:
        #     body_message += "&nbsp;&nbsp;&nbsp; Responsable  : <br/> "
        if "date_pv" in vals:
            month_translation = {
    'january': 'janvier',
    'february': 'février',
    'march': 'mars',
    'april': 'avril',
    'may': 'mai',
    'june': 'juin',
    'july': 'juillet',
    'august': 'août',
    'september': 'septembre',
    'october': 'octobre',
    'november': 'novembre',
    'december': 'décembre'
}                   
            day_translation = {
    'Monday': 'lundi',
    'Tuesday': 'mardi',
    'Wednesday': 'mercredi',
    'Thursday': 'jeudi',
    'Friday': 'vendredi',
    'Saturday': 'samedi',
    'Sunday': 'dimanche'
}               
            #the new date updated
            date = datetime(int(str(vals["date_pv"])[0]+str(vals["date_pv"])[1]+str(vals["date_pv"])[2]+str(vals["date_pv"])[3]), int(str(vals["date_pv"])[5]+str(vals["date_pv"])[6]),int(str(vals["date_pv"])[8]+str(vals["date_pv"])[9]))
            formatted_date = date.strftime('%d , %B , %Y').lower()
            day_name = date.strftime('%A')
            day, month, year = formatted_date.split(' , ')
            # Translate the month to French and capitalize the first letter
            
            month_french = month_translation[month].capitalize()
            day_french = day_translation[day_name].capitalize()
            # Combine the day, translated month, and year
            new_formatted_date_french = f'{day_french} {day} {month_french} {year}'

            #the old date updated
            date = datetime(int(str(self.date_pv)[0]+str(self.date_pv)[1]+str(self.date_pv)[2]+str(self.date_pv)[3]), int(str(self.date_pv)[5]+str(self.date_pv)[6]),int(str(self.date_pv)[8]+str(self.date_pv)[9]))
            formatted_date = date.strftime('%d , %B , %Y').lower()
            day_name = date.strftime('%A')
            day, month, year = formatted_date.split(' , ')
            # Translate the month to French and capitalize the first letter
            
            month_french = month_translation[month].capitalize()
            day_french = day_translation[day_name].capitalize()
            # Combine the day, translated month, and year
            old_formatted_date_french = f'{day_french} {day}  {month_french}  {year}'


            body_message += "&nbsp;&nbsp;&nbsp; Date PV : <span class='fw-bolder'>" + str(old_formatted_date_french) + "</span> à <span class='fw-bolder'>" + str(new_formatted_date_french) + "</span> <br/> "
            
        # else:
        #     body_message += "&nbsp;&nbsp;&nbsp; Date PV  :  <br/> "
        if "type_pv" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Type : <span class='fw-bolder'>" + str(self.type_pv) + "</span> à <span class='fw-bolder'>" + str(vals["type_pv"]) + "</span> <br/> "

        pv = super(project_pv, self).write(vals)

        # Vérifie s'il existe un type d'événement de calendrier nommé "PV".
        # is_project_pv_exist = self.env["calendar.event.type"].search([("name", "=", "PV")])
        # if not is_project_pv_exist:
        #     # S'il n'existe pas, crée un nouveau type d'événement "PV".
        #     self.env["calendar.event.type"].create({
        #         "name": "PV"
        #     })

        # Si des valeurs de suivi ont été mises à jour, traite les champs spécifiques.
        # if len(values_updated) != 0:
        #     for rec in values_updated:
        #         if rec.field.name in ["nom", "user_id", "date_pv", "projet_id"]:
        #             # Met à jour un événement de calendrier associé aux champs spécifiques.

        #             calendar_event = self.env["calendar.event"].search([
        #                 ("res_id", "=", self.id),
        #                 ("res_model_id", "=", self.env['ir.model'].search([('model', '=', 'project.pv')], limit=1).id)
        #             ], limit=1)

        #             # Met à jour l'enregistrement de l'événement de calendrier associé au PV
        #             # calendar_event.write({
        #             #     # Met à jour l'ID de l'utilisateur associé à l'événement de calendrier
        #             #     'user_id': self.user_id.id,

        #             #     # Met à jour la catégorie de l'événement de calendrier en recherchant un type d'événement de calendrier nommé "PV"
        #             #     # et en utilisant son ID
        #             #     'categ_ids': [[6, False, [self.env["calendar.event.type"].search([("name", "=", "PV")], limit=1).id]]],

        #             #     # Met à jour le nom de l'événement de calendrier en ajoutant "PV : " suivi du nom de l'enregistrement 'project.pv'
        #             #     'name': "PV : " + str(self.nom),

        #             #     # Met à jour la date de début de l'événement de calendrier en convertissant la date du champ 'date_pv' de 'project.pv'
        #             #     # en format de date
        #             #     'start': datetime.strptime(str(self.date_pv), "%Y-%m-%d"),

        #             #     # Met à jour la description de l'événement de calendrier en incluant le nom de l'enregistrement 'project.pv' et la date de création
        #             #     'description': "Un PV avec le nom : " + str(self.nom) + ", créé en " + str(self.date_pv) + ": ",

        #             #     # Met à jour la liste des partenaires associés à l'événement de calendrier en utilisant l'ID du partenaire de l'utilisateur de 'project.pv'
        #             #     'partner_ids': [[6, False, [self.user_id.partner_id.id]]],

        #             #     # Met à jour la durée de l'événement de calendrier en définissant une durée de 1 (peut être modifiée en fonction de vos besoins)
        #             #     'duration': 1,

        #             #     # Met à jour la date de création de l'événement de calendrier avec la date et l'heure actuelles
        #             #     "create_date": datetime.now()
        #             # })

        #         if rec.field.field_description == "Date PV":
        #             body_message += "&nbsp;&nbsp;&nbsp; " + str(rec.field.field_description) + " : <span class='fw-bolder'>" + str(rec.old_value_datetime) + "</span> à <span class='fw-bolder'>" + str(rec.new_value_datetime) + "</span> <br/> "
        #         else:
        #             body_message += "&nbsp;&nbsp;&nbsp; " + str(rec.field.field_description) + " : <span class='fw-bolder'>" + str(rec.old_value_char) + "</span> à <span class='fw-bolder'>" + str(rec.new_value_char) + "</span> <br/> "

        user = self.env.user
        # Crée un nouveau message de type "comment" pour enregistrer les modifications du PV
        self.env["mail.message"].create({

            "body": body_message,  # Le corps du message contenant les détails des modifications

            'email_from': '"' + user.partner_id.name + '" <' + user.login + '>',  # L'expéditeur du message

            'message_type': 'comment',  # Type de message (commentaire)

            'subtype_id': 1,  # ID du sous-type de message (généralement utilisé pour les commentaires)

            'subject': False,  # Sujet du message (dans ce cas, non spécifié)

            'model': 'mail.channel',  # Modèle lié au message (mail.channel)

            'res_id': self.projet_id.channel_id.id,

            'record_name': 'Chantier',  # Nom du record associé (dans ce cas, "Chantier")

        })
        # Retourne le résultat de la mise à jour de l'enregistrement PV.
        return pv

    @api.model
    # Crée un nouveau PV en utilisant la méthode create de la classe parente
    def create(self, vals):
        pv = super(project_pv, self).create(vals)

        # Vérifie si un canal de discussion "Chantier" existe, sinon le crée
        # is_channel_chantier_exist = self.env["mail.channel"].search([("name", "=", "Chantier"), ("channel_type", "=", "channel")])
        # if not is_channel_chantier_exist:
        #     self.env["mail.channel"].create({
        #         "name": "Chantier",
        #         "channel_type": "channel"
        #     })

        # Crée un message pour enregistrer la création du PV
        body_message = "PV créé Par : <span class='fw-bolder'>"+str(self.env.user.partner_id.name)+"</span><br/>"
        if "nom" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Nom  : <span class='fw-bolder'>" + str(vals["nom"]) + "  </span><br/> "
        # else:
        #     body_message += "&nbsp;&nbsp;&nbsp; Nom  :   </span><br/> "
        if "user_id" in vals and pv.user_id.partner_id.name!=False:
            body_message += "&nbsp;&nbsp;&nbsp; Responsable  : <span class='fw-bolder'>" + str(pv.user_id.partner_id.name) + " <" + str(pv.user_id.login) + ">  </span><br/> "
        # else:
        #     body_message += "&nbsp;&nbsp;&nbsp; Responsable  :  </span><br/> "
        if "date_pv" in vals:
            month_translation = {
    'january': 'janvier',
    'february': 'février',
    'march': 'mars',
    'april': 'avril',
    'may': 'mai',
    'june': 'juin',
    'july': 'juillet',
    'august': 'août',
    'september': 'septembre',
    'october': 'octobre',
    'november': 'novembre',
    'december': 'décembre'
}                   
            day_translation = {
    'Monday': 'lundi',
    'Tuesday': 'mardi',
    'Wednesday': 'mercredi',
    'Thursday': 'jeudi',
    'Friday': 'vendredi',
    'Saturday': 'samedi',
    'Sunday': 'dimanche'
}
            date = datetime(int(str(vals["date_pv"])[0]+str(vals["date_pv"])[1]+str(vals["date_pv"])[2]+str(vals["date_pv"])[3]), int(str(vals["date_pv"])[5]+str(vals["date_pv"])[6]),int(str(vals["date_pv"])[8]+str(vals["date_pv"])[9]))
            formatted_date = date.strftime('%d , %B , %Y').lower()
            day_name = date.strftime('%A')
            day, month, year = formatted_date.split(' , ')
            # Translate the month to French and capitalize the first letter
            
            month_french = month_translation[month].capitalize()
            day_french = day_translation[day_name].capitalize()
            # Combine the day, translated month, and year
            formatted_date_french = f'{day_french} {day}  {month_french}  {year}'
            body_message += "&nbsp;&nbsp;&nbsp; Date PV  : <span class='fw-bolder'>" + str(formatted_date_french) + "  </span><br/> "
        # else:
        #     body_message += "&nbsp;&nbsp;&nbsp; Date PV  :   </span><br/> "
        if "type_pv" in vals and pv.type_pv_libelle!=False:
            body_message += "&nbsp;&nbsp;&nbsp; Type  : <span class='fw-bolder'>" + str(pv.type_pv_libelle) + "  </span><br/> "
        # else:
        #     body_message += "&nbsp;&nbsp;&nbsp; Type  :  <br/> "
        # if pv.projet_id.name:
        #     body_message += "&nbsp;&nbsp;&nbsp; Projet  : " + str(pv.projet_id.name) + " <br/> "
        # else:
        #     body_message += "&nbsp;&nbsp;&nbsp; Projet  :  <br/> "

        # Vérifie si le type "PV" existe dans les événements du calendrier, sinon le crée
        is_prject_pv_exist = self.env["calendar.event.type"].search([("name","=", "PV")])
        if not is_prject_pv_exist:
            self.env["calendar.event.type"].create({
                "name": "PV"
            })

        # Crée un message pour les abonnés du projet
        user = self.env.user
        self.env["mail.message"].create({
            "body": body_message,
            'email_from': '"' + user.partner_id.name + '" <' + user.login + '>',
            'message_type': 'comment',
            'subtype_id': 1,
            'subject': False,
            'model': 'mail.channel',
            'res_id': pv.projet_id.channel_id.id,
            'record_name': 'Chantier',
        })

        # Obtenir les abonnés du projet
        users_project = self.env["mail.followers"].sudo().search([('res_id', '=', pv.projet_id.id),
                                                                 ('res_model', '=', 'project.project')])

        if users_project:
            for f in users_project:
                o1 = self.env["res.users"].sudo().search([('partner_id', '=', f.partner_id.id)], limit=1)

                # Crée un message pour chaque abonné du projet
                if self.env["mail.wizard.invite"].search_count(
                        [('res_model', '=', 'project.pv'), ('message', '=', "Vous avez invité au PV " + vals['nom']),
                         ('res_id', '=', pv.id)]) == 0:
                    self.env["mail.wizard.invite"].create({
                        "res_id": pv.id,
                        "res_model": "project.pv",
                        "message": "Vous avez invité au PV " + vals["nom"],
                    })

                # Crée des abonnés pour le PV et le partenaire associé
                filter_data = self.env["mail.followers"].sudo().search(
                    [('res_id', '=', pv.id), ('partner_id', '=', o1.partner_id.id), ('res_model', '=', "project.pv")])
                if not filter_data and o1.partner_id.id!=False:                    
                    self.env["mail.followers"].sudo().with_context(mail_create_nosubscribe=True).create({
                        "res_id": pv.id,
                        "partner_id": o1.partner_id.id,
                        "res_model": "project.pv"
                    })

                filter_data = self.env["mail.followers"].sudo().search(
                    [('res_id', '=', pv.user_id.partner_id.id), ('partner_id', '=', o1.partner_id.id), ('res_model', '=', "res.partner")])
                if not filter_data:

                    if pv.user_id.partner_id.id!=0 and o1.partner_id.id:
                      self.env["mail.followers"].sudo().with_context(mail_create_nosubscribe=True).create({
                          "res_id": pv.user_id.partner_id.id,
                          "partner_id": o1.partner_id.id,
                          "res_model": "res.partner"
                      })

        return pv  # Retourne le PV créé
    def add_active_in_menu(self):
       for rec in self:
          rec.active=False
    def _get_is_active(self):
        # Cette fonction met à jour le champ 'is_active' pour indiquer si l'enregistrement est archivé ou non.
        # Si l'enregistrement est actif (non archivé), 'is_active' est défini sur "Archive".
        # Si l'enregistrement n'est pas actif, 'is_active' est défini sur "Désarchiver".

        for rec in self:
            rec.is_active = "Archive" if rec.active == True else "Désarchiver"
        # @api.model
    def archive_action_function(self):
        # Cette fonction est conçue pour basculer l'état d'archivage de l'enregistrement
        # et mettre à jour le champ 'is_active' pour indiquer si l'enregistrement est archivé ou non.

        # Vérifiez si l'enregistrement est actuellement actif (non archivé).
        # S'il est actif, définissez 'is_active' sur "Archiver", indiquant l'archivage.
        # S'il n'est pas actif, définissez 'is_active' sur "Désarchiver", indiquant la désactivation de l'archivage.
        self.is_active = "Archiver" if self.active == True else "Désarchiver"

        # Basculez le champ 'active' en le passant de True à False, ou vice versa.
        self.active = not self.active
