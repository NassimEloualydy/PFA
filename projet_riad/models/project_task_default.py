from odoo import models,fields,api,_
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from datetime import date
class project_task_default(models.Model):
    
    # Définition du modèle "project.task.default"
    _name = "project.task.default"
    
    # Champ pour la date de début de la tâche
    date_debut = fields.Date("date_debut", required=True)
    
    # Champ pour la date de fin de la tâche
    date_fin = fields.Date("date_fin", required=True)
    
    # Champ pour le nom de la tâche
    name = fields.Char("name", required=True)
    
    # Champ pour le type de tâche (Admin ou Installation)
    type_task = fields.Selection([('Admin', 'Admin'), ('Installation', 'Installation')], required=True)
    
    # Champ pour stocker l'ID du projet auquel cette tâche est attribuée
    id_project_assign_to = fields.Integer("id_project_assign_to")
    is_task_initial=fields.Boolean("La tâche de départ")
    the_start_task=fields.Many2one("project.task.default",string="Tâche Procédures")
    nbr_days_task_start=fields.Integer(string="Procédures")
    sequece=fields.Integer(string="Séquence")
    # Définition de la méthode "write" pour le modèle "project.task.default"

    def write(self, vals):
        # Initialisation des variables date_debut et date_fin
        date_debut = None
        date_fin = None
        # # Vérification si les champs 'date_debut' ou 'date_fin' sont présents dans les valeurs à mettre à jour
        # if 'date_debut' in vals or 'date_fin' in vals:
        #     # Vérification de la présence de 'date_debut' dans les valeurs
        #     if 'date_debut' in vals:
        #         date_debut = vals["date_debut"]
        #     # Vérification de la présence de 'date_fin' dans les valeurs
        #     if 'date_fin' in vals:
        #         date_fin = vals["date_fin"]
            
        #     # Si 'date_debut' est présent dans les valeurs, on utilise sa valeur, sinon on récupère la date de début existante
        #     date_debut = date_debut if date_debut is not None else str(self.env["project.task.default"].search([("id", "=", self.id)], limit=1).date_debut)
        #     # Si 'date_fin' est présent dans les valeurs, on utilise sa valeur, sinon on récupère la date de fin existante
        #     date_fin = date_fin if date_fin is not None else str(self.env["project.task.default"].search([("id", "=", self.id)], limit=1).date_fin)
            
        #     # Conversion des dates en objets datetime
        #     date_debut = datetime.strptime(str(date_debut), '%Y-%m-%d')
        #     date_fin = datetime.strptime(str(date_fin), '%Y-%m-%d')
            
        #     # Calcul de la différence de jours entre date_debut et date_fin
        #     delta = date_fin - date_debut
        #     days_remaining = delta.days
            
        #     # Vérification que la date de fin est supérieure à la date de début
        #     if days_remaining <= 0:
        #         raise ValidationError(_("S'il vous plaît, la date de fin doit être supérieure à la date de début"))
    
        #     # Calcul du nombre de jours ouvrables (sans samedis) entre date_debut et date_fin
        #     curent_date = date_debut
        #     days_added = 0
        #     while curent_date <= date_fin:
        #         if curent_date.strftime('%A') == 'Saturday':
        #             days_added += 1
        #         curent_date += timedelta(days=1)
            
        #     # Ajout des jours ouvrables supplémentaires à la date de fin
        #     date_fin = date_fin + timedelta(days=days_added)
        #     # Mise à jour de la valeur de 'date_fin' dans les valeurs à écrire
        #     vals["date_fin"] = date_fin.strftime('%Y-%m-%d')
    
        # # Appel de la méthode "write" de la classe parente
        return super().write(vals)


    # Définition de la méthode "create" pour le modèle "project.task.default"
    @api.model
    def create(self, vals_list):
        # Conversion des dates de début et de fin en objets datetime
        date_debut = datetime.strptime(vals_list["date_debut"], '%Y-%m-%d')
        date_fin = datetime.strptime(vals_list["date_fin"], '%Y-%m-%d')
    
        # Calcul de la différence de jours entre date_debut et date_fin
        delta = date_fin - date_debut
        days_remaining = delta.days
    
        # Vérification que la date de fin est supérieure à la date de début
        if days_remaining <= 0:
            raise ValidationError(_("S'il vous plaît, la date de fin doit être supérieure à la date de début"))
    
        # Initialisation des variables pour le calcul des jours ouvrables
        curent_date = date_debut
        days_added = 0
    
        # Boucle pour parcourir les jours entre date_debut et date_fin
        while curent_date <= date_fin:
            # Si le jour courant est un samedi, on incrémente le compteur des jours ouvrables supplémentaires
            if curent_date.strftime('%A') == 'Saturday':
                days_added += 1
            # Passage au jour suivant
            curent_date += timedelta(days=1)
    
        # Ajout des jours ouvrables supplémentaires à la date de fin
        date_fin = date_fin + timedelta(days=days_added)
        # Mise à jour de la valeur de 'date_fin' dans les valeurs à créer
        vals_list["date_fin"] = date_fin.strftime('%Y-%m-%d')
    
        # Appel de la méthode "create" de la classe parente pour créer l'enregistrement
        return super().create(vals_list)

    # Définition de la méthode "insert_data"
    def insert_data(self):
        
        # Recherche des tags "Admin" et "Installation"
        is_tag_admin = self.env["project.tags"].search([("name", "=", "Admin")])
        is_tag_chantier = self.env["project.tags"].search([("name", "=", "Installation")])
        starting_date=self.env["project.task.default"].search([("is_task_initial","=",True)],limit=1).date_debut
        # for rec in self.env["project.task.default"].search([]):
            # print("starting date ")
            # print(starting_date)
            # print(rec.date_debut)
            # print(timedelta((rec.date_debut-starting_date).days))
            # print(timedelta((rec.date_fin-starting_date).days))
            # print("----")
            # date_debut=date.today()+timedelta((rec.date_debut-starting_date).days)
            # date_fin=date.today()+timedelta((rec.date_fin-starting_date).days)
            # print(date_debut)
            # print(date_fin)
            # print("------")
        # Création du tag "Installation" s'il n'existe pas
        if not is_tag_chantier:
            self.env["project.tags"].create({
                "name": "Installation",
            })
        
        # Création du tag "Admin" s'il n'existe pas
        if not is_tag_admin:
            self.env["project.tags"].create({
                "name": "Admin",
            })
        
        # Récupération des IDs des tags "Admin" et "Installation"
        id_tag_admin = self.env["project.tags"].search([("name","=", "Admin")], limit=1).id
        id_tag_chantier = self.env["project.tags"].search([("name","=", "Installation")], limit=1).id
    
        # Récupération de l'utilisateur actuel
        user = self.env.user
    
        # Boucle sur les enregistrements de la classe
        for rec in self:
            # Vérification si l'enregistrement est dans la liste d'IDs
            if rec.id in self.ids:
                # Recherche d'une tâche existante avec le même nom et le même projet
                is_exist = self.env["project.task"].search([('name', '=', rec.name), ('project_id', '=', rec.id_project_assign_to)])

                # if rec.type_task == "Admin":
                #         rec.write({
                #         "date_debut":date.today(),
                #         "date_fin":str(date.today()+timedelta((rec.date_fin-rec.date_debut).days)),
                #     })
                # if rec.type_task == "Installation":
                #     print("The Date End is ")
                #     date_debut_new=self.env["project.task.default"].search([("type_task","=","Admin")],limit=1).date_debut+timedelta(60)
                #     date_fin_new=date_debut_new+timedelta((rec.date_fin-rec.date_debut).days)
                #     # print(self.env["project.task.default"].search([("type_task","=","Admin")],limit=1).date_debut)
                #     rec.write({
                #         "date_debut":date_debut_new,
                #         "date_fin":date_fin_new,
                #     })


                if not is_exist:
                    self.env["project.task"].create({
                        "date_debut": str(rec.date_debut),
                        "date_fin_project": str(rec.date_fin),
                        "name": rec.name,
                        "project_id": rec.id_project_assign_to,
                        "user_ids": [[6, False, [user.id]]],
                        "tag_ids": [[6, False, [id_tag_chantier]]] if rec.type_task == "Installation" else [[6, False, [id_tag_admin]]],
                        "stage_id": self.env["project.task.type"].search([("name","=", "Nouvelle Tâche")], limit=1).id
                    }) 
                    # str(datetime.strptime(str(date.today()), "%Y-%m-%d"))[:-9]
                    # str(datetime.strptime(str(date.today()+timedelta((rec.date_fin-rec.date_debut).days)), "%Y-%m-%d"))[:-9]

                    # rec.date_debut=str(date.today())
                    # rec_date_fin = datetime.strptime(rec.date_fin, '%Y-%m-%d').date()
                    # # rec_date_debut = datetime.strptime(rec.date_debut, '%Y-%m-%d').date()

                    # # new_date_end = date.today() + timedelta((rec_date_fin - rec_date_debut).days)
                    # # new_date_end=date.today()+timedelta((rec.date_fin-rec.date_debut).days)
                    # print("---")
        #                                 # rec.date_fin=str(date.today()+timedelta((rec.date_fin-rec.date_debut).days))
      


