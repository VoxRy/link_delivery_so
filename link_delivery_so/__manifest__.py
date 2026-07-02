{
    'name': 'Link Delivery to Sales Order',
    'summary': 'Link stock moves of manual deliveries to sales order lines',
    'version': '15.0.1.0.0',
    'category': 'Inventory',
    'author': 'Kais Akram',
    'depends': ['sale_stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
