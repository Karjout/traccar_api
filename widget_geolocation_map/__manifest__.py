# -*- coding: utf-8 -*-
{
    'name': 'alter_deco_maps',
    'version': '1.0.0',
    'summary': """ Widget Geolocation Map Summary """,
    'author': 'Abdeslam Karjout',
    'website': 'obystech.com',
    'category': 'Tools',
    'depends': ['base', 'web'],
    "data": [
        "views/res_partner_views.xml"
    ],
    'assets': {
        'web.assets_backend': [
            'widget_geolocation_map/static/src/**/*'
        ],
    },
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
