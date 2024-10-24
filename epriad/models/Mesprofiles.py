import json
from odoo import models, fields, api


class MonCompte(models.Model):

    _name = 'riad.profiles'
    

    classes = fields.Char("classes")
    villes = fields.Char("villes")
    motcle1 = fields.Char("motcle1")
    motcle2= fields.Char("motcle2")
    motcle3= fields.Char("motcle3")
    DatEnt = fields.Char("DatEnt")
    DatEt= fields.Char("DatEt")
    CautEnt= fields.Char("CautEnt")
    CautEt= fields.Char("CautEt")
    BudgEnt= fields.Char("BudgEnt")
    BudgEt= fields.Char("BudgEt")
    ordre= fields.Char("ordre")
    refe= fields.Char("refe")
    EtOu1= fields.Char("EtOu1")
    EtOu2= fields.Char("EtOu2")
    
    

    @api.model
    def ajouterProfile(self, classes, villes, motcle1, motcle2, motcle3, DatEnt, DatEt, CautEnt, CautEt, BudgEnt, BudgEt, ordre, refe, EtOu1, EtOu2):
      profile = self.env['riad.profiles'].search([], limit=1)
      vals = {
          'classes': json.dumps(classes),
          'villes': json.dumps(villes),
          'motcle1': motcle1,
          'motcle2': motcle2,
          'motcle3': motcle3,
          'DatEnt': DatEnt,
          'DatEt': DatEt,
          'CautEnt': CautEnt,
          'CautEt': CautEt,
          'BudgEnt': BudgEnt,
          'BudgEt': BudgEt,
          'ordre': ordre,
          'refe': refe,
          'EtOu1': EtOu1,
          'EtOu2': EtOu2
      }

      if profile:
          # Update the existing record
          profile.write(vals)
      else:
          # Create a new record
          self.env['riad.profiles'].create(vals)

       

    @api.model
    def getProfile(self):         
         profile = self.env['riad.profiles'].search([], limit=1)

         if not profile :
             return None
         
         P={
            "classes": profile.classes,
            "villes": profile.villes,
            "motcle1": profile.motcle1,
            "motcle2": profile.motcle2,
            "motcle3": profile.motcle3,
            "DatEnt": profile.DatEnt,
            "DatEt": profile.DatEt,
            "CautEnt": profile.CautEnt,
            "CautEt": profile.CautEt,
            "BudgEnt": profile.BudgEnt,
            "BudgEt": profile.BudgEt,
            "ordre": profile.ordre,
            "refe": profile.refe,
            "EtOu1": profile.EtOu1,
            "EtOu2": profile.EtOu2       
            }
         
         return json.dumps(P,ensure_ascii=False)

