/** @odoo-module */
console.log("hghghghghgh")

import { patch } from "@web/core/utils/patch";
import { DocumentsSearchPanel } from "@documents/views/search/documents_search_panel";
import { Component, useExternalListener, useRef, useState } from "@odoo/owl";

export class DocumentsSearchPanelItemSettingsPopover extends Component {}
DocumentsSearchPanelItemSettingsPopover.template = "documents.DocumentsSearchPanelItemSettingsPopover";

patch(DocumentsSearchPanel.prototype,"projet_riad.sendQuery", {
    // setup() {
    //     super.setup(...arguments);
    //     console.log("Hellow wordk from documentunt")
    // }
    // onSectionValueTouchStart(ev, section, value, group) {
    //     console.log("works on the selected")
    //     if (!device.isMobile || !this.supportedEditionFields.includes(section.fieldName)) {
    //         return;
    //     }
    //     this.touchStartMs = Date.now();
    //     if (!this.longTouchTimer) {
    //         this.longTouchTimer = browser.setTimeout(() => {
    //             this.openEditPopover(ev, section, value, group);
    //             this.resetLongTouchTimer();
    //         }, LONG_TOUCH_THRESHOLD);
    //     }
    // }

    async openEditPopover(ev, section, value, group) {
        const [resModel, resId] = this.getResModelResIdFromValueGroup(section, value, group);
        const target = ev.currentTarget || ev.target;
        const label = target.closest(".o_search_panel_label");
        const counter = label && label.querySelector(".o_search_panel_counter");
        
        if (this.popoverClose) {
            this.popoverClose();
        }
        this.popoverClose = this.popover.add(ev.target, DocumentsSearchPanelItemSettingsPopover, {
            onEdit: () => {
                this.popoverClose();
                this.state.showMobileSearch = false;
                this.editSectionValue(resModel, resId);                 
            },
            onCreateChild: () => {
                this.popoverClose();
                this.addNewSectionValue(section, value || group);
            },
            onDelete: () => {
                this.popoverClose();
                this.state.showMobileSearch = false;
                this.removeSectionValue(section, resModel, resId);
                
            },
            onArchive: () => {
                this.popoverClose();
                this.state.showMobileSearch = false;
                console.log(resModel)
                console.log(section)
                console.log(resId)
                this.archiveSectionValue(section, resModel, resId);                

            },
            createChildEnabled: this.supportedNewChildModels.includes(resModel),
            isArchive: await this.isArchive(section, resModel, resId)

        }, {
            onClose: () => {
                target.classList.remove("d-block");
                if (counter) {
                    counter.classList.remove("d-none");
                }
            },
            popoverClass: "o_search_panel_item_settings_popover",
        });
        target.classList.add("d-block");
        if (counter) {
            counter.classList.add("d-none");
        }
        
    },
    async isArchive(section, resModel, resId){
        return await this.orm.call("documents.folder","is_archive",[resId])
         
    }
    ,
    async archiveSectionValue(section, resModel, resId) {
        await this.orm.call("documents.folder","archive_folder",[resId])
        await this._reloadSearchModel(resModel === "documents.folder" && !section.enableCounters);
    },
    
    async _reloadSearchModel(reloadCategories) {
        console.log("Hellow word from create")
        const searchModel = this.env.searchModel;
        if (reloadCategories) {
            await searchModel._fetchSections(
                searchModel.getSections((s) => s.type === "category" && s.fieldName === "folder_id"),
                []
            );
        }
        await searchModel._notify();
    }



})