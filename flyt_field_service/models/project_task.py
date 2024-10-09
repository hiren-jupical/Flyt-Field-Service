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

from odoo import api, fields, models, _
from datetime import timedelta
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):

    _inherit = 'project.task'

    is_so_task = fields.Boolean("IS sale order task",copy=False)
    field_service_status = fields.Selection([('reserve','Reserve'),('confirm','Confirm')], string="Field Service Status")
    so_ids = fields.Many2many('sale.order', string="Sale Order",copy=False)
    
    @api.model_create_multi
    def create(self, vals_list):  
        res_ids = super(ProjectTask, self).create(vals_list)

        if not self.env.context.get('from_fields_service'):
            for task in res_ids:
                if task.is_so_task and task.company_id and task.so_ids:
                    service_status = 'reserve'

                    if all(sale.state == 'sale' for sale in task.so_ids):
                        service_status = 'confirm'

                    task.write({'field_service_status': service_status})
                    product_id = task.company_id.montering_product_id
                    print("task.so_ids=====",task.so_ids)
                    if product_id:
                        task.so_ids.write({'monitor_task_id':task.id})
                        for order in task.so_ids:

                            order_line = self.env['sale.order.line'].with_context(from_fields_service=True).create({
                                'product_id':product_id.id,
                                'order_id':order.id,
                                'name':product_id.display_name,
                                'product_uom_qty':1,
                                'price_unit':product_id.list_price,
                                })
        
        return res_ids

    def date_range(self, start_date, end_date):
        for n in range((end_date - start_date).days + 1):
            yield start_date + timedelta(n)

    @api.constrains('planned_date_begin', 'date_deadline')
    def _check_limit_per_user(self):
        if self.env.user.has_group('flyt_field_service.sales_user_field_service'):
            for task in self:
                if task.is_fsm:
                    fsm_user_group = self.env.ref('industry_fsm.group_fsm_user')
                    fsm_fsm_group = self.env.ref('industry_fsm.group_fsm_manager')
                    user_count = self.env['res.users'].search_count([
                        ('groups_id', 'in', [fsm_user_group.id, fsm_fsm_group.id])
                    ])
                    task_start_date = task.planned_date_begin.date()
                    task_end_date = task.date_deadline.date() if task.date_deadline else task_start_date

                    for current_date in self.date_range(task_start_date, task_end_date):
                        task_count = self.search_count([
                            ('is_fsm', '=', True),
                            ('planned_date_begin', '<=', current_date),
                            ('date_deadline', '>=', current_date)
                        ])
                        if user_count and task_count:
                            if task_count > user_count:
                                raise ValidationError(
                                    _("You cannot create more tasks than the number of users (%s) on this date." % user_count)
                                )

