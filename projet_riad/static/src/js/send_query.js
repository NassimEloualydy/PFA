/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { SearchBar } from "@web/search/search_bar/search_bar";

patch(SearchBar.prototype, "projet_riad.sendQuery", {
    setup() {
        this._super();
        // remove the checkbox
        var lev=false
        if(this.env.searchModel.resModel=="ir.attachment"){
            window.addEventListener('popstate', function(event) {
                // Your event handling code goes here
                console.log('URL changed!');
            });        }
        if(this.env.searchModel.resModel=="project.task"){
            console.log("the search mode is")
            console.log(this.env.searchModel)
            lev=true
            document.addEventListener('click', function abc(event) {
                // Your event handling code here
                var keyPressed = event.target;
                setTimeout(() => {
    
                    // thus function this.waitForElement();
                  function  waitForElement(){
    
                        const element = document.querySelector('span.id');
                        if(!element){
                            document.removeEventListener('click',abc)
                        }
                        if (element) {
                
                            // Element found, do something
                
                          //this function  this.getFollowers();
                          const divsWithIdClass = document.querySelectorAll('span.id');
    
                          divsWithIdClass.forEach(div => {
                  
                              const idValue = div.querySelector('span').textContent.replace(/\s/g, '');
                              function getDataAjax(leadId,div){
    
    
    
    
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
                              
                              getDataAjax(parseInt(idValue),div);
                              
                  
                  
                          });
                
                            // this.onFillterSelected();
                
                            // Add your code here
                
                        } else {
                
                            // Element not found yet, wait and try again
                
                            // setTimeout(() => waitForElement(), 1000); // Fix here
                            console.log("not found")
                        }
                
                    }
                
                    waitForElement()
                
                }, 1000);
        
                    
            });                

        }else if(lev==true){
            lev=false
            console.log("remove event")
            ;
    
        }
        
        if(this.env.searchModel.resModel=="ir.attachment"){
            var spans = document.querySelectorAll('span[class*="o_column_title"]');
            document.body.addEventListener('event', function(event) {
                // Your event handling code here
                console.log("the body is here")
            });                
            function repeatFunctionIrAttachment() {
                setTimeout(() => {
                    var spans = document.querySelectorAll('span[class*="o_column_title"]');
                    if (spans.length>0) {
                        spans.forEach(function(span) {
                            console.log(span.textContent);
                            
                            if(span.textContent.split('/').length==2){
                                span.textContent=span.textContent.split('/')[1]
                            }
                            console.log(span.textContent);
                            
                        });
                        
                    var iconWithTitle = document.querySelector('button.o_kanban_add_column.btn.btn-outline-secondary.w-100');
                    iconWithTitle.addEventListener('click', function() {
                        console.log("the button founded is ")
                        var addButton = document.querySelector('span.input-group-append');
                        function findButton(){
                            setTimeout(() => {
                        var addButton = document.querySelector('span.input-group-append');
                        document.addEventListener('keydown', function(event) {
                            var keyPressed = event.key;
                            if(keyPressed=="Escape"){
                                repeatFunctionIrAttachment();
                            }
                            // Trigger any action you want here based on the key pressed
                        });
                            if(addButton!=null){
                                var inptuFolder=document.querySelector('input.form-control.o_input.bg-transparent.fs-4[placeholder="Documents Folder..."]')
                                console.log("the input is")
                                console.log(inptuFolder)

                                inptuFolder.addEventListener('input',(e)=>{
                                            console.log("the value of input i ")
                                            // console.log(e.target.value)
                                            console.log(e)
                                            if(e.target.value!=""){
                                                var spans = document.querySelectorAll('span[class*="o_column_title"]');
                                                var inptuFolder=document.querySelector('input.form-control.o_input.bg-transparent.fs-4[placeholder="Documents Folder..."]')
                                                if(inptuFolder.value!=""){
                                                    var spansloaded=spans.length+1
                                                    function loadTheSpanAdded(){
                                                        setTimeout(()=>{
                                                            var spans = document.querySelectorAll('span[class*="o_column_title"]');
                                                            if(spans.length==spansloaded){
                                                                spans.forEach(function(span) {
                                                                    if(span.textContent.split('/').length==2){
            
                                                                        span.textContent=span.textContent.split('/')[1]
                                                                        console.log(span.textContent);
                                                                        findButton() 
                                                                    }
                                        
                                                                });
                                           
                                                            }else{
                                                                loadTheSpanAdded()
                                                            }
                                                        },7)
                                                    }
                                                    loadTheSpanAdded()
            
                                                }                                            
                                            }
                                })  
                                addButton.addEventListener('click',()=>{
                                    var spans = document.querySelectorAll('span[class*="o_column_title"]');
                                    var inptuFolder=document.querySelector('input.form-control.o_input.bg-transparent.fs-4[placeholder="Documents Folder..."]')
                                    if(inptuFolder.value!=""){
                                        var spansloaded=spans.length+1
                                        function loadTheSpanAdded(){
                                            setTimeout(()=>{
                                                var spans = document.querySelectorAll('span[class*="o_column_title"]');
                                                if(spans.length==spansloaded){
                                                    spans.forEach(function(span) {
                                                        if(span.textContent.split('/').length==2){

                                                            span.textContent=span.textContent.split('/')[1]
                                                            console.log(span.textContent);
                                                            findButton() 
                                                        }
                            
                                                    });
                               
                                                }else{
                                                    loadTheSpanAdded()
                                                }
                                            },7)
                                        }
                                        loadTheSpanAdded()

                                    }
                                })
                            }else{
                                findButton();
                            }
                            }, 7);
    
                        }
                        findButton();
                    });

                } else {
                        // Call the function recursively until the condition is met
                        repeatFunctionIrAttachment();
                    }
                }, 7);
            }
            repeatFunctionIrAttachment()


        }
        if (this.env.searchModel.resModel == "project.task") {
            var path="body > div.o_action_manager > div > div.o_control_panel > div.o_cp_top > div.o_cp_top_right > div > div > div > input"
            
            // var search_input=document.querySelector(path)
            // function findInputSearch(){
            //     setTimeout(()=>{
            //         var search_input=document.querySelector(path)
            //         if(search_input!=null){
            //             search_input.addEventListener('input',()=>{
            //                 console.log("Changeed")
            //             })
            //         }else{
            //             findInputSearch();
            //         }
            //     },7)
            // }
            // findInputSearch()
            var divs = document.querySelectorAll('.o_searchview_facet');
            var loading=divs.length+1
            function repeatFunction() {
                setTimeout(() => {
                    var divs = document.querySelectorAll('.o_searchview_facet');
                    if (divs.length>0) {
                        divs.forEach(function(div) {
                            var facetValue = div.querySelector('.o_facet_value');
                            if (facetValue && facetValue.textContent.trim() === 'Assignée / Suivies') {
                                div.style.display = 'none';

                            }
                        });
            
                    } else {
                        // Call the function recursively until the condition is met
                        repeatFunction();
                    }
                }, 7);
            }
            repeatFunction()

        } 

    },


    removeFacet(facet) {
        console.log("the facet deleted is ")
        console.log(facet['values'][0])
        
        if(facet['type']=="groupBy" && facet['values'][0]=="Assignée / Suivies "){
          var group_id=null
          var data_search = this.env.searchModel.getSearchItems()
          data_search.forEach(item => {
              if (item.description == "Assignée / Suivies") {
                this.env.searchModel.deactivateGroup(item.id)
                }
        })
        }
        
        this.env.searchModel.deactivateGroup(facet.groupId);
        this.inputRef.el.focus();
        const data = this.env.searchModel.getSearchItems();
        const query_data = this.env.searchModel.query
        var user = ""
        if (this.env.searchModel.resModel == "project.task") {
            data.forEach(item => {
                // Process each item here
                if (item.description == "Assignée / Suivies") {

                    for (var i = 0; i < query_data.length; i++) {
                        if (query_data[i].searchItemId == item.id) {
                            user = query_data[i].autocompleteValue['label']
                        }
                    }
                    var project_id = null
                    if (user != "") {

                        this.env.searchModel.searchDomain.forEach(item => {

                            if (Array.isArray(item)) {
                                if (item[0] == "project_id")
                                    project_id = item[2]
                            }
                        })
                        this.env.searchModel.searchDomain
                        if (this.env.searchModel.searchDomain != undefined) {
                            var project_id = null
                            this.env.searchModel.searchDomain.forEach(item => {

                                if (Array.isArray(item)) {
                                    if (item[0] == "project_id")
                                        project_id = item[2]
                                }
                            })
                            console.log(project_id);
                            this.env.searchModel.searchDomain
                            if (this.env.searchModel.searchDomain != undefined) {
                                this.orm.call("project.task", "retrieve_data_test", [user, project_id]);
                            }
                        }
                    }

                }
            });
            this.waitForTitle();
        }
        // if (user == "") {
        //     if(this.env.searchModel.searchDomain!=undefined){
        //         var project_id=null    
        //         this.env.searchModel.searchDomain.forEach(item=>{

        //             if(Array.isArray(item)){
        //                 if(item[0]=="project_id")
        //                 project_id=item[2]   
        //             }
        //         })   
        //         console.log(project_id);             
        //         this.env.searchModel.searchDomain
        //         if(this.env.searchModel.searchDomain!=undefined){
        //             this.orm.call("project.task", "retrieve_data_test", [user, project_id]);
        //         }
        // }

        // }

    },
    waitForTitle() {

        const element = document.querySelector('span.id');
        if (element != null) {

            let titleElement = element.querySelector('i');

            let title = titleElement ? titleElement.getAttribute('title') : null;
            if (title) {
                setTimeout(() => this.waitForTitle(), 1000); // Pass a reference to the function
            } else {
                // Title disappeared, do something or exit loop
                this.getFollowers();
            }
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
    async selectItem(item) {
        console.log("the selected item is ")
        console.log(JSON.stringify(item))
        if (!item.unselectable) {
            const { searchItemId, label, operator, value } = item;
            
            this.env.searchModel.addAutoCompletionValues(searchItemId, { label, operator, value });
            console.log("the facets are")
            // this.env.searchModel.facets=this.env.searchModel.facets.forEach(item=>{
            //     if(item.title=="Tâche"){
            //         item.separator="et"
            //         console.log("the item separator found is ")
            //         console.log(item.separator)
            //     }
            // })
            console.log(this.env.searchModel.facets)
        }
        
        this.resetState();
        const data = this.env.searchModel.getSearchItems();
        const query_data = this.env.searchModel.query
        const searchCriteria = {
            "fieldType": "many2one",
            "description": "Assignée / Suivies"
        };
        function findGroupId(data, searchCriteria) {
            for (const item of data) {
                if (item.fieldType === searchCriteria.fieldType && item.description === searchCriteria.description) {
                    return item.groupId;
                }
            }
            return null; // Return null if not found
        }
        const groupId = findGroupId(data, searchCriteria);

        var user = ""
        var group_id = null
        if (this.env.searchModel.resModel == "project.task" && item.searchItemId==groupId) {
            // Assignée / Suivies 
            
            data.forEach(item => {
                if (item.name == "is_mes_tach_suivi") {
                    group_id = item.id;
                    console.log(item);
                    console.log("Item")
                }
            })
            data.forEach(async item => {
                // Process each item here
                
                if (item.description == "Assignée / Suivies") {

                    for (var i = 0; i < query_data.length; i++) {
                        if (query_data[i].searchItemId == item.id) {
                            user = query_data[i].autocompleteValue['label']
                            console.log(user)
                        }
                    }

                    if (this.env.searchModel.searchDomain != undefined) {
                        var project_id = null
                        this.env.searchModel.searchDomain.forEach(item => {

                            if (Array.isArray(item)) {
                                if (item[0] == "project_id")
                                    project_id = item[2]
                            }
                        });

                        this.env.searchModel.searchDomain
                            
                                    if (this.env.searchModel.searchDomain != undefined) {
                                        await this.orm.call("project.task", "retrieve_data_test", [user, project_id])
            
                                    }
                                    console.log("the search model query ")
                                    console.log(this.env.searchModel.searchDomain)
                                    
                                    await this.env.searchModel.toggleSearchItem(group_id);
                                    console.log("Added Group Herere")
                                    console.log(item.searchItemDescription)
                        

                        console.log("the group id addedd ")
                        console.log(group_id)
                        console.log("the item is ")
                        console.log(item)
                        var divs = document.querySelectorAll('.o_searchview_facet');
                        var loading=divs.length+1
                        function repeatFunction() {
                            setTimeout(() => {
                                var divs = document.querySelectorAll('.o_searchview_facet');
                                if (loading === divs.length) {
                                    console.log("the divs are");
                                    console.log(divs);
                                    divs.forEach(function(div) {
                                        var facetValue = div.querySelector('.o_facet_value');
                                        if (facetValue && facetValue.textContent.trim() === 'Assignée / Suivies') {
                                            div.style.display = 'none';
                                        }
                                    });
                                } else {
                                    // Call the function recursively until the condition is met
                                    repeatFunction();
                                }
                            }, 7);
                        }
                        repeatFunction()
                        // setTimeout(() => {
                        //     divs = document.querySelectorAll('.o_searchview_facet');
                        //     if(loading==divs.length){

                        //         console.log("the divs are");
                        //         console.log(divs);
                        //         divs.forEach(function (div) {
                        //             var facetValue = div.querySelector('.o_facet_value');
                                    
                        //             if (facetValue && facetValue.textContent.trim() === 'Assignée / Suivies') {
                        //                 div.style.display = 'none';
                        //             }
                        //         });
                        //     } 
                                
                        // }, 7);



                    }
                    // this.env.searchModel.toggleSearchItem(group_id);
                }
            });
            this.waitForTitle();

        }
        if (user == "") {
            if (this.env.searchModel.searchDomain != undefined) {
                if (this.env.searchModel.searchDomain != undefined) {
                    var project_id = null
                    this.env.searchModel.searchDomain.forEach(item => {

                        if (Array.isArray(item)) {
                            if (item[0] == "project_id")
                                project_id = item[2]
                        }
                    })
                    console.log(project_id);
                    this.env.searchModel.searchDomain

                    if (this.env.searchModel.searchDomain != undefined) {
                        this.orm.call("project.task", "retrieve_data_test", [user, project_id]);
                    }
                }
            }

        }

    },

});