/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { CalendarCommonRenderer } from "@web/views/calendar/calendar_common/calendar_common_renderer";
import { renderToString } from "@web/core/utils/render";
import { is24HourFormat } from "@web/core/l10n/dates";
// import { getColor } from "colors";

const CSS_COLOR_REGEX = /^((#[A-F0-9]{3})|(#[A-F0-9]{6})|((hsl|rgb)a?\(\s*(?:(\s*\d{1,3}%?\s*),?){3}(\s*,[0-9.]{1,4})?\))|)$/i;
const colorMap = new Map();


const { DateTime } = luxon;


patch(CalendarCommonRenderer.prototype, "projet_riad.sendQuery", {
    setup() {
        this._super();
    },
    getColor(key) {
        if (!key) {
            return false;
        }
        if (colorMap.has(key)) {
            return colorMap.get(key);
        }
    
        // check if the key is a css color
        if (typeof key === "string" && key.match(CSS_COLOR_REGEX)) {
            colorMap.set(key, key);
        } else if (typeof key === "number") {
            colorMap.set(key, ((key - 1) % 55) + 1);
        } else {
            colorMap.set(key, (((colorMap.size + 1) * 5) % 24) + 1);
        }
    
        return colorMap.get(key);
    },
    getStartTime(record) {
        const timeFormat = is24HourFormat() ? "HH:mm" : "hh:mm a";
        return record.start.toFormat(timeFormat);
    }
,
    getEndTime(record) {
        const timeFormat = is24HourFormat() ? "HH:mm" : "hh:mm a";
        return record.end.toFormat(timeFormat);
    }
,
    onEventRender(info) {
        const { el, event } = info;
        el.dataset.eventId = event.id;
        el.classList.add("o_event");
        const record = this.props.model.records[event.id];
        const allDay = record.isAllDay || record.end.diff(record.start, "hours").hours >= 24;
        
        // var endate=(["week", "month"].includes(this.props.model.scale) && allDay) ||
        // record.isAllDay ||
        // (allDay && record.end.toMillis() !== record.end.startOf("day").toMillis())
        // ? record.end.plus({ days: 1 }).toISO()
        // : record.end.toISO()
        
        if (record) {
            // This is needed in order to give the possibility to change the event template.
            const { resModel } = this.env.searchModel

            // console.log(record)
            console.log(resModel)
            var end_date="NASSIM"
            if(resModel=="calendar.event")
            end_date=record.rawRecord.stop.toString().slice(0, 10)
            if(resModel=="project.task")
            end_date=record.rawRecord.date_fin_project.toString().slice(0, 10)
            console.log(end_date)
            const injectedContentStr = renderToString(this.constructor.eventTemplate, {
                ...record,
                startTime: this.getStartTime(record),
                endTime: this.getEndTime(record),
                end_date:end_date
            });
            const domParser = new DOMParser();
            const { children } = domParser.parseFromString(injectedContentStr, "text/html").body;
            el.querySelector(".fc-content").replaceWith(...children);

            const color = this.getColor(record.colorIndex);
            if (typeof color === "string") {
                el.style.backgroundColor = color;
            } else if (typeof color === "number") {
                el.classList.add(`o_calendar_color_${color}`);
            } else {
                el.classList.add("o_calendar_color_0");
            }

            if (record.isHatched) {
                el.classList.add("o_event_hatched");
            }
            if (record.isStriked) {
                el.classList.add("o_event_striked");
            }
            if (record.duration <= 0.25) {
                el.classList.add("o_event_oneliner");
            }
            if (DateTime.now() >= record.end) {
                el.classList.add("o_past_event");
            }

            if (!record.isAllDay && !record.isTimeHidden && record.isMonth) {
                el.classList.add("o_event_dot");
            } else if (record.isAllDay) {
                el.classList.add("o_event_allday");
            }

            if (!el.classList.contains("fc-bg")) {
                const bg = document.createElement("div");
                bg.classList.add("fc-bg");
                el.appendChild(bg);
            }
        }
    }
,
    // convertRecordToEvent(record) {
    //     const allDay = record.isAllDay || record.end.diff(record.start, "hours").hours >= 24;
    //     var endate=(["week", "month"].includes(this.props.model.scale) && allDay) ||
    //     record.isAllDay ||
    //     (allDay && record.end.toMillis() !== record.end.startOf("day").toMillis())
    //     ? record.end.plus({ days: 1 }).toISO()
    //     : record.end.toISO()

    //     return {
    //         id: record.id,
    //         title: record.title,
    //         start: record.start.toISO(),
    //         end_date:endate.toString().slice(0, 10),
    //         end:
    //             (["week", "month"].includes(this.props.model.scale) && allDay) ||
    //             record.isAllDay ||
    //             (allDay && record.end.toMillis() !== record.end.startOf("day").toMillis())
    //                 ? record.end.plus({ days: 1 }).toISO()
    //                 : record.end.toISO(),
    //         allDay: allDay,
    //     };
    // }

});