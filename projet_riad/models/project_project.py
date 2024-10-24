from odoo import models,fields,api,_
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import ast
import re
class project_project(models.Model):
        
    _inherit="project.project"
    # active=fields.Boolean(string="Active",default=True,groups='project.group_project_manager')

    # Champ pour l'email du projet
    email_project = fields.Char(string="Choisissez l'email du projet",track_visibility='always')
    # Champ pour le numéro du marché
    numero_marche = fields.Char(string="Numéro du marché",track_visibility='always')

    # Champ pour le montant du marché (Monétaire)
    montant_marche = fields.Monetary(string="Montant marché")

    # Champ pour les travaux exécutés (Monétaire, calculé par la méthode "_get_travaux_executer")
    travaux_executes = fields.Monetary(string="Travaux Exécutés", compute="_get_travaux_executer")

    # Champ pour le montant restant (Monétaire, calculé par la méthode "_get_montant_restant")
    montant_restant = fields.Monetary(string="Montant restant", compute="_get_montant_restant")

    # Champ pour le pré-financement (Monétaire)
    pre_financement = fields.Monetary(string="Pré-financement")

    # Champ pour le type (Sélection parmi 'chantier' ou 'interne', par défaut 'chantier')
    type = fields.Selection([('chantier', 'Chantier'), ('interne', 'Interne')], string="Type", default='chantier',track_visibility='always')

    # Champ pour la confidentialité (Sélection parmi différentes options)
    privacy_visibility_new = fields.Selection([
        ('followers', 'Sur invitation uniquement'),
        ('employees', 'Visible par tous les salariés'),
        ('portal', 'Visible par les clients suiveurs'),
    ], string='Confidentialité', required=True, default='followers')

    # Champ pour le compte bancaire (Many2one, lié au modèle "res.partner.bank")
    compt_banqaire = fields.Many2one("res.partner.bank", "Compte bancaire")
    channel_id=fields.Many2one("mail.channel")
    # Champ pour la sous-tâche du projet (Many2one, lié au modèle "project.task")
    # sous_tache_projet = fields.Many2one("project.task", string="Sous-tâche du projet")
    sous_tache_project = fields.Many2one("project.project", string="Sous-tâche du projet")

    # Champ pour la séquence (Entier)
    sequence = fields.Integer(string="Séquence")

    # Champs pour le délai d'exécution Mois
    delai_exuction_mois = fields.Integer(string="Délai d'éxecution")
    
    # Champs pour le délai d'exécution Jours
    delai_exuction_jour = fields.Integer(string="Délai d'éxecution")

    # Champs pour le délai d'avenant Mois 
    delai_avenant_mois = fields.Integer(string="Délai d'avenant")
    
    # Champs pour le délai d'avenant Jours
    delai_avenant_jours = fields.Integer(string="Délai d'avenant")

    # Champ pour le nombre de fichiers joints (Entier, calculé par la méthode "_compute_nbr_attached_file")
    nbr_field_attached = fields.Integer(string='Nombre Des Fichier', compute='_compute_nbr_attached_file')

    # Champ pour l'ordre de service (Date)
    ordre_de_service = fields.Date(string="Ordre de service")

    # Champ pour la date de réception provisoire (Datetime, calculé par la méthode "_get_date_reception_provisoire")
    date_reception_provisoire = fields.Datetime(string="Date de réception provisoire", compute="_get_date_reception_provisoire")

    # Champ pour le délai consommé (Texte, calculé par la méthode "_get_delai_consomer_from_order_date")
    delai_consome = fields.Char(string="Délai consommé", compute='_get_delai_consomer_from_order_date')

    # Champ pour le nombre de jours de délai consommé (Entier, par défaut 0)
    delai_consome_nbr = fields.Integer(string="Délai consommé", default=0)

    # Champ pour l'achat du projet (Entier, par défaut 0, calculé par la méthode "_get_purchase_order_to_this_project")
    achat_prject = fields.Integer(string="Achat Project", default=0, compute="_get_purchase_order_to_this_project")

    # Champ pour le calendrier des arrêts (Many2one, lié au modèle "resource.calendar")
    calendrier_des_arret = fields.Many2one("resource.calendar", string='Calendrier des arrêts')

    # Champ pour le total des arrêts (Texte, calculé par la méthode "_get_totale_des_arret")
    totale_des_arrets = fields.Char(string="Total des arrêts", compute="_get_totale_des_arret")

    # Champ pour le délai restant (Texte, calculé par la méthode "_get_delai_delai_restant")
    delai_restant = fields.Char(string="Délai restant", compute="_get_delai_delai_restant")

    # Champ pour le nombre de jours de délai restant (Entier)
    delai_restant_nbr = fields.Integer("Délai restant", compute="_get_delai_delai_restant",default=0)

    # Champ pour le compte des mouvements comptables (Texte, calculé par la méthode "_comput_get_account_move")
    dp_account_move = fields.Char("Compte des mouvements comptables", compute="_compute_get_account_move")

    # Champ pour le nombre de tâches de projet (Entier, calculé par la méthode "_compute_get_pv_task_of_prject")
    pv_project_task = fields.Integer("Nombre de tâches de projet", compute="_compute_get_pv_task_of_project")

    # Champ pour le nombre de tâches pour le projet (Texte, calculé par la méthode "_compute_nbr_tasks_for_project")
    nbr_tasks_for_project = fields.Char("Nombre de tâches pour le projet", compute="_compute_nbr_tasks_for_project")

    # Champ pour le nombre d'activités de courrier électronique pour le projet (Texte, calculé par la méthode "_get_nbr_mail_activity_for_project")
    nbr_mail_activity_for_proj = fields.Char("Nombre d'activités de courrier électronique pour le projet", compute="_get_nbr_mail_activity_for_project")

    # Champ pour le nombre de factures (Entier, calculé par la méthode "_nbr_invoices")
    nbr_invoices = fields.Integer("Nombre de factures", compute="_nbr_invoices")

    # Champ pour le nombre de mouvements de stock (Entier, calculé par la méthode "_nbr_stock_move")
    nbr_stock_move = fields.Integer("Nombre de mouvements de stock", compute="_nbr_stock_move")

    # Champ pour le budget du projet (Many2one, lié au modèle "crossovered.budget")
    budget_id = fields.Many2one("crossovered.budget", "Budget du projet")

    # Champ pour l'état du budget du projet (Sélection, lié à l'état du budget)
    budget_state = fields.Selection("Status", related='budget_id.state')

    # Champ pour les lignes de budget du projet (One2many, lié aux lignes de budget du budget principal)
    budget_lines = fields.One2many(
        comodel_name='crossovered.budget.lines',
        inverse_name='crossovered_budget_id',
        related='budget_id.budget_lines',
        string='',
        readonly=True
    )

    # Champ Many2one pour le responsable des études associé à un partenaire
    resp_etude = fields.Many2one("res.partner", "Resp. Etudes")

    # Champ Many2one pour le responsable du recouvrement associé à un utilisateur
    resp_Recouvrement = fields.Many2one("res.users", "Resp. Recouvrement")

    # Champ Many2one pour le chef de chantier associé à un partenaire
    chef_chantier = fields.Many2one("res.partner", "Chef de chantier")

    # Champ Many2one pour le métreur associé à un utilisateur
    metreur = fields.Many2one("res.users", "Métreur")

    # Champ Many2one pour le comptable associé à un utilisateur
    comptable = fields.Many2one("res.users", "Comptable / Caissier")
    

    # Champ Many2one pour le réceptionniste associé à un partenaire
    receptionniste = fields.Many2one("res.partner", "Réceptionniste")
     
    # Champ Many2one pour le pointeur associé à un partenaire
    pointeur = fields.Many2one("res.partner", "Pointeur")
    
    # Champ pour le type de construction (Sélection parmi plusieurs options)
    type_of_construction = fields.Selection([
        ('agricultural', 'Agriculture'),
        ('residential', 'Résidence'),
        ('commercial', 'Commercial'),
        ('institutional', 'Institution'),
        ('industrial', 'Industriel'),
        ('heavy_civil', 'Civil'),
        ('environmental', 'Environnement'),
        ('other', 'Autre')],
        string='Type de chantier'
    )


    # Champ Many2one pour l'architecte associé à un partenaire
    architect_id = fields.Many2one("res.partner", "Architecte")

    # Champ Many2one pour le bureau d'études techniques (B.E.T) associé à un partenaire
    bet = fields.Many2one("res.partner", "B.E.T")

    # Champ Many2one pour le bureau de contrôle technique (B.C.T) associé à un partenaire
    bct = fields.Many2one("res.partner", "B.C.T")

    # Champ Many2one pour le laboratoire associé à un partenaire
    lab_id = fields.Many2one("res.partner", "Laboratoire")

    # Champ Many2one pour le topographe associé à un partenaire
    topographe_id = fields.Many2one("res.partner", "Topographe")

    # Champ Many2one pour le métreur externe associé à un partenaire
    metreur_ext_id = fields.Many2one("res.partner", "Métreur externe")

    # Champ pour le nombre de factures payées (Entier, calculé par la méthode "_get_invoice_payer")
    get_invoice_payer = fields.Integer("Nombre de factures payées", compute="_get_invoice_payer")

    # Champ pour le nombre d'arrêts (Entier, calculé par la méthode "_get_leave_account")
    leave_count = fields.Integer('Nombre d\'arrêts', compute='_get_leave_account')

    # Champ pour les arrêts et les reprises (One2many, lié au modèle "resource.calendar.leaves")
    leave_ids = fields.One2many('resource.calendar.leaves', related='resource_calendar_id.leave_ids', string='Arrêts/reprises')

    # Champ pour le nombre de lignes comptables analytiques (Entier, calculé par la méthode "_get_account_analitic_line")
    get_account_analytic_line = fields.Integer("Nombre de lignes comptables analytiques", compute="_get_account_analytic_line")

    # Champ pour l'état actif (Texte, calculé par la méthode "_get_is_active")
    is_active = fields.Char("État actif", compute="_get_is_active")

    # Champ pour le fishier d'order de service
    order_service_file = fields.Binary("order_service_file")
    documents_folder_id=fields.Many2one("documents.folder","Espace de travail",store=True)
    message_partner_ids=fields.Many2many('res.partner','')
    #tests_ids = fields.Many2many('demo.tests','demo_test_id','name','tests ids')
    # is_visible_for_user_connected=fields.Boolean("is_visible_for_user_connected",compute='_is_visible_for_user_connected',store=True)
    resp_etude=fields.Many2one("res.users",string="Resp. Etudes")
    rapoteur=fields.Many2one("res.users",string="Rapporteur (Admin)")
    check_user = fields.Boolean(string='check_user',track_visibility='always')
    # Définition d'une fonction pour déterminer l'état actif ou inactif

    # @api.depends('name','privacy_visibility','message_partner_ids')
    # @api.onchange('name','privacy_visibility','message_partner_ids')
    # def _is_visible_for_user_connected(self):
    #     print("test")
    #     partner_connected=self.env["res.users"].sudo().search([('id','=',self.env.uid)],limit=1)                
    #     for rec in self:
    #         rs=True
            
    #         if partner_connected.login=='rem@entrepriseriad.ma':
    #             rec.is_visible_for_user_connected=True
    #             query = "UPDATE PROJECT_PROJECT SET is_visible_for_user_connected=%s WHERE ID=%s"
    #             self.env.cr.execute(query, (True,rec.id))

    #         else:
    #             if rec.privacy_visibility_new=="followers" and  partner_connected.partner_id.id not in rec.message_partner_ids.ids:
    #                 rs=False
    #             query = "UPDATE PROJECT_PROJECT SET is_visible_for_user_connected=%s WHERE ID=%s"
    #             self.env.cr.execute(query, (rs,rec.id))
                
            
    def _get_is_active(self):
     
        # Pour chaque enregistrement (self) dans le contexte
        for rec in self:
            # Si l'enregistrement est actif (active est vrai), définir "Archiver" dans le champ is_active
            # Sinon, définir "Désarchiver" dans le champ is_active
            rec.is_active = "Archiver" if rec.active == True else "Désarchiver"

          
    # Définition d'une fonction pour obtenir le montant total des travaux exécutés

    def _get_travaux_executer(self):

        # Pour chaque enregistrement (self) dans le contexte

        for rec in self:
            # Recherche des factures (account.move) associées à l'enregistrement actuel (projet) avec certaines conditions :
            # 1. project_id doit correspondre à l'ID de l'enregistrement actuel (rec.id).
            # 2. state doit être l'une des valeurs 'draft', 'posted' ou 'open'.
            # Calcule la somme des montants totaux signés des factures trouvées.
            
            rec.travaux_executes = sum(self.env['account.move'].search([
                ('project_id', '=', rec.id),
                ('state', 'in', ['draft', 'posted', 'open'])
            ]).mapped('amount_total_signed'))
                
    # Définition d'une fonction avec une dépendance aux champs 'montant_marche'
    @api.depends('montant_marche')
    def _get_montant_restant(self):

        # Pour chaque enregistrement (self) dans le contexte
        for rec in self:

            # Si le champ 'montant_marche' est défini pour cet enregistrement
            if rec.montant_marche:

                # Calculer le champ 'montant_restant' comme la différence entre 'montant_marche' et 'travaux_executes'
                rec.montant_restant = rec.montant_marche - rec.travaux_executes
            else:

                # Si 'montant_marche' n'est pas défini, définir 'montant_restant' à 0
                rec.montant_restant = 0

                
    # Définition d'une fonction pour obtenir le nombre de mouvements de stock liés à un projet
    def _nbr_stock_move(self):

        # Pour chaque enregistrement (self) dans le contexte
        for rec in self:

            # # Recherche des commandes d'achat (purchase.order) associées à l'enregistrement actuel (projet) avec certaines conditions :
            # purchase_order = self.env['purchase.order'].search([('projet', '=', rec.id)])

            # if purchase_order:
            #     # Si des commandes d'achat sont trouvées, calcule le nombre de mouvements de stock en parcourant les listes de prélèvements (picking)
            #     stock_moves_count = sum(len(picking.move_ids) for picking in purchase_order.picking_ids)
            #     # Met à jour le champ 'nbr_stock_move' avec le nombre de mouvements de stock calculé
            #     rec.nbr_stock_move = stock_moves_count
            # else:
            #     # Si aucune commande d'achat n'est trouvée, définir le champ 'nbr_stock_move' à 0
                rec.nbr_stock_move = 0


    # Définition d'une fonction pour obtenir le nombre de factures fournisseur liées à un projet
    def _nbr_invoices(self):

        # Pour chaque enregistrement (self) dans le contexte
        for rec in self:

            # Recherche et compte le nombre de factures fournisseur (account.move) associées à l'enregistrement actuel (projet) avec certaines conditions :
            rec.nbr_invoices = self.env['account.move'].search_count([
                ('project_id', '=', rec.id),
                ('state', '=', 'open'),
                ('move_type', '=', 'in_invoice')
            ])

    # Définition d'une fonction pour obtenir le nombre d'activités par courrier électronique liées à un projet
    def _get_nbr_mail_activity_for_project(self):

        # Pour chaque enregistrement (self) dans le contexte
        for rec in self:

            # Recherche et compte le nombre d'activités en retard (overdue activities) liées à l'enregistrement actuel (projet) avec certaines conditions :
            over_due_activities = self.env["mail.activity"].search_count([
                ('date_deadline', '<', datetime.now()),
                ('res_id', '=', rec.id),
                ('res_model_id', '=', self.env['ir.model'].search([('model', '=', 'project.project')], limit=1).id if self.env['ir.model'].search([('model', '=', 'project.project')], limit=1) else -1)
            ])
            
            # Recherche et compte le nombre total d'activités (all activities) liées à l'enregistrement actuel (projet) avec certaines conditions :
            all_activities = self.env["mail.activity"].search_count([
                ('res_id', '=', rec.id),
                ('res_model_id', '=', self.env['ir.model'].search([('model', '=', 'project.project')], limit=1).id if self.env['ir.model'].search([('model', '=', 'project.project')], limit=1) else -1)
            ])
            
            # Combine les nombres d'activités en retard et le nombre total d'activités dans une chaîne de texte
            rec.nbr_mail_activity_for_proj = str(over_due_activities) + "/" + str(all_activities)
              
    def _compute_nbr_tasks_for_project(self):
        for rec in self:
            task_assign=0
            task_suvie=0
            all_tasks_count=self.env["project.task"].sudo().search_count([("project_id","=",rec.id)])
            all_tasks=self.env["project.task"].sudo().search([("project_id","=",rec.id)])
            for t in all_tasks:
                if self.env.user.id in t.user_ids.ids: 
                    task_assign+=1
                if self.env.user.partner_id.id in t.message_partner_ids.ids: 
                    task_suvie+=1
            
            if self.env.user.has_group('project.group_project_manager') or rec.rapoteur.id==self.env.user.id or self.env.user.has_group('admin_without_delete.admin_without_delete'):
                rec.nbr_tasks_for_project = str(task_assign) + ' / ' + str(task_suvie) +' / ' + str(all_tasks_count) +" Tâches"
            else:
                rec.nbr_tasks_for_project = str(task_assign) + ' / ' + str(task_suvie)  +" Tâches"

                  
    def _compute_get_pv_task_of_project(self):

        for rec in self:
            # Recherche du nombre de tâches PV associées au projet
            rec.pv_project_task = self.env['project.pv'].search_count([('projet_id', '=', rec.id)])

    def _compute_get_account_move(self):
        for rec in self:
            # Recherche du nombre de mouvements comptables en état brouillon pour le projet
            account_invoice_draft = self.env['account.move'].search_count([('project_id', '=', rec.id), ('state', '=', 'draft')])

            # Recherche du nombre de mouvements comptables en état ouvert pour le projet
            account_invoice_open = self.env['account.move'].search_count([('project_id', '=', rec.id), ('state', '=', 'open')])

            # Recherche du nombre de mouvements comptables en état posté pour le projet
            account_invoice_posted = self.env['account.move'].search_count([('project_id', '=', rec.id), ('state', '=', 'posted')])

            # Met à jour le champ "dp_account_move" de l'enregistrement avec les résultats sous la forme "brouillon / ouvert / posté"
            rec.dp_account_move = str(account_invoice_draft) + "/" + str(account_invoice_open) + "/" + str(account_invoice_posted)

    @api.depends('delai_exuction_mois', 'ordre_de_service', 'delai_exuction_jour', 'calendrier_des_arret', 'delai_avenant_mois', 'delai_avenant_jours')
    def _get_delai_delai_restant(self):
        for rec in self:
            rec.delai_restant_nbr = 0
            delai_exeuction_mois = 0              
            delai_exeuction_jour = 0
            delai_avenant_mois = 0
            delai_avenant_jours = 0
            totale_des_arrer = 0

            if rec.date_reception_provisoire:
                # Conversion des dates en objets datetime
                target_date = datetime.strptime(str(rec.date_reception_provisoire), "%Y-%m-%d %H:%M:%S").replace(hour=0, minute=0, second=0, microsecond=0)
                current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                delta = target_date - current_date
                days_remaining = delta.days

                if delta.days < 0:
                    rec.delai_restant = "0 jours | 0 %"
                else:
                    if rec.calendrier_des_arret:
                        # Calcul du total des arrêts à partir du modèle "resource.calendar.leaves"
                        totale_des_arrer = sum(self.env['resource.calendar.leaves'].search([('calendar_id', '=', rec.calendrier_des_arret.id)]).mapped('totale_des_arret'))

                    # Calcul du nombre total de jours incluant les délais
                    all_days = days_remaining + delai_exeuction_mois * 30 + delai_exeuction_jour + delai_avenant_jours + delai_avenant_mois * 30

                    months = all_days // 30
                    remaining_days = all_days % 30
                    days_remaining = days_remaining + delai_avenant_mois * 30 + delai_avenant_jours + totale_des_arrer + delai_exeuction_jour + delai_exeuction_mois * 30
                    progress_days = 0

                    if rec.ordre_de_service and rec.date_reception_provisoire:
                        # Conversion des dates en objets datetime
                        date_start_order = datetime.strptime(str(rec.ordre_de_service), "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
                        date_end_date_reception_provisoire = datetime.strptime(str(rec.date_reception_provisoire), "%Y-%m-%d %H:%M:%S").replace(hour=0, minute=0, second=0, microsecond=0)
                        total_days = date_end_date_reception_provisoire - date_start_order

                        if total_days.days + totale_des_arrer == 0:
                            progress_days = 0
                            rec.delai_restant_nbr = 0
                        else:
                            progress_days = ((all_days) / (total_days.days + totale_des_arrer)) * 100
                            progress_days = round(progress_days, 2)

                            if progress_days > 100:
                                progress_days = 100

                        rec.delai_restant_nbr = progress_days

                    if months == 0:
                        rec.delai_restant = f"{remaining_days} jours | " + str(progress_days) + " %"
                    elif months == 1 and remaining_days == 0:
                        rec.delai_restant = "1 mois / " + str(progress_days) + " %"
                    elif months == 1:
                        rec.delai_restant = f"1 mois et {remaining_days} jours / " + str(progress_days) + " %"
                    elif remaining_days == 0:
                        rec.delai_restant = f"{months} mois / " + str(progress_days) + " %"
                    else:
                        rec.delai_restant = f"{months} mois et {remaining_days} jours / " + str(progress_days) + " %"
            else:
                rec.delai_restant = ""
                rec.delai_restant_nbr = 0

    @api.depends('calendrier_des_arret')
    def _get_totale_des_arret(self):
        for rec in self:
            if rec.calendrier_des_arret:
                # Vérifie si des congés spécifiés dans le calendrier d'arrêt existent
                if self.env['resource.calendar.leaves'].search([('calendar_id', '=', rec.calendrier_des_arret.id)]):
                    # Calcul du total des jours de congé à partir du modèle "resource.calendar.leaves"
                    days = sum(self.env['resource.calendar.leaves'].search([('calendar_id', '=', rec.calendrier_des_arret.id)]).mapped('totale_des_arret'))
                    months = days // 30
                    remaining_days = days % 30

                    if months == 0:
                        rec.totale_des_arrets = f"{remaining_days} jours"
                    elif months == 1 and remaining_days == 0:
                        rec.totale_des_arrets = "1 mois"
                    elif months == 1:
                        rec.totale_des_arrets = f"1 mois et {remaining_days} jours"
                    elif remaining_days == 0:
                        rec.totale_des_arrets = f"{months} mois"
                    else:
                        rec.totale_des_arrets = f"{months} mois et {remaining_days} jours"
                else:
                    rec.totale_des_arrets = 0
            else:
                rec.totale_des_arrets = 0
                 
                         
                
                       
                  
         
    @api.depends('ordre_de_service', 'delai_exuction_mois', 'delai_exuction_jour', 'delai_avenant_mois', 'delai_avenant_jours','totale_des_arrets')
    def _get_date_reception_provisoire(self):
        for rec in self:
            if rec.ordre_de_service:
                # here we should the total des arrete

                # Initialisation des variables pour les jours et les mois ajoutés
                days_added = 0
                months_added = 0

                days_added_second = 0
                months_added_second = 0
                total_des_arret=0
                if rec.calendrier_des_arret:
                        total_des_arret = sum(self.env['resource.calendar.leaves'].search([('calendar_id', '=', rec.calendrier_des_arret.id)]).mapped('totale_des_arret'))
                # Vérification des délais d'avenant et mise à jour des variables
                if rec.delai_avenant_mois:
                    months_added_second = rec.delai_avenant_mois

                if rec.delai_avenant_jours:
                    days_added_second = rec.delai_avenant_jours


                # Vérification des délais d'exécution et mise à jour des variables
                if rec.delai_exuction_mois:
                    months_added = rec.delai_exuction_mois

                if rec.delai_exuction_jour:
                    days_added = rec.delai_exuction_jour

                # Calcul de la date de réception provisoire en ajoutant les délais
                rec.date_reception_provisoire = rec.ordre_de_service + relativedelta(days=days_added_second) + relativedelta(months=months_added_second) + relativedelta(days=total_des_arret)  + relativedelta(days=days_added) + relativedelta(months=months_added)

            else:

                # Si le champ "ordre_de_service" n'est pas défini, la date de réception provisoire est définie comme nulle
                rec.date_reception_provisoire = None

    def _get_purchase_order_to_this_project(self):

        for rec in self:

            # Recherche du nombre de commandes d'achat associées au projet

            # rec.achat_prject = self.env["purchase.order"].search_count([('projet', '=', rec.id)])
            rec.achat_prject = 0
    
    @api.depends('calendrier_des_arret', 'delai_avenant_mois', 'delai_avenant_jours', 'date_reception_provisoire', 'delai_exuction_mois', 'delai_exuction_jour')

    def _get_delai_consomer_from_order_date(self):

        for rec in self:

            if rec.date_reception_provisoire:

                # Conversion des dates en objets datetime

                target_date = datetime.strptime(str(rec.ordre_de_service), "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)

                current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

                delta = current_date - target_date

                if delta.days < 0:

                    rec.delai_consome = "0 jours"

                else:

                    days_remaining = delta.days

                    tt_arret = 0

                    delai_avenant_mois = 0

                    delai_avenant_jours = 0

                    delai_exeuction_mois = 0

                    delai_exeuction_jour = 0

                    if rec.calendrier_des_arret:

                        # Vérification des congés dans le calendrier d'arrêt

                        if self.env['resource.calendar.leaves'].search([('calendar_id', '=', rec.calendrier_des_arret.id)]):

                            tt_arret = tt_arret + sum(self.env['resource.calendar.leaves'].search([('calendar_id', '=', rec.calendrier_des_arret.id)]).mapped('totale_des_arret'))

                    days_remaining = days_remaining + delai_avenant_mois * 30 + delai_avenant_jours + tt_arret + delai_exeuction_jour + delai_exeuction_mois * 30

                    progress_days = 0

                    if rec.ordre_de_service and rec.date_reception_provisoire:

                        date_start_order = datetime.strptime(str(rec.ordre_de_service), "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)

                        date_end_date_reception_provisoire = datetime.strptime(str(rec.date_reception_provisoire), "%Y-%m-%d %H:%M:%S").replace(hour=0, minute=0, second=0, microsecond=0)

                        total_days = date_end_date_reception_provisoire - date_start_order

                        if total_days.days + tt_arret == 0:

                            progress_days = 0

                        else:

                            progress_days = ((days_remaining) / (total_days.days + tt_arret)) * 100

                            progress_days = round(progress_days, 2)

                            if progress_days > 100:

                                progress_days = 100


                    months = days_remaining // 30

                    remaining_days = days_remaining % 30

                    if months == 0:
     
                        rec.delai_consome = f"{remaining_days} jours | " + str(progress_days) + " %"
     
                    elif months == 1 and remaining_days == 0:
     
                        rec.delai_consome = "1 mois | " + str(progress_days) + " %"
     
                    elif months == 1:
     
                        rec.delai_consome = f"1 mois et {remaining_days} jours | " + str(progress_days) + " %"
     
                    elif remaining_days == 0:

                        rec.delai_consome = f"{months} mois | " + str(progress_days) + " %"

                    else:

                        rec.delai_consome = f"{months} mois et {remaining_days} jours | " + str(progress_days) + " %"

            else:

                rec.delai_consome = ""

                rec.delai_consome_nbr = 0


         
    def _compute_nbr_attached_file(self):
        self = self.sudo()        
        for record in self:
            is_checke_user=False
            if record.env.user.has_group('project.group_project_manager'):
                is_checke_user=True
            if record.rapoteur.id==self.env.user.id:
                is_checke_user=True
            query = "UPDATE PROJECT_PROJECT SET check_user=%s WHERE ID=%s"
            self.env.cr.execute(query, (is_checke_user,record.id))
            # Recherche du nombre de fichiers attachés à l'enregistrement actuel
            # record.nbr_field_attached=record.documents_folder_id.document_count
            ids=record.documents_folder_id.children_folder_ids.ids
            ids.append(record.documents_folder_id.id)
            documents_nbr=self.env["documents.document"].search_count([("folder_id","in",ids)])
            record.nbr_field_attached = documents_nbr
            # record.nbr_field_attached = self.env["ir.attachment"].search_count([('projet_id', '=', record.id)])

            # if record.name=="Nassim Is Odoo":
            #     for f in record.documents_folder_id.children_folder_ids:
            #         print(f.name)
            #         print("---")
            #     nbr_documents=self.env["documents.document"].search_count([("res_model","=","project.task"),("res_id","in",record.task_ids.ids)])+self.env["documents.document"].search_count([("res_model","=","project.project"),("res_id","=",record.id)])
            #     #                 ('res_model', '=', 'project.project'), ('res_id', '=', self.id),
            #     # '&',
            #     # ('res_model', '=', 'project.task'), ('res_id', 'in', self.task_ids.ids)
            #     print(nbr_documents)
            #     # print(record.documents_folder_id.document_count)
            #     # print(record.documents_folder_id.children_folder_ids[0].document_count)
            #     print("---")

    def get_attachment_for_user(self):
        self = self.sudo()
        self.env["ir.attachment"].search([("res_id","=",self.id),("res_model","=","project.project")]).write({
            "projet_id":self.id
        })
        for t in self.env["project.task"].search([("project_id","=",self.id),("active","in",[True,False])]):
            self.env["ir.attachment"].search([("res_model","=","project.task"),("res_id","=",t.id)]).write({
            "projet_id":self.id
            })
        self.ensure_one()
        # return {
        #     'res_model': 'documents.document',
        #     'type': 'ir.actions.act_window',
        #     'name': _("%(project_name)s's Documents", project_name=self.name),
        #     'domain': [
        #     '|',
        #         '&',
        #         ('res_model', '=', 'project.project'), ('res_id', '=', self.id),
        #         '&',
        #         ('res_model', '=', 'project.task'), ('res_id', 'in', self.task_ids.ids)
        #     ],
        #     'view_mode': 'kanban,tree,form',
        #     'context': {'default_res_model': 'project.project', 'default_res_id': self.id, 'limit_folders_to_project': True},
        # }

#         action = self.env['ir.actions.act_window']._for_xml_id('documents_project.action_view_documents_project_task')
#         action['context']={
#             'folder_id':self.documents_folder_id.id,
#             # 'default_tag_ids': self.documents_tag_ids.ids,
# 'limit_folders_to_project': True,

#         }
#         # action['context'] = {
#         #     **ast.literal_eval(action['context'].replace('active_id', str(self.id))),
#         #     'default_tag_ids': self.documents_tag_ids.ids,
#         # }
#         print(action['context'])
#         print("----")

#         return action

        return {

            'name': _('Fichiers joints'),  # Nom de la fenêtre contextuelle
            
            'domain': [("project_id","=",self.id)],  # Critères de recherche

            'view_type': 'kanban',  # Type de vue

            'context': {
                
                "default_res_model": "project.project",

                "default_res_id": self.id,
                "limit_folders_to_project":True
                # "search_default_projet_id": self.id


            },  # Contexte pour la création de nouveaux enregistrements

            'res_model': 'documents.document',  # Modèle cible de la fenêtre contextuelle

            'view_id': False,  # ID de la vue à utiliser (dans ce cas, aucune vue spécifique n'est définie)

            'view_mode': 'tree,kanban,form',  # Modes de vue disponibles

            'type': 'ir.actions.act_window'  # Type de l'action de fenêtre
        }

    def get_achat_for_project(self):

        return {

            'name': _('Les Achats'),  # Nom de la vue contextuelle

            'domain': [('projet', '=', self.id)],  # Critères de recherche pour les achats associés à ce projet

            'context': {

                "default_projet": self.id,

                "search_default_projet": self.id

            },  # Contexte pour la création de nouveaux enregistrements et les valeurs de recherche par défaut

            'view_type': 'form',  # Type de vue

            'res_model': 'purchase.order',  # Modèle cible de la vue contextuelle

            'view_id': False,  # ID de la vue à utiliser (dans ce cas, aucune vue spécifique n'est définie)

            'view_mode': 'tree,form,kanban',  # Modes de vue disponibles

            'type': 'ir.actions.act_window'  # Type de l'action de fenêtre contextuelle

        }

    def get_account_move_project(self):

        return {

            'name': _('Factures clients'),  # Nom de la vue contextuelle

            'domain': [('project_id', '=', self.id)],  # Critères de recherche pour les factures clients associées à ce projet

            'context': {

                "default_project_id": self.id,

                "search_default_project_id": self.id

            },  # Contexte pour la création de nouveaux enregistrements et les valeurs de recherche par défaut

            'view_type': 'kanban',  # Type de vue

            'res_model': 'account.move',  # Modèle cible de la vue contextuelle

            'view_id': False,  # ID de la vue à utiliser (dans ce cas, aucune vue spécifique n'est définie)

            'view_mode': 'tree,form,kanban',  # Modes de vue disponibles

            'type': 'ir.actions.act_window'  # Type de l'action de fenêtre contextuelle

        }
    
    def get_pv_for_project(self):

        for rec in self:

            return {

                'name': _('PV(S)'),  # Nom de la vue contextuelle

                'domain': [('projet_id', '=', rec.id)],  # Critères de recherche pour les PV associés à ce projet

                'context': {

                    "default_is_project_readonly": True,

                    "default_projet_id": rec.id,

                    "search_default_projet_id": rec.id

                },  # Contexte pour la création de nouveaux enregistrements et les valeurs de recherche par défaut

                'view_type': 'tree,form',  # Type de vue

                'res_model': 'project.pv',  # Modèle cible de la vue contextuelle

                'view_id': False,  # ID de la vue à utiliser (dans ce cas, aucune vue spécifique n'est définie)

                'view_mode': 'tree,form',  # Modes de vue disponibles

                'type': 'ir.actions.act_window'  # Type de l'action de fenêtre contextuelle

            }

    def get_nbr_task_for_project(self):
        # for rec in self.env["user.filter"].search([]):
        #     rec.unlink()

        project = self.sudo().browse(self.ids)
        return project.action_view_tasks_sudo()

        # return {

        #     'name': _('Tâches'),  # Nom de la vue contextuelle

        #     'domain': [('project_id', '=', self.id),('message_is_follower','=',True)],  # Critères de recherche pour les tâches associées à ce projet

        #     'context': {

        #         "default_is_project_readonly": True,
        #         "search_default_followed_by_me": 1,

        #         "default_project_id": self.id,

        #         "search_default_project_id": self.id

        #     },  # Contexte pour la création de nouveaux enregistrements et les valeurs de recherche par défaut

        #     'view_type': 'tree',  # Type de vue

        #     'res_model': 'project.task',  # Modèle cible de la vue contextuelle

        #     'view_id': False,  # ID de la vue à utiliser (dans ce cas, aucune vue spécifique n'est définie)

        #     'view_mode': 'kanban,tree,form,calendar,gantt',  # Modes de vue disponibles

        #     'type': 'ir.actions.act_window'  # Type de l'action de fenêtre contextuelle

        # }

    def get_the_activity_platform_for_project(self):

        return {

            'name': _('Activités'),  # Nom de la vue contextuelle

            'domain': [('res_id', '=', self.id), ('res_model_id', '=', self.env['ir.model'].search([('model', '=', 'project.project')], limit=1).id if self.env['ir.model'].search([('model', '=', 'project.project')], limit=1) else -1)],  # Critères de recherche pour les activités associées à ce projet

            'context': {

                "default_project_id": self.id,

                "search_default_project_id": self.id

            },  # Contexte pour la création de nouveaux enregistrements et les valeurs de recherche par défaut

            'view_type': 'tree',  # Type de vue

            'res_model': 'mail.activity',  # Modèle cible de la vue contextuelle

            'view_id': False,  # ID de la vue à utiliser (dans ce cas, aucune vue spécifique n'est définie)

            'view_mode': 'tree,form',  # Modes de vue disponibles

            'type': 'ir.actions.act_window'  # Type de l'action de fenêtre contextuelle

        }

    def get_invoices_open_in_onvoice(self):

        return {
            'name': _('Factures clients'),  # Nom de la vue contextuelle

            'domain': [('project_id', '=', self.id), ('state', '=', 'open'), ('move_type', '=', 'in_invoice')],  # Critères de recherche pour les factures clients ouvertes associées à ce projet

            'context': {

                "default_project_id": self.id,

                "search_default_project_id": self.id

            },  # Contexte pour la création de nouveaux enregistrements et les valeurs de recherche par défaut

            'view_type': 'tree',  # Type de vue

            'res_model': 'account.move',  # Modèle cible de la vue contextuelle

            'view_id': False,  # ID de la vue à utiliser (dans ce cas, aucune vue spécifique n'est définie)

            'view_mode': 'tree,form,kanban',  # Modes de vue disponibles

            'type': 'ir.actions.act_window'  # Type de l'action de fenêtre contextuelle
        }

    def get_stock_move_for_project(self):
        return {

            'name': _('Mouvements de stocks'),  # Nom de la vue contextuelle

            'domain': [

                ('projet', '=', self.id),  # Remplacez 'project_id' par le nom du champ correct

                ('picking_ids', '!=', False)  # Filtrer les commandes d'achat avec au moins un mouvement de stock associé

            ],

            'context': {

                "default_projet": self.id,

                "search_default_projet": self.id

            },  # Contexte pour la création de nouveaux enregistrements et les valeurs de recherche par défaut

            'view_type': 'kanban',  # Type de vue

            'res_model': 'purchase.order',  # Modèle cible de la vue contextuelle (c'est peut-être un modèle incorrect dans le contexte des mouvements de stock)

            'view_id': False,  # ID de la vue à utiliser (dans ce cas, aucune vue spécifique n'est définie)

            'view_mode': 'tree,form,kanban',  # Modes de vue disponibles

            'type': 'ir.actions.act_window'  # Type de l'action de fenêtre contextuelle
        }

    def create_purchase_order(self):
        

        view_id = self.env.ref('projet_riad.id_project_create_sale_order_view_form').id  # ID de la vue de formulaire à utiliser

        return {

            'name': _('Créer un bon de commande'),  # Nom de la vue contextuelle

            'context': {"default_partner_id": self.id},  # Contexte pour la création de nouveaux enregistrements et les valeurs par défaut

            'type': 'ir.actions.act_window',  # Type de l'action de fenêtre contextuelle

            'view_mode': 'form',  # Mode de vue

            'res_model': 'project.create.sale.order',  # Modèle cible de la vue contextuelle

            'view_id': view_id,  # ID de la vue de formulaire

            'views': [(view_id, 'form')],  # Spécifie la vue à utiliser

            'target': 'new',  # Ouvrir la vue dans une nouvelle fenêtre
        }

    def get_account_move_project_payer(self):

        return {

            'name': _('Factures clients'),  # Nom de la vue contextuelle

            'domain': [('project_id', '=', self.id), ('state', '=', 'posted')],  # Critères de recherche pour les factures clients payées associées à ce projet

            'context': {

                "default_project_id": self.id,

                "search_default_project_id": self.id,

                "search_default_state": "posted"

            },  # Contexte pour la création de nouveaux enregistrements et les valeurs de recherche par défaut

            'view_type': 'kanban',  # Type de vue

            'res_model': 'account.move',  # Modèle cible de la vue contextuelle

            'view_id': False,  # ID de la vue à utiliser (dans ce cas, aucune vue spécifique n'est définie)

            'view_mode': 'tree,form,kanban',  # Modes de vue disponibles

            'type': 'ir.actions.act_window'  # Type de l'action de fenêtre contextuelle
        }

    def _get_invoice_payer(self):

        for rec in self:

            # Initialisation du champ 'get_invoice_payer' pour l'enregistrement actuel

            rec.get_invoice_payer = self.env['account.move'].search_count([

                ('project_id', '=', rec.id),  # Recherche de factures liées à ce projet

                ('state', '=', 'posted')  # Recherche de factures dans l'état "posté" (payées)

            ])

    def _get_leave_account(self):

        for rec in self:

            # Initialisation du champ 'leave_count' pour l'enregistrement actuel

            rec.leave_count = len(rec.resource_calendar_id.global_leave_ids)

    def get_view_leave_count(self):
        return {

            'name': _('Congés globaux'),  # Nom de la vue contextuelle

            'domain': [('calendar_id', '=', self.resource_calendar_id.id)],  # Filtrer les congés globaux pour ce calendrier de ressources

            'context': {

                "default_calendar_id": self.resource_calendar_id.id  # Définir la valeur par défaut du champ 'calendar_id'

            },

            'view_type': 'tree',  # Type de vue

            'res_model': 'resource.calendar.leaves',  # Modèle cible de la vue contextuelle

            'view_id': False,  # ID de la vue à utiliser (dans ce cas, aucune vue spécifique n'est définie)

            'view_mode': 'tree,form,kanban',  # Modes de vue disponibles

            'type': 'ir.actions.act_window'  # Type de l'action de fenêtre contextuelle
        }

    def _get_account_analytic_line(self):
        
        for rec in self:
        
            # Initialisation du champ 'get_account_analitic_line' pour l'enregistrement actuel
        
            rec.get_account_analytic_line = sum(self.env['account.analytic.line'].search([('project_id', '=', rec.id)]).mapped('amount'))

    def show_account_analytic_line(self):
        return {
            'name': _('Coûts & revenus'),  # Nom de la vue contextuelle

            'domain': [('project_id', '=', self.id)],  # Filtrer les lignes analytiques pour ce projet

            'context': {

                "default_project_id": self.id  # Définir la valeur par défaut du champ 'project_id'

            },

            'view_type': 'tree',  # Type de vue

            'res_model': 'account.analytic.line',  # Modèle cible de la vue contextuelle

            'view_id': False,  # ID de la vue à utiliser (dans ce cas, aucune vue spécifique n'est définie)

            'view_mode': 'tree,form,kanban',  # Modes de vue disponibles

            'type': 'ir.actions.act_window'  # Type de l'action de fenêtre contextuelle

        }

    def archive_action_function(self):

        for rec in self:


            rec.is_active = "Archive" if rec.active == True else "Désarchiver"

            rec.active = not rec.active
    # @api.model
    def write(self, vals):

        if not self.env.user.has_group('project.group_project_manager') and 'active' in vals:
                                    raise ValidationError(_("Vous n'êtes pas autorisé à archiver un projet !!"))

        # if 'active' in vals:
        #              project = super(project_project, self).write(vals)
        #              return project
        data_before_updated={}
        if "name" in vals:
            data_before_updated['name']=str(self.name)
        if "numero_marche" in vals:
            data_before_updated['numero_marche']=str(self.numero_marche)
        if "type" in vals:
            data_before_updated['type']=str(self.type)
        if "privacy_visibility_new" in vals:
            data_before_updated['privacy_visibility_new']=str(self.privacy_visibility_new)
        if "partner_id" in vals:
            data_before_updated['partner_id']=str(self.partner_id.name)
        if "delai_exuction_mois" in vals:
            data_before_updated['delai_exuction_mois']=str(self.delai_exuction_mois)
        if "delai_avenant_mois" in vals:
            data_before_updated['delai_avenant_mois']=str(self.delai_avenant_mois)
        if "delai_avenant_jours" in vals:
            data_before_updated['delai_avenant_jours']=str(self.delai_avenant_jours)
        if "ordre_de_service" in vals:
            data_before_updated['ordre_de_service']=str(self.ordre_de_service)
        if "user_id" in vals:
            data_before_updated['user_id']=str(self.user_id.partner_id.name)
        if "resp_etude" in vals:
            data_before_updated['resp_etude']=str(self.resp_etude.partner_id.name)
        if "rapoteur" in vals:
            data_before_updated['rapoteur']=str(self.rapoteur.partner_id.name)
        if "resp_Recouvrement" in vals:
            data_before_updated['resp_Recouvrement']=str(self.resp_Recouvrement.partner_id.name)
        if "metreur" in vals:
            data_before_updated['metreur']=str(self.metreur.partner_id.name)
        if "comptable" in vals:
            data_before_updated['comptable']=str(self.comptable.partner_id.name)
        if "receptionniste" in vals:
            data_before_updated['receptionniste']=str(self.receptionniste.name)
        if "pointeur" in vals:
            data_before_updated['pointeur']=str(self.pointeur.name)
        if "type_of_construction" in vals:
            data_before_updated['type_of_construction']=str(self.type_of_construction)
        if "delai_exuction_jour" in vals:
            data_before_updated['delai_exuction_jour']=str(self.delai_exuction_jour)

        project = super(project_project, self).write(vals)
        if "resp_etude" in vals or "metreur" in vals or "chef_chantier" in vals or "resp_Recouvrement" in vals and 'user_id' in vals:
            self.add_to_group_compta()

        if len(data_before_updated)>0:
            body_message = "Projet modifié  Par : <span class='fw-bolder'>"+str(self.env.user.partner_id.name)+"</span><br/>"
            if "name" in vals:
                # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
                body_message += "&nbsp;&nbsp;&nbsp; Nom : <span class='fw-bolder'>" + str(data_before_updated["name"]) + "</span> à <span class='fw-bolder'>" + str(self.name) + "</span> <br/> "
            if "numero_marche" in vals:
                # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
                body_message += "&nbsp;&nbsp;&nbsp; Numéro du marché : <span class='fw-bolder'>" + str(data_before_updated["numero_marche"]) + "</span> à <span class='fw-bolder'>" + str(self.numero_marche) + "</span> <br/> "
            if "type" in vals:
                # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
                body_message += "&nbsp;&nbsp;&nbsp; Type : <span class='fw-bolder'>" + str(data_before_updated["type"]) + "</span> à <span class='fw-bolder'>" + str(self.type) + "</span> <br/> "
            if "privacy_visibility_new" in vals:
                # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
                conf_old=data_before_updated["privacy_visibility_new"]
                conf_new=self.privacy_visibility_new
                print(data_before_updated["privacy_visibility_new"])
                if conf_old=="followers": conf_old="Sur invitation uniquement"
                if conf_old=="employees": conf_old="Visible par tous les salariés"
                if conf_old=="portal": conf_old="Visible par les clients suiveurs"

                if conf_new=="followers": conf_new="Sur invitation uniquement"
                if conf_new=="employees": conf_new="Visible par tous les salariés"
                if conf_new=="portal": conf_new="Visible par les clients suiveurs"
                body_message += "&nbsp;&nbsp;&nbsp; Confidentialité : <span class='fw-bolder'>" + str(conf_old) + "</span> à <span class='fw-bolder'>" + str(conf_new)  + "</span> <br/> "
            if "partner_id" in vals:
                # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
                body_message += "&nbsp;&nbsp;&nbsp; Client : <span class='fw-bolder'>" + str(data_before_updated["partner_id"]) + "</span> à <span class='fw-bolder'>" + str(self.partner_id.name) + "</span> <br/> "
            if "delai_exuction_mois" in vals:
                # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
                body_message += "&nbsp;&nbsp;&nbsp; Délai d'éxecution Mois : <span class='fw-bolder'>" + str(data_before_updated["delai_exuction_mois"]) + "</span> à <span class='fw-bolder'>" + str(self.delai_exuction_mois) + "</span> <br/> "
            if "delai_avenant_mois" in vals:
                # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
                body_message += "&nbsp;&nbsp;&nbsp; Délai d'avenant Mois : <span class='fw-bolder'>" + str(data_before_updated["delai_avenant_mois"]) + "</span> à <span class='fw-bolder'>" + str(self.delai_avenant_mois) + "</span> <br/> "
            if "delai_avenant_jours" in vals:
                # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
                body_message += "&nbsp;&nbsp;&nbsp; Délai d'avenant Jour : <span class='fw-bolder'>" + str(data_before_updated["delai_avenant_jours"]) + "</span> à <span class='fw-bolder'>" + str(self.delai_avenant_jours) + "</span> <br/> "
            if "ordre_de_service" in vals:
                # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
                body_message += "&nbsp;&nbsp;&nbsp; Ordre de service : <span class='fw-bolder'>" + str(data_before_updated["ordre_de_service"]) + "</span> à <span class='fw-bolder'>" + str(self.ordre_de_service) + "</span> <br/> "
            if "user_id" in vals:
                # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
                body_message += "&nbsp;&nbsp;&nbsp; Chef de Projet : <span class='fw-bolder'>" + str(data_before_updated["user_id"]) + "</span> à <span class='fw-bolder'>" + str(self.user_id.partner_id.name) + "</span> <br/> "
            if "resp_etude" in vals:
                # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
                body_message += "&nbsp;&nbsp;&nbsp; Resp. Etudes : <span class='fw-bolder'>" + str(data_before_updated["resp_etude"]) + "</span> à <span class='fw-bolder'>" + str(self.resp_etude.partner_id.name) + "</span> <br/> "
            if "rapoteur" in vals:
                # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
                body_message += "&nbsp;&nbsp;&nbsp; Rapporteur : <span class='fw-bolder'>" + str(data_before_updated["rapoteur"]) + "</span> à <span class='fw-bolder'>" + str(self.rapoteur.partner_id.name) + "</span> <br/> "
            if "resp_Recouvrement" in vals:
                # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
                body_message += "&nbsp;&nbsp;&nbsp; Resp. Recouvrement : <span class='fw-bolder'>" + str(data_before_updated["resp_Recouvrement"]) + "</span> à <span class='fw-bolder'>" + str(self.resp_Recouvrement.partner_id.name) + "</span> <br/> "
            if "metreur" in vals:
                # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
                body_message += "&nbsp;&nbsp;&nbsp; Métreur : <span class='fw-bolder'>" + str(data_before_updated["metreur"]) + "</span> à <span class='fw-bolder'>" + str(self.metreur.partner_id.name) + "</span> <br/> "
            if "comptable" in vals:
                # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
                body_message += "&nbsp;&nbsp;&nbsp; Comptable : <span class='fw-bolder'>" + str(data_before_updated["comptable"]) + "</span> à <span class='fw-bolder'>" + str(self.comptable.partner_id.name) + "</span> <br/> "
            if "receptionniste" in vals:
                # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
                body_message += "&nbsp;&nbsp;&nbsp; Réceptionniste : <span class='fw-bolder'>" + str(data_before_updated["receptionniste"]) + "</span> à <span class='fw-bolder'>" + str(self.receptionniste.name) + "</span> <br/> "
            if "pointeur" in vals:
                # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
                body_message += "&nbsp;&nbsp;&nbsp; Pointeur : <span class='fw-bolder'>" + str(data_before_updated["pointeur"]) + "</span> à <span class='fw-bolder'>" + str(self.pointeur.name) + "</span> <br/> "
            if "type_of_construction" in vals:
                # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
                body_message += "&nbsp;&nbsp;&nbsp; Type de chantier : <span class='fw-bolder'>" + str(data_before_updated["type_of_construction"]) + "</span> à <span class='fw-bolder'>" + str(self.type_of_construction) + "</span> <br/> "
            if "delai_exuction_jour" in vals:
                # Si le nom de la tâche est spécifié dans les valeurs, l'ajouter au message
                body_message += "&nbsp;&nbsp;&nbsp; Délai d'éxecution Jour : <span class='fw-bolder'>" + str(data_before_updated["delai_exuction_jour"]) + "</span> à <span class='fw-bolder'>" + str(self.delai_exuction_jour) + "</span> <br/> "


            user = self.env.user

            self.env["mail.message"].create({
                    "body": body_message,

                    'email_from': '"' + user.partner_id.name + '" <' + user.login + '>',

                    'message_type': 'comment',

                    'subtype_id': 1,

                    'subject': False,

                    'model': 'mail.channel',

                    'res_id': self.channel_id.id,

                    'record_name': 'Chantier',
                })

        if "name" in vals:
            self.channel_id.write({
                "name": vals["name"],

                "channel_type": "channel"
            })
            self.documents_folder_id.write({
                "name":vals["name"]
            })
        

        if "active" in  vals and len(vals)==1:
            for rec in self:
                rec.documents_folder_id.write({
                    "active":vals["active"]
                })     
                

                # query="update documents_folder set active=%s where id=%s"
                # self.env.cr.execute(query, (vals["active"],rec.documents.))

            return project
        if self.active == False:
            
            # Recherche du dossier de documents associé à ce projet
            document_folder = self.env["documents.folder"].search([("name", "like", str(self.name)+'%')], limit=1)
            
            # Obtenir les documents de ce dossier
            documents_document = self.env["documents.document"].search([("folder_id", "=", document_folder.id)])
            
            # Archiver les documents
            for rec in documents_document:

                rec.write({

                    "active": False

                })
            
            # Obtenir les dossiers enfants du dossier de documents
            documents_children = self.env["documents.folder"].search([("parent_folder_id", "=", document_folder.id)])
            
            
            # Archiver les documents dans les dossiers enfants
            
            for rec in documents_children:

                documents_document = self.env["documents.document"].search([("folder_id", "=", rec.id)])

                # Archiver les documents
                for rec in documents_document:

                    rec.write({

                        "active": False

                    })

        # Recherche du dernier message lié au modèle 'project.project'
        # id_message_posted = self.env["mail.message"].search([("model", "=", "project.project")], order='id desc', limit=1).id
        
        # # Recherche des valeurs de suivi mises à jour
        # values_updated = self.env["mail.tracking.value"].search([("mail_message_id", "=", id_message_posted)])
        
        # is_channel_updated_old_value = ""
        
        # if len(values_updated) != 0:

        self.clear_caches()

        return project

    
    
    @api.model
    def create(self, vals):
        
        # Vérifie si un canal chantier avec le même nom existe déjà
        is_channel_chantier_exist = self.env["mail.channel"].search([("name", "like", vals["name"]+'%'), ("channel_type", "=", "channel")])

        # Si le canal n'existe pas, crée un nouveau canal
        if not is_channel_chantier_exist:
            self.env["mail.channel"].create({
                "name": vals["name"],

                "channel_type": "channel"
            })
            vals["channel_id"]=self.env["mail.channel"].search([("name","=",vals["name"]),('channel_type','=','channel')]).id
            
            
            
        # Crée un message pour enregistrer la création du projet
        body_message = "Projet créé <br/>"

        # Ajoute les informations du projet au message
        if "name" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Nom  : <span class='fw-bolder'>" + str(vals["name"]) + "</span> <br/> "
        else:
            body_message += "&nbsp;&nbsp;&nbsp; Nom  :  <br/> "
        if "type" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Type  : <span class='fw-bolder'>" + str(vals["type"]) + "</span> <br/> "
        else:
            body_message += "&nbsp;&nbsp;&nbsp; Type  : <br/> "
        if "numero_marche" in vals:
            body_message += "&nbsp;&nbsp;&nbsp; Numéro du marché  : <span class='fw-bolder'>" + str(vals["numero_marche"]) + "</span> <br/> "
        else:
            body_message += "&nbsp;&nbsp;&nbsp; Numéro du marché  :  <br/> "

        user = self.env.user

        # Crée un message pour enregistrer la création du projet
        self.env["mail.message"].create({
            "body": body_message,

            'email_from': '"' + user.partner_id.name + '" <' + user.login + '>',

            'message_type': 'comment',

            'subtype_id': 1,

            'subject': False,

            'model': 'mail.channel',

            'res_id': vals["channel_id"],

            'record_name': vals["name"],
        })

        # Appel de la méthode de création de la classe parente pour créer le projet
        project = super(project_project, self).create(vals)
        if "resp_etude" in vals or "metreur" in vals or "chef_chantier" in vals or "resp_Recouvrement" in vals or 'user_id' in vals:
            project.add_to_group_compta()

        # Crée 4 sous-dossiers nommés (Correspondance, Finance & Comptabilité, Taches photos, Plan & Détail Technique, Administration)
        parent_id = self.env["documents.folder"].search([], order='id desc', limit=1).id
        folder_name_old=self.env["documents.folder"].search([], order='id desc', limit=1).name
        self.env["documents.folder"].search([], order='id desc', limit=1).write({
            "name": folder_name_old+"",
            "project_id":project.id      
        })
        
        
        self.env["documents.folder"].create({
            "name": "Photos et Taches",
            "parent_folder_id": parent_id,
            "project_id":project.id

        })


        # Crée un nouveau calendrier de ressources pour le projet
        self.env["resource.calendar"].create({

            "name": vals["name"],

            "tz": "Europe/Paris"
        })

        # Recherche le calendrier de ressources créé
        r = self.env['resource.calendar'].search([('name', '=', vals["name"])], limit=1)

        # Associe le calendrier de ressources au projet
        project.calendrier_des_arret = r.id

        # Crée des types de tâches par défaut s'ils n'existent pas
        if self.env["project.task.type"].search_count([('name', '=', 'Nouvelle Tâche')]) == 0:
            self.env["project.task.type"].create({"name": "Nouvelle Tâche"})
       
        if self.env["project.task.type"].search_count([('name', '=', 'Etudes En Cours')]) == 0:
            self.env["project.task.type"].create({"name": "Etudes En Cours"})
       
        if self.env["project.task.type"].search_count([('name', '=', 'Exécution En Cours')]) == 0:
            self.env["project.task.type"].create({"name": "Exécution En Cours"})
       
        if self.env["project.task.type"].search_count([('name', '=', 'Tâche Accomplie')]) == 0:
            self.env["project.task.type"].create({"name": "Tâche Accomplie"})
       
        if self.env["project.task.type"].search_count([('name', '=', 'Tâche Annulée')]) == 0:
            self.env["project.task.type"].create({"name": "Tâche Annulée"})

        # Obtient les ID des types de tâches créés
        typ_tach_1 = self.env["project.task.type"].search([('name', '=', 'Nouvelle Tâche')], limit=1).id

        typ_tach_2 = self.env["project.task.type"].search([('name', '=', 'Etudes En Cours')], limit=1).id

        typ_tach_3 = self.env["project.task.type"].search([('name', '=', 'Exécution En Cours')], limit=1).id

        typ_tach_4 = self.env["project.task.type"].search([('name', '=', 'Tâche Accomplie')], limit=1).id

        typ_tach_5 = self.env["project.task.type"].search([('name', '=', 'Tâche Annulée')], limit=1).id

        # Associe les types de tâches au projet
        query = "INSERT INTO project_task_type_rel (type_id,project_id) values (%s,%s)"
        self.env.cr.execute(query, (typ_tach_1, project.id))

        query = "INSERT INTO project_task_type_rel (type_id,project_id) values (%s,%s)"
        self.env.cr.execute(query, (typ_tach_2, project.id))

        query = "INSERT INTO project_task_type_rel (type_id,project_id) values (%s,%s)"
        self.env.cr.execute(query, (typ_tach_3, project.id))

        query = "INSERT INTO project_task_type_rel (type_id,project_id) values (%s,%s)"
        self.env.cr.execute(query, (typ_tach_4, project.id))

        query = "INSERT INTO project_task_type_rel (type_id,project_id) values (%s,%s)"
        self.env.cr.execute(query, (typ_tach_5, project.id))

        # Vérifie si une invitation pour le projet existe déjà
        if self.env["mail.wizard.invite"].search_count([('res_model', '=', 'crm_lead'), ('message', "=", "Vous avez invité au piste " + vals['name']), ('res_id', '=', project.id)]) == 0:

            self.env["mail.wizard.invite"].create({

                "res_id": project.id,

                "res_model": "project.project",

                "message": "Vous avez invité au piste " + vals["name"],

            })

        # Fonction pour ajouter des abonnés à un enregistrement
        
        def add_follower(record, partner, model):

            filter_data = self.env["mail.followers"].sudo().search([('res_id', '=', record.id), ('partner_id', '=', partner.partner_id.id), ('res_model', '=', model)])

            if not filter_data:

                self.env["mail.followers"].sudo().with_context(mail_create_nosubscribe=True).create({

                    "res_id": record.id,

                    "partner_id": partner.partner_id.id,

                    "res_model": model

                })

        # Recherche des utilisateurs qui sont abonnés aux projets
        user_of_crm = self.env["res.users"].search([("is_follower_for_project", "=", True)])
        
        # Ajoute ces utilisateurs comme abonnés du projet
        for rec in user_of_crm:
            add_follower(project, rec, "project.project")

            add_follower(project.user_id, rec, "res.partner")
            #add the followers to the created channel
            channel_id=vals["channel_id"]

            is_user_memeber_already_in_the_channel=self.env["mail.channel.member"].search([("partner_id","=",rec.partner_id.id),(("channel_id","=",channel_id))])
            if not is_user_memeber_already_in_the_channel:
                self.env["mail.channel.member"].create({
                    "partner_id":rec.partner_id.id,
                    "channel_id":channel_id
                })
            
        # Vérifie si les balises (tags) "Admin" et "Installation" existent
        is_tag_admin = self.env["project.tags"].search([("name", "=", "Admin")])
        
        is_tag_chantier = self.env["project.tags"].search([("name", "=", "Installation")])

        # Si les balises n'existent pas, les crée
        if not is_tag_chantier:

            self.env["project.tags"].create({

                "name": "Installation",

            })

        if not is_tag_admin:

            self.env["project.tags"].create({

                "name": "Admin",
            })

        # Retourne l'enregistrement du projet créé
        self.clear_caches()
        return project

    def import_ms_project(self):

        # Obtient l'ID de la vue pour l'action
        view_id = self.env.ref('projet_riad.id_project_ms').id

        return {

            'name': _('IMPORTER UN FICHIER DE MS PROJET'),

            'context': {"default_projet_id": self.id},  # Initialise le contexte avec l'ID du projet actuel

            'domain': [('projet_id', '=', self.id)],  # Filtre les enregistrements par projet_id égal à l'ID du projet actuel

            'type': 'ir.actions.act_window',

            'view_mode': 'form',

            'res_model': 'project.ms',

            'view_id': view_id,  # Utilise l'ID de la vue pour la nouvelle fenêtre

            'views': [(view_id, 'form')],

            'target': 'new'  # Ouvre la nouvelle fenêtre dans un nouvel onglet
        }
 
    
    def import_task_instalation(self):
        for rec in self.env["project.task.default"].search([("is_task_initial","=",True),("type_task","=",'Installation')]):
            date_start=datetime.now()
            date_fin=date_start+timedelta(days=(rec.date_fin-rec.date_debut).days)
            
            rec.write({
                "date_debut":date_start,
                "date_fin":date_fin,
            }) 


        # Parcourt tous les enregistrements dans le modèle "project.task.default"
        for rec in self.env["project.task.default"].search([("is_task_initial","=",False),("type_task","=",'Installation')],order='sequece asc'):
            if rec.the_start_task:
                date_debut=rec.the_start_task.date_fin+timedelta(days=rec.nbr_days_task_start)
                date_fin=date_debut+timedelta(days=(rec.date_fin-rec.date_debut).days)
                rec.write({
                    "date_debut":date_debut,
                    "date_fin":date_fin,
                })

        # Parcourt tous les enregistrements dans le modèle "project.task.default"
        for rec in self.env["project.task.default"].search([]):
            # Met à jour l'attribut 'id_project_assign_to' de chaque enregistrement pour lui assigner l'ID du projet actuel

            rec.write({'id_project_assign_to': self.id})

        return {
            'name': _("Importer des tâches d'installation"),

            'type': 'ir.actions.act_window',

            'domain': [('type_task', '=', 'Installation')],  # Filtrage des enregistrements de type "Installation"

            'context': {'default_type_task': 'Installation'},  # Définition du contexte avec la valeur par défaut "Installation"

            'view_type': 'tree',

            'res_model': 'project.task.default',  # Modèle à afficher

            'view_id': False,

            'view_mode': 'tree,form',  # Modes d'affichage possibles
        }
    
    def import_task_admin(self):
        
        for rec in self.env["project.task.default"].search([("is_task_initial","=",True),("type_task","=",'Admin')]):
            date_start=datetime.now()
            date_fin=date_start+timedelta(days=(rec.date_fin-rec.date_debut).days)
            rec.write({
                "date_debut":date_start,
                "date_fin":date_fin,
            }) 
         
        # Parcourt tous les enregistrements dans le modèle "project.task.default"
        for rec in self.env["project.task.default"].search([("is_task_initial","=",False),("type_task","=",'Admin')],order='sequece asc'):
            if rec.the_start_task:
                deference_of_the_privious_task=rec.the_start_task.date_fin-rec.the_start_task.date_debut
                date_debut=rec.the_start_task.date_fin+timedelta(days=rec.nbr_days_task_start)
                date_fin=date_debut+timedelta(days=(rec.date_fin-rec.date_debut).days)
                rec.write({
                    "date_debut":date_debut,
                    "date_fin":date_fin,
                })

                # print(rec.the_start_task.name)
                # print(deference_of_the_privious_task.days)
                # print("-----")

            # Met à jour l'attribut 'id_project_assign_to' de chaque enregistrement pour lui assigner l'ID du projet actuel
            rec.write({'id_project_assign_to': self.id})

        return {
            'name': _("Importer des tâches d'admin"),

            'type': 'ir.actions.act_window',

            'domain': [('type_task', '=', 'Admin')],  # Filtrage des enregistrements de type "Admin"

            'context': {'default_type_task': 'Admin'},  # Définition du contexte avec la valeur par défaut "Admin"

            'view_type': 'tree',

            'res_model': 'project.task.default',  # Modèle à afficher

            'view_id': False,

            'view_mode': 'tree,form',  # Modes d'affichage possibles
        }
    def creat_folder_and_subfolder(self):
        for rec in self:
            #test if the document exist
            parent_folder=self.env["documents.folder"].search([("name","like","Chantier")],limit=1)


            is_exist=self.env["documents.folder"].search([("name","like",str(rec.name)+"%"),("parent_folder_id","=",parent_folder.id)])        
            if not is_exist:
                self.env["documents.folder"].create({
                    "name":rec.name,
                    "parent_folder_id":parent_folder.id,
                    "description":rec.id
                })
                #get this folder
                folder_created=self.env["documents.folder"].search([("name","like",str(rec.name)+"%"),("parent_folder_id","=",parent_folder.id)],limit=1)
                self.env["documents.folder"].create({
                    "name": "Dossier AO",
                    "parent_folder_id": folder_created.id
                })

                self.env["documents.folder"].create({
                    "name": "Correspondance",
                    "parent_folder_id": folder_created.id
                })


                self.env["documents.folder"].create({
                    "name": "Photos et Taches",
                    "parent_folder_id": folder_created.id
                })

                self.env["documents.folder"].create({
                    "name": "Plans et Détails techniques",
                    "parent_folder_id": folder_created.id
                })



    def action_view_tasks_sudo(self):
        print("test")
        for rec in self.task_ids:
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

        user = self.env.user
        if len(self.task_ids)>0:
            self.task_ids.write({
                "project_id_name":self.with_context(lang='fr_FR').name[:50]+"..."
            })
        for rec in self.env["project.task"].search([("project_id","=",self.id),("active","in",[True,False])]):      
            query = "UPDATE PROJECT_TASK SET nbr_field_attached=%s WHERE ID=%s"
            self.env.cr.execute(query, (self.env["ir.attachment"].sudo().search_count([('res_id', '=', rec.id), ("res_model", "=", "project.task")]),rec.id))

        if not self.env.user.has_group('base.group_erp_manager'):
            for rec in self.env["project.task"].search([("project_id","=",self.id),("active","in",[True,False])]):     
                        if  user.id in rec.user_ids.ids:
                            query = "UPDATE PROJECT_TASK SET is_mes_tach_suivi=%s WHERE ID=%s"
                            self.env.cr.execute(query, ("assigned",rec.id))
                        elif user.partner_id.id in rec.message_partner_ids.ids and user.id not in rec.user_ids.ids:
                            query = "UPDATE PROJECT_TASK SET is_mes_tach_suivi=%s WHERE ID=%s"
                            self.env.cr.execute(query, ("suived",rec.id))

                        else:
                            query = "UPDATE PROJECT_TASK SET is_mes_tach_suivi=%s WHERE ID=%s"
                            self.env.cr.execute(query, ("unsuived",rec.id))

        domain_project=[('project_id', '=', self.id)] if self.env.user.has_group('base.group_erp_manager') or self.rapoteur.id==self.env.user.id  else [('project_id', '=', self.id),('is_mes_tach_suivi','!=','unsuived')]
        for rec in self.env["user.filter"].search([]):
                rec.unlink()

        return {

            'name': _('Tâches'),  # Nom de la vue contextuelle

            # 'domain': [('project_id', '=', self.id),('is_mes_tach_suivi','!=','unsuived')],  # Critères de recherche pour les tâches associées à ce projet
            'domain': domain_project,  # Critères de recherche pour les tâches associées à ce projet

            'context': {

                "default_is_project_readonly": True,
                # "search_default_followed_by_me": 1,
                "search_default_next_45_days": 1,

                "default_project_id": self.id,

                "search_default_project_id": self.id

            },  # Contexte pour la création de nouveaux enregistrements et les valeurs de recherche par défaut

            'view_type': 'tree',  # Type de vue

            'res_model': 'project.task',  # Modèle cible de la vue contextuelle

            'view_id': False,  # ID de la vue à utiliser (dans ce cas, aucune vue spécifique n'est définie)

            'view_mode': 'kanban,tree,form,calendar,gantt',  # Modes de vue disponibles

            'type': 'ir.actions.act_window'  # Type de l'action de fenêtre contextuelle

        }

    def action_view_tasks(self):
        # for rec in self.env["user.filter"].search([]):
        #         rec.unlink()

        project = self.sudo().browse(self.ids)
        return project.action_view_tasks_sudo()
        # action = self.env['ir.actions.act_window'].with_context({'active_id': self.id})._for_xml_id('project.act_project_project_2_project_task_all')
        # action['display_name'] = _("%(name)s", name=self.name)
        # context = action['context'].replace('active_id', str(self.id))
        
        # context = ast.literal_eval(context)
        # context.update({
        #     'create': self.active,
        #     'active_test': self.active,
        #     'is_project_readonly':True
        #     })
        # action['context'] = context
        # return action
    def unlink(self):
        for rec in self:
            rec.documents_folder_id.unlink()                
            query="update project_project set documents_folder_id=%s where id=%s"
            self.env.cr.execute(query,(self.env["documents.folder"].search([("name","like","Chantier%"),("parent_folder_id","=",False)],limit=1).id, rec.id))

        project = super(project_project, self).unlink()
        return project
    def clean_folder_data(self):
        documents=self.env["ir.attachment"].search([("res_model","in",["project.project","project.task"])])
        documents.unlink()
        for rec in self:
            document_folder=self.env["documents.folder"].search([("name","like",rec.name+'%')])
            if len(document_folder)>1:
                   folders_to_delete = document_folder[1:]
                   folders_to_delete.unlink()            
            document_folder=self.env["documents.folder"].search([("name","like",rec.name+'%')])
            for rec_2 in document_folder:
                rec_2.write({
                    "name":rec.name+" (0) "
                })
                children_of_this_folder=self.env["documents.folder"].search([("parent_folder_id","=",rec_2.id)])
                                
                for record in children_of_this_folder:
                    record.unlink()
                self.env["documents.folder"].create({
                    "name": "Dossier AO",
                    "parent_folder_id": rec_2.id
                })

                self.env["documents.folder"].create({
                    "name": "Correspondance",
                    "parent_folder_id": rec_2.id
                })


                self.env["documents.folder"].create({
                    "name": "Photos et Taches",
                    "parent_folder_id": rec_2.id
                })

                self.env["documents.folder"].create({
                    "name": "Plans et Détails techniques",
                    "parent_folder_id": rec_2.id
                })

                

            #verify if the parent folder is containe any document
            folder_of_the_project=self.env['documents.folder'].search([("name","like",rec.name+'%')])
            if len(folder_of_the_project)>0:
                for rec in folder_of_the_project:
                    documents_folder=self.env["documents.document"].search([("folder_id","=",rec.id)])
                    if len(documents_folder)>0:
                        for rec in documents_folder:
                            rec.unlink()
                

            
            

                         
    def _message_get_suggested_recipients(self):
        recipients = super(project_project, self)._message_get_suggested_recipients()
        transformed_data = {key: [] for key in recipients}
        return transformed_data
    def add_to_group_compta(self):
        self = self.sudo()        

        users=self.env["res.groups"].search([("name","=","Facturation")],limit=1).sudo().users.ids
        users_sale=self.env["res.groups"].search([("name","=","Utilisateur : mes documents seulement")],limit=1).sudo().users.ids

        for rec in self.env["project.project"].sudo().search([]):
            if rec.resp_etude and rec.resp_etude.id not in users:
                users.append(rec.resp_etude.id)

            if rec.metreur and rec.metreur.id not in users_sale:
                users_sale.append(rec.metreur.id)

            if rec.metreur and rec.metreur.id not in users:
                users.append(rec.metreur.id)

            if rec.user_id and rec.user_id.id not in users_sale:
                users_sale.append(rec.user_id.id)

            if rec.resp_Recouvrement and rec.resp_Recouvrement.id not in users:
                users.append(rec.resp_Recouvrement.id)
        
        self.env["res.groups"].search([("name","=","Facturation")],limit=1).sudo().write({
                "users":[[6,False,users]]
            })     
        self.env["res.groups"].search([("name","=","Utilisateur : mes documents seulement")],limit=1).sudo().write({
                "users":[[6,False,users_sale]]
            })     
