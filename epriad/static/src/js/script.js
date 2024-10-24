odoo.define('epriad.crm_view', function (require) {
   
    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');
    var ajax = require('web.ajax');

    var classes = []
    var villes = []
    var secteurs = []
    var domains = []

    var Offres = AbstractAction.extend({
        template: 'crm_view',
        cssLibs: [
      ],
      jsLibs: [
      ],

      events: {

        'click .item': 'addClasse',
        'click .itemVille':'addville',

        'click .cherche': 'cherche',
        'click .leadGene': 'LeadGeneration',
        'click .profile': 'profilefiltre',

        'input  #referenceInput':'cumulativeSearch',
        'input #cautionInput':'cumulativeSearch',
        'input  #budgetInput':'cumulativeSearch',
        'input  #villeInput':'cumulativeSearch',
        'input  #organismeInput':'cumulativeSearch',
        
        'input  #classificationinput':'cumulativeSearch',
        'click  tr':'LienSite',
        //the script for the button plus
        'click .btn_plus':'btn_plus',
        //the script for the function moins
        'click .btn_moin':'btn_moin',
        //the script for the function who get secteurs depending on the domain selected
        'change .selectIDomain' :'selectidomain',
        'click .downloadCPS':'downloadCPS'
    },
        on_attach_callback: function () {
            villes=[]
            classes=[]
            this.ShowClasses()
            this.ShowVilles()
            return this._super.apply(this, arguments);
          },

          
          ShowClasses : function(ev){

            classes=[]
            let ListClasses="";
            ChercheClasses.forEach(element => {
              let item = `<div class="item" id=${element['id']} data-info=${element['id']}>${element['Classe']}</div>`;
              ListClasses+=item;
            });
            document.querySelector('.selection').innerHTML=ListClasses;

            ListClasses=""
            ChercheClasses.forEach(element => {
              let item = `<div class="item desactive" id=${element['id']} data-info=${element['id']}>${element['Classe']}</div>`;
              ListClasses+=item;
            });
            document.querySelector('.selecteddd').innerHTML=ListClasses;
          },

          ShowVilles : function(){  
            let ListVilles="";
            Villes.forEach(element => {
              let item = `<div class="itemVille" id=${element['id']} data-ville=${element['id']}>${element['city']}</div>`;
              ListVilles+=item;
            });
            document.querySelector('.selectionVilles').innerHTML=ListVilles;

            ListVilles="";
            Villes.forEach(element => {
              let item = `<div class="itemVille desactive" id=${element['id']} data-ville=${element['id']}>${element['city']}</div>`;
              ListVilles+=item;
            });
            document.querySelector('.selectedVilles').innerHTML=ListVilles;
          },

          addClasse : function(ev){

            let classData = ev.target.getAttribute('data-info');
            let elementWithDataInfo = document.querySelectorAll(`[data-info="${classData}"]`);

            elementWithDataInfo[0].classList.toggle('desactive');
            elementWithDataInfo[1].classList.toggle('desactive');

            if (classes.indexOf(classData) !== -1) {
              classes.splice(classes.indexOf(classData), 1);
            } else {
              classes.push(classData);
            }
          },
          addclassesExi : function(cl)
            {
              classes=[]
              this.ShowClasses()
              cl.forEach(element => {
              let elementWithDataInfo = document.querySelectorAll(`[data-info="${element}"]`);
              elementWithDataInfo[0].classList.toggle('desactive');
              elementWithDataInfo[1].classList.toggle('desactive');
              if (classes.indexOf(element) !== -1) {
                classes.splice(classes.indexOf(element), 1);
              } else {
                classes.push(element);
              } 
              });
            },

          addville : function(ev){
            let villeData = ev.target.getAttribute('data-ville');
            let elementWithDataInfo = document.querySelectorAll(`[data-ville="${villeData}"]`);
            elementWithDataInfo[0].classList.toggle('desactive');
            elementWithDataInfo[1].classList.toggle('desactive');
            if (villes.indexOf(villeData) !== -1) {
              villes.splice(villes.indexOf(villeData), 1);
            } else {
              villes.push(villeData);
            }
          },
          addvillesExi : function(cl)
          {
            villes=[]
            this.ShowVilles()
            cl.forEach(element => {
              let elementWithDataInfo = document.querySelectorAll(`[data-ville="${element}"]`);
              elementWithDataInfo[0].classList.toggle('desactive');
              elementWithDataInfo[1].classList.toggle('desactive');
              if (villes.indexOf(element) !== -1) {
                villes.splice(villes.indexOf(element), 1);
              } else {
                villes.push(element);
              }
            });
          },
          downloadCPS:function(e){
            var theId = e.currentTarget.id;
            url=theId
            const link = document.createElement("a");
            link.href = url;
            link.download = "nassim.zip";
            link.click();
          }
          ,
          selectidomain:function(e){
            var theId = e.currentTarget.id;
            var theValue = e.currentTarget.value;
            if(theValue=="1"){
             var data="";
data+="<option value=''>Tous les secteurs</option>";
// data+="<option value='1 '>1 </option>";
// data+="<option value='2 '>2 </option>";
// data+="<option value='3 '>3 </option>";
// data+="<option value='4 '>4 </option>";
// data+="<option value='5 '>5 </option>";
// data+="<option value='6 '>6 </option>";
// data+="<option value='7 '>7 </option>";
// data+="<option value='8 '>8 </option>";
// data+="<option value='9 '>9 </option>";
// data+="<option value='10'>10</option>";
// data+="<option value='11'>11</option>";
// data+="<option value='12'>12</option>";
// data+="<option value='13'>13</option>";
// data+="<option value='14'>14</option>";
// data+="<option value='15'>15</option>";
// data+="<option value='16'>16</option>";
// data+="<option value='17'>17</option>";
// data+="<option value='18'>18</option>";
// data+="<option value='19'>19</option>";
// data+="<option value='20'>20</option>";
// data+="<option value='21'>21</option>";
// data+="<option value='22'>22</option>";
// data+="<option value='23'>23</option>";
// data+="<option value='24'>24</option>";
// data+="<option value='25'>25</option>";
data+="<option value='91'>A</option>";

data+="<option value='92'>B</option>";
data+="<option value='93'>C</option>";
data+="<option value='94'>D</option>";
data+="<option value='95'>E</option>";
data+="<option value='96'>F</option>";
data+="<option value='97'>G</option>";
data+="<option value='98'>H</option>";
data+="<option value='99'>I</option>";
data+="<option value='100'>J</option>";
data+="<option value='101'>K</option>";
data+="<option value='102'>L</option>";
data+="<option value='103'>M</option>";
data+="<option value='104'>N</option>";
data+="<option value='105'>O</option>";
data+="<option value='106'>P</option>";
data+="<option value='107'>Q</option>";
data+="<option value='108'>R</option>";
data+="<option value='109'>S</option>";
data+="<option value='110'>T</option>";
data+="<option value='111'>U</option>";
data+="<option value='112'>V</option>";
data+="<option value='113'>W</option>";
data+="<option value='114'>X</option>";
data+="<option value='119'>Y</option>";
document.getElementById("secteur"+theId).innerHTML=data;
            }
            if(theValue=="2"){
              document.getElementById("secteur"+theId).innerHTML="<option value='Equipement'>Habitat</option>";
              var data="";
              data+="<option value=''>Tous les secteurs</option>";

              data+="<option value='26'>1</option>";
              data+="<option value='27'>2</option>";
              data+="<option value='28'>3</option>";
              data+="<option value='29'>4</option>";
              data+="<option value='30'>5</option>";
              data+="<option value='31'>6</option>";
              data+="<option value='32'>7</option>";
              data+="<option value='33'>8</option>";
              data+="<option value='34'>9</option>";
              data+="<option value='35'>10</option>";
              data+="<option value='36'>11</option>";
              data+="<option value='37'>12</option>";
              data+="<option value='38'>13</option>";
              data+="<option value='39'>14</option>";
              data+="<option value='40'>15</option>";
              data+="<option value='41'>16</option>";
              data+="<option value='42'>17</option>";
              data+="<option value='43'>18</option>";
              data+="<option value='44'>19</option>";
              data+="<option value='45'>20</option>";
              data+="<option value='46'>21</option>";
              data+="<option value='47'>22</option>";
              data+="<option value='48'>23</option>";
              data+="<option value='49'>24</option>";
              
document.getElementById("secteur"+theId).innerHTML=data;

            }
            console.log("the id is "+theId);
            console.log("the value is "+theValue);
            
          },
          //the function of the button btn_moin
          btn_moin:function(e){            
              var htmlString = e.currentTarget.id;
              console.log(htmlString);
              document.getElementById("r"+htmlString).style.display="None";
          },
//the function btn_plus
btn_plus: function(){
  var searchContainer = document.getElementById('search_container');

  // Select all div elements with class 'rowm' inside the 'search_container' div

  var rowmDivs = searchContainer.querySelectorAll('.rowm').length;
  var indexOItmes=rowmDivs;
  var t_first=new Array();
  var t_second=new Array();
  for(i=0;i<document.getElementsByClassName("selectI").length;i++){
    t_first.push(document.getElementsByClassName("selectI")[i].value);
  }

  for(i=0;i<document.getElementsByClassName("selectIDomain").length;i++){
    t_second.push(document.getElementsByClassName("selectIDomain")[i].value);
  }
  
  var dataAdded="<div   id='rowm_"+indexOItmes+"' class='rowm'>";
  dataAdded+="<div class='fieldsm'>";
  dataAdded+="<span class='spanSearch'>Domaine</span>";
  dataAdded+="<select id='select"+(indexOItmes+1)+"' class='selectIDomain'  name='Domain' >";
  dataAdded+="<option value=''>Tous les domaines</option>";
  dataAdded+="<option value='1'>Equipement</option>";
  dataAdded+="<option value='2'>Habitat</option>";
  dataAdded+="</select>";
  dataAdded+="<span class='spanSearch'>Secteur</span>";

  dataAdded+="<select id='secteurselect"+(indexOItmes+1)+"' class='selectI sectuers'>";
  dataAdded+="<option value=''>Tous les secteurs</option>";
  dataAdded+="</select>";
// dataAdded+="<span class='spanSearch'>Qualification</span>";

  // dataAdded+="<select class='selectI' name='Qualification' id='Qualification'>";
  // dataAdded+="<option value=''>Choisir un Qualification</option>";
  // dataAdded+="<option value='all'>Tout les Qualification</option>";  

  // dataAdded+="</select>";
  // dataAdded+="<span class='spanSearch'>Class</span>";

  // dataAdded+="<select class='selectI' name='Classe' id='Classe'>";
  // dataAdded+="<option value=''>Choisir un Class</option>";
  // dataAdded+="<option value='all'>Tout les class</option>";

  // dataAdded+="</select>";
  dataAdded+="<input type='button' class='btn_plus' value='+'/>&nbsp;";
  dataAdded+="<input  id='owm_"+indexOItmes+"' type='button' class='btn_moin' value='-'/>";
  dataAdded+="</div>";
  dataAdded+="</div>";
  document.getElementById("search_container").innerHTML=document.getElementById("search_container").innerHTML+dataAdded;

  for(i=0;i<t_first.length;i++){
    document.getElementsByClassName("selectI")[i].value=t_first[i]
  }
  
  for(i=0;i<t_second.length;i++){
    document.getElementsByClassName("selectIDomain")[i].value=t_second[i]
  }
 
  console.log(indexOItmes);
}
,
          cherche: function () {
            secteurs=[]
            domains=[]
            console.log("we entered")
            for(i=0;i<document.getElementsByClassName("selectIDomain").length;i++){
              var added=true;
              var sec= document.getElementsByClassName("sectuers")[i].value;
              var domain= document.getElementsByClassName("selectIDomain")[i].value;
              for(j=0;j<secteurs.length;j++){
                if(secteurs[j]==sec && domains[j]==domain){
                    added=false;
                    break;
                }
               }
               if(added==true){
                domains.push(domain);
                secteurs.push(sec);
               }
            }
            console.log("the nass")
            console.log(secteurs)
            console.log(domains)

            console.log(villes)
            console.log(classes)
            let motcle1 =document.getElementById("Cle1").value
            let motcle2 =document.getElementById("Cle2").value
            let motcle3 =document.getElementById("Cle3").value
            let DatEnt=document.getElementById("Datentre").value
            let DatEt=document.getElementById("Datet").value
            let CautEnt=document.getElementById("Cauentre").value
            let CautEt=document.getElementById("Cauet").value
            let BudgEnt=document.getElementById("Budentre").value
            let BudgEt=document.getElementById("Budet").value
            let ordre=document.getElementById("ordre").value
            let refe=document.getElementById("ref").value
            let EtOu1 = document.getElementById("EtOu1").value
            let EtOu2 = document.getElementById("EtOu2").value
            
            try {
              var self = this;
              self._rpc({
                  model:"entreprise.offre",
                  method:"getpOffres",
                  args:["All",domains,secteurs,classes,villes,motcle1,motcle2,motcle3,DatEnt,DatEt,CautEnt,CautEt,BudgEnt,BudgEt,ordre,refe,EtOu1,EtOu2]
                }).then(function(result){
                      showTableAll(result)
                      document.getElementById('referenceInput').style.display = "inline";
                      document.getElementById('cautionInput').style.display='inline'
                      document.getElementById('budgetInput').style.display='inline'
                      document.getElementById('villeInput').style.display='inline'
                      document.getElementById('organismeInput').style.display='inline'
                      
                      document.getElementById('classificationinput').style.display='inline'
                              })
            .catch(error => {
                console.error('Error fetching JSON:', error);
            });

                }catch (err) {
                    console.log("the error is " + err)
                  }       
            
                 
                },

          cumulativeSearch:function() {
            var referenceInput = document.getElementById("referenceInput").value.toUpperCase();
            var organismeInput = document.getElementById("organismeInput").value.toUpperCase();

            var villeInput = document.getElementById("villeInput").value.toUpperCase();
            
            var classificationInput = document.getElementById("classificationinput").value.toUpperCase();
            var cautionInput = parseInt(document.getElementById("cautionInput").value.replace(/\./g, '').replace(',', ''));
            var budgetInput = parseInt(document.getElementById("budgetInput").value.replace(/\./g, '').replace(',', ''));
        
            var table = document.getElementById("myTable");
            var tr = table.getElementsByTagName("tr");
            var displayedRowCount = 0;
        
            for (var i = 1; i < tr.length; i++) {
                var tdReference = tr[i].getElementsByTagName("td")[1];
                var tdOrganisme = tr[i].getElementsByTagName("td")[2];
                var tdVille = tr[i].getElementsByTagName("td")[5];
                var tdclassification = tr[i].getElementsByTagName("td")[7];
                var tdCaution = tr[i].getElementsByTagName("td")[3];
                var tdBudget = tr[i].getElementsByTagName("td")[4];
        
                var displayRow = true;
                if (tdOrganisme && tdOrganisme.textContent.toUpperCase().indexOf(organismeInput) === -1) {
                  displayRow = false;
              }
      
                if (tdReference && tdReference.textContent.toUpperCase().indexOf(referenceInput) === -1) {
                    displayRow = false;
                }
        
                if (tdVille && tdVille.textContent.toUpperCase().indexOf(villeInput) === -1) {
                    displayRow = false;
                }

                if (tdclassification && tdclassification.textContent.toUpperCase().indexOf(classificationInput) === -1) {
                  displayRow = false;
               }
        
                if (tdCaution) {
                    var cautionValue = parseFloat(tdCaution.textContent.slice(0, -3).replace(/\./g, '').replace(',', ''));
                    if (isNaN(cautionValue)){
          
                    }
                    else if (cautionValue<cautionInput){
                      displayRow=false
                    }
                }
        
                if (tdBudget) {
                    var budgetValue = parseFloat(tdBudget.textContent.slice(0, -3).replace(/\./g, '').replace(',', ''));
                    if (isNaN(budgetValue)) {
                        
                    }
                    else if(budgetValue < budgetInput)
                    {
                      displayRow = false;
                    }
                }
        
                if (displayRow) {
                    tr[i].style.display = "";
                    displayedRowCount++;
                } else {
                    tr[i].style.display = "none";
                }
            }

            document.getElementsByClassName('total')[0].innerHTML=" "+displayedRowCount+"  Appel(s) d'offre trouvé(s)";

          },
              
          
          LienSite:function(ev){
            let linkref = ev.target.parentNode.getAttribute('data-link')
            if(linkref != null)
            {
              linkref = "https://global-marches.com/detailresultat?PERPAGE=100&OS%5B%5D="+linkref
              window.open(linkref, '_blank');

            }
          },

          LeadGeneration:function(ev){
            // <td><button class="leadGeneDejaLu" disabled >Déjà Pisté</button></td>

            ev.target.innerHTML="Déjà Pisté";
            ev.target.classList.remove("leadGene");
            ev.target.classList.add("leadGeneDejaLu");
            ev.target.classList.add("leadGeneDejaLu");
            ev.target.setAttribute('disabled', 'disabled');
            let data = []
            ev.stopPropagation();

            let row = ev.target.parentNode.parentNode
            let Reference = row.getElementsByTagName("td")[1].textContent;
            let Organisme = row.getElementsByTagName("td")[2].textContent;
            let caution = row.getElementsByTagName("td")[3].textContent;
            let budget = row.getElementsByTagName("td")[4].textContent;
            let ville = row.getElementsByTagName("td")[5].textContent;
            let DateLimite = row.getElementsByTagName("td")[6].textContent;
            let classification = row.getElementsByTagName("td")[7].textContent;
            let details = "https://global-marches.com/detailresultat?PERPAGE=100&OS%5B%5D="+row.getAttribute('data-link');
            data = [Reference,Organisme,caution,budget,ville,DateLimite,classification,details]
            try {
              var self = this;
              self._rpc({
                  model:"entreprise.offre",
                  method:"InsereDonnees",
                  args:[data]
                }).then(function(result){

                showSuccessNotification(result)

                })
              
          .catch(error => {
              console.error('Error fetching JSON:', error);
          });

              }catch (err) {
                  console.log("the error is " + err)
                } 
          },
          profilefiltre : function()
          {
            try {
              var self = this;
              self._rpc({
                  model:"riad.profiles",
                  method:"getProfile",
                }).then(function(result){   
                  if(result==null){
                    return
                  }
                  
                  let profile = JSON.parse(result)
                  let cl = JSON.parse(profile['classes'])
                  let vi = JSON.parse(profile['villes'])
                  self.addvillesExi(vi)
                  self.addclassesExi(cl)

                  let motcle1 =document.getElementById("Cle1").value=profile['motcle1']
                  let motcle2 =document.getElementById("Cle2").value=profile['motcle2']
                  let motcle3 =document.getElementById("Cle3").value=profile['motcle3']
                  let DatEnt=document.getElementById("Datentre").value=profile['DatEnt']
                  let DatEt=document.getElementById("Datet").value=profile['DatEt']
                  let CautEnt=document.getElementById("Cauentre").value=profile['CautEnt']
                  let CautEt=document.getElementById("Cauet").value=profile['CautEt']
                  let BudgEnt=document.getElementById("Budentre").value=profile['BudgEnt']
                  let BudgEt=document.getElementById("Budet").value=profile['BudgEt']
                  let ordre=document.getElementById("ordre").value=profile['ordre']
                  let refe=document.getElementById("ref").value=profile['refe']
                  let EtOu1 = document.getElementById("EtOu1").value=profile['EtOu1']
                  let EtOu2 = document.getElementById("EtOu2").value=profile['EtOu2']

                              })
            .catch(error => {
                console.error('Error fetching JSON:', error);
            });

                }catch (err) {
                    console.log("the error is " + err)
                  } 
          }
                
              });

            function showSuccessNotification(message) {
              var notification = document.createElement('div');
               if(message=="l'opportunité est ajouté à la piste avec succès"){
                 
                 notification.className = 'success-notification';
               }else{
                notification.className = 'danger-notification';
               }
                notification.textContent = message;
                document.querySelector('.MyContainer').appendChild(notification);
        
                setTimeout(function () {
                    notification.style.display = 'none';
                    notification.remove();
                }, 3000);
            }
            function showTableAll(result){
              let FullContent=`<table id='myTable'>
                        <tr>
                          <th>N°</th>
                          <th>N° RÉFÉRENCE</th>
                          <th>ORGANISME/OBJET</th>
                          <th>CAUTION</th>
                          <th>BUDGET</th>
                          <th>VILLE</th>
                          <th>D. LIMITE</th>
                          <th>CLASSIFICATION</th>
                          <th>D.A.O</th>
                          <th>ACTION</th>
                        </tr>`
                        var N=1
                        JSON.parse(result).forEach(element => {
                          let dao = '';
                          if(element["DAOzip"] != null){
                            console.log("the url is ")
                            console.log(element["DAOzip"])
                            // dao = `<a class='downloadCPS' href="${element["DAOzip"]}" id="${element["DAOzip"] }" target="_blank">CPS</a>`
                            dao = `<a class='downloadCPS'  id="${element["DAOzip"] }" target="_blank">CPS</a>`
                          }

                          let se = '';
                          if(element["DAOse"] != null){
                            se = `<a   href="${element["DAOse"] }"  target="_blank">S.E</a>`
                          }
                          var row=``;
                          console.log(element['deja_pister']);
                          if(element['deja_pister']=="no"){
                            row = `
                            <tr data-link=${element['Link']}>
                            <td>${N}</td>
                            <td>${element["Reference"]}</td>
                            <td>${element["Organisme"]}</td>
                            <td>${element["caution"]}</td>
                            <td>${element["budget"]}</td>
                            <td>${element["ville"]}</td>
                            <td>${element["DateLimite"]}</td>
                            <td>${element["classification"]}</td>
                            <td>
                              <div class='dao'>
                                 ${dao}
                                 ${se}
                              </div>
                            </td>
                            <td><button class="leadGene">Pister</button></td>
                          </tr>
                                  `;
                          }else{

                            row = `
                            <tr data-link=${element['Link']}>
                            <td>${N}</td>
                            <td>${element["Reference"]}</td>
                            <td>${element["Organisme"]}</td>
                            <td>${element["caution"]}</td>
                            <td>${element["budget"]}</td>
                            <td>${element["ville"]}</td>
                            <td>${element["DateLimite"]}</td>
                            <td>${element["classification"]}</td>
                            <td>
                              <div class='dao'>
                                 ${dao}
                                 ${se}
                              </div>
                            </td>
                            <td><button class="leadGeneDejaLu" disabled >Déjà Pisté</button></td>
                          </tr>
                                  `;
                          }
                          N+=1;
                          FullContent+=row;
                        });

                        FullContent+="</table>";
                        document.getElementById('Table').innerHTML=FullContent;
                        N-=1;
                        document.getElementsByClassName('total')[0].innerHTML=" "+N+"   Appel(s) d'offre trouvé(s)";
            }

            ChercheClasses = [
              {
                'id':'1',
                'Classe':'T11 Travaux de construction et d’aménagement'
              },
              {
                'id':'2',
                'Classe':'T12 Travaux de Terrassements'
              },{
                'id':'3',
                'Classe':'T13 Travaux de menuiserie en bois, aluminium et metallique - travaux de ferronnerie et charpente'
              },{
                'id':'4',
                'Classe':'T14 Travaux de plomberie, installation de climatisation et chauffage'
              },{
                'id':'5',
                'Classe':'T15 Travaux de Peinture et travaux de miroiterie et vitrerie'
              },{
                'id':'6',
                'Classe':'T16 Travaux d’etancheite et d’isolation thermique et acoustique'
              },{
                'id':'7',
                'Classe':'T17 Travaux de Revetement'
              },{
                'id':'8',
                'Classe':'T18 Travaux en platre et faux plafonds'
              },{
                'id':'9',
                'Classe':'T19 Travaux d’installation d’ascenseurs et de monte charges'
              },{
                'id':'10',
                'Classe':"T20 Construction d'ouvrages d'art; genie civile et amenagement exterieur"
              },{
                'id':'11',
                'Classe':"T21 Amenagement de jardins, d'espaces verts "
              },{
                'id':'12',
                'Classe':'T22 Amenagements interieur divers'
              },{
                'id':'13',
                'Classe':'T23 Travaux d’assainissement et de reseaux divers'
              },{
                'id':'15',
                'Classe':"T25 Travaux d'automatisme ,hydromecaniques et traitement d'eau potable"
              },{
                'id':'17',
                'Classe':"T27 Travaux de voiries, chemins, pistes et voies ferrées"
              },{
                'id':'19',
                'Classe':"T29 Travaux d'electricite et d'eclairage public"
              },{
                'id':'20',
                'Classe':"T30 Travaux d’installation d’équipement de détection, controle d’acces, audiovisuel et protection incendie"
              },{
                'id':'21',
                'Classe':"T31 Travaux de reseaux telephoniques, informatiques et electroniques"
              },{
                'id':'25',
                'Classe':"E35 Équipements hydro-electromécaniques, electromécaniques et similaires"
              },{
                'id':'34',
                'Classe':"E44 Fournitures scolaires et d’enseignement - materiel et outillage didactique "
              },{
                'id':'35',
                'Classe':"E45 Materiel et accessoires informatique, logiciels et pieces de rechanges"
              },{
                'id':'42',
                'Classe':"E52 Materiel, mobilier et fournitures de Bureau"
              },{
                'id':'59',
                'Classe':"S71 services de nettoyage"
              },{
                'id':'60',
                'Classe':"S72 Service de gardiennage, surveillance et d'interims"
              }
            ]

            var Villes = [
              {"id": 1, "city": "---REGION DE SOUSS- MASSA"},
              {"id": 11, "city": "---REGION MARRAKECH - SAFI"},
              {"id": 19, "city": "---REGION DE CASABLANCA - SETTAT"},
              {"id": 24, "city": "---REGION RABAT-SALE-KENITRA"},
              {"id": 29, "city": "---REGION DES FES- MEKNES"},
              {"id": 33, "city": "---REGION DE L'ORIENTAL"},
              {"id": 40, "city": "---REGION DE DRAA - TAFILALET"},
              {"id": 47, "city": "---REGION TANGER-TETOUAN- AL HOCEIMA"},
              {"id": 64, "city": "---REGION DE BENI MELLAL-KHENIFRA"},
              {"id": 78, "city": "---REGION DE GUELMIM - OUED NOUN"},
              {"id": 84, "city": "---REGION DE LAAYOUNE - SAGUIA AL HAMRA"},
              {"id": 88, "city": "---REGION DE DAKHLA OUED EDDAHAB"},
              {"id": 92, "city": "---Ville etrangere"},
          ]

              core.action_registry.add('crm.Actions', Offres);

              return Offres;
    });
            

