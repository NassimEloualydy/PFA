from odoo import models,fields,api,_
from datetime import datetime,timedelta
import re
class documents_folder(models.Model):
    _rec_name = "name"
    _inherit="documents.folder"
    project_id=fields.Many2one("project.project","Projet")
    # display_name=fields.Char("Display Name")
    active=fields.Boolean(string="Active",default=True)

    # @api.depends(lambda self: (self._rec_name,) if self._rec_name else ())
    # def _compute_display_name(self):
    #     """Compute the value of the `display_name` field.

    #     The `display_name` field is a textual representation of the record.
    #     This method can be overridden to change the representation.  If needed,
    #     it can be made field-dependent using :attr:`~odoo.api.depends` and
    #     context-dependent using :attr:`~odoo.api.depends_context`.
    #     """
    #     if self._rec_name:
    #         convert = self._fields[self._rec_name].convert_to_display_name
    #         for record in self:
    #             record.display_name = convert(record[self._rec_name], record)
    #     else:
    #         for record in self:
    #             record.display_name = f"{record._name},{record.id}"
    @api.model
    def create(self,vals):

        if self._context.get("default_res_model")=="project.project":
             id_project=self._context.get('active_id')
             parent_folder_id=self.env["project.project"].search([("id","=",id_project)],limit=1).documents_folder_id.id 
             vals["parent_folder_id"]=parent_folder_id
        
        document_folder = super(documents_folder, self).create(vals)
        document_folder.name=document_folder.name+" ("+str(document_folder.document_count)+")"
        return document_folder
    
    # @api.model
    def write(self,vals):
        if "active" in vals:
            if vals["active"]==False:
                archive_folder=self.env["documents.folder"].search([("name","like","Projets Archivés%"),("parent_folder_id","=",False)])
                if not archive_folder:
                    self.env["documents.folder"].create({
                        "name":"Archivé"
                    })
                parent_foler=self.env["documents.folder"].search([("name","like","Projets Archivés%"),("parent_folder_id","=",False)],limit=1).id
                vals["parent_folder_id"]=parent_foler
            if vals["active"]==True:
                parent_foler=self.env["documents.folder"].search([("name","like","Chantier%"),("parent_folder_id","=",False)],limit=1).id
                vals["parent_folder_id"]=parent_foler
        # name_of_the_folder=self.name.splite('(')[0]
        vals["active"]=True
        # input_string=self.name if "name" not in vals else vals["name"]
        # pattern = r'^.*?(?=\s\(\d+\)$)'
        
        # Extract the desired part using regular expression
        # if self.parent_folder_id:
        #     result = re.match(pattern, input_string).group(0) if re.match(pattern, input_string)!=None else input_string
        #     nbr_chidren_document=self.env["documents.document"].search_count([("folder_id.parent_folder_id","=",self.id)])
        #     vals["name"]=result+" ("+str(self.document_count+nbr_chidren_document)+")"
        # else:
        #     result = re.match(pattern, input_string).group(0) if re.match(pattern, input_string)!=None else input_string
        #     # nbr_chidren_document=self.env["documents.document"].search_count([("folder_id.parent_folder_id","=",self.id)])
        #     nbr_folder=self.env["documents.folder"].search_count([("parent_folder_id","=",self.id)])
        #     vals["name"]=result+" ("+str(nbr_folder)+")"
        # if "parent_folder_id" in vals:
        #     print(vals["parent_folder_id"])
        #     print("---")
        if "parent_folder_id" in vals:
            vals["project_id"]=self.env["documents.folder"].search([("id","=",vals["parent_folder_id"])],limit=1).project_id.id
            #              print(rec.res_model_name)
            #  print(rec.res_name)
            #  print("---")

            self.env["documents.document"].search([("folder_id","=",self.id)]).write({
                "project_id":vals["project_id"],
                "res_id":vals["project_id"],
            })
            self.env["ir.attachment"].search([("documents_folder_id","=",self.id)]).write({
                "projet_id":vals["project_id"]
            })

        document_folder = super(documents_folder, self).write(vals)

        return document_folder
    # @api.depends('name')
    # def _compute_display_name(self):
        
    #     for record in self.env["documents.folder"].sudo().search([("active","in",[True,False])]):
    #         record.display_name=re.sub(r'\s*\(\d+\)$', '',record.with_context(lang='fr_FR').name)
    #         record.write({
    #             "name": re.sub(r'\s*\(\d+\)$', '',record.with_context(lang='fr_FR').name)
    #         })
    @api.model
    def archive_folder(self,res_id):
        archive_folder=self.env["documents.folder"].search([("name","like","Projets Archivés%"),("parent_folder_id","=",False)],limit=1).name
        chantier_folder=self.env["documents.folder"].search([("name","like","Chantier%"),("parent_folder_id","=",False)],limit=1).name
        is_archive_f=False if self.env["documents.folder"].search([("id","=",res_id)],limit=1).parent_folder_id.name==chantier_folder else True
        self.env["documents.folder"].search([("id","=",res_id)],limit=1).write({
            "active":is_archive_f
        })
    @api.model
    def is_archive(self,res_id):
        archive_folder=self.env["documents.folder"].search([("name","like","Projets Archivés%"),("parent_folder_id","=",False)],limit=1).name
        chantier_folder=self.env["documents.folder"].search([("name","like","Chantier%"),("parent_folder_id","=",False)],limit=1).name
        parent_folder_name=""
        if self.env["documents.folder"].search([("id","=",res_id)],limit=1).parent_folder_id.name==archive_folder:
             parent_folder_name  ="Archive"     
        if self.env["documents.folder"].search([("id","=",res_id)],limit=1).parent_folder_id.name==chantier_folder:
             parent_folder_name  ="Chantier"     
        return parent_folder_name
    