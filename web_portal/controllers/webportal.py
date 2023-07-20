from odoo import http, api
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from werkzeug.utils import redirect
import datetime


class AdminController(http.Controller):
    @http.route('/admin', auth='public', type='http', website=True)
    def admin_page(self, **kwargs):
        # Your logic for the admin page goes here
        return http.request.render('web_portal.portal_my_home_login')

    @http.route('/login', auth='public', type='http', website=True, methods=['POST'])
    def login(self, **kwargs):
        # Handle the login logic here
        username = kwargs.get('username')
        password = kwargs.get('password')

        # Your authentication logic goes here
        if username == 'admin' and password == 'password':
            # Successful login, redirect to collage_list_view_portal
            return redirect('/my/collages#collage_list_view_portal')
        else:
            # Incorrect credentials, display an error message
            return http.request.render('web_portal.portal_my_home_login', {'error': 'Invalid username or password'})

    @http.route('/my/collages/booking', type='http', website=True)
    def webpageCollageBooking(self, **kw):
        return request.render("web_portal.collage_form_view_portal")

    @http.route('/my/collages/booking/submit', type='http', website=True)
    def webpageCollageBookingSubmit(self, **kw):
        vals= request.env['exam.center.booking'].create({
            'booked_slots': 1,
            'center_id' : 1,
        })
        return request.render("web_portal.employee_thanks", vals)


class WebsitePortal(CustomerPortal):
    # @api.model
    def _prepare_home_portal_values(self, counters):
        rtn = super(WebsitePortal, self)._prepare_home_portal_values(counters)
        rtn['collages_count'] = request.env['exam.center.booking'].search_count([])
        return rtn

    @http.route(['/my/collages', '/my/collages/page/<int:page>'], type='http', website=True)
    def webpageCollageList(self, page=1, **kw):
        collage_contact = request.env['exam.center.booking']
        total_collages = collage_contact.search_count([])
        page_details = pager(url='/my/collages',
                             total=total_collages,
                             page=page,
                             step=2)
        collage_list = collage_contact.search([], limit=5, offset=page_details['offset'])

        vals = {'collage_list': collage_list, 'page_name': 'collage_list_view_portal', 'pager': page_details}
        return request.render("web_portal.collage_list_view_portal", vals)

