# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
import requests
import json
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class TraccarCar(models.Model):
    _inherit = 'fleet.vehicle'
    is_trackable = fields.Boolean(string="Traccar ?", default=False)
    traccar_id = fields.Char(string="Traccar ID", required=False)
    is_online = fields.Char(string="Est-il en ligne ?", required=False)
    device_id = fields.Char(string="Device ID", required=False)
    device_name = fields.Char(string="Device Name", required=False)
    traccar_category = fields.Char(string="Device Category", required=False)
    device_long = fields.Char(string="Longitude", readonly=True)
    device_lat = fields.Char(string="Latitude", readonly=True)
    last_trip_update = fields.Datetime(string="Last Trip Update", readonly=True)
    last_route_update = fields.Datetime(string="Last Route Update", readonly=True)
    event_ids = fields.One2many('traccar_log_events', 'device_id', string="Events")
    totalDistance = fields.Char(string="Total Distance(Km)", readonly=True)

    def fetch_stops_reports(self):
        return True
    def get_events(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'device_summury_fleet',
            'name': 'Events',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                    'default_is_event_invisible':0,
                    'default_device_id': self.device_id,
                    'default_vehicule_id': self.id},
        }
    def validate_device(self):
        return True
    def open_device_summary(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'device_summury_fleet',
            'name': 'Device Summary',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_is_event_invisible':1,
                'default_device_id': self.device_id,
                'default_vehicule_id': self.id},
        }
    def fetch_trip_reports(self):
        return True
    def fetch_route_reports(self):
        return True
    def view_device_map(self):
        return True
    def get_server_info(self):
        server_info = self.env['traccar.traccar'].search([('active', '=', True)], limit=1)
        if not server_info:
            raise UserError(_("Aucun serveur Traccar actif trouvé"))
        return server_info
    
    def traccar_api_call(self, method="GET", endpoint="", params=None, payload=None):
        """
        Fonction générique pour appeler l'API Traccar dynamiquement avec cookie de session.
        """
        try:
            server_info = self.get_server_info()
            base_url = server_info.traccar_session_url.rstrip('/')
            full_url = f"{base_url}{endpoint}"

            headers = {'Accept': 'application/json'}

            # 🔹 Vérifie et prépare le cookie
            cookie_value = server_info.web_socket_cookie
            if not cookie_value:
                raise UserError(_("Aucun cookie de session (JSESSIONID) trouvé dans la configuration."))

            # Si c’est une chaîne (ex: "JSESSIONID=node01abcd1234xyz.node0"), on la convertit en dict
            if isinstance(cookie_value, str):
                if "=" in cookie_value:
                    parts = cookie_value.split("=")
                    jsessionid_cookie = {parts[0]: parts[1]}
                else:
                    raise UserError(_("Format de cookie Traccar invalide."))
            elif isinstance(cookie_value, dict):
                jsessionid_cookie = cookie_value
            else:
                raise UserError(_("Type de cookie Traccar invalide (doit être str ou dict)."))

            _logger.info(f"Traccar API Request → {method} {full_url}")
            _logger.info(f"Params: {params} | Payload: {payload} | Cookies: {jsessionid_cookie}")

            response = requests.request(
                method=method.upper(),
                url=full_url,
                headers=headers,
                params=params or {},
                json=payload or {},
                cookies=jsessionid_cookie,
                timeout=30
            )

            _logger.info(f"Traccar Response [{response.status_code}]: {response.text}")

            if response.status_code in [200, 201]:
                return response.json()
            else:
                raise UserError(_(f"Erreur Traccar ({response.status_code}): {response.text}"))

        except Exception as e:
            _logger.error(f"Erreur API Traccar: {e}")
            raise UserError(_("Erreur lors de l'appel à Traccar : %s") % e)

    def device_status(self):
        """Vérifie le statut du device sur Traccar"""
        self.ensure_one()
        endpoint = f"/api/devices"
        params = {"uniqueId": self.traccar_id}

        data = self.traccar_api_call(method="GET", endpoint=endpoint, params=params)

        if data and len(data) > 0:
            device_info = data[0]
            _logger.info(f"Device info: {device_info}")
            self.write({
                'is_online': device_info.get("status"),
                'device_id': device_info.get("id"),
                'device_name': device_info.get("name"),
                'traccar_category': device_info.get("category") if device_info.get("category") else "Default",
            })
            if device_info.get("positionId") and device_info.get("positionId") != "":
                get_position = self.traccar_api_call(method="GET", endpoint=f"/api/positions?id={device_info.get('positionId')}")
                if get_position and len(get_position) > 0:
                    position_info = get_position[0]
                    _logger.info(f"Position info: {position_info}")
                    self.write({
                    'device_long': position_info.get("longitude"),
                    'device_lat': position_info.get("latitude"),
                    'totalDistance': int(position_info.get('attributes', {}).get('totalDistance', 0.0)) /1000 #to convet to KM
                })
            return True
        else:
            self.write({
                'is_online': False,
                'device_id': False,
                'device_name': False,
                'traccar_category': False,
                'device_long': False,
                'device_lat': False,
                })
            return True

