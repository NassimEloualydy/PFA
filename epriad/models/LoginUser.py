from odoo import models, fields, api


class MonCompte(models.Model):

    _name = 'riad.compte'
    
    login = fields.Char(string='Login', required=True)
    password = fields.Char(string='Password', required=True)

    def caesar_encrypt(self,plaintext):
        encrypted_text = ""
        for char in plaintext:
            if char.isalpha():
                encrypted_char = chr((ord(char) - ord('a') + 3) % 26 + ord('a'))
                encrypted_text += encrypted_char
            else:
                encrypted_text += char
        return encrypted_text


    @api.model
    def create(self, vals):
        
        if 'password' in vals:
            vals['password'] = self.caesar_encrypt(vals['password'])

        existing_record = self.search([], limit=1)
        if existing_record:
            existing_record.write({'login': vals.get('login'), 'password': vals.get('password')})
            return existing_record
        return super(MonCompte, self).create(vals)
