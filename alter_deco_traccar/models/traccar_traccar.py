# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
import requests
import json
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)

class TraccarTraccar(models.Model):
    _name = 'traccar.traccar'
    _description = 'TraccarTraccar'
    active = fields.Boolean(string="Actif", default=True)
    traccar_name = fields.Char(string="Nom du serveur", required=True)
    traccar_session_url = fields.Char(string="URL de session", required=True)
    traccar_description = fields.Json()
    traccar_login = fields.Char(string="Login Account", required=False)
    traccar_password = fields.Char(string="Password", required=False)
    google_map_api_key = fields.Char(string="Google Maps Clé API", required=False)
    active_live_tracking = fields.Boolean(string="Activer le suivi en temps réel", default=False)
    web_socket_url = fields.Char(string="URL WebSocket", required=False)
    web_socket_cookie = fields.Char(string="Cookie WebSocket", required=False)
    def test_connection(self):
        try:
            login_url = f"{self.traccar_session_url}/api/session"
            _logger.info(f"URL: {login_url}")
            payload = {
                "email": self.traccar_login,
                "password": self.traccar_password,
            }

            headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json",
                }

            # Start session to persist cookies
            session = requests.Session()
            response = session.post(login_url, data=payload, headers=headers)
            _logger.info(f"Response: {response.json()}")
            if response.status_code == 200:
                # Extract cookie
                cookies = session.cookies.get_dict()
                jsessionid = cookies.get('JSESSIONID')

                _logger.info(f"Traccar login OK — JSESSIONID: {jsessionid}")
                _logger.info(f"Response JSON: {response.json()}")

                # Save the cookie in your model
                self.write({
                    'web_socket_cookie': 'JSESSIONID=' + jsessionid,
                    'traccar_description': str(response.json()),
                })

                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': "Succès",
                        'message': "Connexion avec Traccar effectuée avec succès",
                        'sticky': False,
                        'type': 'success',
                    }
                }
            else:
                raise UserError(_(f"Échec de connexion: {response.status_code} — {response.text}"))

        except Exception as e:
            raise UserError(_("Erreur lors du test de connexion: %s") % e)

            
    @api.depends('traccar_name', 'traccar_session_url')
    def _compute_display_name(self):
        for model in self:
            new_name="{}".format(model.traccar_name)
            model.display_name = new_name
    
