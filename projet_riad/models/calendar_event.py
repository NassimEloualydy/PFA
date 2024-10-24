from odoo import api, fields, models
from datetime import datetime,timedelta


class calendar_event(models.Model):
    _inherit = 'calendar.event'


    project_id=fields.Many2one("project.project",string="Chantier")
    name_project=fields.Char("Nom projet",related="project_id.name")
    duree=fields.Char("Duree")
    state=fields.Char("state")
    res_modeeel_id=fields.Char("Projet",related="res_model_id.name")    
    new_name=fields.Char(string="Projet",compute="_change_name")    
    
    @api.depends('res_modeeel_id')
    def _change_name(self):
        for record in self:
            # if record.res_modeeel_id == "Piste/Opportunité":
            #     record.new_name = "CRM"
            if record.res_modeeel_id == "Tâche":
                record.new_name = "Tâche"
            else:
                record.new_name = ""
                 
            # else:
            #     record.new_name = "PV"
                 

    
    # task_id=fields.Many2one("project.task",string="task_id")
    # crm_lead=fields.Many2one("crm.lead",string="crm_lead")
    
    def create(self,vals):        
        if "res_model" not in vals:
            calendar = super(calendar_event, self).create(vals)
            return calendar
        if "res_model" in vals and vals["res_mode"]=='project.task':
            if calendar.res_model_id.name=="Tâche":
                tach=self.env["project.task"].search([("id","=",calendar.res_id)],limit=1)
                if tach.date_fin_project is not False:
                        deference=(tach.date_debut-tach.date_fin_project).days
                        deference=abs(deference)
                        date_fin=calendar.start+timedelta(days=deference)
                        calendar.stop=date_fin
                        calendar.duree=f"{deference} jours"
                        calendar.state=tach.stage_id.name


            return calendar

    def write(self,vals):
        # Crée une pièce jointe en utilisant la méthode create de la classe parente (superclasse)
        calendar = super(calendar_event, self).write(vals)
        if "start" in vals and calendar:
            if self.res_model_id.name=="Tâche":
                tach=self.env["project.task"].search([("id","=",self.res_id)],limit=1)
                
                if tach.date_fin_project is not False:
                    deference=(tach.date_debut-tach.date_fin_project).days
                    deference=abs(deference)
                    date_fin=self.start+timedelta(days=deference)
                    self.stop=date_fin
                    self.duree=f"{deference} jours"
                    self.state=tach.stage_id.name

                    query="UPDATE project_task SET date_debut=%s,date_fin_project=%s WHERE id=%s"
                    self.env.cr.execute(query, (str(self.start),str(date_fin),str(tach.id)))
                else:
                    query="UPDATE project_task SET date_debut=%s WHERE id=%s"
                    self.env.cr.execute(query, (self.start,tach.id))         
            if self.res_model_id.name=="Piste/Opportunité":
                    crm=self.env["crm.lead"].search([("id","=",self.res_id)],limit=1)
                    if crm.date_deadline is not False:
                            query="UPDATE crm_lead SET date_deadline=%s WHERE id=%s"
                            self.env.cr.execute(query, (self.start,crm.id))                                                           
        calendar = super(calendar_event, self).write(vals)
        return calendar
    def _compute_display_name(self):
        """ Return the categories' display name, including their direct
            parent by default.
        """
        
        for c in self:
             c.display_name = str(c.name[:41])+'...' if len(c.name)>41 else str(c.name)+'...'