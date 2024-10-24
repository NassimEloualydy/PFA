odoo.define('epriad.profile_view', function (require) {
   
    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');
    var ajax = require('web.ajax');

    var classes = []
    var villes = []

    var operation = ''

    var profile = AbstractAction.extend({
        template: 'profile_view',
        cssLibs: [
        ],
        jsLibs: [
        ],
  
        events: {

          'click .item': 'addClasse',
          'click .itemVille':'addville',
          'click #operation':'enregestre',
    
          
      },
          on_attach_callback: function () {
          
             this.ShowClasses()
             this.ShowVilles()
             this.getProfile()
              return this._super.apply(this, arguments);
            },

             
            ShowClasses : function(){
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
              console.log(classes)
            },

            addclassesExi : function(cl)
            {
              classes=[]
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
              console.log(villes)
            },
            addvillesExi : function(cl)
            {
              villes=[]
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

            getProfile : function(ev){
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
                    console.log(cl)
                    let vi = JSON.parse(profile['villes'])
                    console.log(vi)
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

            },
            enregestre : function(){
              try {
                
                var self = this;
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
                self._rpc({
                  
                    model:"riad.profiles",
                    method:"ajouterProfile",
                    args : [classes,villes,motcle1,motcle2,motcle3,DatEnt,DatEt,CautEnt,CautEt,BudgEnt,BudgEt,ordre,refe,EtOu1,EtOu2]
                  }).then(function(result){   
                    
                    showSuccessNotification("enregistrer avec succès")
                    
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
               notification.className = 'success-notification';
               notification.textContent = message;
               document.querySelector('.MyContainer').appendChild(notification);
       
               setTimeout(function () {
                   notification.style.display = 'none';
                   notification.remove();
               }, 3000);
            }
             var ChercheClasses = [
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
            
              core.action_registry.add('monProfile.Actions', profile);

              return profile;
    });
            

