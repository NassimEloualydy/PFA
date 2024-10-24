/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { GroupByMenu } from "@web/search/group_by_menu/group_by_menu";
import { useAutofocus, useBus, useService } from "@web/core/utils/hooks";

patch(GroupByMenu.prototype, "projet_riad.group_by_menu", {

    setup() {
        this._super();
        this.orm = useService("orm");
    },
   async onGroupBySelected({ itemId, optionId }) {

        if (this.env.searchModel.resModel == "project.task"){
            const data_group_by = this.env.searchModel.getSearchItems();
            var group_id=null
            
            for(var i=0;i<data_group_by.length;i++)
            {
if(data_group_by[i].description=="Assignée / Suivies ")                {
    group_id=data_group_by[i].id
    break
}

            }
            if(group_id==itemId){
               var project_id=null;
               this.env.searchModel._domain.forEach(item => {

                if (Array.isArray(item)) {
                    if (item[0] == "project_id")
                        project_id = item[2]
                }
            })

               await this.orm.call("project.task", "retrieve_data_test", ["", project_id]);
  
            }
        }
        if (optionId) {
            console.log("the option id is ")
            console.log(optionId)
            this.env.searchModel.toggleDateGroupBy(itemId, optionId);
            console.log("after the group id ")
            this.env.searchModel.getSearchItems((searchItem) =>        
            console.log(searchItem.options)
            );
        } else {
            this.env.searchModel.toggleSearchItem(itemId);
        }
        if (this.env.searchModel.resModel == "project.task"){

            
            this.waitForTitle();
        }

    },
    waitForTitle() {
        const element = document.querySelector('span.id');
        let titleElement = element.querySelector('i');

        let title = titleElement ? titleElement.getAttribute('title') : null;
        if (title) {
            setTimeout(() => this.waitForTitle(), 1000); // Pass a reference to the function
        } else {
            // Title disappeared, do something or exit loop
            this.getFollowers();
        }
    },
    getFollowers() {

        const divsWithIdClass = document.querySelectorAll('span.id');

        divsWithIdClass.forEach(div => {
            const idValue = div.querySelector('span').textContent.replace(/\s/g, '');
            this.getDataAjax(parseInt(idValue), div)
        });
    },

    getDataAjax(leadId, div) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/owl/followers/' + leadId, true);
        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                var responseData = JSON.parse(xhr.responseText);
                div.querySelector('i').setAttribute('title', responseData.followers);

            } else {
                console.error('Request failed with status', xhr.status);
            }
        };
        xhr.send();
    },


});