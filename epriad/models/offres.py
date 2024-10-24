from datetime import datetime,timedelta
import json
from odoo import models, fields, api
import requests
from bs4 import BeautifulSoup
from odoo.exceptions import UserError


class Appeloffre(models.Model):
    
    _name = 'entreprise.offre'

    Link = fields.Char("Link")
    reference = fields.Char("reference")
    organisme = fields.Char("organisme")
    caution = fields.Char("caution")
    budget = fields.Char("budget")
    ville = fields.Char("ville")
    DateLimite = fields.Char("DateLimite")
    classification = fields.Char("classification")
    Categorie = fields.Char("Categorie")
    classes = fields.Char("classes")


    @api.model
    def InsereDonnees(self,data):


        if len(data)==5:
            ordre,Organisme,datePrevue,av,details,categorie = data
            print(ordre,Organisme,datePrevue,av,details)

            # return "Le lead avec l'Ordre {} a été généré avec succès".format(ordre) 
            return "l'opportunité est ajouté à la piste avec succès"
        else:
            
            # Reference,Organisme,caution,budget,ville,DateLimite,classification,details,categorie = data
            Reference,Organisme,caution,budget,ville,DateLimite,classification,details = data
        
        date_visite_lieu=None
        

        login_url = 'https://global-marches.com/profile/signin'
        
        user = self.env['riad.compte'].search([], limit=1)

        login = user.login
        password = self.caesar_decrypt(user.password)

        login_payload = {
            'LOGIN': login,
            'PASSWORD': password,
            'CONNECT': 'Connexion...'
        }
        with requests.session() as session:
            session.post(login_url, data=login_payload)
            response = session.get(details)
            soup = BeautifulSoup(response.content,'lxml')
            print("the data")
            print(soup.find("div",{"class":"resultItem"}).find_all('tr',{}))
            date_visite_lieu = soup.find("div",{"class":"resultItem"}).find_all('tr',{})[10].find('td',{}).text
        print(date_visite_lieu)

        login_payload = {
            'LOGIN': 'steriad',
            'PASSWORD': 'steriad07',
            'CONNECT': 'Connexion...'
        }


        with requests.session() as session:
            session.post(login_url, data=login_payload)
            response = session.get(details)
            soup = BeautifulSoup(response.content,'lxml')
            print("the data")
            print(soup.find("div",{"class":"resultItem"}).find_all('tr',{}))
            date_visite_lieu = soup.find("div",{"class":"resultItem"}).find_all('tr',{})[10].find('td',{}).text
        if "-" not in date_visite_lieu and  date_visite_lieu:
            if len(date_visite_lieu)==10:
                date_visite_lieu=datetime.strptime(date_visite_lieu, "%d/%m/%Y")
            else:   
                date_visite_lieu=datetime.strptime(date_visite_lieu, "%d/%m/%Y %H:%M")            
        else:
            date_visite_lieu=None
        parsed_datetime =datetime.strptime(DateLimite, "%d/%m/%Y %H:%M")
        bdg=budget
        if "--" in budget:
            bdg=0
        else:
            bdg=budget.replace(",", "").replace(".", "")

        cst=caution
        if "--" in caution:
            cst=0
        else:
            cst=caution.replace(",", "").replace(".", "")
        index_org = Organisme.find("Organisme")
        index_obj = Organisme.find("Objet")

        # Extract the values
        orgnaisme = Organisme[index_org + len("Organisme") + 2 : index_obj].strip()
        objet = Organisme[index_obj + len("Objet") + 2 :].strip()
        if self.env["res.partner"].search_count([("name",'=',orgnaisme)])==0:
            partner_cr=self.env["res.partner"].create({
                'name':orgnaisme
            })
        else:
            partner_cr=self.env['res.partner'].search([("name",'=',orgnaisme)],limit=1)

        print("the id of the partner created")
        print(partner_cr)
        print("the id is ")
        print(partner_cr.id)
        print("the date is ")
        print(date_visite_lieu)
        Reference=Reference.replace("Déja lu","").replace(" ","")
        data=self.env["crm.lead"].search([('numero_a_o','=',Reference)])
        if data:
            return "l'opportunité est déjà existé à la piste "
        print("the date is ")

        print(parsed_datetime.strftime('%Y-%m-%d %H:%M:%S'))
        formatted_datetime = parsed_datetime.strftime('%Y-%m-%d %H:%M:%S')
        formatted_datetime_as_datetime = datetime.strptime(formatted_datetime, '%Y-%m-%d %H:%M:%S')

        new_datetime = formatted_datetime_as_datetime - timedelta(hours=2)
        if date_visite_lieu==None:
                    # lead = super(crm_lead, self).create(vals)

            self.env["crm.lead"].create({
            'numero_a_o':Reference,
            'partner_id':partner_cr.id,
            'name':objet,
            'caution_provisoire':float(int(cst)/100.0),
            'expected_revenue':float(int(bdg)/100.0),
            'street':ville,
            'date_deadline':str(new_datetime),
            'qualifications':classification,
            'nature_de_marche': "marches_publics",
            'is_visite_des_lieux':False,
            'is_date_ech':False,
        })


        else:
            new_date_visite_lieu=date_visite_lieu-timedelta(hours=2)
            self.env["crm.lead"].create({
            'numero_a_o':Reference,
            'partner_id':partner_cr.id,
            'name':objet,
            'caution_provisoire':float(int(cst)/100.0),
            'expected_revenue':float(int(bdg)/100.0),
            'street':ville,
            'date_deadline':str(new_datetime),
            'qualifications':classification,
            'nature_de_marche': "marches_publics",
            'is_visite_des_lieux':False,
            'is_date_ech':False,
            'date_visite':str(new_date_visite_lieu)
        })

        print("the field date_visite_lieu")
        print(date_visite_lieu)
        # #otenire les abonnee        
        # o1=self.env["res.users"].search([('name','=','Khaoula Bousghiri')],limit=1)
        # o2=self.env["res.users"].search([('name','=','Riad El Mahmoudi')],limit=1)
        # #cree mail_wizard_invite
        # self.env["mail.wizard.invite"].create({
        #     "res_id":self.env["crm.lead"].search([('name','=',objet)],limit=1).id,
        #     "res_model":"crm.lead",
        #     "message":"Vous avez invité au piste "+objet,
        # })

        # #cree  mail_followers pour le premier abonne
        # self.env["mail.followers"].create({
        #     "res_id":self.env["crm.lead"].search([('name','=',objet)],limit=1).id,
        #     "partner_id":o1.partner_id.id,
        #     "res_model":"crm.lead"
        # })
        # self.env["mail.followers"].create({
        #     "res_id":self.env["crm.lead"].search([('name','=',objet)],limit=1).partner_id.id,
        #     "partner_id":o1.partner_id.id,
        #     "res_model":"res.partner"
        # })
        # #cree  mail_followers pour le deuxieme abonne
        # self.env["mail.followers"].create({
        #     "res_id":self.env["crm.lead"].search([('name','=',objet)],limit=1).id,
        #     "partner_id":o2.partner_id.id,
        #     "res_model":"crm.lead"
        # })
        # self.env["mail.followers"].create({
        #     "res_id":self.env["crm.lead"].search([('name','=',objet)],limit=1).partner_id.id,
        #     "partner_id":o2.partner_id.id,
        #     "res_model":"res.partner"
        # })
        # print("the lead is is  from epriad")
        # print(self.env["crm.lead"].search([('name','=',objet)],limit=1).id)

        print("created with success")

        print(Reference,Organisme,caution,budget,ville,DateLimite,classification,details)

        # return "Le lead avec la référence {} a été généré avec succès".format(Reference)        
        return "l'opportunité est ajouté à la piste avec succès"
    @api.model
    def getpOffres(self,Cate,domains,secteurs,classes,villes,motcle1,motcle2,motcle3,DatEnt,DatEt,CautEnt,CautEt,BudgEnt,BudgEt,ordre,refe,EtOu1,EtOu2):

        return self.getpOffresALL(Cate,domains,secteurs,classes,villes,motcle1,motcle2,motcle3,DatEnt,DatEt,CautEnt,CautEt,BudgEnt,BudgEt,ordre,refe,EtOu1,EtOu2)

    

    def caesar_decrypt(self,ciphertext):
        decrypted_text = ""
        for char in ciphertext:
            if char.isalpha():
                decrypted_char = chr((ord(char) - ord('a') - 3) % 26 + ord('a'))
                decrypted_text += decrypted_char
            else:
                decrypted_text += char
        return decrypted_text


    @api.model
    def getpOffresALL(self,Cate,domains,secteurs,classes,villes,motcle1,motcle2,motcle3,DatEnt,DatEt,CautEnt,CautEt,BudgEnt,BudgEt,ordre,refe,EtOu1,EtOu2):

        login_url = 'https://global-marches.com/profile/signin'
        search_url = 'https://global-marches.com/listresultatao'
        
        user = self.env['riad.compte'].search([], limit=1)

        login = user.login
        password = self.caesar_decrypt(user.password)

        login_payload = {
            'LOGIN': login,
            'PASSWORD': password,
            'CONNECT': 'Connexion...'
        }
        if len(domains) == 0 or domains[0]=='':
                domains='%'
        if len(secteurs) == 0  or secteurs[0]=='':
                secteurs='%'
        print("the domains are")
        print(domains)
        print("the secteurs are")
        print(secteurs)

        if(len(classes) == 0):
            classes="%"
        if(len(villes) == 0):
            villes="%"
        print("the domains that comming from nass")
        print(domains)
        form_params = {
            'DATE_PARUTION_1': '',
            'DATE_PARUTION_2': datetime.now().strftime('%d/%m/%Y'),
            'CAT_OFFRE': Cate,
            'CLASSES[]': classes,
            'VILLE[]': villes,
            'ORG[]': '%',
            'Domaine[]': domains,
            'Secteur[]': secteurs,
            'Qualification[]': '%',
            'Classe[]': '%',
            'MOT_CLE_1': motcle1,
            'MOT_CLE_CRET_1':EtOu1,
            'MOT_CLE_2': motcle2,
            'MOT_CLE_CRET_2': EtOu2,
            'MOT_CLE_3': motcle3,
            'DATE_LIMIT_1': DatEnt,
            'DATE_LIMIT_2': DatEt,
            'CAUTION_1': CautEnt,
            'CAUTION_2': CautEt,
            'NULL_INCLU_1': '1',
            'BUDJET_1': BudgEnt,
            'BUDJET_2': BudgEt,
            'NULL_INCLU_2': '1',
            'ORDRE': ordre,
            'REFERENCE': refe,
            'se': '',
            'preselection': '',
            'type_oa': '',
            'SAVE': '',
            'PARPAGE_FILRT':'100',
            'page':''
        }       


        with requests.session() as session:

            offres=[]
            session.post(login_url, data=login_payload)
            response = session.get(search_url,params=form_params)
            soup = BeautifulSoup(response.content, 'html.parser')

            LastPage = soup.find('div',{'id':"NB_RESULT"}).text
            LastPage = int(int(LastPage[:LastPage.index(" ")])/100)+1

            
            for page in range(1,LastPage+1):
                form_params['page']=page
                response = session.get(search_url, params=form_params)
                soup = BeautifulSoup(response.content, 'html.parser')
                data = soup.find('tbody', {})
                if data is None:
                    return json.dumps(offres,ensure_ascii=False)
                data = data.find_all('tr', {})
                for i in data:
                    row = i.find_all('td')
                    Ref = row[1]
                    Link = Ref.find('input', {}).attrs['value']
                    reference = Ref.text.strip().replace('\n', ' ')
                    organisme = row[2].text.strip().replace('\n', ' ')
                    caution = row[3].find_all('span',{})[0].text
                    budget = row[3].find_all('span', {})[1].text
                    ville = row[4].text.strip()
                    DateLimite = row[5].text.strip()
                    classification = row[6].text.replace("  "," ")
                    DAO = row[7].find_all("a",{})
                    if(len(DAO)>0):
                      DAOzip = DAO[0].attrs['href']
                      if ".zip" in DAOzip:
                          DAOzip = "https://global-marches.com" + DAOzip
                      else:
                          DAOzip = None
                    else:
                      DAOzip = None

                    if(len(DAO)>1):
                      DAOse = DAO[len(DAO)-1].attrs['href']
                      if "javascript" in DAOse:
                          DAOse = None
                    else:
                      DAOse = None
                      
                    deja_pister="no"
                    print(reference)
                    data=self.env["crm.lead"].search([('numero_a_o','=',reference.replace("Déja lu","").replace(" ",""))])
                    
                    if data:
                        deja_pister="yes"

                    offres.append({
                        "Link":Link,
                        "Reference": reference,
                        "Organisme": organisme,
                        "caution": caution,
                        "budget":budget,
                        "ville":ville,
                        "DateLimite":DateLimite,
                        "classification":classification,
                        "DAOzip":DAOzip,
                        "DAOse":DAOse,
                        "deja_pister":deja_pister,
                    })
        return json.dumps(offres,ensure_ascii=False)


    

