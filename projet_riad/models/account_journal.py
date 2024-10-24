from odoo import models,fields,api,_
import ast


class Account_Journal(models.Model):
    _inherit="account.journal"

    nb_facture_archive=fields.Integer(string="",compute="_compute_nbr_active_records",default=0)
    total_archive=fields.Float(default=0,compute="_get_total_archive")
    
    
    def open_action_active(self):
        view_id = self.env.ref('account.view_in_invoice_bill_tree').id
        view_id_form=self.env.ref('account.view_move_form').id
        view_id_kanban=self.env.ref('account.view_account_move_kanban').id
        return {
            'name': _('Factures Archivés'),  # Nom de la vue
            'type': 'ir.actions.act_window',
            'domain': [('active', '=', False)],
            'view_mode': 'tree',  # Mode de vue (formulaire)
            'res_model': 'account.move',  # Modèle associé à l'assistant
            'view_id': view_id,  # ID de la vue
            'views': [(view_id, 'tree'),(view_id_form, 'form'),(view_id_kanban,'kanban')],  # Spécification des vues (dans ce cas, une vue de formulaire)
            'context':{'order':'write_date desc'}
        }
        # action = self.env['ir.actions.act_window']._for_xml_id('')
        # action['display_name'] = _("%(name)s", name=self.name)
        # context = action['context'].replace('active_id', str(self.id))
        
        # context = ast.literal_eval(context)
        # context.update({
        #     'active':False
        #     })
        # action['context'] = context
        # return action

        """return action based on type for related journals"""
        # self.ensure_one()
        # action_name = self._select_action_to_open()
        

        # # Set 'account.' prefix if missing.
        # if not action_name.startswith("account."):
        #     action_name = 'account.%s' % action_name

        # action = self.env["ir.actions.act_window"]._for_xml_id(action_name)          
        # context = self._context.copy()
        # action['context'] = context
        # action['context'].update({
        #     'default_journal_id': self.id,
        #     'default_active': False,
        # })
        # return action
        # action=super(Account_Journal,self).open_action()
        # action['context'].update({
        #     'default_active': False,
        # })
        # return action

        #   name="Factures archivés"
        #   return{
        #     'name':name,    
        #      'domain': [('active', '=', False)], 
        #       'context': {             
        #        "default_active":False
                
        #     }, 
        #     'type':'ir.actions.act_window',
        #     'view_mode':'tree,form,kanban',
        #     'res_model':'account.move',
        #     'view_id' : False,
        # }
    def _compute_nbr_active_records(self):
        for record in self:
           
            nombre_record_archive = self.env["account.move"].search_count([('active', '=', False)])

            record.nb_facture_archive = nombre_record_archive 

    
    def _get_total_archive(self):
      for record in self:
        total = 0
        total_archive_records = self.env["account.move"].search([('active', '=', False)])
        
        # Sum the 'amount_total_signed' from the actual records
        total_archive_amount = sum(total_archive_records.mapped('amount_total_signed'))
        total_archive_amount += total

        print("Total Archive Amount:")
        print(total_archive_amount)

        record.total_archive = total_archive_amount

    def get_bar_graph_datas(self):
        res=super(Account_Journal,self).get_bar_graph_datas()
        query="""
            SELECT move.journal_id,
            COALESCE(SUM(move.amount_residual_signed) FILTER (WHERE EXTRACT(MONTH FROM invoice_date_due) = 1), 0) AS Janvier,
            COALESCE(SUM(move.amount_residual_signed) FILTER (WHERE EXTRACT(MONTH FROM invoice_date_due) = 2), 0) AS Février,
            COALESCE(SUM(move.amount_residual_signed) FILTER (WHERE EXTRACT(MONTH FROM invoice_date_due) = 3), 0) AS Mars,
            COALESCE(SUM(move.amount_residual_signed) FILTER (WHERE EXTRACT(MONTH FROM invoice_date_due) = 4), 0) AS Avril,
            COALESCE(SUM(move.amount_residual_signed) FILTER (WHERE EXTRACT(MONTH FROM invoice_date_due) = 5), 0) AS Mai,
            COALESCE(SUM(move.amount_residual_signed) FILTER (WHERE EXTRACT(MONTH FROM invoice_date_due) = 6), 0) AS Juin,
            COALESCE(SUM(move.amount_residual_signed) FILTER (WHERE EXTRACT(MONTH FROM invoice_date_due) = 7), 0) AS Juillet,
            COALESCE(SUM(move.amount_residual_signed) FILTER (WHERE EXTRACT(MONTH FROM invoice_date_due) = 8), 0) AS Août,
            COALESCE(SUM(move.amount_residual_signed) FILTER (WHERE EXTRACT(MONTH FROM invoice_date_due) = 9), 0) AS Septembre,
            COALESCE(SUM(move.amount_residual_signed) FILTER (WHERE EXTRACT(MONTH FROM invoice_date_due) = 10), 0) AS Octobre,
            COALESCE(SUM(move.amount_residual_signed) FILTER (WHERE EXTRACT(MONTH FROM invoice_date_due) = 11), 0) AS Novembre,
            COALESCE(SUM(move.amount_residual_signed) FILTER (WHERE EXTRACT(MONTH FROM invoice_date_due) = 12), 0) AS Décembre
            FROM account_move move
            WHERE move.journal_id = %(journal_ids)s
               AND move.state = 'posted'
               AND move.payment_state in ('not_paid', 'partial','in_payment')
               AND move.move_type IN %(invoice_types)s
                         GROUP BY move.journal_id
            """
        self.env.cr.execute(query,{
            'invoice_types': tuple(self.env['account.move'].get_invoice_types(True)),
            'journal_ids': self.id,
        })
        query_results = {r['journal_id']: r for r in self.env.cr.dictfetchall()}

        if len(query_results)>0:
          for key in query_results:
            res[0]['values'][0]['label']="Janvier"
            res[0]['values'][0]['type']="o_sample_data"
            res[0]['values'][0]['value']=query_results[key]['janvier']

            res[0]['values'][1]['label']="Février"
            res[0]['values'][1]['type']="o_sample_data"
            res[0]['values'][1]['value']=query_results[key]['février']

            res[0]['values'][2]['label']="Mars"
            res[0]['values'][2]['type']="o_sample_data"
            res[0]['values'][2]['value']=query_results[key]['mars']


            res[0]['values'][3]['label']="Avril"
            res[0]['values'][3]['type']="o_sample_data"
            res[0]['values'][3]['value']=query_results[key]['avril']


            res[0]['values'][4]['label']="Mai"
            res[0]['values'][4]['type']="o_sample_data"
            res[0]['values'][4]['value']=query_results[key]['mai']


            res[0]['values'][5]['label']="Juin"
            res[0]['values'][5]['type']="o_sample_data"
            res[0]['values'][5]['value']=query_results[key]['juin']


            res[0]['values'].append({'label': 'Juillet', 'value': 102, 'type': 'o_sample_data','value':query_results[key]['juillet']})
            res[0]['values'].append({'label': 'Août', 'value': 92, 'type': 'o_sample_data','value':query_results[key]['août']})
            res[0]['values'].append({'label': 'Septembre', 'value': 82, 'type': 'o_sample_data','value':query_results[key]['septembre']})
            res[0]['values'].append({'label': 'Octobre', 'value': 52, 'type': 'o_sample_data','value':query_results[key]['octobre']})
            res[0]['values'].append({'label': 'Novembre', 'value': 42, 'type': 'o_sample_data','value':query_results[key]['novembre']})
            res[0]['values'].append({'label': 'Décembre', 'value': 32, 'type': 'o_sample_data','value':query_results[key]['décembre']})
        res[0]['key']="Montant résiduel"
        return res

   