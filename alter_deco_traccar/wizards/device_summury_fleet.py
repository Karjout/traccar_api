# -*- coding: utf-8 -*-
import logging
from dateutil import parser
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timezone
_logger = logging.getLogger(__name__)

class Device_summury_fleet(models.TransientModel):
    _name = 'device_summury_fleet'
    _description = _('Device_summury_fleet')
    device_id  = fields.Char(string="Device ID", readonly=True)
    device_name = fields.Char(string="Device Name", readonly=True)
    distance = fields.Char(string="Distance(km)", readonly=True)
    distance = fields.Char(string="Distance(km)", readonly=True)
    engine_hours = fields.Char(string="Engine Hours", readonly=True)
    fuel_consumption = fields.Char(string="Fuel Consumption", readonly=True)
    max_speed = fields.Char(string="Max Speed(km/h)",readonly=True)
    vehicule_id = fields.Many2one('fleet.vehicle', string="Vehicle", readonly=True)
    start_odometer = fields.Char(string="Start Odometer", readonly=True)
    end_odometer = fields.Char(string="End Odometer", readonly=True)
    from_date = fields.Datetime(string="From Date", required=True,default=fields.Datetime.now())
    to_date = fields.Datetime(string="To Date", required=True,default=fields.Datetime.now())
    spent_fuel = fields.Char(string="Spent Fuel", readonly=True)
    average_speed = fields.Char(string="Average Speed", readonly=True)
    message = fields.Char(string="Message", readonly=True)
    visible = fields.Boolean(string="Visible", default=False)
    def get_traccar_event(self):
        from_date_iso = self.from_date.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        to_date_iso = self.to_date.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        events = self.vehicule_id.traccar_api_call(method="GET", endpoint=f"/api/reports/events?deviceId={self.device_id}&from={from_date_iso}&to={to_date_iso}")
        
        if events:
            _logger.info("Traccar events received: %s", events)
            self.vehicule_id.event_ids.unlink()
            # Créer les lignes de résultat
            for e in events:
                _logger.info('Vehicule Name %s',self.vehicule_id.name)
                self.vehicule_id.event_ids.create({
                    'event_id': e.get('id'),
                    'device_id':self.vehicule_id.id,
                    'device_name': self.vehicule_id.device_name if self.vehicule_id.device_name else 'Unknown',
                    'event_type': e.get('type'),
                    'fix_time': parser.isoparse(e.get('eventTime')).astimezone(timezone.utc).replace(tzinfo=None),
                    'event_data': str(e.get('attributes', {})),
                    'event_geofence': e.get('geofenceId'),
                    'maintenance': e.get('maintenanceId'),
                })
            return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Events fetched successfully',
                        'message': f"Events fetched successfully.",
                        'type': 'success',
                        'sticky': False,
                    }
                }

    def get_device_summary(self):
        """
        Get device summary data from Traccar API.
        :return: dict or None
        """
        from_date_iso = self.from_date.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        to_date_iso = self.to_date.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        device_summary = self.vehicule_id.traccar_api_call(method="GET", endpoint=f"/api/reports/summary?deviceId={self.device_id}&daily=true", params={"from": from_date_iso, "to": to_date_iso})
        if device_summary and len(device_summary) > 0:
            get_device_summary = device_summary[0]
            _logger.info("Traccar device summary received: %s", get_device_summary)
            self.write({
                'visible': True,
                'device_name': get_device_summary.get('deviceName'),
                'average_speed': get_device_summary.get('averageSpeed'),
                'distance': get_device_summary.get('distance')/1000,#to convert to km
                'engine_hours': get_device_summary.get('engineHours'),
                'fuel_consumption': get_device_summary.get('fuelConsumption'),
                'max_speed': get_device_summary.get('maxSpeed'),
                'spent_fuel': get_device_summary.get('spentFuel'),
                'start_odometer': get_device_summary.get('startOdometer')/1000,#to convert to km
                'end_odometer': get_device_summary.get('endOdometer')/1000,#to convert to km
        })
        else:
            self.write({
                'visible': False,
                'message': "No data found for the selected date.",
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': self.env.context,
    }
        
