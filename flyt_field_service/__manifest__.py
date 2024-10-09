# -*- coding: utf-8 -*-

##############################################################################
#
#    Flyt Consulting AS
#    Copyright (C) 2019-Today Flyt Consulting AS.(<https://www.flytconsulting.no>).
#    Author: Flyt Consulting AS. (<https://www.flytconsulting.no>) 
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Salespersons to sell field-service type tasks',
    'summary': 'salespersons to sell field-service type tasks',
    'version': '17.0.0.0.8',
    'category': 'Tools',
    'license': 'OPL-1',
    "author":"Flyt Consulting AS",
    'maintainer': 'Flyt Consulting AS',
    'website': 'https://www.flytconsulting.no',    
    'depends': ['sale_management','industry_fsm','project','sale_service'],
    'data': [
        'security/groups_security.xml',
        'data/demo_data.xml',
        'views/res_settings.xml',
        'views/sale_order.xml',
        'views/project_task_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'flyt_field_service/static/src/**/*',
            'flyt_field_service/static/src/css/*',
        ],
    },
}
