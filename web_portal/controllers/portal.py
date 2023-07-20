from odoo import http, api
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from werkzeug.utils import redirect

class Home(http.Controller):
    @http.route('/hi', auth='public', type='http', website=True)
    def admin_page(self, **kwargs):
        # Your logic for the admin page goes here
        return http.request.render('web_portal.home1')