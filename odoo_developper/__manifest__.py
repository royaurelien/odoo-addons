# -*- coding: utf-8 -*-
{
    'name': 'Odoo Developper',
    'version': '15.0.1.0',
    "sequence":"0",
    'category': 'Technical',
    'description': """""",
    'author': 'Aurelien ROY',
    'depends': [
        'base', 
        'web',
    ],
    'data': [
        'views/ir_actions_report.xml',
        'wizard/open_report.xml',
        'wizard/analyze_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'odoo_developper/static/src/webclient/**/*',    
            'odoo_developper/static/src/webclient/user_menu/user_menu_items.js',
        ]
    },
    'application': False,
    'license': 'OPL-1',
}
