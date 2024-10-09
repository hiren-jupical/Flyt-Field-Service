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
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    monitor_task_id = fields.Many2one('project.task',string="Moniter Task", copy=False)
    planned_date_begin = fields.Datetime(related='monitor_task_id.planned_date_begin') 
    planned_date_end = fields.Datetime(related='monitor_task_id.date_deadline') 

    def open_fields_task(self):
        actions = []
        sale_order_ids = self.mapped('id')
        partner_ids = self.mapped('partner_id')
        sale_order_names = ", ".join(self.mapped('name'))
    
        if len(partner_ids) != 1:
            raise ValidationError("Selected sale orders must belong to the same partner.")
        if all(x.monitor_task_id for x in self):
            
            action = {
                    'view_type': 'form',
                    'view_mode': 'form',
                    'view_id': self.env.ref('project_enterprise.project_task_view_form').id,
                    'res_model': 'project.task',
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'res_id': self[0].monitor_task_id.id,
                    'context' : {'call_from_sale_order_view' : True}
                }
            return action

        action = self.env.ref('industry_fsm.project_task_action_fsm_planning_groupby_user').read()[0]
        monitor_product = self[0].company_id.montering_product_id
        default_name = ''
        if monitor_product:
            default_name = str(self[0].partner_id.name)+ " - "+ str(monitor_product.name)+ " - "+ str(sale_order_names)
        
        action['context'] = {'default_name':default_name,
                            'default_is_so_task':True,
                            'default_so_ids':[(6, 0, sale_order_ids)],
                            'default_partner_id':self[0].partner_id.id,
                            'fsm_mode': 1, 
                            'task_nameget_with_hours': 1, 
                            'default_scale': 'week', 
                            'default_user_ids': False,
                            'call_from_sale_order_view' : True,
                            }
        action['views'] = [
                            (self.env.ref('industry_fsm.project_task_view_calendar_fsm').id, 'calendar'),
                            (self.env.ref('project_enterprise.project_task_view_gantt').id, 'gantt'),
                            (self.env.ref('industry_fsm.project_task_map_view_fsm').id, 'map'),
                            (self.env.ref('industry_fsm.project_task_view_list_fsm').id, 'tree'),
                            (self.env.ref('industry_fsm.project_task_view_pivot_group_by_users_fsm').id, 'pivot'),
                            (self.env.ref('project.view_project_task_graph').id, 'graph'),
                            (self.env.ref('industry_fsm.project_task_view_kanban_fsm').id, 'kanban'),
                          ]
        return action 
        
    def action_confirm(self):
        if self.monitor_task_id:
            self.monitor_task_id.write({'field_service_status':'confirm'})
        return super(SaleOrder, self).action_confirm()
