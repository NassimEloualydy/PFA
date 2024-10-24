from odoo import models,fields,api,_
from datetime import datetime,timedelta,date
from odoo.exceptions import ValidationError
import ast

# import win32com.client

class project_task(models.Model):
    _inherit="project.task"

    # add_in_calendar=fields.Boolean(string="Add In G-Calendar Event	",widget='radio')
    
    # Identificateur de devise pour les champs montants
    currency_id = fields.Many2one('res.currency', string='Currency')

    # Champs pour le revenu, dépenses et marge, avec suivi de la devise
    revenu = fields.Monetary(string="Revenu", currency_field="currency_id", track_visibility='always')
    depense = fields.Monetary(string="Dépense", currency_field="currency_id", track_visibility='always')
    marge = fields.Monetary(string="Marge", currency_field="currency_id", track_visibility='always')

    # Date de début du projet (obligatoire) et date de fin (optionnelle)
    date_debut = fields.Date(string="Date de début", required=True, track_visibility='always')
    date_fin_project = fields.Date(string="Date de fin", required=False, track_visibility='always')

    # Champ calculé pour la durée de la tâche
    duree_de_tach = fields.Char(string='Durée de tâche', compute='_comput_duree_de_tach', track_visibility='always',store="true")

    # Champ calculé pour l'échéance/fin
    echance_fin = fields.Char(string='Echéance / Fin', compute='_comput_echance_fin', track_visibility='always',store=True)

    # Quantité planifiée et temps de travail enregistré
    qte_planifier = fields.Integer(string='Quantité planifiées', track_visibility='always')
    temp_de_travail_enrgistrer = fields.Integer(string='Temps de Travail Enregistré', track_visibility='always')

    # Lien vers le projet PV associé
    pv_id = fields.Many2one("project.pv")

    # Nom du PV lié (champ calculé)
    nom_pv = fields.Char("PV", related="pv_id.nom", track_visibility='always')

    # Libellé du type de PV lié (champ calculé)
    type_pv_libelle = fields.Char("type_pv_libelle", related='pv_id.type_pv_libelle')

    # Identificateur du type de PV lié
    type_pv_id = fields.Many2one("roject.pv.type", "type_pv_libelle", related='pv_id.type_pv')

    # Champ booléen pour l'affichage
    is_shown = fields.Boolean(string="is_shown", default=False)

    # Date de début du calendrier
    date_start_calendar = fields.Datetime("date_start_calendar")

    # Calcul du delta entre la date de début et la date de fin
    delta_date_debut = fields.Integer(compute='_get_delta_date_debut', string=u'date debut', default=0)
    delta_date_fin = fields.Integer(compute='_get_delta_date_fin', string=u'date fin', default=0)

    # Messages pour le delta entre la date de début et la date de fin
    message_delta_date_debut = fields.Char(string="", default="")
    message_delta_date_fin = fields.Char(string="", default="")

    # Nombre de fichiers attachés
    nbr_field_attached = fields.Integer(string='Nombre Des Fichier', compute='_compute_nbr_attached_file',store=True)
    nbr_file_attached = fields.Integer(string='Nombre Des Fichier')
    
    # Champ booléen pour la lecture seule du projet
    is_project_readonly = fields.Boolean(string="", default=False)

    # Champ pour l'état actif (champ calculé)
    is_active = fields.Char("is_active", compute="_get_is_active")

    # Nom du projet lié (champ calculé)
    name_of_the_project = fields.Char(related="project_id.name", string="")
    
    #user_id field
    user_id=fields.Many2one("res.users","Assigné à")
    tag_id=fields.Many2one("project.tags","tag_id")
    project_id_name=fields.Char(related='project_id.name',store=True)
    is_mes_tach_suivi=fields.Selection([
        ('suived','Tâches suivies'),
        ('unsuived','Tâches Non Suivies'),
        ('assigned','Assignées'),
    ],store=True,string="Mes Tâches",track_visibility='always')
    in_15_days=fields.Integer("in_15_days")
    unread_messages=fields.Boolean("unread_messages");
    nbr_message_partner_ids=fields.Integer("nbr_message_partner_ids")
    rec_id=fields.Integer("rec_id")
    user_tobe_filter_is=fields.Many2one("res.users","user_tobe_filter_is")

    # message_is_follower=fields.Boolean("Est un abonné",store=True,compute="_get_message_is_follower")

    @api.depends('message_partner_ids','user_ids','user_id')
    @api.onchange('message_partner_ids')
    def get_message_is_follower(self):
        user = self.env.userA
        for rec in self:
            if len(rec.user_ids.ids)>0:
                if  user.id in rec.user_ids.ids:
                    rec.is_mes_tach_suivi="assigned"
                    query = "UPDATE PROJECT_TASK SET is_mes_tach_suivi=%s WHERE ID=%s"
                    self.env.cr.execute(query, ("assigned",rec.id))
                if user.partner_id.id in rec.message_partner_ids.ids or user.id in rec.user_ids.ids:
                    rec.is_mes_tach_suivi="suived"
                    query = "UPDATE PROJECT_TASK SET is_mes_tach_suivi=%s WHERE ID=%s"
                    self.env.cr.execute(query, ("suived",rec.id))
                else:
                    query = "UPDATE PROJECT_TASK SET is_mes_tach_suivi=%s WHERE ID=%s"
                    self.env.cr.execute(query, ("suived",rec.id))

                    # rec.message_is_follower=False
                # rec.nbr_message_partner_ids=len(rec.message_partner_ids)
            # # if user.id in self.fol
            # print(user.partner_id.id)
            # print(rec.message_partner_ids)
            # print("---")
    # # def _get_name_project(self):
    #     project=self.env["project.task"].search([])
    #     for rec in project:          
    #         rec.project_id_name=rec.project_id_name[:60]

    # Add a related Many2many field to the same model

    def archive_action_function(self):
        # Cette fonction est conçue pour basculer l'état d'archivage de l'enregistrement
        # et mettre à jour le champ 'is_active' pour indiquer si l'enregistrement est archivé ou non.
        # Vérifiez si l'enregistrement est actuellement actif (non archivé).
        # S'il est actif, définissez 'is_active' sur "Archiver", indiquant l'archivage.
        # S'il n'est pas actif, définissez 'is_active' sur "Désarchiver", indiquant la désactivation de l'archivage.
        self.is_active = "Archiver" if self.active == True else "Désarchiver"

        # Basculez le champ 'active' en le passant de True à False, ou vice versa.
        self.active = not self.active

    def _get_is_active(self):
        for rec in self:
            rec.is_active = "Archiver" if rec.active == True else "Désarchiver"
        # @api.model

    def archivetask(self):
        # Cette fonction est conçue pour archiver toutes les tâches dont l'étape est "Tâche Accomplie".
        # Elle recherche toutes les tâches et désactive celles dont l'étape est "Tâche Accomplie".

        tasks = self.env["project.task"].sudo().search([])  # Recherche de toutes les tâches
        
        for rec in tasks:
            print(rec.stage_id.name)
            if rec.stage_id.name == "Tâche Accomplie" or  rec.stage_id.name == "Tâche Annulée": # Vérifie si l'étape de la tâche est "Tâche Accomplie"
                rec.sudo().write({
                    "active":False
                })
                # rec.active = False  # Désactive la tâche en la marquant comme inactive

    def notifuserfortasks(self):
        # Cette fonction a pour but de notifier les utilisateurs concernant les tâches.
        # Elle recherche toutes les tâches et envoie des notifications aux utilisateurs si certaines conditions sont remplies.        
        tasks = self.env["project.task"].search([])  # Recherche de toutes les tâches
        for rec in tasks:
            # Notification pour les tâches ayant une date de fin projet
            if rec.date_fin_project:
                target_date = datetime.strptime(str(rec.date_fin_project), "%Y-%m-%d")  # Date de fin projet
                current_date = datetime.now()  # Date actuelle
                delta = target_date - current_date  # Calcul de la différence entre la date cible et la date actuelle
                days_remaining = delta.days  # Nombre de jours restants jusqu'à la date cible
                days_remaining = days_remaining + 1  # Ajout d'un jour car 'delta' ne tient pas compte de la date actuelle
                           
            if rec.date_fin_project:
                target_date = datetime.strptime(str(rec.date_fin_project), "%Y-%m-%d")  # Date de début
                current_date = datetime.now()  # Date actuelle
                delta = target_date - current_date  # Calcul de la différence entre la date cible et la date actuelle
                days_remaining = delta.days  # Nombre de jours restants jusqu'à la date cible
                days_remaining = days_remaining + 1  # Ajout d'un jour car 'delta' ne tient pas compte de la date actuelle
                
                if days_remaining == 3:
                    # Création d'un message de notification
                    partnsers=""
                    for p in rec.user_ids:
                        partnsers+=str(p.partner_id.name)+" ,"   
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
                    
                    date = datetime(int(str(rec.date_debut)[0]+str(rec.date_debut)[1]+str(rec.date_debut)[2]+str(rec.date_debut)[3]), int(str(rec.date_debut)[5]+str(rec.date_debut)[6]),int(str(rec.date_debut)[8]+str(rec.date_debut)[9]))
                    formatted_date = date.strftime('%d , %B , %Y').lower()
                    day_name = date.strftime('%A')
                    day, month, year = formatted_date.split(' , ')
                    # Translate the month to French and capitalize the first letter
                    
                    month_french = month_translation[month].capitalize()
                    day_french = day_translation[day_name].capitalize()
                    # Combine the day, translated month, and year
                    formatted_date_french = f'{day} , {day_french} , {month_french} , {year}'
                    formatted_date_french_end=""
                    if rec.date_fin_project!=False:
                        date_end = datetime(int(str(rec.date_fin_project)[0]+str(rec.date_fin_project)[1]+str(rec.date_fin_project)[2]+str(rec.date_fin_project)[3]), int(str(rec.date_fin_project)[5]+str(rec.date_fin_project)[6]),int(str(rec.date_fin_project)[8]+str(rec.date_fin_project)[9]))
                        formatted_date_end = date_end.strftime('%d , %B , %Y').lower()
                        day_name = date_end.strftime('%A')
                        day_end, month_end, year_end = formatted_date_end.split(' , ')
    
                        day_french_end = day_translation[day_name].capitalize()
                        month_french_end = month_translation[month_end].capitalize()
                        formatted_date_french_end = f'{day_end} , {day_french_end} , {month_french_end} , {year_end}'

                    body_message = "<span class='fw-bolder text-danger'> Rappel<br/></span>"
                    body_message += "Tâche : <span class='fw-bolder'>" + rec.name + "</span><br/>"
                    body_message += "Assigné à : <span class='fw-bolder'>" + str(partnsers) + "</span><br/>"            
                    body_message += "État : <span class='fw-bolder'>" + str(rec.stage_id.name) + "</span><br/>"
                    body_message += "Date de début : <span class='fw-bolder'>" + formatted_date_french + "</span><br/>"
                    body_message += "Date de fin : <span class='fw-bolder text-danger'>" + formatted_date_french_end + "</span><br/>"
                    body_message += "Durée de tâche : <span class='fw-bolder text-danger'>" + str(rec.duree_de_tach) + "</span><br/>"
                    # body_message += "Il ne reste que 3 jours pour que cette tâche puisse commencer"
                    body_message += "<span class='fw-bolder text-danger'> Il reste 3 Jours pour la fin de cette Tache. </span>"

                    user = self.env.user
                    # Création du message dans le système de messagerie
                    self.env["mail.message"].create({
                        "body": body_message,
                        'email_from': '"' + user.partner_id.name + '" <' + user.login + '>',
                        'message_type': 'comment',
                        'subtype_id': 1,
                        'subject': False,
                        'model': 'mail.channel',
                        'res_id':rec.project_id.channel_id.id,
                        'record_name': 'Chantier',
                    })
    def write(self, vals):
 
        #referec the calendar event 
        if "name" in vals:
            for rec in self.env["project.task"].search([("active","=",False)]):
                partner_ids = [[6, False, []]]
                for p in rec.user_ids:
                    partner_id = self.env["res.users"].search([("id","=",p.id)], limit=1).partner_id.id
                    partner_ids[0][2].append(partner_id)
                    self.env["calendar.event"].search([("res_model_id","=",self.env['ir.model'].search([('model','=','project.task')],limit=1).id),("res_id","=",rec.id)], limit=1).write({
                        'partner_ids': partner_ids,
                        'active':False
                    })


            #end
        partner_ids = [[6, False, []]]

        if 'user_ids' in vals:
            if len(vals['user_ids'][0][2]) > 0:
                for rec in vals['user_ids'][0][2]:
                    partner_id = self.env["res.users"].search([("id","=",rec)], limit=1).partner_id.id
                    partner_ids[0][2].append(partner_id)
                vals["description"]=" the id of the cevent "+str(self.env["calendar.event"].search([("res_model_id","=",self.env['ir.model'].search([('model','=','project.task')],limit=1).id),("res_id","=",self.id)], limit=1).id)
                vals["description"]+=" the partner_ids are of the cevent "+str(partner_ids)

                self.env["calendar.event"].search([("res_model_id","=",self.env['ir.model'].search([('model','=','project.task')],limit=1).id),("res_id","=",self.id)], limit=1).write({
                    'partner_ids': partner_ids,
                })

        if len(self)>1 and "project_id_name" in vals:
            return super(project_task, self).write(vals)

        data_before_updated={}
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
        if "name" in vals:
            data_before_updated['name']=str(self.name)
        if "pv_id" in vals:
            data_before_updated['pv_id']=str(self.pv_id.nom)
        if "date_debut" in vals:
            date = datetime(int(str(self.date_debut)[0]+str(self.date_debut)[1]+str(self.date_debut)[2]+str(self.date_debut)[3]), int(str(self.date_debut)[5]+str(self.date_debut)[6]),int(str(self.date_debut)[8]+str(self.date_debut)[9]))
            formatted_date = date.strftime('%d , %B , %Y').lower()
            day_name = date.strftime('%A')
            day, month, year = formatted_date.split(' , ')
            month_french = month_translation[month].capitalize()
            day_french = day_translation[day_name].capitalize() 
            formatted_date_french = f'{day_french} {day}  {month_french}  {year}'
            data_before_updated['date_debut']=str(formatted_date_french)
        if "date_fin_project" in vals:
            date = datetime(int(str(self.date_fin_project)[0]+str(self.date_fin_project)[1]+str(self.date_fin_project)[2]+str(self.date_fin_project)[3]), int(str(self.date_fin_project)[5]+str(self.date_fin_project)[6]),int(str(self.date_fin_project)[8]+str(self.date_fin_project)[9]))
            formatted_date = date.strftime('%d , %B , %Y').lower()
            day_name = date.strftime('%A')
            day, month, year = formatted_date.split(' , ')
            month_french = month_translation[month].capitalize()
            day_french = day_translation[day_name].capitalize() 
            formatted_date_french = f'{day_french} {day}  {month_french}  {year}'
            data_before_updated['date_fin_project']=str(formatted_date_french)
        # if "qte_planifier" in vals:
        #     data_before_updated['qte_planifier']=str(self.qte_planifier)
        if "temp_de_travail_enrgistrer" in vals:
            data_before_updated['temp_de_travail_enrgistrer']=str(self.temp_de_travail_enrgistrer)
        if "stage_id" in vals:
            data_before_updated['stage_id']=(self.stage_id.name)
        if "user_ids" in vals:
            user_ids=""
            for rec in self.user_ids.ids:
                    user_id = self.env["res.users"].search([("id", "=", rec)], limit=1)
                    user_ids += "<span class='fw-bolder'>" + user_id.partner_id.name + "</span> "
            data_before_updated['user_ids']=user_ids
        user = self.env.user
        
        if len(self)>1 and len(vals)==1 and "active" in vals:
                if vals["active"]==False:
                    body_message = "<span class='fw-bolder'> Rappel</span> <br/> <span class='fw-bolder text-danger'> Tâche Archivée </span> <br/>"
                if vals["active"]==True:
                    body_message = "<span class='fw-bolder'> Rappel</span> <br/>Tâche Désarchiver  <br/>"
                for r in self:
                    body_message+="<span class='fw-bolder'>"+r.name+"</span>  ,"
                    # if vals["active"]==False:
                    #     body_message = "Tâche Archrappelivée <span class='fw-bolder'>"+name_of_the_task+"</span> Par  : <span class='fw-bolder'>"+str(self.env.user.partner_id.name)+"</span><br/>"
                    # if vals["active"]==True:
                    #     body_message = "Tâche Disarchive  <span class='fw-bolder'>"+name_of_the_task+"</span> Par : <span class='fw-bolder'>"+str(self.env.user.partner_id.name)+"</span><br/>"
                body_message+="<br/>Par  : <span class='fw-bolder'>"+str(self.env.user.partner_id.name)+"</span><br/>"
                if 'active' not in vals:
                    self.env["mail.message"].create({
                        "body": body_message,
                        'email_from': '"'+user.partner_id.name+'" <'+user.login+'>',
                        'message_type': 'comment',
                        'subtype_id': 1,
                        'subject': False,
                        'model': 'mail.channel',
                        'task_id':self[0].id,
                        'res_id': self[0].project_id.channel_id.id,
                        'record_name': 'Chantier',
                    })

            
                return super(project_task, self).write(vals)
        name_of_the_task=self.name
            
        for rec in self.env["project.task"].search([("project_id","=",self.id),("active","in",[True,False])]):     
            query = "UPDATE PROJECT_TASK SET nbr_field_attached=%s WHERE ID=%s"
            self.env.cr.execute(query, (self.env["ir.attachment"].sudo().search_count([('res_id', '=', rec.id), ("res_model", "=", "project.task")]),rec.id))

        if len(vals)==1 and "message_delta_date_debut" in vals or "message_delta_date_fin" in vals:
            return super(project_task, self).write(vals)
        
        user_tobe_filter_is=self.env["user.filter"].search([],limit=1)        
        user = user_tobe_filter_is.user_id  if user_tobe_filter_is else self.env.user

        if "is_mes_tach_suivi" in vals:
            if vals["is_mes_tach_suivi"]=="assigned":
                vals["user_ids"]=[[6,False,[user.id]]]
            elif vals["is_mes_tach_suivi"]=="suived":
                #remove it from user_ids
                data=self.env["mail.followers"].sudo().search([
                    ("res_id","=",self.id),
                    ("partner_id","!=",user.partner_id.id),
                    ("res_model","=","project.task"),
                    ],limit=1)
                
                # vals["user_ids"]=[[6,False,[vals["user_id"]]]]                   
                user_id_from_follower=self.env["res.users"].search([("partner_id","=",data.partner_id.id)],limit=1).id
                ids=self.message_partner_ids.ids

                ids_user=[]
                for p_id in ids:
                   ids_user.append(self.env['res.users'].search([("partner_id","=",p_id)],limit=1).id) 
                ids=ids_user
                # if self.env.user.partner_id.id in ids:
                #     ids.remove(self.env.user.partner_id.id)
                # self.env["project.task.user.rel"].unlink()
                          
                vals["user_ids"]=[[6,False,[ids[1]]]] if len(ids)>1 else [[6,False,[]]]
                
                #add it as follower
                is_exist=self.env["mail.followers"].sudo().search([
                    ("res_id","=",user.partner_id.id),
                    ("partner_id","=",user.partner_id.id),
                    ("res_model","=","res.partner"),
                    ])
                
                is_exist_two=self.env["mail.followers"].sudo().search([
                    ("res_id","=",self.id),
                    ("partner_id","=",user.partner_id.id),
                    ("res_model","=","project.task"),
                    ])
                if not is_exist_two:
                        self.env["mail.followers"].sudo().with_context(mail_create_nosubscribe=True).create({

                        "res_id": self.id,

                        "partner_id": user.partner_id.id,

                        "res_model": "project.task"

                    })
                        
                if not is_exist:
                            self.env["mail.followers"].sudo().with_context(mail_create_nosubscribe=True).create({

                        "res_id": user.partner_id.id,

                        "partner_id": user.partner_id.id,

                        "res_model": "res.partner"

                    })


            elif vals["is_mes_tach_suivi"]=="unsuived":
                # print("------")
                # if user.id not in self.user_ids.ids:
                    self.env["mail.followers"].sudo().search([
                        ("res_id","=",user.partner_id.id),
                        ("partner_id","=",user.partner_id.id),
                        ("res_model","=","res.partner"),
                        ],limit=1).unlink() 
                    self.env["mail.followers"].sudo().search([
                        ("res_id","=",self.id),
                        ("partner_id","=",user.partner_id.id),
                        ("res_model","=","project.task"),
                        ],limit=1).unlink()
                    print("----")
                # else:
                #     print("----")
                    data=self.env["mail.followers"].sudo().search([
                        ("res_id","=",self.id),
                        # ("partner_id","=",user.partner_id.id),
                        ("res_model","=","project.task"),
                        ],limit=1)
                    
                    # vals["user_ids"]=[[6,False,[vals["user_id"]]]]                   
                    user_id_from_follower=self.env["res.users"].search([("partner_id","=",data.partner_id.id)],limit=1).id

                    # self.env["project.task.user.rel"].unlink()
                    ids=self.message_partner_ids.ids
                    ids_user=[]
                    for p_id in ids:
                       ids_user.append(self.env['res.users'].search([("partner_id","=",p_id)],limit=1).id) 
                    ids=ids_user

                    # if self.env.user.partner_id.id in ids:
                    #     ids.remove(self.env.user.partner_id.id)
                    
                    vals["user_ids"]=[[6,False,[ids[2]]]] if len(ids)>3 else [[6,False,[]]]
            # super(project_task, self).write(vals)

                #remove it from the follower and from assign a
        if "user_ids" in vals and user.id in vals['user_ids'][0][2]:
            vals['is_mes_tach_suivi']="assigned"
        if "user_ids" in vals and user.id not in vals['user_ids'][0][2]:
            if user.partner_id.id in self.message_follower_ids.ids:
                vals['is_mes_tach_suivi']="suived"
            else:
                vals['is_mes_tach_suivi']="unsuived"

        if len(self)>1 and "active" in vals:
            return super(project_task, self).write(vals)
        if len(self)==1:
            if "date_fin_project" not in vals and "date_debut" in vals:
                vals["date_fin_project"]=self.date_fin_project+timedelta((datetime.strptime(vals["date_debut"], '%Y-%m-%d').date()-self.date_debut).days)
                if "date_fin_project" in vals:
                    date = datetime(int(str(self.date_fin_project)[0]+str(self.date_fin_project)[1]+str(self.date_fin_project)[2]+str(self.date_fin_project)[3]), int(str(self.date_fin_project)[5]+str(self.date_fin_project)[6]),int(str(self.date_fin_project)[8]+str(self.date_fin_project)[9]))
                    formatted_date = date.strftime('%d , %B , %Y').lower()
                    day_name = date.strftime('%A')
                    day, month, year = formatted_date.split(' , ')
                    month_french = month_translation[month].capitalize()
                    day_french = day_translation[day_name].capitalize() 
                    formatted_date_french = f'{day}  {day_french}  {month_french}  {year}'
                    data_before_updated['date_fin_project']=formatted_date_french

        if "user_ids" in vals:
            user_ids=""
            for rec in self.user_ids.ids:
                    user_id = self.env["res.users"].search([("id", "=", rec)], limit=1)
                    user_ids += "<span class='fw-bolder'>" + user_id.partner_id.name + "</span> "
            data_before_updated['user_ids']=user_ids
            print(data_before_updated['user_ids'])
            print("---")
        task = super(project_task, self).write(vals)  # Appel de la méthode d'écriture parente

        active_id=self._context.get('active_id')
        

        value_date_debut=self.date_debut;
            

        user = self.env.user
        if active_id is None:
            if  value_date_debut != self.date_debut :                               
                    if self.date_fin_project is not  False:
                       difference_en_jours = (self.date_debut - value_date_debut).days
                       if difference_en_jours >0:
                         self.date_fin_project =self.date_fin_project+timedelta(days=abs(difference_en_jours)) 
                       else :                    
                         self.date_fin_project =self.date_fin_project-timedelta(days=abs(difference_en_jours))
                           
       
            

        id_message_posted = self.env["mail.message"].search([("model","=","project.task")], order='id desc', limit=1).id

        values_updated = self.env["mail.tracking.value"].search([("mail_message_id","=",id_message_posted)])
        partner_ids = [[6, False, []]]
        if 'user_ids' in vals:
            if len(vals['user_ids'][0][2]) > 0:
                for rec in vals['user_ids'][0][2]:
                    partner_id = self.env["res.users"].search([("id","=",rec)], limit=1).partner_id.id
                    partner_ids[0][2].append(partner_id)
                self.env["calendar.event"].search([("res_model_id","=",self.env['ir.model'].search([('model','=','project.task')],limit=1).id),("res_id","=",self.id)], limit=1).write({
                    'partner_ids': partner_ids,
                })
        

        # if len(values_updated) != 0:
        #     body_message = "Tâche Modifiée <br/>"
        #     body_message += "&nbsp;&nbsp;&nbsp; Projet  : <span class='fw-bolder'>" + str(self.project_id.name) + "</span> <br/> "
        #     body_message += "&nbsp;&nbsp;&nbsp; Nom  : <span class='fw-bolder'>" + str(self.name) + "</span> <br/> "

            # for rec in values_updated:
            #     if rec.field.name == "name" or rec.field.name == "date_debut" or rec.field.name == "date_fin_project" or rec.field.name == "stage_id":
            #         # Mettre à jour l'événement du calendrier
            #             is_prject_task_exist = self.env["calendar.event.type"].search([("name","=","Tâche")])
            #             if not is_prject_task_exist:
            #                 self.env["calendar.event.type"].create({
            #                     "name":"Tâche"
            #                 })
            if "date_debut" in vals or "date_fin_project" in vals or "name" in vals:
                self.env["calendar.event"].search([("res_model_id","=",self.env['ir.model'].search([('model','=','project.task')],limit=1).id),("res_id","=",self.id)],limit=1).write({
                                'name': str(self.name),
                                'categ_ids':[[6, False, [self.env["calendar.event.type"].search([("name","=","Tâche")],limit=1).id]]],
                                'start': datetime.strptime(str(self.date_debut), "%Y-%m-%d"),
                                # 'stop': datetime.strptime(str(self.date_fin_project), "%Y-%m-%d"),
                                'stop': datetime.strptime(str(self.date_fin_project), "%Y-%m-%d") if self.date_fin_project != False else  datetime.strptime(str(self.date_debut), "%Y-%m-%d")+timedelta(hours=1),
                                # 'description': body_message,
                                'duration': 1,
                                "create_date": datetime.now(),
                                # 'task_id':self.id,
                                'project_id':self.project_id.id,

                            })

            # body_message += "&nbsp;&nbsp;&nbsp; "+str(rec.field.field_description)+"  : <span class='fw-bolder'>"+str(rec.old_value_char)+"</span> à <span class 'fw-bolder'>"+str(rec.new_value_char)+"</span> <br/> "
            
            # # Création d'un message de notification
            
            # if  self.stage_id.name=="Tâche Accomplie":
            #         body_message = "Tâche Accomplie <br/>"
            #         body_message += "&nbsp;&nbsp;&nbsp; Projet  : <span class='fw-bolder'>" + str(self.project_id.name) + "</span> <br/> "
            #         body_message += "&nbsp;&nbsp;&nbsp; Tâche  : <span class='fw-bolder'>" + str(self.name) + "</span> <br/> "
            #         body_message += "&nbsp;&nbsp;&nbsp; Assigné à  : "
                    
            #         for rec in self.user_ids:
            #            body_message += "<span class='fw-bolder'>" + rec.partner_id.name + "</span> "
            #         body_message += "<br/>"

            #         #print users of Assigné à 

            #         if not self.env["mail.message"].search([("body","=",body_message)]):
            #             self.env["mail.message"].create({
            #                 "body": body_message,
            #                 'email_from': '"'+user.partner_id.name+'" <'+user.login+'>',
            #                 'message_type': 'comment',
            #                 'subtype_id': 1,
            #                 'subject': False,
            #                 'model': 'mail.channel',
            #                 'res_id': self.env["mail.channel"].search([("name","like",str(self.project_id.name)+'%'),("channel_type","=","channel")],limit=1).id,
            #                 'record_name': 'Chantier',
            #             })
        ids_tasks=[]
        for rec in self:
            body_message=""
            ids_tasks.append(rec.id)
            vals['project_id_name']=str(rec.project_id_name).replace('...','')[:50]+"..."
            if len(rec.user_ids)>0:
                if not rec.user_id:
                    rec.user_id=rec.user_ids[0]
                if rec.user_id.id!=rec.user_ids[0].id:
                    rec.user_id=rec.user_ids[0]
            if len(rec.tag_ids)>0:
                if not rec.tag_id:
                    rec.tag_id=rec.tag_ids[0]
                if rec.tag_id.id!=rec.tag_ids[0].id:
                    rec.tag_id=rec.tag_ids[0]
            
            
            if "user_id" in vals:
                if len(rec.user_ids)>0:
                    if rec.user_ids[0].id!=vals["user_id"]:
                        rec.user_ids=[[6,False,[vals["user_id"]]]]
                if len(rec.user_ids)==0:
                    rec.user_ids=[[6,False,[vals["user_id"]]]]
            if "tag_id" in vals:
                if len(rec.tag_ids)>0:
                    if rec.tag_ids[0].id!=vals["tag_id"]:
                        rec.tag_ids=[[6,False,[vals["tag_id"]]]]
                if len(rec.tag_ids)==0:
                    rec.tag_ids=[[6,False,[vals["tag_id"]]]]
        
                    
                    # body_message += "&nbsp;&nbsp;&nbsp; Projet  : <span class='fw-bolder'>" + str(self.project_id.name) + "</span> <br/> "
                    body_message += "&nbsp;&nbsp;&nbsp; Tâche  : <span class='fw-bolder'>" + str(self.name) + "</span> <br/> "
                    body_message += "&nbsp;&nbsp;&nbsp; Assigné à  : "
                    
                    for u in self.user_ids:
                       body_message += "<span class='fw-bolder'>" + u.partner_id.name + "</span> "
                    body_message += "<br/>"

                    # if not self.env["mail.message"].search([("body","=",body_message)]):
        is_posted=False
        if "active" in vals:
                    if vals["active"]==False:
                        if self.env.user.partner_id.name=="OdooBot":
                            body_message = "<span class='fw-bolder text-danger'> Tâche Archivée</span> <br/><span class='fw-bolder'>"+name_of_the_task+"</span><br/>"
                        else:
                            body_message = "<span class='fw-bolder text-danger'> Tâche Archivée</span> <br/><span class='fw-bolder'>"+name_of_the_task+"</span><br/> Par  : <span class='fw-bolder'>"+str(self.env.user.partner_id.name)+"</span><br/>"
                    if vals["active"]==True:
                        body_message = "Tâche Désarchiver  <br/><span class='fw-bolder'>"+name_of_the_task+"</span> Par : <span class='fw-bolder'>"+str(self.env.user.partner_id.name)+"</span><br/>"
                        print("--")
                    is_posted=True
        if "active" not in vals:   
            body_message = "Modifiée Par  : <span class='fw-bolder'>"+str(self.env.user.partner_id.name)+"</span><br/>"
        if "name" in vals:
            # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
            body_message += "&nbsp;&nbsp;&nbsp; Nom : <span class='fw-bolder'>" + str(data_before_updated["name"]) + "</span> à <span class='fw-bolder'>" + vals["name"] + "</span> <br/> "
            is_posted=True
        if "pv_id" in vals:
            # Si l'ID du PV est spécifié dans les valeurs, l'ajouter au message
            body_message += "&nbsp;&nbsp;&nbsp; PV  : <span class='fw-bolder'>" + str(data_before_updated["pv_id"]) + "</span> à <span class='fw-bolder'>" + str(self.pv_id.nom) + "</span> <br/> "
            is_posted=True
        if "date_debut" in vals:
            # Si la date de début est spécifiée dans les valeurs, l'ajouter au message
            date = datetime(int(str(self.date_debut)[0]+str(self.date_debut)[1]+str(self.date_debut)[2]+str(self.date_debut)[3]), int(str(self.date_debut)[5]+str(self.date_debut)[6]),int(str(self.date_debut)[8]+str(self.date_debut)[9]))
            formatted_date = date.strftime('%d , %B , %Y').lower()
            day_name = date.strftime('%A')
            day, month, year = formatted_date.split(' , ')
            month_french = month_translation[month].capitalize()
            day_french = day_translation[day_name].capitalize() 
            formatted_date_french = f'{day}  {day_french}  {month_french}  {year}'

            body_message += "&nbsp;&nbsp;&nbsp; Date Debut : <span class='fw-bolder'>" + str(data_before_updated["date_debut"]) + "</span> à <span class='fw-bolder'>" + str(formatted_date_french) + "</span> <br/> "
            is_posted=True
        if "date_fin_project" in vals:            
            # Si la date de fin du projet est spécifiée dans les valeurs, l'ajouter au message            
            date = datetime(int(str(self.date_fin_project)[0]+str(self.date_fin_project)[1]+str(self.date_fin_project)[2]+str(self.date_fin_project)[3]), int(str(self.date_fin_project)[5]+str(self.date_fin_project)[6]),int(str(self.date_fin_project)[8]+str(self.date_fin_project)[9]))
            formatted_date = date.strftime('%d , %B , %Y').lower()
            day_name = date.strftime('%A')
            day, month, year = formatted_date.split(' , ')
            month_french = month_translation[month].capitalize()
            day_french = day_translation[day_name].capitalize() 
            formatted_date_french = f'{day_french} {day} {month_french}  {year}'


            body_message += "&nbsp;&nbsp;&nbsp; Date Fin  : <span class='fw-bolder'>" + str(data_before_updated["date_fin_project"]) + "</span> à <span class='fw-bolder'>" + str(formatted_date_french) + "</span> <br/> "
            is_posted=True
        # if "qte_planifier" in vals:
        #     # Si la quantité planifiée est spécifiée dans les valeurs, l'ajouter au message
        #     body_message += "&nbsp;&nbsp;&nbsp; Quantité planifiée  : <span class='fw-bolder'>" + str(data_before_updated["qte_planifier"]) + "</span> à <span class='fw-bolder'>" + str(self.qte_planifier) + "</span> <br/> "
        #     is_posted=True
        # if "temp_de_travail_enrgistrer" in vals:
        #     # Si le temps de travail enregistré est spécifié dans les valeurs, l'ajouter au message
        #     body_message += "&nbsp;&nbsp;&nbsp; Temps de Travail Enregistré  : <span class='fw-bolder'>" + str(data_before_updated["temp_de_travail_enrgistrer"]) + "</span> à <span class='fw-bolder'>" + str(self.temp_de_travail_enrgistrer) + "</span> <br/> "
        #     is_posted=True
        if "stage_id" in vals:
            # Si le temps de travail enregistré est spécifié dans les valeurs, l'ajouter au message
            body_message += "&nbsp;&nbsp;&nbsp; Status  : <span class='fw-bolder'>" + str(data_before_updated["stage_id"]) + "</span> à <span class='fw-bolder'>" + str(self.stage_id.name) + "</span> <br/> "
            is_posted=True
        if "user_ids" in vals:
            if len(vals["user_ids"][0][2]) > 0:
                is_posted=True
                # Si des utilisateurs sont assignés, les ajouter au message                                                                                                
                body_message += "&nbsp;&nbsp;&nbsp; Assigné à : <span class='fw-bolder'>" + str(data_before_updated["user_ids"]) + "</span>  à "
                for u in vals["user_ids"][0][2]:
                    user_id = self.env["res.users"].search([("id", "=", u)], limit=1)
                    body_message += "<span class='fw-bolder'>" + user_id.partner_id.name + "</span> "
            body_message += "<br/>"

        # Récupérer l'utilisateur actuel
        user = self.env.user

        # Créer un message pour notifier la création de la tâche
        
        # self.env["mail.message"].create({
        #     "body": body_message,
        #     'email_from': '"'+user.partner_id.name+'" <'+user.login+'>',
        #     'message_type': 'comment',
        #     'subtype_id': 1,
        #     'subject': False,
        #     'model': 'mail.channel',
        #     'res_id': self.env["mail.channel"].search([("name", "like", str(project_Task.project_id.name)+'%'), ("channel_type", "=", "channel")], limit=1).id,
        #     'record_name': 'Chantier',
        # })
        body_message_main_info=""
        if is_posted==True:
            partnsers=""
            print(rec)
            print("test")
            for p in rec.user_ids:
                partnsers+=str(p.partner_id.name)+" ,"   
            

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
                    
            date = datetime(int(str(rec.date_debut)[0]+str(rec.date_debut)[1]+str(rec.date_debut)[2]+str(rec.date_debut)[3]), int(str(rec.date_debut)[5]+str(rec.date_debut)[6]),int(str(rec.date_debut)[8]+str(rec.date_debut)[9]))
            formatted_date = date.strftime('%d , %B , %Y').lower()
            day_name = date.strftime('%A')
            day, month, year = formatted_date.split(' , ')
            # Translate the month to French and capitalize the first letter

            month_french = month_translation[month].capitalize()
            day_french = day_translation[day_name].capitalize()
            # Combine the day, translated month, and year
            formatted_date_french = f'{day_french} {day} {month_french} {year}'
            formatted_date_french_end=""
            date_end = datetime(int(str(rec.date_fin_project)[0]+str(rec.date_fin_project)[1]+str(rec.date_fin_project)[2]+str(rec.date_fin_project)[3]), int(str(rec.date_fin_project)[5]+str(rec.date_fin_project)[6]),int(str(rec.date_fin_project)[8]+str(rec.date_fin_project)[9]))
            formatted_date_end = date_end.strftime('%d , %B , %Y').lower()
            day_name = date_end.strftime('%A')
            day_end, month_end, year_end = formatted_date_end.split(' , ')

            day_french_end = day_translation[day_name].capitalize()
            month_french_end = month_translation[month_end].capitalize()
            formatted_date_french_end = f'{day_french_end} {day_end} {month_french_end}  {year_end}'
            
            target_date = datetime.strptime(str(self.date_fin_project), "%Y-%m-%d")  # Date de début
            current_date = datetime.now()  # Date actuelle
            delta = target_date - current_date  # Calcul de la différence entre la date cible et la date actuelle
            days_remaining = delta.days  # Nombre de jours restants jusqu'à la date cible
            days_remaining = days_remaining + 1  # Ajout d'un jour car 'delta' ne tient pas compte de la date actuelle

            body_message_main_info = "<span class='fw-bolder text-danger'> Rappel<br/></span>"
            body_message_main_info += "Tâche : <span class='fw-bolder'>" + self.name + "</span><br/>"
            body_message_main_info += "Assigné à : <span class='fw-bolder'>" + str(partnsers) + "</span><br/>"
            body_message_main_info += "État : <span class='fw-bolder'>" + str(rec.stage_id.name) + "</span><br/>"
           
            body_message_main_info += "Date de début : <span class='fw-bolder'>" + formatted_date_french + "</span><br/>"
            body_message_main_info += "Date de fin : <span class='fw-bolder text-danger'>" + formatted_date_french_end + "</span><br/>"
            body_message_main_info += "Durée de tâche : <span class='fw-bolder text-danger'>" + str(rec.duree_de_tach) + "</span><br/>"
            self.env["mail.message"].create({
                        "body":body_message_main_info+""+body_message+"<span class='fw-bolder text-danger'> Il reste "+str(days_remaining)+" Jours pour la fin de cette Tache. </span>",
                        'email_from': '"'+user.partner_id.name+'" <'+user.login+'>',
                        'message_type': 'comment',
                        'subtype_id': 1,
                        'subject': False,
                        'model': 'mail.channel',
                        # 'task_id':self.id,
                        'res_id': self.project_id.channel_id.id,
                        'record_name': 'Chantier',
                    })
        return task


        # if self.project_id.documents_folder_id.id!=False:
        #     folders=self.env["documents.folder"].search([("id","=",self.project_id.documents_folder_id.id)],limit=1)
        #     folders.write({
        #         "display_name":folders.name
        #     });
        #     for rec in self.env["documents.folder"].search([("parent_folder_id","=",folders.id)]):
        #         rec.write({
        #         "display_name":rec.name
        #              });

        return task


    
    @api.model
    def create(self, vals):   
        
        print("the vals of the project task model")
        print(vals)

        # Appel de la méthode de création parente pour créer l'enregistrement
        project_Task = super(project_task, self).create(vals)
        # Vérifier si le canal "Chantier" existe
        # is_channel_chantier_exist = self.env["mail.channel"].search([("name", "=", "Chantier"), ("channel_type", "=", "channel")])

        # if not is_channel_chantier_exist:
        #     # Créer le canal "Chantier" s'il n'existe pas
        #     self.env["mail.channel"].create({
        #         "name": "Chantier",
        #         "channel_type": "channel"
        #     })

        # Préparer le message de création de tâche
        body_message = "Tâche créee <br/>"
        if "name" in vals:
            # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
            body_message += "&nbsp;&nbsp;&nbsp; Tâche  : <span class='fw-bolder'>" + vals["name"] + "</span> <br/> "
        else:
            body_message += "&nbsp;&nbsp;&nbsp; Nom  :  <br/> "
        # if "project_id" in vals:              
        #     # Si l'ID du projet est spécifié dans les valeurs, l'ajouter au message
        body_message += "&nbsp;&nbsp;&nbsp; Projet  : <span class='fw-bolder'>" + str(project_Task.project_id.name) + "</span> <br/> "
        # else:
        #     body_message += "&nbsp;&nbsp;&nbsp; Projet  : <br/> "
        if "pv_id" in vals:
            # Si l'ID du PV est spécifié dans les valeurs, l'ajouter au message
            body_message += "&nbsp;&nbsp;&nbsp; PV  : <span class='fw-bolder'>" + str(project_Task.pv_id.nom) + "</span> <br/> "
        else:
            body_message += "&nbsp;&nbsp;&nbsp; PV  :  <br/> "
        if "date_debut" in vals:
            # Si la date de début est spécifiée dans les valeurs, l'ajouter au message
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
            date = datetime(int(str(vals["date_debut"])[0]+str(vals["date_debut"])[1]+str(vals["date_debut"])[2]+str(vals["date_debut"])[3]), int(str(vals["date_debut"])[5]+str(vals["date_debut"])[6]),int(str(vals["date_debut"])[8]+str(vals["date_debut"])[9]))
            formatted_date = date.strftime('%d , %B , %Y').lower()
            day_name = date.strftime('%A')
            day, month, year = formatted_date.split(' , ')
            # Translate the month to French and capitalize the first letter
            
            month_french = month_translation[month].capitalize()
            day_french = day_translation[day_name].capitalize()
            # Combine the day, translated month, and year
            formatted_date_french = f'{day_french} {day}  {month_french}  {year}'

            # Si la date de début est spécifiée dans les valeurs, l'ajouter au message
            body_message += "&nbsp;&nbsp;&nbsp; Date Debut  : <span class='fw-bolder'>" + str(formatted_date_french) + "</span> <br/> "
        else:
            body_message += "&nbsp;&nbsp;&nbsp; Date Debut  :  <br/> "
        if "date_fin_project" in vals:
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
            date = datetime(int(str(vals["date_fin_project"])[0]+str(vals["date_fin_project"])[1]+str(vals["date_fin_project"])[2]+str(vals["date_fin_project"])[3]), int(str(vals["date_fin_project"])[5]+str(vals["date_fin_project"])[6]),int(str(vals["date_fin_project"])[8]+str(vals["date_fin_project"])[9]))
            formatted_date = date.strftime('%d , %B , %Y').lower()
            day_name = date.strftime('%A')
            day, month, year = formatted_date.split(' , ')
            # Translate the month to French and capitalize the first letter
            
            month_french = month_translation[month].capitalize()
            day_french = day_translation[day_name].capitalize()
            # Combine the day, translated month, and year
            formatted_date_french = f'{day_french} {day}  {month_french}  {year}'

            # Si la date de fin du projet est spécifiée dans les valeurs, l'ajouter au message
            body_message += "&nbsp;&nbsp;&nbsp; Date Fin  : <span class='fw-bolder'>" + str(formatted_date_french) + "</span> <br/> "
        else:
            body_message += "&nbsp;&nbsp;&nbsp; Date Fin  :  <br/> "
        # if "qte_planifier" in vals:
        #     # Si la quantité planifiée est spécifiée dans les valeurs, l'ajouter au message
        #     body_message += "&nbsp;&nbsp;&nbsp; Quantité planifiée  : <span class='fw-bolder'>" + str(project_Task.qte_planifier) + "</span> <br/> "
        # else:
        #     body_message += "&nbsp;&nbsp;&nbsp; Quantité planifiée  :  <br/> "
        # if "temp_de_travail_enrgistrer" in vals:
        #     # Si le temps de travail enregistré est spécifié dans les valeurs, l'ajouter au message
        #     body_message += "&nbsp;&nbsp;&nbsp; Temps de Travail Enregistré  : <span class='fw-bolder'>" + str(project_Task.temp_de_travail_enrgistrer) + "</span> <br/> "
        # else:
        #     body_message += "&nbsp;&nbsp;&nbsp; Temps de Travail Enregistré  :  <br/> "
        if "user_ids" in vals:
            if len(vals["user_ids"][0][2]) > 0:
                # Si des utilisateurs sont assignés, les ajouter au message
                body_message += "&nbsp;&nbsp;&nbsp; Assigné à  :  "
                for rec in vals["user_ids"][0][2]:
                    user_id = self.env["res.users"].search([("id", "=", rec)], limit=1)
                    body_message += "<span class='fw-bolder'>" + user_id.partner_id.name + "</span> "
        body_message += "<br/>"

        # Récupérer l'utilisateur actuel
        user = self.env.user

        # Créer un message pour notifier la création de la tâche
        
        self.env["mail.message"].create({
            "body": body_message,
            'email_from': '"'+user.partner_id.name+'" <'+user.login+'>',
            'message_type': 'comment',
            'subtype_id': 1,
            'subject': False,
            'model': 'mail.channel',
            'res_id': project_Task.project_id.channel_id.id,
            'record_name': 'Chantier',
        })
        if "date_debut" in vals:
            vals["date_start_calendar"] = vals["date_debut"]

        # Vérifier si le sous-type "PV" existe
        is_subtype_pv_exist = self.env["mail.message.subtype"].search([("name", "=", "PV"), ("res_model", "=", "project.task")])
        if not is_subtype_pv_exist:
            # Créer le sous-type "PV" s'il n'existe pas
            self.env["mail.message.subtype"].create({
                "name": "PV",
                "res_model": "project.task",
            })

        partner_ids = [[6, False, []]]
        is_prject_task_exist=False
        if 'user_ids' in vals:
            if len(vals['user_ids'][0][2]) > 0:
                for rec in vals['user_ids'][0][2]:
                    partner_id = self.env["res.users"].search([("id", "=", rec)], limit=1).partner_id.id
                    partner_ids[0][2].append(partner_id)
            is_prject_task_exist = self.env["calendar.event.type"].search([("name","=", "Tâche")])
        
        if not is_prject_task_exist:
            self.env["calendar.event.type"].create({
                "name": "Tâche"
            })
        
        self.env["calendar.event"].create({
                'categ_ids': [[6, False, [self.env["calendar.event.type"].search([("name", "=","Tâche")], limit=1).id]]],
                'res_model_id': self.env['ir.model'].search([('model',"=", 'project.task')], limit=1).id,
                'res_id': project_Task.id, 
                'user_id': vals['user_ids'][0][2][0],
                'partner_ids': partner_ids,
                'name':  vals["name"] + " ",
                'start': datetime.strptime(vals["date_debut"], "%Y-%m-%d"),
                'stop': datetime.strptime(vals["date_fin_project"], "%Y-%m-%d") if vals["date_fin_project"]!=False else datetime.strptime(vals["date_debut"], "%Y-%m-%d") + timedelta(hours=1),
                'description': body_message,
                'duration': 1,
                'project_id':project_Task.project_id.id,
                'res_model_id': self.env['ir.model'].search([('model','=','project.task')],limit=1).id,
                'res_id': project_Task.id,
                "create_date": datetime.now()
            })
        return project_Task

    # @api.depends('attachment_ids','date_debut','date_fin_project')
    # @api.onchange('attachment_ids')
    @api.depends('date_debut')
    def _compute_nbr_attached_file(self):
        # Pour chaque enregistrement dans le jeu de données

        for record in self:
            
            query = "UPDATE PROJECT_TASK SET nbr_field_attached=%s WHERE ID=%s"
            print(self.env["ir.attachment"].sudo().search_count([('res_id', '=', record.id), ("res_model", "=", "project.task")]))
            print("-----")
            
            self.env.cr.execute(query, (self.env["ir.attachment"].sudo().search_count([('res_id', '=', record.id), ("res_model", "=", "project.task")]),record.id))

            # record.nbr_field_attached = self.env["ir.attachment"].sudo().search_count([('res_id', '=', record.id), ("res_model", "=", "project.task")])

            
    @api.depends('date_fin_project')
    def _get_delta_date_fin(self):
        # Pour chaque enregistrement dans le jeu de données
        for rec in self:
            days_remaining = 0
            if rec.date_fin_project:
                # Si la date de fin du projet est définie
                target_date = datetime.strptime(str(rec.date_fin_project), "%Y-%m-%d")
                current_date = datetime.now()
                delta = target_date - current_date
                days_remaining = delta.days
                days_remaining = days_remaining + 1
                message_delta_date_fin=""
                if days_remaining > 0:
                    # Si le nombre de jours restants est supérieur à zéro
                    message_delta_date_fin = " Reste " + str(days_remaining) + " jours"
                elif days_remaining < 0:
                    # Si le nombre de jours restants est négatif (retard)
                    message_delta_date_fin = " Retard " + str(-days_remaining) + " jours"
                else:
                    # Si le nombre de jours restants est égal à zéro (aujourd'hui)
                    message_delta_date_fin = " Aujourd'hui"
                query = "UPDATE PROJECT_TASK SET message_delta_date_fin=%s where id=%s"
                self.env.cr.execute(query, (message_delta_date_fin,rec.id))

            if rec.date_fin_project:
                # Si la date de fin du projet est définie
                rec.delta_date_fin = days_remaining
            else:
                # Si la date de fin du projet n'est pas définie
                rec.delta_date_fin = 0

    
    @api.depends('date_debut')
    def _get_delta_date_debut(self):

        # Pour chaque enregistrement dans le jeu de données
        for rec in self:
            query = "UPDATE PROJECT_TASK SET nbr_message_partner_ids=%s WHERE ID=%s"
            self.env.cr.execute(query, (len(rec.message_follower_ids),rec.id))
            print(len(rec.message_follower_ids))
            print("----")
            message_delta_date_debut=""
            if rec.delta_date_debut > 0:
                # Si le nombre de jours restants est supérieur à zéro
                message_delta_date_debut = " Reste " + str(rec.delta_date_debut) + " jours"
            elif rec.delta_date_debut < 0:
                # Si le nombre de jours restants est négatif (retard)
                message_delta_date_debut = " Retard " + str(-rec.delta_date_debut) + " jours"
            else:
                # Si le nombre de jours restants est égal à zéro (aujourd'hui)
                message_delta_date_debut = " Aujourd'hui"
            days_remaining = 0
            if rec.date_debut:
                # Si la date de début est définie
                target_date = datetime.strptime(str(rec.date_debut), "%Y-%m-%d")
                current_date = datetime.now()
                delta = target_date - current_date
                days_remaining = delta.days
                days_remaining = days_remaining + 1

                if days_remaining > 0:
                    # Si le nombre de jours restants est supérieur à zéro
                    message_delta_date_debut = " Reste " + str(days_remaining) + " jours"
                elif days_remaining < 0:
                    # Si le nombre de jours restants est négatif (retard)
                    message_delta_date_debut = " Retard " + str(-days_remaining) + " jours"
                else:
                    # Si le nombre de jours restants est égal à zéro (aujourd'hui)
                    message_delta_date_debut = " Aujourd'hui"
            query = "UPDATE PROJECT_TASK SET message_delta_date_debut=%s WHERE id=%s"
            self.env.cr.execute(query, (message_delta_date_debut,rec.id))

            if rec.date_debut:
                # Si la date de début est définie
                rec.delta_date_debut = days_remaining
            else:
                # Si la date de début n'est pas définie
                rec.delta_date_debut = 0



     
    @api.depends('date_fin_project')
    @api.depends('name')
    def _comput_echance_fin(self):
        # if self.env["project.task"].search_count([("project_id","=",self._context.get('active_id'))])>0:
        #     for record in self:      

        #         query = "UPDATE PROJECT_TASK SET nbr_field_attached=%s WHERE ID=%s"
        #         self.env.cr.execute(query, (self.env["ir.attachment"].sudo().search_count([('res_id', '=', record.id), ("res_model", "=", "project.task")]),record.id))

        # Pour chaque enregistrement dans le jeu de données
        for rec in self:
            res = ""

            days_remaining = 0
            if rec.date_debut and rec.date_fin_project:
                print("test")
                # Si les dates de début et de fin du projet sont définies
                target_date_fin = datetime.strptime(str(rec.date_fin_project), "%Y-%m-%d")
                target_date_debut = datetime.strptime(str(rec.date_debut), "%Y-%m-%d")
                current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

                delta = target_date_fin - current_date
                days_remaining = delta.days
                difference = target_date_fin - target_date_debut

                if difference.days >= 0:
                    if days_remaining - 1 > 0:
                        # S'il reste plus d'un jour avant la date de fin
                        days_remaining = days_remaining + 1
                        res = " Reste " + str(days_remaining) + "  Jours "
                    elif days_remaining - 1 == 0:
                        # S'il reste un jour avant la date de fin (aujourd'hui)
                        res = " Aujourd'hui " + str(days_remaining) + " Jours"
                    else:
                        # En cas de retard (la date de fin est dépassée)
                        days_remaining = days_remaining * -1
                        res = " Retard " + str(days_remaining) + " Jours"
                else:
                    if days_remaining > 0:
                        # S'il reste plus d'un jour avant la date de fin
                        days_remaining = days_remaining + 1
                        res = "  " + str(days_remaining) + " Jours"
                    elif days_remaining == 0:
                        # S'il reste un jour avant la date de fin (aujourd'hui)
                        res = " Aujourd'hui " + str(days_remaining) + " Jours"
                    else:
                        # En cas de retard (la date de fin est antérieure à la date de début)
                        days_remaining = days_remaining * -1
                        res = " Retard " + str(days_remaining) + " Jours"
                        raise ValidationError(_("S'il vous plaît, la date de fin doit être supérieure à la date de début"))
            else:
                res = "  " + str(days_remaining) + " Jours"
            rec.echance_fin = res



    # Cette méthode renvoie un dictionnaire pour ouvrir une vue de liste (kanban) des pièces jointes liées à une tâche de projet.
    def get_attachment_for_task_project(self):
        # Définition du début du dictionnaire
        self = self.sudo()
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id('documents_project.action_view_documents_project_task')
        action['context'] = {
            **ast.literal_eval(action['context'].replace('active_id', str(self.id))),
            'default_tag_ids': self.project_id.documents_tag_ids.ids,
        }
        return action
        # return {
        #     'name': _('Fichiers joints'),  # Nom de l'action : "Fichiers joints"
            
        #     # Domaine de recherche pour filtrer les pièces jointes liées à l'ID de la tâche de projet actuelle et au modèle "project.task".
        #     'domain': [('res_id', '=', self.id), ("res_model", "=", "project.task")],
            
        #     'view_type': 'kanban',  # Type de vue : "kanban"
        #     'context': {
        #         "default_res_model": "project.task",


        #         "search_default_projet_id": self.project_id.id

        #     },  # Contexte pour la création de nouveaux enregistrements et les valeurs de recherche par défaut

        #     'res_model': 'ir.attachment',  # Modèle de données associé à cette action : "ir.attachment"
            
        #     'view_id': False,  # Aucune vue spécifique associée, la vue par défaut sera utilisée.
            
        #     'view_mode': 'kanban,tree,form',  # Mode de vue : "kanban"
            
        #     'type': 'ir.actions.act_window'  # Type d'action : "ir.actions.act_window", indiquant une action pour ouvrir une fenêtre.
        # }

    @api.depends('date_debut', 'date_fin_project')
    def _comput_duree_de_tach(self):
        for rec in self:
            res = ""
            days_remaining = 0
            if rec.date_debut and rec.date_fin_project:
                # Conversion des dates de chaînes de texte en objets de date
                date_debut = datetime.strptime(str(rec.date_debut), "%Y-%m-%d")
                date_fin_project = datetime.strptime(str(rec.date_fin_project), "%Y-%m-%d")

                # Calcul de la différence entre la date de fin et la date de début
                delta = date_fin_project - date_debut

                # Calcul du nombre de jours restants
                days_remaining = delta.days - 1

                if days_remaining > 0:
                    days_remaining = days_remaining + 1
                    res = "  " + str(days_remaining) + " Jours"
                elif days_remaining < -1:
                    days_remaining = days_remaining + 1
                    res = " " + str(-days_remaining) + " Jours"
                elif days_remaining == -1:
                    days_remaining = days_remaining + 1
                    res = " " + str(days_remaining) + " Jours"
                else:
                    days_remaining = days_remaining + 1
                    res = " " + str(days_remaining) + " Jours"
            else:
                res = "  " + str(days_remaining) + " Jours"

            rec.duree_de_tach = res
            
            # deference=int(str(res).replace("Jours","").replace(" ",""))
            # rec.date_fin_project=datetime.strptime(str(rec.date_fin_project), "%Y-%m-%d")+timedelta(deference)


    # Cette méthode est utilisée pour créer une vue de formulaire pour l'assistant de création d'achat.
    def cree_une_achat(self):
        # Récupérer l'ID de la vue associée à l'assistant de création d'achat depuis une référence.
        view_id = self.env.ref('projet_riad.id_wizard_purchase_order').id
    
        return {
            'name': _('Assistant création achat'),  # Nom de la vue
            'type': 'ir.actions.act_window',
            'view_mode': 'form',  # Mode de vue (formulaire)
            'res_model': 'purchase.order.wizard',  # Modèle associé à l'assistant
            'view_id': view_id,  # ID de la vue
            'views': [(view_id, 'form')],  # Spécification des vues (dans ce cas, une vue de formulaire)
            'target':"new"            
        }
    @api.model
    def retrieve_data_test(self, userQuery,project_id):
        if project_id!=False and project_id!=True:
            
            for rec in self.env["user.filter"].sudo().search([]):
                    rec.unlink()

            if userQuery!="":
                partner=self.env["res.partner"].sudo().search([("name","=",str(userQuery))],limit=1)
                if partner:
                    user_id_F=self.env["res.users"].search([("partner_id","=",partner.id)],limit=1)
                    self.env["user.filter"].sudo().create({
                        "user_id":user_id_F.id
                    });
            user_tobe_filter_is=self.env["user.filter"].search([],limit=1)

            user = user_tobe_filter_is.user_id  if user_tobe_filter_is else self.env.user
            for rec in self.env["project.task"].search([("project_id","=",project_id)]):     
                    if  user.id in rec.user_ids.ids:
                        query = "UPDATE PROJECT_TASK SET is_mes_tach_suivi=%s WHERE ID=%s"
                        self.env.cr.execute(query, ("assigned",rec.id))
                    elif user.partner_id.id in rec.message_partner_ids.ids and user.id not in rec.user_ids.ids:
                        query = "UPDATE PROJECT_TASK SET is_mes_tach_suivi=%s WHERE ID=%s"
                        self.env.cr.execute(query, ("suived",rec.id))

                    else:
                        query = "UPDATE PROJECT_TASK SET is_mes_tach_suivi=%s WHERE ID=%s"
                        self.env.cr.execute(query, ("unsuived",rec.id))
            if self.id!=False:
                query = "SELECT count(*) FROM mail_followers WHERE res_model = %s and res_id=%s and partner_id=%s"
                self.env.cr.execute(query, ("project.task",self.id,user.partner_id.id))
                result = self.env.cr.fetchone()
                print(result)
    
                print("----")
            return True        
    # def action_view_documents_project_task(self):

    def merge_tasks(self):
        view_id = self.env.ref('projet_riad.merge_task').id

        return {

            'name': _('Fusionner Des Tâches'),

            # 'context': {"default_tasks":[[6,False,self.ids]] },  # Initialise le contexte avec l'ID du projet actuel
            'context': {"default_tasks":self.ids,"default_task_one":self.ids[0],"default_task_tow":self.ids[1] },  # Initialise le contexte avec l'ID du projet actuel

            'domain': [('tasks', '=',self.ids )],  # Filtre les enregistrements par projet_id égal à l'ID du projet actuel

            'type': 'ir.actions.act_window',

            'view_mode': 'form',

            'res_model': 'merge.task',

            'view_id': view_id,  # Utilise l'ID de la vue pour la nouvelle fenêtre

            'views': [(view_id, 'form')],

            'target': 'new'  # Ouvre la nouvelle fenêtre dans un nouvel onglet
        }


    def _message_get_suggested_recipients(self):
        recipients = super(project_task, self)._message_get_suggested_recipients()
        transformed_data = {key: [] for key in recipients}
        return transformed_data
    def _compute_display_name(self):
        """ Return the categories' display name, including their direct
            parent by default.
        """
        
        for c in self:
            c.display_name = str(c.name[:41])+'...' if len(c.name)>41 else str(c.name)+'...'