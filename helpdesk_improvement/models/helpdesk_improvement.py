from odoo import fields, models, _


class HelpdeskBlacklistLine(models.Model):
    _name = "helpdesk.ticket.blacklist.line"
    _description = "Emails detected as machines"

    _sql_constraints = [
        ('helpdesk_ticket_blacklist_lineunique_code', 'UNIQUE (email)',
         _('The email must be unique!')),
    ]

    email = fields.Char('Email', help="email to block", required=True)
    comment = fields.Text(
        'Comment',
        help="Reason wich this email is in the list", required=True)


class HelpdeskWhitelistLine(models.Model):
    _name = "helpdesk.ticket.whitelist.line"
    _description = "Emails excluded from blacklist"

    _sql_constraints = [
        ('crm_helpdesk_whitelist_unique_code', 'UNIQUE (email)',
         _('The email must be unique!')),
    ]

    email = fields.Char(
        'Email', help="email to exclude from blacklist",
        required=True)
    comment = fields.Text(
        'Comment',
        help="Reason wich this email is in the list", required=True)
