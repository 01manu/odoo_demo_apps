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
            return http.request.render('web_portal.portal_my_home_login_main',
                                       {'error': 'Invalid username or password'})


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

    @http.route(['/my/collages/servers/web/<model("res.partner"):partner_id>'], type='http', website=True,
                auth='user')
    def webpagecollageservers(self, partner_id, **kw):
        vals = {'image_ids': partner_id.class_lines, 'page_name': 'collage_image_web_view_portal'}
        print(vals, "@@@@@@@@@@@@@@@@@@")
        return request.render("web_portal.image_web", vals)

    @http.route('/my/collages/booking', type='http', website=True)
    def exam_booking_form(self, **kwargs):
        colleges = request.env['res.partner'].sudo().search([])
        exams = request.env['exam.name'].sudo().search([])
        # selected_college_id = int(kwargs.get('colleges', False))  # Get the selected college ID from the request parameters
        remaining_slots = []
        selected_college_id = int(kwargs.get('colleges', False))
        # if selected_college_id:
        remaining_slots = request.env['create.classroom'].sudo().search([('create_id', '=', selected_college_id)])
        print(remaining_slots, "$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(selected_college_id, '######################')
        return request.render('web_portal.collage_form_view_portal', {
            'colleges': colleges,
            'exams': exams,
            'selected_college_id': selected_college_id,
            'remaining_slots': remaining_slots,
        })

    @http.route('/exam/booking/submit', type='http', auth='public', website=True, methods=['POST'])
    def submit_booking(self, **kwargs):
        center_id = int(kwargs.get('center_id', 0))
        name_of_exam = int(kwargs.get('name_of_exam'))
        booked_slots = kwargs.get('booked_slots')
        avaliable_slots = kwargs.get('avaliable_slots')
        remaining_slot_ids = request.httprequest.form.getlist('remaining_slots')  # Get the selected remaining slots
        remaining_slots = request.env['create.classroom'].sudo().browse(map(int, remaining_slot_ids))

        if avaliable_slots and avaliable_slots.isdigit():
            avaliable_slots = int(avaliable_slots)
        else:
            # Handle the case where slots is not provided or is not a valid number
            # You can set a default value or raise an error based on your requirements
            avaliable_slots = 0  # Default value

        # Create a new booking record in the backend
        booking = request.env['exam.center.booking'].sudo().create({
            'center_id': center_id,
            'name_of_exam': name_of_exam,
            'avaliable_slots': avaliable_slots,
            'booked_slots': booked_slots,
            'remaining_slots': [(6, 0, remaining_slots.ids)],  #

            # Add any other required fields for the booking
        })

        # Redirect the user to a success page or display a success message
        return http.request.render('web_portal.employee_thanks')

    @http.route('/collage/list', type="http", website=True, auth='user')
    def collage_ist(self, **kw):
        patient_name = request.env['res.partner'].sudo().search([])
        for rec in patient_name:
            print(rec.total_slots,"##################################")
        return request.render("web_portal.collage_list_form_view_portal", {
            'collage_list': patient_name
        })

    @http.route('/collage/list/form/details/<model("res.partner"):partner_id>', type="http", website=True, auth='user')
    def collage_list_form(self,partner_id, **kw):
        # patient_name = request.env['res.partner'].sudo().search([])
        return request.render("web_portal.collage_details_form_view_portal", {
            'collage_list': partner_id
        })
