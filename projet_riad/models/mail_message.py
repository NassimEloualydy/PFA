"""
 if somone post message in the pv or in the task or in the project
 this message must be posted to in the channel of this project
"""
from odoo import models,fields,api,_
from datetime import datetime,timedelta,date
from odoo.exceptions import ValidationError

class mail_message(models.Model):
    _inherit="mail.message"
    @api.model    
    def create(self,vals):
        if isinstance(vals,list):

         if "subtype_id" in vals[0] and vals[0]["subtype_id"]==1:
             if vals[0]["model"]=="crm.lead":                      
                 if  "attachment_ids" in vals[0] or vals[0]['body']!="":
                     type_crm="Opportunité" if self.env["crm.lead"].search([("id","=",vals[0]['res_id'])],limit=1).type=="opportunity" else "Piste"
                     self.env["mail.message"].create({
                                     "email_from": vals[0]["author_id"],
                                     'body':"Message envoyé par <span class='fw-bolder'>"+str(self.env["res.partner"].search([("id","=",vals[0]["author_id"])],limit=1).name)+"</span> <br/> sur le "+type_crm+" <span class='fw-bolder'>"+str(self.env["crm.lead"].search([("id","=",vals[0]['res_id'])],limit=1).name)+"</span> :<br/> "+vals[0]["body"],
                                     'message_type': 'comment',
                                     'subtype_id': 1,
                                     'subject': False,
                                     'model': 'mail.channel',
                                    #  'res_id': self.env["mail.channel"].search([("name","like",str(self.env["project.pv"].search([("id","=",vals[0]['res_id'])],limit=1).projet_id.with_context(lang='fr_FR').name)+'%'),("channel_type","=","channel")],limit=1).id,
                                    'res_id': self.env["mail.channel"].search([("name","=","CRM"),("channel_type","=","channel")],limit=1).id,
                                     'record_name': 'CRM',
                                     'attachment_ids':vals[0]["attachment_ids"] if "attachment_ids" in vals[0] else []
                                 })


             if vals[0]["model"]=="account.move":                      
                 if  "attachment_ids" in vals[0] or vals[0]['body']!="":
                     channel_id=self.env["mail.channel"].search([("name","=","Situation des décomptes")],limit=1).id
                     
                     self.env["mail.message"].create({
                                     "email_from": vals[0]["author_id"],
                                     'body':"Message envoyé par <span class='fw-bolder'>"+str(self.env["res.partner"].search([("id","=",vals[0]["author_id"])],limit=1).name)+"</span><br/> sur la facture suivant <span class='fw-bolder'>"+str(self.env["account.move"].search([("id","=",vals[0]['res_id'])],limit=1).name)+"</span> :<br/> "+vals[0]["body"],
                                     'message_type': 'comment',
                                     'subtype_id': 1,
                                     'subject': False,
                                     'model': 'mail.channel',
                                    #  'res_id': self.env["mail.channel"].search([("name","like",str(self.env["project.pv"].search([("id","=",vals[0]['res_id'])],limit=1).projet_id.with_context(lang='fr_FR').name)+'%'),("channel_type","=","channel")],limit=1).id,
                                     'res_id': channel_id,
                                     'record_name': 'Chantier',
                                     'attachment_ids':vals[0]["attachment_ids"] if "attachment_ids" in vals[0] else []
                                 })
             if vals[0]["model"]=="account.payment":                      
                 if  "attachment_ids" in vals[0] or vals[0]['body']!="":
                     channel_id=self.env["mail.channel"].search([("name","=","Situation des décomptes")],limit=1).id
                     
                     self.env["mail.message"].create({
                                     "email_from": vals[0]["author_id"],
                                     'body':"Message envoyé par <span class='fw-bolder'>"+str(self.env["res.partner"].search([("id","=",vals[0]["author_id"])],limit=1).name)+"</span><br/> sur la paiment suivant <span class='fw-bolder'>"+str(self.env["account.payment"].search([("id","=",vals[0]['res_id'])],limit=1).name)+"</span> :<br/> "+vals[0]["body"],
                                     'message_type': 'comment', 
                                     'subtype_id': 1,
                                     'subject': False,
                                     'model': 'mail.channel',
                                    #  'res_id': self.env["mail.channel"].search([("name","like",str(self.env["project.pv"].search([("id","=",vals[0]['res_id'])],limit=1).projet_id.with_context(lang='fr_FR').name)+'%'),("channel_type","=","channel")],limit=1).id,
                                     'res_id': channel_id,
                                     'record_name': 'Chantier',
                                     'attachment_ids':vals[0]["attachment_ids"] if "attachment_ids" in vals[0] else []
                                 })


             if vals[0]["model"]=="project.pv":                      
                 if  "attachment_ids" in vals[0] or vals[0]['body']!="" and "Vous avez été assigné à Tâche" not in vals[0]['body'] and " vous a invité a suivre" not in vals[0]["body"]:
                     self.env["mail.message"].create({
                                     "email_from": vals[0]["author_id"],
                                     'body':"Message envoyé par <span class='fw-bolder'>"+str(self.env["res.partner"].search([("id","=",vals[0]["author_id"])],limit=1).name)+"</span> <br/> sur le PV <span class='fw-bolder'>"+str(self.env["project.pv"].search([("id","=",vals[0]['res_id'])],limit=1).nom)+"</span> :<br/> "+vals[0]["body"],
                                     'message_type': 'comment',
                                     'subtype_id': 1,
                                     'subject': False,
                                     'model': 'mail.channel',
                                    #  'res_id': self.env["mail.channel"].search([("name","like",str(self.env["project.pv"].search([("id","=",vals[0]['res_id'])],limit=1).projet_id.with_context(lang='fr_FR').name)+'%'),("channel_type","=","channel")],limit=1).id,
                                     'res_id': self.env["project.pv"].search([("id","=",vals[0]['res_id'])],limit=1).projet_id.channel_id.id,
                                     'record_name': 'Chantier',
                                     'attachment_ids':vals[0]["attachment_ids"] if "attachment_ids" in vals[0] else []
                                 })

             if vals[0]["model"]=="project.task":     
                 if "attachment_ids" in vals[0] or vals[0]['body']!="" and "Vous avez été assigné à Tâche" not in vals[0]['body'] and " vous a invité a suivre" not in vals[0]["body"]:
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
                    rec=self.env["project.task"].search([("id","=",vals[0]['res_id'])],limit=1)
                    partnsers=""
                    for p in rec.user_ids:
                        partnsers+=str(p.partner_id.name)+" ,"   

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
                    
                    target_date = datetime.strptime(str(rec.date_fin_project), "%Y-%m-%d")  # Date de début
                    current_date = datetime.now()  # Date actuelle
                    delta = target_date - current_date  # Calcul de la différence entre la date cible et la date actuelle
                    days_remaining = delta.days  # Nombre de jours restants jusqu'à la date cible
                    days_remaining = days_remaining + 1  # Ajout d'un jour car 'delta' ne tient pas compte de la date actuelle

                    body_message_main_info = "<span class='fw-bolder text-danger'> Rappel<br/></span>"
                    body_message_main_info += "Tâche : <span class='fw-bolder'>" + rec.name + "</span><br/>"
                    body_message_main_info += "Assigné à : <span class='fw-bolder'>" + str(partnsers) + "</span><br/>"
                    body_message_main_info += "Date de début : <span class='fw-bolder'>" + formatted_date_french + "</span><br/>"
                    body_message_main_info += "Date de fin : <span class='fw-bolder text-danger'>" + formatted_date_french_end + "</span><br/>"
                    body_message_main_info += "Durée de tâche : <span class='fw-bolder text-danger'>" + str(rec.duree_de_tach) + "</span><br/>"
                    body_message="Message envoyé par <span class='fw-bolder'>"+str(self.env["res.partner"].search([("id","=",vals[0]["author_id"])],limit=1).name)+"</span> <br/>  "+vals[0]["body"]+"<br/>" if vals[0]["body"]!="" else "Message envoyé par <span class='fw-bolder'>"+str(self.env["res.partner"].search([("id","=",vals[0]["author_id"])],limit=1).name)+"</span> <br/> "+vals[0]["body"]

                    self.env["mail.message"].create({
                                     "email_from": vals[0]["author_id"],
                                     "body":body_message_main_info+""+body_message+"<span class='fw-bolder text-danger'> Il reste "+str(days_remaining)+" Jours pour la fin de cette Tache. </span>",
                                     'message_type': 'comment',
                                     'subtype_id': 1,
                                     'subject': False,
                                     'model': 'mail.channel',
                                     'res_id': self.env["project.task"].search([("id","=",vals[0]['res_id'])],limit=1).project_id.channel_id.id,
                                     'record_name': 'Chantier',
                                     'attachment_ids':vals[0]["attachment_ids"] if "attachment_ids" in vals[0] else []
                                 })
             if vals[0]["model"]=="project.project":                      
                 if  "attachment_ids" in vals[0] or vals[0]['body']!="" and vals[0]['body']!="Projet créé" and " vous a invité a suivre" not in vals[0]["body"]:
                     print(vals[0]["attachment_ids"])
                     self.env["mail.message"].create({
                                     "email_from": vals[0]["author_id"],
                                     'body':"Message envoyé par <span class='fw-bolder'>"+str(self.env["res.partner"].search([("id","=",vals[0]["author_id"])],limit=1).name)+"</span>  :<br/> "+vals[0]["body"],
                                     'message_type': 'comment',
                                     'subtype_id': 1,
                                     'subject': False,
                                     'model': 'mail.channel',
                                     'res_id': self.env["project.project"].search([("id","=",vals[0]['res_id'])],limit=1).channel_id.id,
                                     'record_name': 'Chantier',
                                     'attachment_ids':vals[0]["attachment_ids"] if "attachment_ids" in vals[0] else []
                                 })
        if isinstance(vals,dict):
            if "subtype_id" in vals and vals["subtype_id"]==1:
             if vals["model"]=="crm.lead":
                 if "attachment_ids"  in vals or vals['body']!="":
                     type_crm="Opportunité" if self.env["crm.lead"].search([("id","=",vals['res_id'])],limit=1).type=="opportunity" else "Piste"

                     self.env["mail.message"].create({
                                     "email_from": vals["author_id"],
                                     'body':"Message envoyé par <span class='fw-bolder'>"+str(self.env["res.partner"].search([("id","=",vals["author_id"])],limit=1).name)+"</span> <br/> sur le "+type_crm+" <span class='fw-bolder'>"+str(self.env["crm.lead"].search([("id","=",vals['res_id'])],limit=1).name)+"</span> :<br/> "+vals["body"],
                                     'message_type': 'comment',
                                     'subtype_id': 1,
                                     'subject': False,
                                     'model': 'mail.channel',
                                     'res_id': self.env["mail.channel"].search([("name","=","CRM"),("channel_type","=","channel")],limit=1).id,
                                     'record_name': 'CRM',
                                     'attachment_ids':vals["attachment_ids"] if "attachment_ids" in vals else []
                                 })
             
             if vals["model"]=="account.payment":
                 if "attachment_ids"  in vals or vals['body']!="":                     
                     channel_id=self.env["mail.channel"].search([("name","=","Situation des décomptes")],limit=1).id

                     self.env["mail.message"].create({
                                     "email_from": vals["author_id"],
                                     'body':"Message envoyé par <span class='fw-bolder'>"+str(self.env["res.partner"].search([("id","=",vals["author_id"])],limit=1).name)+"</span> <br/> sur le paiment <span class='fw-bolder'>"+str(self.env["account.payment"].search([("id","=",vals['res_id'])],limit=1).name)+"</span> :<br/> "+vals["body"],
                                     'message_type': 'comment',
                                     'subtype_id': 1,
                                     'subject': False,
                                     'model': 'mail.channel',
                                     'res_id': channel_id,
                                     'record_name': 'Chantier',
                                     'attachment_ids':vals["attachment_ids"] if "attachment_ids" in vals else []
                     })

             if vals["model"]=="account.move":
                 if "attachment_ids"  in vals or vals['body']!="":                     
                     channel_id=self.env["mail.channel"].search([("name","=","Situation des décomptes")],limit=1).id

                     self.env["mail.message"].create({
                                     "email_from": vals["author_id"],
                                     'body':"Message envoyé par <span class='fw-bolder'>"+str(self.env["res.partner"].search([("id","=",vals["author_id"])],limit=1).name)+"</span> <br/> sur la Facture <span class='fw-bolder'>"+str(self.env["account.move"].search([("id","=",vals['res_id'])],limit=1).name)+"</span> :<br/> "+vals["body"],
                                     'message_type': 'comment',
                                     'subtype_id': 1,
                                     'subject': False,
                                     'model': 'mail.channel',
                                     'res_id': channel_id,
                                     'record_name': 'Chantier',
                                     'attachment_ids':vals["attachment_ids"] if "attachment_ids" in vals else []
                     })
             if vals["model"]=="project.pv":
                 if "attachment_ids"  in vals or vals['body']!="" and "Vous avez été assigné à Tâche" not in vals['body'] and " vous a invité a suivre" not in vals["body"]:
                    
                     self.env["mail.message"].create({
                                     "email_from": vals["author_id"],
                                     'body':"Message envoyé par <span class='fw-bolder'>"+str(self.env["res.partner"].search([("id","=",vals["author_id"])],limit=1).name)+"</span> <br/> sur le PV <span class='fw-bolder'>"+str(self.env["project.pv"].search([("id","=",vals['res_id'])],limit=1).nom)+"</span> :<br/> "+vals["body"],
                                     'message_type': 'comment',
                                     'subtype_id': 1,
                                     'subject': False,
                                     'model': 'mail.channel',
                                     'res_id': self.env["project.pv"].search([("id","=",vals['res_id'])],limit=1).projet_id.channel_id.id,
                                     'record_name': 'Chantier',
                                     'attachment_ids':vals["attachment_ids"] if "attachment_ids" in vals else []
                                 })

             if vals["model"]=="project.task":                      
                 if "attachment_ids" in vals or vals['body']!="" and "Vous avez été assigné à Tâche" not in vals['body'] and " vous a invité a suivre" not in vals["body"]:
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
                    rec=self.env["project.task"].search([("id","=",vals['res_id']),("active","in",[True,False])],limit=1)
                    partnsers=""
                    for p in rec.user_ids:
                        partnsers+=str(p.partner_id.name)+" ,"   

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
                    
                    target_date = datetime.strptime(str(rec.date_fin_project), "%Y-%m-%d")  # Date de début
                    current_date = datetime.now()  # Date actuelle
                    delta = target_date - current_date  # Calcul de la différence entre la date cible et la date actuelle
                    days_remaining = delta.days  # Nombre de jours restants jusqu'à la date cible
                    days_remaining = days_remaining + 1  # Ajout d'un jour car 'delta' ne tient pas compte de la date actuelle

                    body_message_main_info = "<span class='fw-bolder text-danger'> Rappel<br/></span>"
                    body_message_main_info += "Tâche : <span class='fw-bolder'>" + rec.name + "</span><br/>"
                    body_message_main_info += "Assigné à : <span class='fw-bolder'>" + str(partnsers) + "</span><br/>"
                    body_message_main_info += "Date de début : <span class='fw-bolder'>" + formatted_date_french + "</span><br/>"
                    body_message_main_info += "Date de fin : <span class='fw-bolder text-danger'>" + formatted_date_french_end + "</span><br/>"
                    body_message_main_info += "Durée de tâche : <span class='fw-bolder text-danger'>" + str(rec.duree_de_tach) + "</span><br/>"
                    body_message="Message envoyé par <span class='fw-bolder'>"+str(self.env["res.partner"].search([("id","=",vals["author_id"])],limit=1).name)+"</span> <br/> "+vals["body"]+"<br/>" if vals["body"]!='' else "Message envoyé par <span class='fw-bolder'>"+str(self.env["res.partner"].search([("id","=",vals["author_id"])],limit=1).name)+"</span> <br/> "+vals["body"]
                    self.env["mail.message"].create({
                                            "email_from": vals["author_id"],
                                            "body":body_message_main_info+""+body_message+"<span class='fw-bolder text-danger'> Il reste "+str(days_remaining)+" Jours pour la fin de cette Tache. </span>",
                                            'message_type': 'comment',
                                            'subtype_id': 1,
                                            'subject': False,
                                            'model': 'mail.channel',
                                            'res_id': self.env["project.task"].search([("id","=",vals['res_id'])],limit=1).project_id.channel_id.id,
                                            'record_name': 'Chantier',
                                            'attachment_ids':vals["attachment_ids"] if "attachment_ids" in vals else []
                                        })
    
             if vals["model"]=="project.project":         
                 if  "attachment_ids" in vals or vals['body']!="" and vals['body']!="Projet créé" and " vous a invité a suivre" not in vals["body"] and " vous a invité a suivre" not in vals["body"]:
                    self.env["mail.message"].create({
                                    "email_from": vals["author_id"] if "author_id" in vals else None,
                                    'body':"Message envoyé par <span class='fw-bolder'>"+str(self.env["res.partner"].search([("id","=",vals["author_id"])],limit=1).name)+"</span> :<br/> "+vals["body"],
    
                                    'message_type': 'comment',
                                    'subtype_id': 1,
                                    'subject': False,
                                    'model': 'mail.channel',
                                    'res_id': self.env["project.project"].search([("id","=",vals['res_id'])],limit=1).channel_id.id,
                                    'record_name': 'Chantier',
                                    'attachment_ids':vals["attachment_ids"] if "attachment_ids" in vals else []
    
                                })
                         
        return super(mail_message, self.with_context(mail_create_nosubscribe=True)).create(vals)              