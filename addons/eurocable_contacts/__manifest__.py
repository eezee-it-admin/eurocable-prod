# Copyright 2022 Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Eurocable Contacts',
    'version': '15.0.1.0.1',
    'author': 'Eezee-It',
    'category': 'Sale',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'contacts',
        'account',
        'account_followup'
    ],
    'data': [
        'views/res_partner_view.xml',
        'data/reminder_mail_template.xml',
        'security/group.xml'
    ],
}
