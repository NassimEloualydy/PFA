from odoo import models,fields,api,_
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta
from odoo.exceptions import ValidationError
import re
class crm_lead(models.Model):
    _inherit="crm.lead"

    # Champ pour le numéro d'appel d'offres (AO)
    numero_a_o = fields.Char(string="Numero A.O",track_visibility='always')

    # Champ pour indiquer si une visite des lieux est prévue
    is_visite_des_lieux = fields.Boolean(string="Visite des lieux",track_visibility='always')

    # Champ pour la date de visite pour les pistes
    date_visite = fields.Datetime("Date visite",track_visibility='always')

    # Champ pour la durée d'exécution en mois
    duration_months = fields.Integer('Délai d\'éxecution en mois',track_visibility='always')

    # Champ pour la durée d'exécution en jours
    duration_days = fields.Integer('Délai d\'éxecution en jours',track_visibility='always')

    # Champ pour indiquer s'il s'agit d'un groupement
    groupement = fields.Boolean(string="Groupement",track_visibility='always')

    # Champ pour le partenaire du groupement
    partner_id_groupement = fields.Many2one('res.partner', string="Partenaires",track_visibility='always')

    # Champ pour l'adresse e-mail
    courriel = fields.Char(string="Courriel",track_visibility='always')

    # Champ pour le Bureau d'Études Techniques (B.E.T)
    bet = fields.Many2one("res.partner", string="B.E.T",track_visibility='always')

    # Champ pour l'architecte
    architecte = fields.Many2one("res.partner", string="Architecte",track_visibility='always')

    # Champ pour la Bureau de Contrôle Technique (B.C.T)
    bct = fields.Many2one("res.partner", string="B.C.T",track_visibility='always')

    # Champ pour indiquer si une date d'échéance est définie
    is_date_ech = fields.Boolean(string="Dépôt échantillon",track_visibility='always')

    # Champ pour les qualifications
    qualifications = fields.Text(string='Qualifications',track_visibility='always')

    # Champ pour la nature du marché (marchés privés ou marchés publics)
    nature_de_marche = fields.Selection([
        ('marches_prives', 'Marches prives'),
        ('marches_publics', 'Marches publics')],
        string="Nature du marche",track_visibility='always')

    # Champ pour indiquer si la soumission est électronique
    s_electronique = fields.Boolean(string="S.Electronique", widget='radio',track_visibility='always')
    # Champ pour les qualifications
    qualification = fields.Char(string="Qualifcations",track_visibility='always')

    # Champ pour le numéro de téléphone
    phone_crm = fields.Char(
        'Telephone', tracking=50,
        compute='_compute_phone', inverse='_inverse_phone', readonly=False, store=True,track_visibility='always')

    # Champ pour compter le nombre de fichiers joints
    nbr_field_attached = fields.Integer(string='Nombre Des Fichier', compute='_compute_nbr_attached_file')

    # Champ pour compter le nombre de documents joints
    nbr_documents = fields.Integer(string="nbr_documents", compute="_get_nbr_documents")

    # Champ pour définir la couleur de la date en fonction de la différence entre date_deadline et la date d'aujourd'hui
    color_for_date = fields.Char('color_date', compute='_compute_date_dead_line')

    # Champ pour le nom du contact
    nom_du_contact = fields.Char(String='Nom du Contact',track_visibility='always')

    # Champ pour le titre du nom du contact
    titre_nom_du_contact = fields.Selection([
        ('docteur', 'Docteur'),
        ('madame', 'Madame'),
        ('mademoiselle', 'Mademoiselle'),
        ('Monsieur', 'Monsieur'),
        ('Professeur', 'Professeur')],
        string="Titre",track_visibility='always')

    # Champ pour l'adresse du site web
    site_web = fields.Char(String='Site Web',track_visibility='always')

    # Champ pour le numéro de téléphone mobile
    mobile = fields.Char(String='Mobile',track_visibility='always')

    # Champ pour afficher un message indiquant la différence entre la date d'aujourd'hui et la date de date_visite_des_lieux
    message_date_visite_des_lieux = fields.Char(string="message_date_visite_des_lieux", compute='_compute_message_date_visite_des_lieux')
    # Champ pour afficher un message indiquant la différence entre la date d'aujourd'hui et la date de date_visite_des_lieux
    message_date_visite = fields.Char(string="message_date_visite", compute='_compute_message_date_visite_des_lieux')

    # Champ pour afficher un message indiquant la différence entre la date d'aujourd'hui et la date de date_ech
    message_date_ech = fields.Char(string="message_date_ech", compute='_compute_message_date_ech')

    # Champ pour afficher un message indiquant la différence entre la date d'aujourd'hui et la date de date_deadline
    message_date_deadline = fields.Char(string="message_date_deadline", compute='_compute_message_date_deadline')

    # Champ pour la caution provisoire
    caution_provisoire = fields.Monetary(string="Caution Provisoire", currency_field='company_currency',track_visibility='always')

    # Champ pour afficher la caution provisoire avec un format spécifique
    caution_provisoire_with_span = fields.Char(string="caution_provisoire on dh", readonly=False, compute='_caution_provisoire_with_span', store=True)

    # Champ pour afficher le montant prévu avec un format spécifique
    expected_revenue_with_span = fields.Char( string="My Field with DH", readonly=False, compute='_compute_my_field_with_span', store=True)

    # Champ pour indiquer le nombre de jours entre la date d'aujourd'hui et la date de date_deadline
    delta_deadline = fields.Integer(compute='_get_delta', string=u'Echéance / Fin',track_visibility='always',required=True)

    # Champ pour indiquer le nombre de jours entre la date d'aujourd'hui et la date de date_ech
    delta_date_ech = fields.Integer(compute='_get_delta_date_ech', string=u'date ech')

    # Champ pour indiquer le nombre de jours entre la date d'aujourd'hui et la date de date_visite_des_lieux
    delta_date_visite_des_lieux = fields.Integer(compute='_get_delta_date_visite_des_lieux', string=u'date visite')
    delta_date_visite = fields.Integer(compute='_get_delta_date_visite_des_lieux', string=u'date visite')

    # Champ pour la date de visite des lieux
    date_visite_des_lieux = fields.Datetime("Date visite des lieux",track_visibility='always')

    # Champ pour la date d'échéance
    date_deadline = fields.Datetime("D. Soumission",track_visibility='always')

    # Champ pour la date de dépôt
    date_ech = fields.Datetime(string="Date de dépôt",track_visibility='always')
    
    #une fonction qui fait que le champ delta_date_ech prend combien de jours entre le champ delta_date_ech et la date d'aujourd'hui 
    @api.depends('date_ech')
    def _get_delta_date_ech(self):
        for rec in self:
            if rec.date_ech:
                # Calcul de la différence en secondes entre la date d'échéance (date_ech) et la date et l'heure actuelles (fields.Datetime.now())
                rec.delta_date_ech = (rec.date_ech - fields.Datetime.now()).total_seconds()
                # Affichage de la différence en secondes (facultatif, à des fins de débogage)
                print(rec.delta_date_ech)
            else:
                # Si la date d'échéance (date_ech) est vide, définir la différence à zéro
                rec.delta_date_ech = 0

    #une fonction qui fait que le champ delta_date_visite_des_lieux prend combien de jours entre le champ date_visite_des_lieux et la date d'aujourd'hui 
    @api.depends('date_visite_des_lieux','date_visite')
    def _get_delta_date_visite_des_lieux(self):
        for rec in self:
            
            if rec.date_visite:
                # Calcul de la différence en secondes entre la date de visite des lieux (date_visite) et la date et l'heure actuelles (fields.Datetime.now())
                rec.delta_date_visite = (rec.date_visite - fields.Datetime.now()).total_seconds()
    
                # Affichage de la différence en secondes (facultatif, à des fins de débogage)
            else:
                # Si la date de visite des lieux (date_visite_des_lieux) est vide, définir la différence à zéro
                rec.delta_date_visite = 0

            if rec.date_visite_des_lieux:
                # Calcul de la différence en secondes entre la date de visite des lieux (date_visite_des_lieux) et la date et l'heure actuelles (fields.Datetime.now())
                rec.delta_date_visite_des_lieux = (rec.date_visite_des_lieux - fields.Datetime.now()).total_seconds()
    
                # Affichage de la différence en secondes (facultatif, à des fins de débogage)
                print(rec.delta_date_visite_des_lieux)
            else:
                # Si la date de visite des lieux (date_visite_des_lieux) est vide, définir la différence à zéro
                rec.delta_date_visite_des_lieux = 0
    #une fonction qui fait que le champ delta_deadline prend combien de jours entre le champ date_deadline et la date d'aujourd'hui 
    @api.depends('date_deadline')
    def _get_delta(self):
        for rec in self:
            if rec.date_deadline:
                # Calcul de la différence en secondes entre la date limite (date_deadline) et la date et l'heure actuelles (fields.Datetime.now())
                rec.delta_deadline = (rec.date_deadline - fields.Datetime.now()).total_seconds()

                # Affichage de la différence en secondes (facultatif, à des fins de débogage)
                print(rec.delta_deadline)
            else:
                # Si la date limite (date_deadline) est vide, définir la différence à zéro
                rec.delta_deadline = 0

    #une fonction qui change l'affichage du champs caution_provisoire 
    @api.depends("caution_provisoire")
    def _caution_provisoire_with_span(self):
        for record in self:

            # Formatage de la valeur de caution provisoire avec des espaces pour les milliers, une virgule comme séparateur décimal et ajout de " DH" à la fin
            formatted_value = "{:,.2f}".format(record.caution_provisoire).replace(',', ' ').replace('.', ',')

            # Stockage de la valeur formatée dans un champ "caution_provisoire_with_span"
            record.caution_provisoire_with_span = formatted_value + " DH"

    #une fonction qui change l'affichage du champs expected_revenue 
    @api.depends('expected_revenue')
    def _compute_my_field_with_span(self):
        for record in self:
            # Formatage de la valeur de "expected_revenue" avec des espaces pour les milliers, une virgule comme séparateur décimal et ajout de " DH" à la fin
            formatted_value = "{:,.2f}".format(record.expected_revenue).replace(',', ' ').replace('.', ',')

            # Stockage de la valeur formatée dans un champ "expected_revenue_with_span"
            record.expected_revenue_with_span = formatted_value + " DH"

    #un fonction qui reteur un message qui indique combien de jour entre le champs date_ech et la date d'aujourd'hui 
    def _compute_message_date_ech(self):
        for record in self:
            # Vérification si "is_date_ech" est vrai et si "date_ech" existe
            if record.is_date_ech and record.date_ech:
                # Conversion de la date cible en format datetime
                target_date = datetime.strptime(str(record.date_ech), "%Y-%m-%d %H:%M:%S")

                # Obtention de la date et de l'heure actuelles
                current_date = datetime.now()

                # Calcul de la différence entre la date cible et la date actuelle
                delta = target_date - current_date

                # Calcul du nombre de jours restants
                days_remaining = delta.days
                res = ""

                # Détermination du message en fonction du nombre de jours restants
                if days_remaining > 0:
                    res = " Reste " + str(days_remaining) + " Jours"
                elif days_remaining == 0:
                    res = "Aujourd'hui est la D.Visite"
                else:
                    res = " Retard " + str(-days_remaining) + " Jours"

                # Stockage du message résultant dans le champ "message_date_ech"
                record.message_date_ech = res
            else:
                # Si "is_date_ech" n'est pas vrai ou si "date_ech" est vide, le champ "message_date_ech" est laissé vide
                record.message_date_ech = ""


    #un fonction qui reteur un message qui indique combien de jour entre le champs date_deadline et la date d'aujourd'hui 
    def _compute_message_date_deadline(self):
        for record in self:
            # Vérification si "date_deadline" n'est pas égal à False (c'est-à-dire qu'il existe une date)
            if record.date_deadline != False:

                # Conversion de la date cible en format datetime
                target_date = datetime.strptime(str(record.date_deadline), "%Y-%m-%d %H:%M:%S")

                # Obtention de la date et de l'heure actuelles avec une diminution d'un jour (pour tenir compte de la journée précédente)
                current_date = datetime.now() - timedelta(days=1)

                # Calcul de la différence entre la date cible et la date actuelle
                delta = target_date - current_date

                # Calcul du nombre de jours restants
                days_remaining = delta.days
                res = ""

                # Détermination du message en fonction du nombre de jours restants
                if days_remaining > 0:
                    res = " Reste " + str(days_remaining) + " Jours"
                elif days_remaining == 0:
                    res = "Aujourd'hui"
                else:
                    res = " Retard " + str(-days_remaining) + " Jours"

                # Stockage du message résultant dans le champ "message_date_deadline"
                record.message_date_deadline = res
            else:
                # Si "date_deadline" est égal à False, le champ "message_date_deadline" est laissé vide
                record.message_date_deadline = ""

    #un fonction qui reteur un message qui indique combien de jour entre le champs date_deadline et la date d'aujourd'hui 
    def _compute_message_date_visite_des_lieux(self):
        for record in self:
            # message_date_visite
            if record.date_visite:
                
                # Conversion de la date cible en format datetime
                target_date = datetime.strptime(str(record.date_visite), "%Y-%m-%d %H:%M:%S")
                
                # Obtention de la date et de l'heure actuelles avec une diminution d'un jour (pour tenir compte de la journée précédente)
                current_date = datetime.now() - timedelta(days=1)
                
                # Calcul de la différence entre la date cible et la date actuelle
                delta = target_date - current_date
                
                # Calcul du nombre de jours restants
                days_remaining = delta.days
                res = ""
                
                # Détermination du message en fonction du nombre de jours restants
                if days_remaining > 0:
                    res = " Reste " + str(days_remaining) + " Jours"
                elif days_remaining == 0:
                    res = "Aujourd'hui est la D.Visite"
                else:
                    res = " Retard " + str(-days_remaining) + " Jours"
                
                # Stockage du message résultant dans le champ "message_date_visite_des_lieux"
                record.message_date_visite = res
            else:
                # Si "date_visite_des_lieux" est vide, le champ "message_date_visite_des_lieux" est laissé vide
                record.message_date_visite = ""

            """****************************88"""
            # Vérification si "date_visite_des_lieux" existe
            if record.date_visite_des_lieux:
                
                # Conversion de la date cible en format datetime
                target_date = datetime.strptime(str(record.date_visite_des_lieux), "%Y-%m-%d %H:%M:%S")
                
                # Obtention de la date et de l'heure actuelles avec une diminution d'un jour (pour tenir compte de la journée précédente)
                current_date = datetime.now() - timedelta(days=1)
                
                # Calcul de la différence entre la date cible et la date actuelle
                delta = target_date - current_date
                
                # Calcul du nombre de jours restants
                days_remaining = delta.days
                res = ""
                
                # Détermination du message en fonction du nombre de jours restants
                if days_remaining > 0:
                    res = " Reste " + str(days_remaining) + " Jours"
                elif days_remaining == 0:
                    res = "Aujourd'hui est la D.Visite"
                else:
                    res = " Retard " + str(-days_remaining) + " Jours"
                
                # Stockage du message résultant dans le champ "message_date_visite_des_lieux"
                record.message_date_visite_des_lieux = res
            else:
                # Si "date_visite_des_lieux" est vide, le champ "message_date_visite_des_lieux" est laissé vide
                record.message_date_visite_des_lieux = ""

    # Fonction utilisée pour calculer la couleur d'un champ "color_for_date" en fonction de la date limite "date_dead_line".
    # Si la date limite est supérieure à la date actuelle, la couleur est définie sur "red" (rouge).
    # Sinon, la couleur est définie sur "green" (vert).
    # Si le champ "date_dead_line" n'existe pas, le champ "color_for_date" reste vide.
    def _compute_date_dead_line(self):
        for record in self:
            # Vérification si l'enregistrement a un champ "date_dead_line"
            if hasattr(record, 'date_dead_line'):
                # Comparaison de "date_dead_line" avec la date actuelle
                if record.date_dead_line > fields.Date.today():
                    record.color_for_date = "red"  # Date limite dépassée
                else:
                    record.color_for_date = "green"  # Date limite non dépassée
            else:
                # Si le champ "date_dead_line" n'existe pas, le champ "color_for_date" reste vide
                record.color_for_date = ""
    
    # Cette fonction permet de compter le nombre de documents associés à l'enregistrement actuel.
    def _get_nbr_documents(self):
        for rec in self:
            # Recherche des documents liés à cet enregistrement dans le modèle "documents.document" et compte leur nombre.
            rec.nbr_documents = self.env["documents.document"].search_count([('res_id', '=', rec.id)])

    # Cette fonction calcule le nombre de fichiers joints (attachments) associés à l'enregistrement actuel.
    def _compute_nbr_attached_file(self):
        for record in self:
            # Recherche des fichiers joints liés à cet enregistrement dans le modèle "ir.attachment" et compte leur nombre.
            record.nbr_field_attached = self.env["ir.attachment"].search_count([('res_id', '=', record.id),("res_model","=","crm.lead")])

    # Cette fonction retourne une action permettant d'afficher les fichiers joints (attachments) associés à l'enregistrement actuel.
    def get_attachment_for_user(self):
        return {
            'name': _('Fichiers joints'),  # Nom de l'action
            'domain': [('res_id', '=', self.id),("res_model","=","crm.lead")],  # Filtre pour afficher les attachments liés à cet enregistrement
            'view_type': 'kanban',  # Type de vue par défaut (kanban)
            'res_model': 'ir.attachment',  # Modèle des fichiers joints (ir.attachment)
            'view_id': False,  # ID de la vue (utilisation par défaut)
            'view_mode': 'kanban,tree,form',  # Modes de vue disponibles (kanban, liste, formulaire)
            'type': 'ir.actions.act_window'  # Type d'action (fenêtre)
        }
    
    # Cette fonction est déclenchée lorsque les suiveurs (followers) d'un enregistrement sont modifiés.
    # Elle détermine si l'utilisateur actuel suit l'enregistrement en fonction de la présence de l'utilisateur
    # dans la liste des suiveurs associés à cet enregistrement.
    @api.depends('message_follower_ids')
    def _compute_message_is_follower(self):
        # Recherche des suiveurs associés à cet enregistrement, en excluant l'utilisateur actuel.
        followers = self.env['mail.followers'].sudo().search([
            ('res_model', '=', self._name),
            ('res_id', 'in', self.ids),
            ('partner_id', '!=', self.partner_id.id)
        ])

        # Création d'une liste des IDs des enregistrements suivis.
        following_ids = [res['res_id'] for res in followers.read(['res_id'])]

        # Définition de la valeur du champ "message_is_follower" pour chaque enregistrement en fonction de leur présence dans la liste des suivis.
        for record in self:
            record.message_is_follower = record.id in following_ids


    # Cette fonction est utilisée pour créer un enregistrement et effectuer diverses opérations associées à sa création.
    # @api.model
        # Création de l'enregistrement en utilisant la méthode parente "create" du modèle
    def create(self, vals):
        lead = super(crm_lead, self.with_context(mail_create_nosubscribe=True)).create(vals)
        type_of_crm="Piste" if lead.type=="lead" else "Opportunité"

        # cree un evenement
        user=self.env.user
        startdate=datetime.now()
        enddate=datetime.now()+timedelta(hours=1)
        categ_ids = [[6, False,[]]]
        if lead.type == "lead":
           is_tag_ids_exist_piste = self.env["calendar.event.type"].search([("name", "=", "Piste")])

           if not is_tag_ids_exist_piste:
       
              self.env["calendar.event.type"].create({
              "name": "Piste"
                })

           categ_ids = [[6, False, [self.env["calendar.event.type"].search([("name", "=", "Piste")], limit=1).id]]]
        else:
        # Si le type est une opportunité, utiliser le type d'événement "Opportunité"
           is_tag_ids_exist_opportunity = self.env["calendar.event.type"].search([("name", "=", "Opportunité")])

           if not is_tag_ids_exist_opportunity:
        # Créer le type d'événement "Opportunité" s'il n'existe pas
             self.env["calendar.event.type"].create({
                 "name": "Opportunité"
             })

           categ_ids = [[6, False, [self.env["calendar.event.type"].search([("name", "=", "Opportunité")], limit=1).id]]]

        if type_of_crm=="Opportunité" and lead.date_deadline:
            date_stop=lead.date_deadline+timedelta(hours=1)
            # if lead.date_visite:
            #     date_stop=lead.date_visite
            # if lead.date_visite_des_lieux:
            #     date_stop=lead.date_visite_des_lieux

            # print("the days deference is")
            # print((lead.date_deadline-date_stop).days)
            # print("the date visit is")
            # print(date_stop)
            # print("the date begin")
            # print(lead.date_deadline)
            # print("lead.date_visite")
            # print(lead.date_visite)
            # print("lead.date_visite_des_lieux")
            # print(lead.date_visite_des_lieux)
            self.env["calendar.event"].create({
                       'res_model_id': self.env['ir.model'].search([('model','=','crm.lead')],limit=1).id,
                       'res_id': lead.id,
                       'user_id': user.id,
                       'name': str(lead.name)+" ",
                       'start':lead.date_deadline,
                       'stop':date_stop,
                        # 'stop':lead.date_deadline+timedelta(hours=1),
                        # 'stop': lead.date_viste if lead.type == 'lead' else lead.date_visite_des_lieux,
                        'description': "une "+str(type_of_crm)+" avec le nom : "+str(lead.name)+"",
                        'partner_ids':[[6,False,[lead.user_id.partner_id.id]]],
                        'categ_ids': categ_ids,
                       'duration':1,
                       "create_date":lead.date_deadline
                   })
        



        # test 21/11/2023 CREATION DE CHANELE POUR CRM 
        # is_channel_crm=self.env["mail.channel"].search([("name","=","CRM"),("channel_type","=","group")])
        

        # if not is_channel_crm:

             
        #      self.env["mail.channel"].create({
        #            "name":"CRM",
        #            "channel_type":"group"
        #      })
        
        is_channel_chantier_exist=self.env["mail.channel"].search([("name","=","CRM"),("channel_type","=","channel")])
        

        if not is_channel_chantier_exist:

             
             self.env["mail.channel"].create({
                   "name":"CRM",
                   "channel_type":"channel"
             })
        
        
        body_message=""+type_of_crm+" créé <br/>"
                
        vals=vals[0] if isinstance(vals,list) else vals
        if "name" in vals and vals['name']!=False:
            body_message+="&nbsp;&nbsp;&nbsp; Objet  : <span class='fw-bolder'>"+str(vals["name"])+"</span> <br/> "

        if "numero_a_o" in vals and vals['numero_a_o']!=False:
            body_message+="&nbsp;&nbsp;&nbsp; Numero A.O  : <span class='fw-bolder'>"+str(vals["numero_a_o"])+"</span> <br/> "

        # if "is_visite_des_lieux" in vals:
        #     body_message+="&nbsp;&nbsp;&nbsp; Visite des lieux  : <span class='fw-bolder'>"+str(vals["is_visite_des_lieux"])+"</span> <br/> "
        
        if "date_visite" in vals and vals['date_visite']!=False:
            print(vals)
            print("test")
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
            date = datetime(int(str(vals["date_visite"])[0]+str(vals["date_visite"])[1]+str(vals["date_visite"])[2]+str(vals["date_visite"])[3]), int(str(vals["date_visite"])[5]+str(vals["date_visite"])[6]),int(str(vals["date_visite"])[8]+str(vals["date_visite"])[9]))
            formatted_date = date.strftime('%d , %B , %Y').lower()
            day_name = date.strftime('%A')
            day, month, year = formatted_date.split(' , ')
            # Translate the month to French and capitalize the first letter
            
            month_french = month_translation[month].capitalize()
            day_french = day_translation[day_name].capitalize()
            # Combine the day, translated month, and year
            formatted_date_french = f'{day_french} {day}  {month_french}  {year}'

            body_message+="&nbsp;&nbsp;&nbsp; Date visite  : <span class='fw-bolder'>"+str(formatted_date_french)+"</span> <br/> "

        if "duration_months" in vals and vals['duration_months']!=False:
            body_message+="&nbsp;&nbsp;&nbsp; Délai d'éxecution en mois  : <span class='fw-bolder'>"+str(vals["duration_months"])+"</span> <br/> "

        if "duration_days" in vals and vals['duration_days']!=False:
            body_message+="&nbsp;&nbsp;&nbsp; Délai d\'éxecution en jours  : <span class='fw-bolder'>"+str(vals["duration_days"])+"</span> <br/> "

        if "groupement" in vals and vals['groupement']!=False:
            body_message+="&nbsp;&nbsp;&nbsp; Groupement  : <span class='fw-bolder'>"+str(vals["groupement"])+"</span> <br/> "

        if "partner_id_groupement" in vals and vals['partner_id_groupement']!=False:
            body_message+="&nbsp;&nbsp;&nbsp; Partenaires  : <span class='fw-bolder'>"+str(vals["partner_id_groupement"])+"</span> <br/> "

        if "courriel" in vals and vals['courriel']!=False:
            body_message+="&nbsp;&nbsp;&nbsp; Courriel  : <span class='fw-bolder'>"+str(vals["courriel"])+"</span> <br/> "
        if "bet" in vals and vals['bet']!=False:
            body_message+="&nbsp;&nbsp;&nbsp; B.E.T  : <span class='fw-bolder'>"+str(vals["bet"])+"</span> <br/> "

        if "architecte" in vals and vals['architecte']!=False:
            body_message+="&nbsp;&nbsp;&nbsp; Architecte  : <span class='fw-bolder'>"+str(vals["architecte"])+"</span> <br/> "

        if "bct" in vals and vals['bct']!=False:
            body_message+="&nbsp;&nbsp;&nbsp; B.C.T  : <span class='fw-bolder'>"+str(vals["bct"])+"</span> <br/> "

        # if "is_date_ech" in vals:
        #     body_message+="&nbsp;&nbsp;&nbsp; Dépôt échantillon  : <span class='fw-bolder'>"+str(vals["is_date_ech"])+"</span> <br/> "
        if "qualifications" in vals and vals['qualifications']!=False and vals["qualifications"]!="" and vals["qualifications"]!="\n":        
            body_message+="&nbsp;&nbsp;&nbsp; Qualifications  : <span class='fw-bolder'>"+str(vals["qualifications"])+"</span> <br/> "

        if "nature_de_marche" in vals and vals['nature_de_marche']!=False:
            nature_marche='Marches prives' if vals['nature_de_marche']=='marches_prives' else 'Marches publics'
            body_message+="&nbsp;&nbsp;&nbsp; Nature du marche  : <span class='fw-bolder'>"+nature_marche+"</span> <br/> "

        if "s_electronique" in vals and vals['s_electronique']!=False:
            body_message+="&nbsp;&nbsp;&nbsp; S.Electronique  : <span class='fw-bolder'>"+str(vals["s_electronique"])+"</span> <br/> "


        if "phone_crm" in vals and vals['phone_crm']!=False:
            body_message+="&nbsp;&nbsp;&nbsp; Telephone  : <span class='fw-bolder'>"+str(vals["phone_crm"])+"</span> <br/> "

        if "nom_du_contact" in vals and vals['nom_du_contact']!=False:
            body_message+="&nbsp;&nbsp;&nbsp; Nom du Contact : <span class='fw-bolder'>"+str(vals["nom_du_contact"])+"</span> <br/> "

        if "titre_nom_du_contact" in vals and vals['titre_nom_du_contact']!=False:
            body_message+="&nbsp;&nbsp;&nbsp; Titre  : <span class='fw-bolder'>"+str(vals["titre_nom_du_contact"])+"</span> <br/> "

        if "site_web" in vals and vals['site_web']!=False:
            body_message+="&nbsp;&nbsp;&nbsp; Site Web  : <span class='fw-bolder'>"+str(vals["site_web"])+"</span> <br/> "

        if "mobile" in vals and vals['mobile']!=False:
            body_message+="&nbsp;&nbsp;&nbsp; Mobile  : <span class='fw-bolder'>"+str(vals["mobile"])+"</span> <br/> "

        if "caution_provisoire" in vals and vals['caution_provisoire']!=False:
            body_message+="&nbsp;&nbsp;&nbsp; Caution Provisoire  : <span class='fw-bolder'>"+str(vals["caution_provisoire"])+"</span> <br/> "

        if "date_visite_des_lieux" in vals and vals['date_visite_des_lieux']!=False:
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
            date = datetime(int(str(vals["date_deadline"])[0]+str(vals["date_deadline"])[1]+str(vals["date_deadline"])[2]+str(vals["date_deadline"])[3]), int(str(vals["date_deadline"])[5]+str(vals["date_deadline"])[6]),int(str(vals["date_deadline"])[8]+str(vals["date_deadline"])[9]))
            formatted_date = date.strftime('%d , %B , %Y').lower()
            day_name = date.strftime('%A')
            day, month, year = formatted_date.split(' , ')
            # Translate the month to French and capitalize the first letter
            
            month_french = month_translation[month].capitalize()
            day_french = day_translation[day_name].capitalize()
            # Combine the day, translated month, and year
            formatted_date_french = f'{day_french} {day}  {month_french}  {year}'

            body_message+="&nbsp;&nbsp;&nbsp; Date visite des lieux  : <span class='fw-bolder'>"+str(formatted_date_french)+"</span> <br/> "

        if "date_deadline" in vals and vals['date_deadline']!=False:
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
            date = datetime(int(str(vals["date_deadline"])[0]+str(vals["date_deadline"])[1]+str(vals["date_deadline"])[2]+str(vals["date_deadline"])[3]), int(str(vals["date_deadline"])[5]+str(vals["date_deadline"])[6]),int(str(vals["date_deadline"])[8]+str(vals["date_deadline"])[9]))
            formatted_date = date.strftime('%d , %B , %Y').lower()
            day_name = date.strftime('%A')
            day, month, year = formatted_date.split(' , ')
            # Translate the month to French and capitalize the first letter
            
            month_french = month_translation[month].capitalize()
            day_french = day_translation[day_name].capitalize()
            # Combine the day, translated month, and year
            formatted_date_french = f'{day_french} {day}  {month_french}  {year}'
            body_message+="&nbsp;&nbsp;&nbsp;  D. Soumission  : <span class='fw-bolder'>"+str(formatted_date_french)+"</span> <br/> "

        if "date_ech" in vals and vals['date_ech']!=False:
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
            date = datetime(int(str(vals["date_ech"])[0]+str(vals["date_ech"])[1]+str(vals["date_ech"])[2]+str(vals["date_ech"])[3]), int(str(vals["date_ech"])[5]+str(vals["date_ech"])[6]),int(str(vals["date_ech"])[8]+str(vals["date_ech"])[9]))
            formatted_date = date.strftime('%d , %B , %Y').lower()
            day_name = date.strftime('%A')
            day, month, year = formatted_date.split(' , ')
            # Translate the month to French and capitalize the first letter
            
            month_french = month_translation[month].capitalize()
            day_french = day_translation[day_name].capitalize()
            # Combine the day, translated month, and year
            formatted_date_french = f'{day_french} {day}  {month_french}  {year}'
            body_message+="&nbsp;&nbsp;&nbsp; Date de dépôt  : <span class='fw-bolder'>"+str(formatted_date_french)+"</span> <br/> "

        user=self.env.user
        self.env["mail.message"].create({
              "body":body_message,
               'email_from': '"'+user.partner_id.name+'" <'+user.login+'>',
               'message_type': 'comment',
               'subtype_id': 1,
               'subject': False,
               'model': 'mail.channel',
               'res_id': self.env["mail.channel"].search([("name","=","CRM"),("channel_type","=","channel")],limit=1).id,
               'record_name': 'CRM',
        })
        



        # Suppression des suiveurs associés au partenaire (partner) lié à cet enregistrement
        if hasattr(lead, 'partner'):
            data = self.env["mail.followers"].search([('res_id', '=', lead.partner_id.id), ('res_model', '=', 'res_partner')], limit=1)
            if data:
                data.unlink()
        
        # Ajout de suiveurs aux enregistrements
        def add_follower(record, partner, model):
            filter_data = self.env["mail.followers"].sudo().search([('res_id', '=', record.id), ('partner_id', '=', partner.partner_id.id), ('res_model', '=', model)])
            if not filter_data:
                self.env["mail.followers"].sudo().with_context(mail_create_nosubscribe=True).create({
                    "res_id": record.id,
                    "partner_id": partner.partner_id.id,
                    "res_model": model
                })


        # Recherche des utilisateurs qui sont abonne par default au crm
        user_of_crm=self.env["res.users"].search([("is_follower_for_crm","=",True)])
        for rec in user_of_crm:
            add_follower(lead, rec, "crm.lead")
            add_follower(lead.user_id, rec, "res.partner")

        # Création d'un message d'invitation (mail.wizard.invite) s'il n'existe pas déjà
        is_mail_wizard_invite=self.env["mail.wizard.invite"].search([('res_model','=','crm.lead'),('message',"=","Vous avez invité au piste "+str(lead.name)),('res_id','=',lead.id)])

        if is_mail_wizard_invite:
            self.env["mail.wizard.invite"].create({
                "res_id": lead.id,
                "res_model": "crm.lead",
                "message": "Vous avez invité au piste "+str(lead.name),
            })
        # Suppression des suiveurs associés au partenaire (partner) lié à cet enregistrement
        if lead.partner_id:
            query = "DELETE FROM mail_followers WHERE res_id=%s AND res_model=%s"
            self.env.cr.execute(query, (lead.partner_id.id, "res.partner"))

        # Retour de l'enregistrement créé
        return lead

    # Cette fonction retourne une action permettant d'afficher les fichiers joints (attachments) associés à l'enregistrement actuel.
    def get_documents_for_user(self):
        return {
            'name': _('Fichiers joints'),  # Nom de l'action
            'domain': [('res_id', '=', self.id)],  # Filtre pour afficher les documents liés à cet enregistrement
            'view_type': 'kanban',  # Type de vue par défaut (kanban)
            'context': {
                "default_res_model": "crm.lead",  # Modèle de l'enregistrement parent
                "default_res_id": self.id  # ID de l'enregistrement parent
            },
            'res_model': 'documents.document',  # Modèle des fichiers joints (documents.document)
            'view_id': False,  # ID de la vue (utilisation par défaut)
            'view_mode': 'kanban,form',  # Modes de vue disponibles (kanban, formulaire)
            'type': 'ir.actions.act_window'  # Type d'action (fenêtre)
        }
    def write(self,vals):          
        data_befor_update={}
        if "stage_id" in vals:
            data_befor_update['stage_id']=self.stage_id.name            

        if "name" in vals:
            data_befor_update['name']=self.name            
        if "numero_a_o" in vals:
            data_befor_update['numero_a_o']=self.numero_a_o            
        if "date_visite" in vals:

            if self.date_visite==False:
                data_befor_update['date_visite']=False            

            if self.date_visite!=False:
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
                date = datetime(int(str(self.date_visite)[0]+str(self.date_visite)[1]+str(self.date_visite)[2]+str(self.date_visite)[3]), int(str(self.date_visite)[5]+str(self.date_visite)[6]),int(str(self.date_visite)[8]+str(self.date_visite)[9]))
                formatted_date = date.strftime('%d , %B , %Y').lower()
                day_name = date.strftime('%A')
                day, month, year = formatted_date.split(' , ')
                # Translate the month to French and capitalize the first letter
                
                month_french = month_translation[month].capitalize()
                day_french = day_translation[day_name].capitalize()
                # Combine the day, translated month, and year
                formatted_date_french = f'{day_french} {day}  {month_french}  {year}'

                data_befor_update['date_visite']=formatted_date_french            
        if "duration_months" in vals:
            data_befor_update['duration_months']=self.duration_months            
        if "duration_days" in vals:
            data_befor_update['duration_days']=self.duration_days            
        if "groupement" in vals:
            data_befor_update['groupement']=self.groupement            
        if "partner_id_groupement" in vals:
            data_befor_update['partner_id_groupement']=self.partner_id_groupement.name        
        if "courriel" in vals:
            data_befor_update['courriel']=self.courriel            
        if "bet" in vals:
            data_befor_update['bet']=self.bet.name            
        if "architecte" in vals:
            data_befor_update['architecte']=self.architecte.name       
        if "bct" in vals:
            data_befor_update['bct']=self.bct.name          
        if "qualifications" in vals:
            data_befor_update['qualifications']=self.qualifications            
        if "nature_de_marche" in vals:
            nature_marche='Marches prives' if vals['nature_de_marche']=='nature_de_marche' else 'Marches publics'

            data_befor_update['nature_de_marche']=nature_marche
        if "s_electronique" in vals:
            data_befor_update['s_electronique']=self.s_electronique            
        if "phone_crm" in vals:
            data_befor_update['phone_crm']=self.phone_crm            
        if "nom_du_contact" in vals:
            data_befor_update['nom_du_contact']=self.nom_du_contact            
        if "titre_nom_du_contact" in vals:
            data_befor_update['titre_nom_du_contact']=self.titre_nom_du_contact            
        if "site_web" in vals:
            data_befor_update['site_web']=self.site_web            
        if "mobile" in vals:
            data_befor_update['mobile']=self.mobile            
        if "caution_provisoire" in vals:
            data_befor_update['caution_provisoire']=self.caution_provisoire            
        if "expected_revenue" in vals:
            data_befor_update['expected_revenue']=self.expected_revenue            

        if "date_visite_des_lieux" in vals:
            if self.date_visite_des_lieux==False:
                data_befor_update['expected_revenue']=False

            if self.date_visite_des_lieux!=False:
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
                date = datetime(int(str(self.date_visite)[0]+str(self.date_visite)[1]+str(self.date_visite)[2]+str(self.date_visite)[3]), int(str(self.date_visite)[5]+str(self.date_visite)[6]),int(str(self.date_visite)[8]+str(self.date_visite)[9]))
                formatted_date = date.strftime('%d , %B , %Y').lower()
                day_name = date.strftime('%A')
                day, month, year = formatted_date.split(' , ')
                # Translate the month to French and capitalize the first letter
                
                month_french = month_translation[month].capitalize()
                day_french = day_translation[day_name].capitalize()
                # Combine the day, translated month, and year
                formatted_date_french = f'{day_french} {day}  {month_french}  {year}'

                data_befor_update['date_visite_des_lieux']=formatted_date_french            

        if "date_ech" in vals:
            if self.date_ech!=False:
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
                date = datetime(int(str(self.date_ech)[0]+str(self.date_ech)[1]+str(self.date_ech)[2]+str(self.date_ech)[3]), int(str(self.date_ech)[5]+str(self.date_ech)[6]),int(str(self.date_ech)[8]+str(self.date_ech)[9]))
                formatted_date = date.strftime('%d , %B , %Y').lower()
                day_name = date.strftime('%A')
                day, month, year = formatted_date.split(' , ')
                # Translate the month to French and capitalize the first letter
                
                month_french = month_translation[month].capitalize()
                day_french = day_translation[day_name].capitalize()
                # Combine the day, translated month, and year
                formatted_date_french = f'{day_french} {day}  {month_french}  {year}'

                data_befor_update['date_ech']=formatted_date_french            
            else:
                data_befor_update['date_ech']=False
        if "date_deadline" in vals:
            if self.date_deadline==False:
                data_befor_update['date_deadline']=False
            if self.date_deadline!=False:
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
                date = datetime(int(str(self.date_deadline)[0]+str(self.date_deadline)[1]+str(self.date_deadline)[2]+str(self.date_deadline)[3]), int(str(self.date_deadline)[5]+str(self.date_deadline)[6]),int(str(self.date_deadline)[8]+str(self.date_deadline)[9]))
                formatted_date = date.strftime('%d , %B , %Y').lower()
                day_name = date.strftime('%A')
                day, month, year = formatted_date.split(' , ')
                # Translate the month to French and capitalize the first letter
                
                month_french = month_translation[month].capitalize()
                day_french = day_translation[day_name].capitalize()
                # Combine the day, translated month, and year
                formatted_date_french = f'{day_french} {day}  {month_french}  {year}'            
                data_befor_update['date_deadline']=formatted_date_french            
        print(vals)
        print("test")
        crm=super(crm_lead, self).write(vals)
        
        if self.type=="opportunity":
            body_message="Opportunité <span class='fw-bolder'>"+self.name+"</span> modifié : <br/>"
        if self.type=="lead":
                body_message="Piste <span class='fw-bolder'>"+self.name+"</span> modifié : <br/>"
        if "active" in vals:
            if self.active==True:
                if self.type=="opportunity":
                    body_message="Opportunité <span class='fw-bolder'>"+self.name+"</span> Désarchivé<br/>"
                if self.type=="lead":
                        body_message="Piste <span class='fw-bolder'>"+self.name+"</span> Désarchivé <br/>"
            if self.active==False:
                if self.type=="opportunity":
                    body_message="Opportunité <span class='fw-bolder'>"+self.name+"</span> Archivé <br/>"
                if self.type=="lead":
                        body_message="Piste <span class='fw-bolder'>"+self.name+"</span> Archivé <br/>"
            user=self.env.user
            self.env["mail.message"].create({
                        "body":body_message,
                        'email_from': '"'+user.partner_id.name+'" <'+user.login+'>',
                        'message_type': 'comment',
                        'subtype_id': 1,
                        'subject': False,
                        'model': 'mail.channel',
                        'res_id': self.env["mail.channel"].search([("name","=","CRM"),("channel_type","=","channel")],limit=1).id,
                        'record_name': 'CRM',
                    })

            return crm


        if "name" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Objet  : <span class='fw-bolder'>" + str(data_befor_update["name"]) + "</span> à <span class='fw-bolder'>" + str(self.name) + "</span> <br/> "

        if "stage_id" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Etape  : <span class='fw-bolder'>" + str(data_befor_update["stage_id"]) + "</span> à <span class='fw-bolder'>" + str(self.stage_id.name) + "</span> <br/> "

        if "numero_a_o" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Numero A.O  : <span class='fw-bolder'>" + str(data_befor_update["numero_a_o"]) + "</span> à <span class='fw-bolder'>" + str(self.numero_a_o) + "</span> <br/> "
        if "date_visite" in vals:
            if self.date_visite==False:
                body_message += "&nbsp;&nbsp;&nbsp; Date visite  : <span class='fw-bolder'>False</span> à <span class='fw-bolder'>" + str(formatted_date_french) + "</span> <br/> "

            if self.date_visite!=False:
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
                date = datetime(int(str(self.date_visite)[0]+str(self.date_visite)[1]+str(self.date_visite)[2]+str(self.date_visite)[3]), int(str(self.date_visite)[5]+str(self.date_visite)[6]),int(str(self.date_visite)[8]+str(self.date_visite)[9]))
                formatted_date = date.strftime('%d , %B , %Y').lower()
                day_name = date.strftime('%A')
                day, month, year = formatted_date.split(' , ')
                # Translate the month to French and capitalize the first letter
                
                month_french = month_translation[month].capitalize()
                day_french = day_translation[day_name].capitalize()
                # Combine the day, translated month, and year
                formatted_date_french = f'{day_french} {day}  {month_french}  {year}'
                body_message += "&nbsp;&nbsp;&nbsp; Date visite  : <span class='fw-bolder'>" + str(data_befor_update["date_visite"]) + "</span> à <span class='fw-bolder'>" + str(formatted_date_french) + "</span> <br/> "

        if "duration_months" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Délai d'éxecution en mois  : <span class='fw-bolder'>" + str(data_befor_update["duration_months"]) + "</span> à <span class='fw-bolder'>" + str(self.duration_months) + "</span> <br/> "

        if "duration_days" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Délai d\'éxecution en jours  : <span class='fw-bolder'>" + str(data_befor_update["duration_days"]) + "</span> à <span class='fw-bolder'>" + str(self.duration_days) + "</span> <br/> "
        if "groupement" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Groupement  : <span class='fw-bolder'>" + str(data_befor_update["groupement"]) + "</span> à <span class='fw-bolder'>" + str(self.groupement) + "</span> <br/> "
        if "partner_id_groupement" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Partenaires  : <span class='fw-bolder'>" + str(data_befor_update["partner_id_groupement"]) + "</span> à <span class='fw-bolder'>" + str(self.partner_id_groupement.name) + "</span> <br/> "
        if "courriel" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Courriel  : <span class='fw-bolder'>" + str(data_befor_update["courriel"]) + "</span> à <span class='fw-bolder'>" + str(self.courriel) + "</span> <br/> "
        if "bet" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; B.E.T  : <span class='fw-bolder'>" + str(data_befor_update["bet"]) + "</span> à <span class='fw-bolder'>" + str(self.bet.name) + "</span> <br/> "
        if "architecte" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Architecte  : <span class='fw-bolder'>" + str(data_befor_update["architecte"]) + "</span> à <span class='fw-bolder'>" + str(self.architecte.name) + "</span> <br/> "
        if "bct" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; B.C.T  : <span class='fw-bolder'>" + str(data_befor_update["bct"]) + "</span> à <span class='fw-bolder'>" + str(self.bct.name) + "</span> <br/> "
        if "qualifications" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Qualifications  : <span class='fw-bolder'>" + str(data_befor_update["qualifications"]) + "</span> à <span class='fw-bolder'>" + str(self.qualifications) + "</span> <br/> "
        if "nature_de_marche" in vals:
            nature_marche='Marches prives' if self.nature_de_marche=='marches_prives' else 'Marches publics'
            
            body_message += "&nbsp;&nbsp;&nbsp; Nature du marche  : <span class='fw-bolder'>" + str(data_befor_update["nature_de_marche"]) + "</span> à <span class='fw-bolder'>" + str(nature_marche) + "</span> <br/> "
        if "s_electronique" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; S.Electronique  : <span class='fw-bolder'>" + str(data_befor_update["s_electronique"]) + "</span> à <span class='fw-bolder'>" + str(self.s_electronique) + "</span> <br/> "
        if "phone_crm" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Telephone  : <span class='fw-bolder'>" + str(data_befor_update["phone_crm"]) + "</span> à <span class='fw-bolder'>" + str(self.phone_crm) + "</span> <br/> "
        if "nom_du_contact" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Nom du Contact  : <span class='fw-bolder'>" + str(data_befor_update["nom_du_contact"]) + "</span> à <span class='fw-bolder'>" + str(self.nom_du_contact) + "</span> <br/> "
        if "titre_nom_du_contact" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Titre  : <span class='fw-bolder'>" + str(data_befor_update["titre_nom_du_contact"]) + "</span> à <span class='fw-bolder'>" + str(self.titre_nom_du_contact) + "</span> <br/> "
        if "site_web" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Site Web  : <span class='fw-bolder'>" + str(data_befor_update["site_web"]) + "</span> à <span class='fw-bolder'>" + str(self.site_web) + "</span> <br/> "
        if "expected_revenue" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Caution Provisoire  : <span class='fw-bolder'>" + str(data_befor_update["expected_revenue"]) + "</span> à <span class='fw-bolder'>" + str(self.expected_revenue) + "</span> <br/> "

        if "mobile" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Mobile  : <span class='fw-bolder'>" + str(data_befor_update["mobile"]) + "</span> à <span class='fw-bolder'>" + str(self.mobile) + "</span> <br/> "
        if "caution_provisoire" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Caution Provisoire  : <span class='fw-bolder'>" + str(data_befor_update["caution_provisoire"]) + "</span> à <span class='fw-bolder'>" + str(self.caution_provisoire) + "</span> <br/> "
        if "date_visite_des_lieux" in vals and "date_visite_des_lieux" in data_befor_update:
            if self.date_visite_des_lieux==False:
                body_message += "&nbsp;&nbsp;&nbsp; Date visite des lieux  : <span class='fw-bolder'>" + str(data_befor_update["date_visite_des_lieux"]) + "</span> à <span class='fw-bolder'>False</span> <br/> "

            if self.date_visite_des_lieux!=False:

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
                date = datetime(int(str(self.date_visite_des_lieux)[0]+str(self.date_visite_des_lieux)[1]+str(self.date_visite_des_lieux)[2]+str(self.date_visite_des_lieux)[3]), int(str(self.date_visite_des_lieux)[5]+str(self.date_visite_des_lieux)[6]),int(str(self.date_visite_des_lieux)[8]+str(self.date_visite_des_lieux)[9]))
                formatted_date = date.strftime('%d , %B , %Y').lower()
                day_name = date.strftime('%A')
                day, month, year = formatted_date.split(' , ')
                # Translate the month to French and capitalize the first letter
                
                month_french = month_translation[month].capitalize()
                day_french = day_translation[day_name].capitalize()
                # Combine the day, translated month, and year
                formatted_date_french = f'{day_french} {day}  {month_french}  {year}'

                body_message += "&nbsp;&nbsp;&nbsp; Date visite des lieux  : <span class='fw-bolder'>" + str(data_befor_update["date_visite_des_lieux"]) + "</span> à <span class='fw-bolder'>" + str(formatted_date_french) + "</span> <br/> "

        if "date_ech" in vals:
            if self.date_ech==False:
                body_message += "&nbsp;&nbsp;&nbsp; Date de dépôt  : <span class='fw-bolder'>" + str(data_befor_update["date_ech"]) + "</span> à <span class='fw-bolder'>False</span> <br/> "

            if self.date_ech!=False:

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
                date = datetime(int(str(self.date_ech)[0]+str(self.date_ech)[1]+str(self.date_ech)[2]+str(self.date_ech)[3]), int(str(self.date_ech)[5]+str(self.date_ech)[6]),int(str(self.date_ech)[8]+str(self.date_ech)[9]))
                formatted_date = date.strftime('%d , %B , %Y').lower()
                day_name = date.strftime('%A')
                day, month, year = formatted_date.split(' , ')
                # Translate the month to French and capitalize the first letter
                
                month_french = month_translation[month].capitalize()
                day_french = day_translation[day_name].capitalize()
                # Combine the day, translated month, and year
                formatted_date_french = f'{day_french} {day}  {month_french}  {year}'
                body_message += "&nbsp;&nbsp;&nbsp; Date de dépôt  : <span class='fw-bolder'>" + str(data_befor_update["date_ech"]) + "</span> à <span class='fw-bolder'>" + str(formatted_date_french) + "</span> <br/> "

        if "date_deadline" in vals:
            if self.date_deadline==False:
                body_message += "&nbsp;&nbsp;&nbsp; D. Soumission : <span class='fw-bolder'>" + str(data_befor_update["date_deadline"]) + "</span> à <span class='fw-bolder'>False</span> <br/> "

            if self.date_deadline!=False:
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
                date = datetime(int(str(self.date_deadline)[0]+str(self.date_deadline)[1]+str(self.date_deadline)[2]+str(self.date_deadline)[3]), int(str(self.date_deadline)[5]+str(self.date_deadline)[6]),int(str(self.date_deadline)[8]+str(self.date_deadline)[9]))
                formatted_date = date.strftime('%d , %B , %Y').lower()
                day_name = date.strftime('%A')
                day, month, year = formatted_date.split(' , ')
                # Translate the month to French and capitalize the first letter
                
                month_french = month_translation[month].capitalize()
                day_french = day_translation[day_name].capitalize()
                # Combine the day, translated month, and year
                formatted_date_french = f'{day_french} {day}  {month_french}  {year}'            
                body_message += "&nbsp;&nbsp;&nbsp; D. Soumission : <span class='fw-bolder'>" + str(data_befor_update["date_deadline"]) + "</span> à <span class='fw-bolder'>" + str(formatted_date_french) + "</span> <br/> "
        

        user=self.env.user
        startdate=datetime.now()
        type_of_crm="Piste" if self.type=="Lead" else "Opportunité"
        print("the date from write")
        if "name" in vals or "type" in vals or "date_deadline" and self.date_deadline!=False:
            if type_of_crm=="Opportunité":
                self.env["calendar.event"].search([("res_model_id","=","crm.lead"),("res_id","=",self.id)],limit=1).write({
                           'name': ""+str(type_of_crm)+" : "+str(self.name)+" ",
                           'partner_ids':[[6,False,[self.user_id.partner_id.id]]],
                           'start': datetime.strptime(str(self.date_deadline), "%Y-%m-%d %H:%M:%S"),
                           'stop':self.date_deadline+timedelta(hours=1),
                           'description': "une "+str(self.type)+" avec le nom : "+str(self.name)+"",

            })
        id_message_posted=self.env["mail.message"].search([("model","=","crm.lead")], order='id desc',limit=1).id

        if len(data_befor_update)>0:

            self.env["mail.message"].create({
                      "body":body_message,
                       'email_from': '"'+user.partner_id.name+'" <'+user.login+'>',
                       'message_type': 'comment',
                       'subtype_id': 1,
                       'subject': False,
                       'model': 'mail.channel',
                       'res_id': self.env["mail.channel"].search([("name","=","CRM"),("channel_type","=","channel")],limit=1).id,
                       'record_name': 'CRM',
                })

        return crm
    # Cette fonction est utilisée pour convertir l'enregistrement actuel en un projet (project.project).
    def convert_to_project(self):
        
        
        # Recherche d'un projet existant avec le même nom que l'enregistrement actuel
        data = self.env["project.project"].search([("name", "=", self.name)])
        
        # Si un projet avec le même nom existe, une erreur est levée
        if data:
            raise ValidationError(_("Cette piste existe déjà"))
        
        if len(self.tag_ids)>0:
           for rec in  self.tag_ids:
               #create etiquette project
               if not self.env["project.tags"].search([("name","=",rec.name)]):
                   self.env["project.tags"].create({
                       "name":rec.name
                   })

        # Création d'un nouveau projet en utilisant les données de l'enregistrement actuel
        tag_ids_project=[[6,False,[]]]
        for rec in self.tag_ids:
            tag_ids_project[0][2].append(self.env["project.tags"].search([("name","=",rec.name)],limit=1).id)

        project_created=self.env["project.project"].create({
            "name": self.name,  # Nom du projet
            "numero_marche": self.numero_a_o,  # Numéro de marché
            "montant_marche": self.expected_revenue,  # Montant du marché
            "type": "chantier",  # Type de projet (chantier)
            "ordre_de_service": self.date_deadline,  # Date de l'ordre de service
            "tag_ids":tag_ids_project
        })
        #get the attchmenets

        files=self.env["ir.attachment"].search([("res_model","=","crm.lead"),("res_id","=",self.id)])

        #create tag converted from crm
        is_tag_document_exist=self.env["documents.tag"].search([("name","=","PROJET converti à partir de CRM")])
        if not is_tag_document_exist:
            self.env["documents.tag"].create({
                "name":"PROJET converti à partir de CRM",
                "facet_id":self.env["documents.facet"].search([("name","=","Documents")],limit=1).id
                })
        if len(files)>0:
            parent_folder=self.env["documents.folder"].search([("name","like",str(project_created.name)+'%')],limit=1)
            folder_ao=self.env["documents.folder"].search([("name","like","Dossier AO%"),("parent_folder_id","=",parent_folder.id)],limit=1).id                
            for rec in files:
                rec.write({
                    "res_model":"project.project",
                    "res_id":project_created.id,
                    # "folder_id":folder.id
                })
                
                self.env["documents.document"].search([("attachment_id","=",rec.id)],limit=1).write({
                    "tag_ids":[[6,False,[self.env["documents.tag"].search([("name","=","PROJET converti à partir de CRM")],limit=1).id]]],
                    "folder_id":folder_ao
                })

            # Obtenire le nombre de fishier 
            number_of_files=self.env["documents.document"].search_count([("folder_id","=",folder_ao)])

            self.env["documents.folder"].search([("name","like","Dossier AO%"),("parent_folder_id","=",parent_folder.id)],limit=1).write({
                            "name":"Dossier AO ("+str(number_of_files)+")"
            })
            match = re.search(r'\((\d+)\)', parent_folder.name)

            if match:
                        # Extract the number and convert it to an integer
                        number = int(match.group(1))

                        # Add 7 to the number
                        new_number = number + number_of_files-1

                        # Replace the old number in the original string with the new number
                        new_string = re.sub(r'\((\d+)\)', f'({new_number})', parent_folder.name)
                        parent_folder.write({"name":new_string})


    def archivecrm(self):
        crm_lead_all=self.env["crm.lead"].search([("active","=",False)])
        for rec in crm_lead_all:
                 message=self.env["mail.message"].search([("model","=","crm.lead"),("res_id","=",rec.id)],order="id desc",limit=1)
                 if len(message)==1:
                     mail_tracking=self.env["mail.tracking.value"].search([("mail_message_id","=",message.id)])
                     for record in mail_tracking:
                         if record.field.name=="active" and record.new_value_integer==0:
                            if (datetime.now()-record.create_date).days==180 and rec.type=="lead":
                                rec.unlink()
                            elif (datetime.now()-record.create_date).days==720 and rec.type=="opportunity":
                                rec.unlink()
             
    def delete_piste(self):

       
        
        view_id = self.env.ref('crm_riad.wizard_form_view_delete_piste').id
        name = _('Supprimer Piste')
        return{
            'name':name,
            # 'context': {

             

            #     "default_res_id": self.id

            # }, 
            
            'type':'ir.actions.act_window',
            'view_mode':'form',
            'res_model':'wizard.piste.delete',
            'view_id' : view_id,
            'views' : [(view_id,'form')],
            'target':'new',
            
        }
    def convert_to_opportunity(self):
        self.type="opportunity"
        if self.date_visite:
            self.is_visite_des_lieux=True
            self.date_visite_des_lieux=self.date_visite
        self.redirect_lead_opportunity_view()
    def mark_as_lost(self):
            # print("mark as lost")
        res = self.action_set_lost(lost_reason_id=None)
        return res
    def _message_get_suggested_recipients(self):
        recipients = super(crm_lead, self)._message_get_suggested_recipients()
        transformed_data = {key: [] for key in recipients}
        return transformed_data
