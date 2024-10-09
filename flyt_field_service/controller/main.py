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

from odoo import http, _
from odoo.http import request, content_disposition
from datetime import timedelta, datetime

class CalendarProjectTaskController(http.Controller):

    @http.route('/project/task/indicator', type='json', auth='user')
    def verify_task_user_limit(self, date, company_ids):
        if request.env.user.has_group('flyt_field_service.sales_user_field_service'):
            fsm_user_group = request.env.ref('industry_fsm.group_fsm_user')
            fsm_fsm_group = request.env.ref('industry_fsm.group_fsm_manager')

            user_count = request.env['res.users'].search_count([
                ('groups_id', 'in', [fsm_user_group.id, fsm_fsm_group.id])
            ])
            exceeded_dates = []
            task_count = request.env['project.task'].search_count([
                            ('is_fsm', '=', True),
                            ('planned_date_begin', '<=', date),
                            ('date_deadline', '>=', date),
                            ('company_id', 'in', company_ids),
                        ])
            if task_count >= user_count:
                return {
                    'exceeded_dates': True,
                }
        return {'exceeded_dates': False}

