/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PivotGroupByMenu } from "@web/views/pivot/pivot_group_by_menu";

patch(PivotGroupByMenu.prototype, "projet_riad.sendQuery", {
    
    get items() {

        let items = super.items.filter((i) => !i.custom);
        if (items.length === 0) {
            items = this.fields;
        }

        // Add custom groupbys
        let groupNumber = 1 + Math.max(0, ...items.map(({ groupNumber: n }) => n));
        for (const [fieldName,customGroupBy] of this.props.customGroupBys.entries()) {
            items.push({ ...customGroupBy, name: fieldName, groupNumber: groupNumber++ });
        }
        
        items.array.forEach(item => {
            console.log(item);
        });


        
        return items.map((item) => ({
            ...item,
            id: item.id || item.name,
            fieldName: item.fieldName || item.name,
            description: item.description || item.string,
            isActive: false,
            options:
                item.options || ["date", "datetime"].includes(item.type)
                    ? getIntervalOptions()
                    : undefined,
        }));
    }

});
