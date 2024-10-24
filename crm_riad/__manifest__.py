{
    'name': "CRM Extend",
    'author': 'daisy consulting',
    'summary': """task for crm""",
    'website': 'http://www.daisy.com',
    'license': 'AGPL-3',
    'description': """ """,
    'version': '1.0',
    'depends': ['crm'],
    'data': [

        'security/ir.model.access.csv',
        'views/crm_lead.xml',
        'wizard/delete.xml',
        
        'report/activity_report_action.xml',
        'report/activity_template.xml',
        'data/cron.xml',

    ],    
    'assets':{
     'web.assets_backend':[
         'crm_riad/static/src/css/main.css',
     ]   
    },
    
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
