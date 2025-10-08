# -*- coding: utf-8 -*-
# from odoo import http


# class AlterDecoTraccar(http.Controller):
#     @http.route('/alter_deco_traccar/alter_deco_traccar', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/alter_deco_traccar/alter_deco_traccar/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('alter_deco_traccar.listing', {
#             'root': '/alter_deco_traccar/alter_deco_traccar',
#             'objects': http.request.env['alter_deco_traccar.alter_deco_traccar'].search([]),
#         })

#     @http.route('/alter_deco_traccar/alter_deco_traccar/objects/<model("alter_deco_traccar.alter_deco_traccar"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('alter_deco_traccar.object', {
#             'object': obj
#         })

