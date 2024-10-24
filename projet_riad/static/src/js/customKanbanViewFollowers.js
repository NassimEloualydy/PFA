/** @odoo-module */
import { registry } from "@web/core/registry"
import { kanbanView } from "@web/views/kanban/kanban_view"
import { KanbanController } from "@web/views/kanban/kanban_controller"
import { useService } from "@web/core/utils/hooks"

class customKanbanFollowers extends KanbanController {

    setup(){

        super.setup();
        


        setTimeout(() => {

            this.waitForElement();

        }, 1000);

    }




    waitForElement(){

        const element = document.querySelector('span.id');


        if (element) {

            // Element found, do something

            this.getFollowers();

            this.onFillterSelected();

            // Add your code here

        } else {

            // Element not found yet, wait and try again

            setTimeout(() => this.waitForElement(), 1000); // Fix here

        }

    }




    onFillterSelected() {

        var searchInput = document.querySelector('.o_searchview_inputgg');
        console.log(searchInput)

        if (searchInput!=null) {

            searchInput.addEventListener('keydown', (event) => {

                if (event.key === 'Enter' || event.key === 'Backspace') {

                    setTimeout(() => {

                        this.getFollowers(); // Use arrow function to maintain 'this'

                    }, 1000);

                }

            });

            searchInput.addEventListener('input', (event) => {

                setTimeout(() => {

                    var menuFilter = document.querySelectorAll('.o_menu_item.dropdown-item');

                    menuFilter.forEach((menuFilter) => {
                        menuFilter.addEventListener('click', () => {
                            setTimeout(() => {
                                this.getFollowers(); // Use arrow function to maintain 'this'
                            }, 1000);
                        });

                    });

                }, 200);

            });

        }

        var fillterButton = document.querySelector('.o_dropdown_title');
        if(fillterButton!=null)
        fillterButton.addEventListener('click', (event) => {
            setTimeout(() => {
                var menuFilter = document.querySelectorAll('.dropdown-item');
                menuFilter.forEach((menuFilter) => {
                    menuFilter.addEventListener('click', () => {
                        setTimeout(() => {
                            this.getFollowers();
                        }, 1000);
                    });
                });
            }, 200);
        });
    }



    getFollowers(){




        const divsWithIdClass = document.querySelectorAll('span.id');
        if(divsWithIdClass!=null)
        divsWithIdClass.forEach(div => {

            const idValue = div.querySelector('span').textContent.replace(/\s/g, '');

            this.getDataAjax(parseInt(idValue),div)




        });

    }




    getDataAjax(leadId,div) {




        var xhr = new XMLHttpRequest();




        xhr.open('GET', '/owl/followers/' + leadId, true);




        xhr.onload = function() {

            if (xhr.status >= 200 && xhr.status < 300) {




                var responseData = JSON.parse(xhr.responseText);

                div.querySelector('i').setAttribute('title',responseData.followers);




            } else {

                console.error('Request failed with status', xhr.status);

            }

        };




        xhr.send();

    }















}

















export const customKanbanView = {

    ...kanbanView ,

    Controller : customKanbanFollowers,

}




registry.category("views").add("custom_kanban_view_followers", customKanbanView);