# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Helpdesk Improvement',
    'summary': """
        Helpdesk""",
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'After-Sales',
    'author':   'AdaptiveCity, '
                'C2i Change 2 Improve, '
                'Domatix, '
                'Factor Libre, '
                'SDi Soluciones, '
                'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/helpdesk',
    'depends': [
        'helpdesk',
        'mail',
        'portal',
    ],
    'data': [
        'views/res_config_view.xml',
        'views/helpdesk_improvement_menu.xml',
        'views/helpdesk_improvement_view.xml'
    ],
    'application': True,
    'installable': True,
}