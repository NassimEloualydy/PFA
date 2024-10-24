from odoo import models,fields,api,_
from datetime import datetime,timedelta,time
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
PAYMENT_STATE_SELECTION = [
        ('not_paid', 'Non payées'),
        ('in_payment', 'En cours de paiement'),
        ('paid', 'Payé'),
        ('partial', 'Partiellement réglé'),
        ('reversed', 'Extourné'),
        ('invoicing_legacy', "Historique de l'app facturation"),
]

class account_move(models.Model):
    
    # Inhéritance du modèle "account.move"
    _inherit = "account.move"

    # Champ Many2one pour lier à un modèle "project.project"
    project_id = fields.Many2one("project.project")
    
    # Champ Many2one pour lier à un modèle "crm.team"
    team_id = fields.Many2one("crm.team")

    # Champ "Numéro du marché" lié au champ "numero_marche" du modèle "project.project"
    project_numero_marche = fields.Char("Numéro du marché", related='project_id.numero_marche')

    # Champ "Totale" de type flottant pour le montant total de la transaction
    motant_totale = fields.Float("Totale")

    # Champ "Avance/A.D.C" de type flottant pour le montant de l'avance ou de l'A.D.C
    avance_adc = fields.Float("Avance/A.D.C")

    # Champ "Pièces jointes" de type entier calculé
    nbr_field_attached = fields.Integer(string='Pièces jointes', compute='_compute_nbr_attached_file')
        # state=fields.Selection([("draft","Brouillon"),("posted","Payé"),("cancel","Annulé"),("open","Ouverte")])

    # Champ "msg_date" de type chaîne de caractères pour stocker une date sous forme de texte
    msg_date = fields.Char(string="msg_date", compute="_get_msg_date")

    # Champ "nbr_date" de type entier pour stocker un nombre, calculé via la méthode "_get_msg_date"
    nbr_date = fields.Integer("nbr_date", compute="_get_msg_date")

    # Champ "Décompte N" de type chaîne de caractères
    decompte_n = fields.Char("Décompte N")

    # Champ "Échéance" de type entier, calculé via la méthode "_get_nbr_echeance"
    echeance = fields.Integer("Échéance", compute="_get_nbr_echeance")

    # Champ booléen "is_project_readonly" pour gérer l'état readonly du champ "project_id"
    is_project_readonly = fields.Boolean(string="", default=True, store=True, compute="_get_value_read_only")

    state=fields.Selection([('draft', 'Brouillon'), ('open', 'Ouverte'),('in paiment','En Paiment'),('paid','Payé'),('done','bloqué'),('cancel','Annulé'),('posted','Comptabilisé')],string="État")
    # Définition d'une méthode "_get_value_read_only" dans un modèle Odoo
    id_base_12=fields.Char("id_base_12")
    #type de facture
    type_account_move=fields.Char("Type")
    user_id=fields.Many2one("res.users",string="Resp .Recouvrement",store=True)
    
    active=fields.Boolean(string="Active",default=True)
    invoice_date_due = fields.Date(
        string='Due Date',
        compute='_compute_invoice_date_due_new', store=True, readonly=False,
        states={'draft': [('readonly', False)]},
        index=True,
        copy=False,
    )
    name_journal=fields.Char(related='journal_id.name')
    is_active = fields.Char("is_active", compute="_get_is_active")
    payment_state = fields.Selection(
        selection=PAYMENT_STATE_SELECTION,
        string="Payment Status",
        compute='_compute_payment_state', store=True, readonly=True,
        copy=False,
        tracking=True,
    )
    nbr_days_before_alert=fields.Integer("Nombre de jours avant la création de l'activité",default=15)
    display_name=fields.Char(string="Nom d'affichage",store=True)
    montant_avance=fields.Float("montant_avance",store=True,compute="_get_data_from_purchase")
    montant_restant=fields.Float("montant_restant",store=True,compute="_get_data_from_purchase")
    receipt_status_tree=fields.Selection([ 
        ('pending','Non Reçu'),
        ('partial','Partiellement Reçu'),
        ('full','Entièrement Reçu')        
        ],string="Livraison",store=True,compute="_get_data_from_purchase")
    def _get_value_read_only(self):
        # Parcours de chaque enregistrement (record) dans le modèle
        for rec in self:
            # Si le champ "project_id" est défini (non vide), alors "is_project_readonly" est défini comme True, sinon False
            rec.is_project_readonly = True if rec.project_id else False
                                 
        @api.depends('line_ids.purchase_line_id')
        def _get_data_from_purchase(self):
            print("the achat the comes from ")

        print("-------")
    # Définition d'une méthode "_get_nbr_echeance" dans un modèle Odoo
    @api.depends("invoice_date")
    def _get_nbr_echeance(self):
        # Parcours de chaque enregistrement (record) dans le modèle
        for rec in self:
            if rec.invoice_date:
                # Conversion de la date de facturation en objet datetime
                target_date = datetime.combine(rec.invoice_date, time.min)
                
                # Obtention de la date et de l'heure actuelles avec une heure/min/sec/microsec à zéro
                current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                
                # Calcul de la' différence entre la date actuelle et la date de facturation
                delta = current_date - target_date
                
                # Calcul des jours restants en fonction de la différence
                days_remaining = delta.days
                
                # Mise à jour du champ "echeance" avec le nombre de jours restants
                rec.echeance = days_remaining
            else:
                # Si la date de facturation n'est pas définie, "echeance" est défini à 0
                rec.echeance = 0

    # Définition d'une méthode "_get_msg_date" dans un modèle Odoo
            
    def _get_msg_date(self):
        # Parcours de chaque enregistrement (record) dans le modèle
        for rec in self:
            if rec.invoice_date:
                # Conversion de la date de facturation en objet datetime
                target_date = datetime.combine(rec.invoice_date, time.min)

                # Obtention de la date et de l'heure actuelles avec une heure/min/sec/microsec à zéro
                current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

                # Calcul de la différence entre la date actuelle et la date de facturation
                delta = current_date - target_date

                # Calcul des jours restants en fonction de la différence
                days_remaining = delta.days

                # État initial "Retard"
                state = "Retard"

                # Initialisation du champ "nbr_date" à -1 (en retard)
                rec.nbr_date = -1

                # Si les jours restants sont négatifs, changer l'état en "Rest" et mettre "nbr_date" à 1 (à l'heure)
                if days_remaining < 0:
                    days_remaining = -days_remaining
                    state = "Rest"
                    rec.nbr_date = 1

                # Si les jours restants sont égaux à zéro, mettre "nbr_date" à 0
                if days_remaining == 0:
                    rec.nbr_date = 0
                    state = ""

                # Calcul des mois et jours restants
                months = days_remaining // 30
                remaining_days = days_remaining % 30

                # Construction du message en fonction de l'état, des mois et des jours restants
                if months == 0:
                    rec.msg_date = f"{state} {remaining_days} jours "
                elif months == 1 and remaining_days == 0:
                    rec.msg_date = f"{state} 1 mois "
                elif months == 1:
                    rec.msg_date = f"{state} 1 mois et {remaining_days} jours "
                elif remaining_days == 0:
                    rec.msg_date = f"{state} {months} mois "
                else:
                    rec.msg_date = f"{state} {months} mois et {remaining_days} jours "
            else:
                # Si la date de facturation n'est pas définie, réinitialiser les champs
                rec.msg_date = ""
                rec.nbr_date = None

            
    # # Définition d'une méthode "_compute_nbr_attached_file" dans un modèle Odoo
    # def action_register_payment(self):
    #         return {
    #             'name': _('Register Payment'),
    #             'res_model': 'account.payment.register',
    #             'view_mode': 'form',
    #             'context': {
    #                 'active_model': 'account.move',
    #                 'active_ids': self.ids,
    #             },
    #             'target': 'new',
    #             'type': 'ir.actions.act_window',
    #         }
    def write(self,vals):
        bill = super(account_move, self).write(vals)
        if 'payment_state' in self:
            print("the bille is")
            print(self.payment_state)
        else:
            print("not work")
        return bill
    def _compute_nbr_attached_file(self):
        
        # Parcours de chaque enregistrement (record) dans le modèle
        for record in self:
            # Recherche du nombre d'enregistrements dans le modèle "ir.attachment" liés à l'enregistrement actuel
            nbr_files = self.env["ir.attachment"].search_count([('res_id', '=', record.id)])
            
            # Mise à jour du champ "nbr_field_attached" avec le nombre de fichiers liés
            record.nbr_field_attached = nbr_files
    
    @api.depends('needed_terms')
    def _compute_invoice_date_due_new(self):
        today = fields.Date.context_today(self)        
        
        for move in self:
            
            date_echeance_move_id=self.env["account.payment.register"].search([("move_id","=",move.id)],order="id desc",limit=1)
            if date_echeance_move_id:
                 move.invoice_date_due=date_echeance_move_id.date_echeance
            else:
                move.invoice_date_due=today

            # print(move.invoice_date_due)
    # @api.depends('payment_state')
    # @api.onchange('payment_state')
    # def manage_payment_state(self):
    #     bills=self.env["account.move"].search([])
    #     for rec in bills:
    #         print("the paiment state of the bill"+str(self.id)+" "+str(self.name)+" is ")
    #         print(rec.payment_state)
    def write(self,vals):
        bill=super(account_move, self).write(vals)

        return bill
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
        # Cette fonction met à jour le champ 'is_active' pour indiquer si l'enregistrement est archivé ou non.
        # Si l'enregistrement est actif (non archivé), 'is_active' est défini sur "Archive".
        # Si l'enregistrement n'est pas actif, 'is_active' est défini sur "Désarchiver".

        for rec in self:
            rec.is_active = "Archiver" if rec.active == True else "Désarchiver"
        
    def create_activity_echeance(self):
        bills=self.env["account.move"].search([])
        model_id=self.env["ir.model"].search([("model","=","account.move")],limit=1)
        activity_id=self.env["mail.activity.type"].search([("name","=","To Do")],limit=1)
        for rec in bills:
            if rec.payment_state!="paid":
                target_date = datetime.strptime(str(rec.invoice_date_due), "%Y-%m-%d")  # Date de début
                current_date = datetime.now()  # Date actuelle
                delta=target_date-current_date

                # self
                if delta.days<=rec.nbr_days_before_alert:
                    is_activity_created=self.env["mail.activity"].search([("activity_type_id","=",activity_id.id),("res_model_id","=",model_id.id),("res_id","=",rec.id),("summary","=","Cette facture doit être payée")])
                    if not is_activity_created:
                        self.env["mail.activity"].create({
                            "res_model_id":model_id.id,
                            "res_id":rec.id,
                            "user_id":self.env.uid,
                            "summary":"Cette facture doit être payée",
                            "date_deadline":rec.invoice_date_due,
                            "activity_type_id":activity_id.id
                        })
    # @api.depends('posted_before', 'state', 'journal_id', 'date', 'move_type', 'payment_id')
    # def _compute_name(self):
    #     self = self.sorted(lambda m: (m.date, m.ref or '', m.id))

    #     for move in self:
    #         move_has_name = move.name and move.name != '/'
    #         if move_has_name or move.state != 'posted':
    #             if not move.posted_before and not move._sequence_matches_date():
    #                 if move._get_last_sequence():
    #                     # The name does not match the date and the move is not the first in the period:
    #                     # Reset to draft
    #                     move.name = False
    #                     continue
    #             else:
    #                 if move_has_name and move.posted_before or not move_has_name and move._get_last_sequence():
    #                     # The move either
    #                     # - has a name and was posted before, or
    #                     # - doesn't have a name, but is not the first in the period
    #                     # so we don't recompute the name
    #                     continue
    #         if move.date and (not move_has_name or not move._sequence_matches_date()):
    #             move._set_next_sequence()

    #     self.filtered(lambda m: not m.name and not move.quick_edit_mode).name = '/'
    #     self._inverse_name()