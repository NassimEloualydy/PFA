from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

class purchase_order_wizard(models.TransientModel):
    _name="purchase.order.wizard"

 # Champ 'supplier_ids' de type Many2many (relation avec 'res.partner')
    supplier_ids = fields.Many2many(
        'res.partner',  # Modèle cible de la relation
        string='Suppliers',  # Étiquette du champ à afficher
        required=True,  # Champ requis (non vide)
    )

    # Champ 'product_line_ids' de type One2many (relation avec 'purchase.order.wizard.line')
    product_line_ids = fields.One2many(
        'purchase.order.wizard.line',  # Modèle cible de la relation
        'wizard_id',  # Champ inverse (liant les lignes à cet enregistrement)
        'Lignes'  # Étiquette du champ à afficher
    )

class PurchaseOrderWizardLine(models.TransientModel):
    _name = 'purchase.order.wizard.line'
    
 # Champ 'product_id' de type Many2one (relation avec 'product.product')
    product_id = fields.Many2one(
        'product.product',  # Modèle cible de la relation
        string='Article'  # Étiquette du champ à afficher
    )

    # Champ 'quantity' de type Integer (entier)
    quantity = fields.Integer(
        'Quantité'  # Étiquette du champ à afficher
    )

    # Champ 'product_uom' de type Many2one (relation avec 'uom.uom')
    product_uom = fields.Many2one(
        'uom.uom',  # Modèle cible de la relation
        'Unité de mesure'  # Étiquette du champ à afficher
    )

    # Champ 'qty_available' de type Float (nombre à virgule flottante)
    qty_available = fields.Float(
        'Quantité en stock'  # Étiquette du champ à afficher
    )

    # Champ 'wizard_id' de type Many2one (relation avec 'purchase.order.wizard')
    wizard_id = fields.Many2one(
        'purchase.order.wizard',  # Modèle cible de la relation
        'Purchase Order wizard'  # Étiquette du champ à afficher
    )


