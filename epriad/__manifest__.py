{
    'name': "crm Offres new version",
    'author': 'Daisy consulting new version',
    'summary': """Crm Appel D'offre New Version""",
    'website': 'http://www.daisy.com',
    'license': 'AGPL-3',
    'description': """ """,
    'version': '1.0',
    'depends': ['base'],
     'data': [
         'security/ir.model.access.csv',
         'views/Views.xml',
         'views/Actions.xml',
         'data/cron.xml',
    ],
      'assets': {
        'web.assets_backend': [
            'epriad/static/src/js/script.js',
            'epriad/static/src/js/profile.js',
            'epriad/static/src/xml/View.xml',
            'epriad/static/src/xml/profile.xml',
            'epriad/static/src/css/style.css',
        ],
    },

    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
