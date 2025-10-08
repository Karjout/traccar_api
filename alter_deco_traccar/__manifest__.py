# -*- coding: utf-8 -*-
{
    'name': "alter_deco_traccar",

    'summary': "Module pour la gestion des paramètres Traccar",

    'description': """
    Module pour la gestion des paramètres Traccar
    """,

    'author': "Karjout Abdeslam",
    'website': "https://www.obystech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '18.01',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web','fleet','web_map','widget_geolocation_map'],

    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/inherit_fleet_car.xml",
        "views/menus.xml",
        "views/traccar_traccar_views.xml",
        "wizards/device_summury_fleet.xml"
    ],
     'assets': {
        'web.assets_backend': [
            'alter_deco_traccar/static/lib/json-viewer-master/src/json-viewer.css',
            'alter_deco_traccar/static/lib/json-viewer-master/src/json-viewer.js',
            'alter_deco_traccar/static/src/json/json.scss',
            'alter_deco_traccar/static/src/json/json.xml',
            'alter_deco_traccar/static/src/json/json.js',
        ],
    },
}

