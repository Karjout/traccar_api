# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)

class Traccar_log_events(models.Model):
    _name = 'traccar_log_events'
    _description = 'Traccar_log_events'
    event_id = fields.Char('Event ID')
    device_name = fields.Char('Device Name')
    fix_time = fields.Datetime('Fix Time')
    event_type = fields.Char('Event Type')
    event_data = fields.Char('Event Data')
    event_geofence = fields.Char('Event Geofence')
    maintenance = fields.Char('Maintenance')    
    device_id = fields.Many2one('fleet.vehicle', string="Device")
