from odoo import http
from odoo.http import request
import json

class YourController(http.Controller):
    @http.route('/owl/followers/<int:lead_id>', auth='user', type='http')
    def followers(self, lead_id, **kw):

        lead = request.env['project.task'].browse(lead_id)
        if not lead:
            return request.not_found()

        followers = request.env['mail.followers'].search_read([('res_model', '=', 'project.task'), ('res_id', '=', lead_id)], ['id', 'res_id', 'partner_id'])

        follower_names = []
        for follower in followers:
            partner_id = follower.get('partner_id', False)
            if partner_id:
                partner = request.env['res.partner'].browse(partner_id[0])
                follower_names.append(partner.name)

        response_data = {
            "lead_id": lead_id,
            "followers": ', '.join(follower_names)
        }

        # Serialize the data to JSON
        response = json.dumps(response_data)

        # Return the JSON response with appropriate content type
        return request.make_response(response, headers=[('Content-Type', 'application/json')])