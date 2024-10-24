from odoo import models,fields,api,_
from datetime import datetime,timedelta
import re
class mail_follower(models.Model):
    _inherit = ['mail.followers']

    def unlink(self):
        if len(self)==1 and self.res_model=="project.project":
            self.env['mail.channel.member'].search([("partner_id","=",self.partner_id.id),("channel_id","=",self.env["project.project"].search([("id","=",self.res_id)],limit=1).channel_id.id)]).unlink()
            tasks=self.env["project.task"].search([("project_id","=",self.res_id)])
            self.env["mail.followers"].search([("res_model","=","project.task"),("res_id","in",tasks.ids),('partner_id',"=",self.partner_id.id)]).unlink()
        if len(self)==1 and self.res_model=="project.task":
                user_filter=self.env["user.filter"].sudo().search([],limit=1)
                if not user_filter:
                    user_filter=""
                else:
                    user_filter=user_filter.user_id.partner_id.name
                project_id=self.env["project.task"].search([("id","=",self.res_id)],limit=1).project_id.id
                nbr_message_partner_ids=self.env["project.task"].search([("id","=",self.res_id)],limit=1).nbr_message_partner_ids
                nbr_message_partner_ids=nbr_message_partner_ids-1
                query = "UPDATE PROJECT_TASK SET nbr_message_partner_ids=%s WHERE ID=%s"                
                self.env.cr.execute(query, (nbr_message_partner_ids,self.res_id))                  
                self.env["project.task"].search([("id","=",self.res_id)],limit=1).retrieve_data_test(user_filter,project_id)
                user_filter=user_filter if user_filter!="" else self.env.user.partner_id.name
                if user_filter==self.partner_id.name:
                    query="UPDATE PROJECT_TASK SET is_mes_tach_suivi=%s WHERE ID=%s" 
                    self.env.cr.execute(query, ("unsuived",self.res_id))                  



        mial_follower=super(mail_follower, self).unlink()
        self.clear_caches()

        return mial_follower
    
    # def create(self,vals):
    #      user_filter=self.env["user.filter"].sudo().search([],limit=1)
    #      if not user_filter:
    #          user_filter=""
    #      else:
    #          user_filter=user_filter.user_id.partner_id.name
         
    #      if isinstance(vals,list):
    #          if "res_model" in vals[0]:
    #             if vals[0]["res_model"]=="project.project":
    #                 #send notification to project
    #                 self.env["project.project"].search([("id","=",vals[0]["res_id"]),('active','in',[True,False])],limit=1).message_post(
    #             body=_("Un Nouvel Abonné A été Ajouté : <strong>"+str(self.env["res.partner"].search([("id","=",vals[0]["partner_id"])]).name)+"</strong>"),
    #         )       
    #                 ## add it the to channel
    #                 self.env["mail.message"].create({
    #                     "body": _("Un Nouvel Abonné A été Ajouté : <strong>"+str(self.env["res.partner"].search([("id","=",vals[0]["partner_id"])]).name)+"</strong>"),
    #                     'email_from': '"' + self.env.user.partner_id.name + '" <' + self.env.user.login + '>',
    #                     'message_type': 'comment',
    #                     'subtype_id': 1,
    #                     'subject': False,
    #                     'model': 'mail.channel',
    #                     'res_id':self.env["project.project"].search([("id","=",vals[0]["res_id"]),('active','in',[True,False])],limit=1).channel_id.id,
    #                     'record_name': 'Chantier',
    #                 })

    #                 ## create a memeber 
    #                 partner_id=vals[0]["partner_id"]
    #                 channel_id=self.env["project.project"].search([("id","=",vals[0]["res_id"]),('active','in',[True,False])],limit=1).channel_id.id
                    
    #                 if channel_id:
    #                  if self.env["mail.channel.member"].search_count([("partner_id","=",partner_id),("channel_id","=",channel_id)])==0:
    #                      self.env['mail.channel.member'].create({
    #                          "partner_id":partner_id,
    #                          "channel_id":channel_id
    #                      })
    #                  ## let's add it to all tasks
                    
    #                 tasks=self.env["project.task"].search([("project_id","=",vals[0]["res_id"])])
    #                 tag_id_travaux=self.env["project.tags"].search([("name", "=", "Travaux")],limit=1)
    #                 for t in tasks:
    #                     if tag_id_travaux.id in t.tag_ids.ids:
    #                     #    vals_task="[{'res_model': 'project.task', 'partner_id': 3, 'res_id': 122}]"
    #                        vals_task=[{}]
    #                        vals_task[0]['res_model']='project.task'
    #                        vals_task[0]['res_id']=t.id
    #                        vals_task[0]['partner_id']=vals[0]['partner_id']
    #                        super(mail_follower, self).create(vals_task)


    #             if vals[0]["res_model"]=="project.task":              
    #                 self.env["project.task"].search([("id","=",vals[0]["res_id"]),('active','in',[True,False])],limit=1).message_post(
    #             body=_("Un Nouvel Abonné A été Ajouté : <strong>"+str(self.env["res.partner"].search([("id","=",vals[0]["partner_id"])]).name)+"</strong>"),
    #         )
    #                 self.env["mail.message"].create({
    #                     "body": _("Un Nouvel Abonné A été Ajouté : <strong>"+str(self.env["res.partner"].search([("id","=",vals[0]["partner_id"])]).name)+"</strong> <br/> Sur la tâche  :<strong>"+str(self.env["project.task"].search([("id","=",vals[0]["res_id"]),('active','in',[True,False])],limit=1).name)+"</strong>"),
    #                     'email_from': '"' + self.env.user.partner_id.name + '" <' + self.env.user.login + '>',
    #                     'message_type': 'comment',
    #                     'subtype_id': 1,
    #                     'subject': False,
    #                     'model': 'mail.channel',
    #                     'res_id':self.env["project.task"].search([("id","=",vals[0]["res_id"]),('active','in',[True,False])],limit=1).project_id.channel_id.id,
    #                     'record_name': 'Chantier',
    #                 })


    #                 nbr_message_partner_ids=self.env["project.task"].search([("id","=",vals[0]["res_id"])],limit=1).nbr_message_partner_ids
    #                 nbr_message_partner_ids=nbr_message_partner_ids+1
    #                 query = "UPDATE PROJECT_TASK SET nbr_message_partner_ids=%s WHERE ID=%s"                
    #                 self.env.cr.execute(query, (nbr_message_partner_ids,vals[0]["res_id"]))  
    #                 #test if you are a follwer of the project of this tasks
    #                 project_id=self.env["project.task"].search([("id","=",vals[0]["res_id"])],limit=1).project_id.id

    #                 self.env["project.task"].search([("id","=",vals[0]["res_id"])],limit=1).retrieve_data_test(user_filter,project_id)
    #                 user_filter=user_filter if user_filter!="" else self.env.user.partner_id.name
    #                 if user_filter==self.env["res.partner"].search([("id","=",vals[0]['partner_id'])],limit=1).name:
    #                     query="UPDATE PROJECT_TASK SET is_mes_tach_suivi=%s WHERE ID=%s" 
    #                     self.env.cr.execute(query, ("suived",vals[0]['res_id']))                  

    #             task_id=vals[0]['res_id']
    #             partner_id=vals[0]['partner_id']
    #             project_of_the_Task=self.env["project.task"].search([("id","=",task_id)],limit=1).project_id.id
    #             f_project=self.env["mail.followers"].search([("res_model","=","project.project"),("res_id","=",project_of_the_Task),("partner_id","=",partner_id)])
    #             if project_of_the_Task!=False:
    #                 if not f_project:
    #                     query = "INSERT INTO mail_followers (res_model,partner_id,res_id) values (%s,%s,%s)"
    #                     self.env.cr.execute(query, ("project.project",partner_id,project_of_the_Task))

    #     #         {'res_model': 'project.task', 'partner_id': 7530, 'subtype_ids': [(<Command.SET: 6>, 0, [1, 44])], 'res_id': 917}
    #      if isinstance(vals,dict):
    #          if "res_model" in vals:
    #             if vals["res_model"]=="project.project":    
    #                 self.env["project.project"].search([("id","=",vals["res_id"]),('active','in',[True,False])],limit=1).message_post(
    #             body=_("Un Nouvel Abonné A été Ajouté : <strong>"+str(self.env["res.partner"].search([("id","=",vals["partner_id"])]).name)+"</strong>"),
    #         )
    #                 self.env["mail.message"].create({
    #                     "body": _("Un Nouvel Abonné A été Ajouté : <strong>"+str(self.env["res.partner"].search([("id","=",vals["partner_id"])]).name)+"</strong>"),
    #                     'email_from': '"' + self.env.user.partner_id.name + '" <' + self.env.user.login + '>',
    #                     'message_type': 'comment',
    #                     'subtype_id': 1,
    #                     'subject': False,
    #                     'model': 'mail.channel',
    #                     'res_id':self.env["project.project"].search([("id","=",vals["res_id"]),('active','in',[True,False])],limit=1).channel_id.id,
    #                     'record_name': 'Chantier',
    #                 })

    #                 partner_id=vals["partner_id"]
    #                 channel_id=self.env["project.project"].search([("id","=",vals["res_id"]),('active','in',[True,False])],limit=1).channel_id.id  
    #                 if channel_id:
    #                  if self.env["mail.channel.member"].search_count([("partner_id","=",partner_id),("channel_id","=",channel_id)])==0:
    #                      self.env['mail.channel.member'].create({
    #                          "partner_id":partner_id,
    #                          "channel_id":channel_id
    #                      })
    #                 tasks=self.env["project.task"].search([("project_id","=",vals[0]["res_id"])])
    #                 tag_id_travaux=self.env["project.tags"].search([("name", "=", "Travaux")],limit=1)
    #                 for t in tasks:
    #                     if tag_id_travaux.id in t.tag_ids.ids:
    #                     #    vals_task="[{'res_model': 'project.task', 'partner_id': 3, 'res_id': 122}]"
    #                        vals_task=[{}]
    #                        vals_task[0]['res_model']='project.task'
    #                        vals_task[0]['res_id']=t.id
    #                        vals_task[0]['partner_id']=vals[0]['partner_id']
    #                     #    query = "DELETE FROM mail_followers WHERE res_id=%s AND res_model=%s"
    #                        query="INSERT INTO mail_followers (res_model,res_id,partner_id) VALUES (%s,%s,%s)"
    #                        self.env.cr.execute(query, ("project.task",t.id,vals[0]['partner_id']))

    #                         # super(mail_follower, self).create(vals)
                    
    #             if vals["res_model"]=="project.task":    
                    
    #                 self.env["project.task"].search([("id","=",vals["res_id"]),('active','in',[True,False])],limit=1).message_post(
    #             body=_("Un Nouvel Abonné A été Ajouté : <strong>"+str(self.env["res.partner"].search([("id","=",vals["partner_id"])]).name)+"</strong>"),
    #         )          
    #                 self.env["mail.message"].create({
    #                     "body": _("Un Nouvel Abonné A été Ajouté : <strong>"+str(self.env["res.partner"].search([("id","=",vals["partner_id"])]).name)+"</strong><br/> Sur la tâche  :<strong>"+str(self.env["project.task"].search([("id","=",vals["res_id"]),('active','in',[True,False])],limit=1).name)+"</strong>"),
    #                     'email_from': '"' + self.env.user.partner_id.name + '" <' + self.env.user.login + '>',
    #                     'message_type': 'comment',
    #                     'subtype_id': 1,
    #                     'subject': False,
    #                     'model': 'mail.channel',
    #                     'res_id':self.env["project.task"].search([("id","=",vals["res_id"]),('active','in',[True,False])],limit=1).project_id.channel_id.id,
    #                     'record_name': 'Chantier',
    #                 })

    #                 nbr_message_partner_ids=self.env["project.task"].search([("id","=",vals["res_id"])],limit=1).nbr_message_partner_ids
    #                 nbr_message_partner_ids=nbr_message_partner_ids+1
    #                 query = "UPDATE PROJECT_TASK SET nbr_message_partner_ids=%s WHERE ID=%s"                
    #                 self.env.cr.execute(query, (nbr_message_partner_ids,vals["res_id"]))  
    #                 project_id=self.env["project.task"].search([("id","=",vals["res_id"])],limit=1).project_id.id

    #                 self.env["project.task"].search([("id","=",vals["res_id"])],limit=1).retrieve_data_test(user_filter,project_id)
    #                 user_filter=user_filter if user_filter!="" else self.env.user.partner_id.name
    #                 if user_filter==self.env["res.partner"].search([("id","=",vals['partner_id'])],limit=1).name:
    #                     query="UPDATE PROJECT_TASK SET is_mes_tach_suivi=%s WHERE ID=%s" 
    #                     self.env.cr.execute(query, ("suived",vals['res_id']))                  
    #             task_id=vals['res_id']
    #             partner_id=vals['partner_id']
    #             project_of_the_Task=self.env["project.task"].search([("id","=",task_id)],limit=1).project_id.id
    #             f_project=self.env["mail.followers"].search([("res_model","=","project.project"),("res_id","=",project_of_the_Task),("partner_id","=",partner_id)])
    #             if not f_project:
    #                 if project_of_the_Task!=False:
    #                     query = "INSERT INTO mail_followers (res_model,partner_id,res_id) values (%s,%s,%s)"
    #                     self.env.cr.execute(query, ("project.project",partner_id,project_of_the_Task))

    #      mf = super(mail_follower, self).create(vals)              
    #      return mf;