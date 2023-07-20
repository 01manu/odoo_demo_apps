from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager

from odoo import http




class Primeminds(http.Controller):

    @http.route('/primeminds/patients/', type="http", website=True, auth='user')
    def prime_minds(self, **kw):
        patient_name = request.env['exam.center.booking'].sudo().search([])
        # brand_name = request.env['uom.uom'].sudo().search([])
        return request.render("web_portal.create_collage", {
            'patient_name': patient_name
        })
    # @http.route('/primeminds/employees/', type="http", website=True, auth='user')
    # def prime_minds_tree(self, **kw):
    #
    #     return request.render("a_module.create_employee", {
    #
    #     })

    @http.route("/create/collage/", type="http", website=True, auth='user')
    def create_web_thanks(self, **kw):
        request.env['exam.center.booking'].sudo().create(kw)
        return request.render("web_portal.employee_thanks", {})



