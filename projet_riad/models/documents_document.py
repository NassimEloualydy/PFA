from odoo import models,fields,api,_
from datetime import datetime,timedelta
import re
class documents_document(models.Model):
    _inherit="documents.document"
    project_id = fields.Many2one("project.project","Projet")

    def unlink(self):
        document = super(documents_document, self).unlink()
        # folders=self.env["documents.folder"].search([])
        # for folder in folders:
        #     query = "SELECT id, name, parent_path FROM documents_folder WHERE parent_path LIKE %s OR parent_path LIKE %s OR parent_path LIKE %s" 
        #     params = (str(folder.id) + '/%', '%' + str(folder.id) + '/%', '%' + str(folder.id) + '%')
        #     self.env.cr.execute(query, params)
        #     result = self.env.cr.fetchall()
        #     nbr_files=0
        #     for rec in result:
        #             nbr_files+=self.env["documents.document"].search_count([("folder_id","=",rec[0]),("active","=",True)])
        #     pattern = r'\(\d+\)'
        #     replacement ="("+str(nbr_files)+")"
        #     the_old_name_folder=folder.name
        #     the_new_name=re.sub(pattern, replacement, the_old_name_folder)
        #     query="UPDATE documents_folder SET name=jsonb_set(cast(name as jsonb),'{fr_FR}', %s,true) WHERE id=%s"
        #     self.env.cr.execute(query, ('"'+the_new_name+'"',folder.id))                                                           


        return document
    def write(self,vals):
         if "folder_id" in vals:
              self.env["ir.attachment"].sudo().search([("id","=",self.attachment_id.id)],limit=1).write({
                   "documents_folder_id":vals["folder_id"]
              })
         document = super(documents_document, self).write(vals)              
         return document
         if "folder_id" in vals:
              self.env["ir.attachment"].search([("id","=",self.attachment_id.id)],limit=1).write({
                   "documents_folder_id":vals["folder_id"]
              })
         folders=self.env["documents.folder"].search([])
         #update the project_id in the documents_document
         projects=self.env["project.project"].search([("active","in",[True,False])])
         
         for p in projects:
               folder_of_the_project=self.env["documents.folder"].search([("id","=",p.documents_folder_id.id)],limit=1)
               children=self.env["documents.folder"].search([("parent_path","like",str(folder_of_the_project.parent_path)+"%")],limit=1)
               for c in children:
                   documents_document_of_this_folder=self.env["documents.document"].search([("folder_id","=",c.id)])
                   for d in documents_document_of_this_folder:
                       query="UPDATE documents_document SET project_id=%s WHERE id=%s"

                       self.env.cr.execute(query, (p.id,d.id))                                                           

         #
         for folder in folders:
             query = "SELECT id, name, parent_path FROM documents_folder WHERE parent_path LIKE %s OR parent_path LIKE %s OR parent_path LIKE %s" 
             params = (str(folder.id) + '/%', '%/' + str(folder.id) , '%/' + str(folder.id) + '/%')
             self.env.cr.execute(query, params)
             result = self.env.cr.fetchall()
             nbr_files=0
             for rec in result:
                     nbr_files+=self.env["documents.document"].search_count([("folder_id","=",rec[0]),("active","=",True)])                     
             pattern = r'\(\d+\)'
             replacement ="("+str(nbr_files)+")"
             the_old_name_folder=folder.name
             
             the_new_name=re.sub(pattern, replacement, the_old_name_folder)
             if bool(re.search(pattern, the_old_name_folder))==False:
                    the_new_name=the_new_name+" (0)"                        
             query="UPDATE documents_folder SET name=jsonb_set(cast(name as jsonb),'{fr_FR}', %s,true) WHERE id=%s"
    
             self.env.cr.execute(query, ('"'+the_new_name+'"',folder.id))                                                           

         return document
            


    def create(self, vals):
        document = super(documents_document, self).create(vals)
        if document.folder_id.project_id:
             document.write({
                  "project_id":document.folder_id.project_id.id
             })             
        return document