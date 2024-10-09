/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { CalendarCommonRenderer } from "@web/views/calendar/calendar_common/calendar_common_renderer";
import { patch } from "@web/core/utils/patch";

patch(CalendarCommonRenderer.prototype, {
    setup() {
        super.setup();
        this.rpc = useService("rpc");
        this.exceededDates = [];
    },

    async onDayRender(info) {
        super.onDayRender(info);
        if (this.props.model.meta.resModel === 'project.task' && this.props.model.meta.context.call_from_sale_order_view) {
            const date = luxon.DateTime.fromJSDate(info.date).toISODate();
            await this.rpc('/project/task/indicator', {'date':date,'company_ids': this.props.model.meta.context.allowed_company_ids}).then((response) => {
                if (response.exceeded_dates) {
                    info.el.classList.add("task_limit_indicator");
                }
            }).catch((error) => {
                console.error('Error fetching task limit indicator:', error);
            });
        }
    },
})