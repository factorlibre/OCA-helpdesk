from odoo import api, fields, models, _


class HelpdeskTicket(models.Model):

    _name = 'helpdesk.ticket'
    _rec_name = 'number'
    _order = 'number desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_stage_id(self):
        return self.env['helpdesk.ticket.stage'].search([], limit=1).id

    number = fields.Char(string='Ticket number', default="/",
                         readonly=True, copy=False)
    name = fields.Char(string='Title', required=True)
    description = fields.Text(required=True)
    user_id = fields.Many2one(
        'res.users',
        string='Assigned user',)

    @api.multi
    def name_get(self):
        res = []
        for obj in self:
            case = '[' + obj.number + '] '
            res.append((obj.id, case + obj.name))
        return res

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['helpdesk.ticket.stage'].search([])
        return stage_ids

    @api.multi
    def _get_name_from(self):
        for record in self:
            record.name_from = record.partner_id.name or \
                record.partner_email or ''

    stage_id = fields.Many2one(
        'helpdesk.ticket.stage',
        string='Stage',
        group_expand='_read_group_stage_ids',
        default=_get_default_stage_id,
        track_visibility='onchange',
    )
    partner_id = fields.Many2one('res.partner')
    partner_name = fields.Char()
    partner_email = fields.Char()
    email_origin = fields.Char('Email origin')
    last_stage_update = fields.Datetime(
        string='Last Stage Update',
        default=fields.Datetime.now(),
    )
    assigned_date = fields.Datetime(string='Assigned Date')
    closed_date = fields.Datetime(string='Closed Date')
    closed = fields.Boolean(related='stage_id.closed')
    unattended = fields.Boolean(related='stage_id.unattended')
    tag_ids = fields.Many2many('helpdesk.ticket.tag')
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        default=lambda self: self.env['res.company']._company_default_get(
            'helpdesk.ticket')
    )
    channel_id = fields.Many2one(
        'helpdesk.ticket.channel',
        string='Channel',
        help='Channel indicates where the source of a ticket'
             'comes from (it could be a phone call, an email...)',
    )
    category_id = fields.Many2one('helpdesk.ticket.category',
                                  string='Category')
    team_id = fields.Many2one('helpdesk.ticket.team')
    priority = fields.Selection(selection=[
        ('0', _('Low')),
        ('1', _('Medium')),
        ('2', _('High')),
        ('3', _('Very High')),
    ], string='Priority', default='1')
    attachment_ids = fields.One2many(
        'ir.attachment', 'res_id',
        domain=[('res_model', '=', 'website.support.ticket')],
        string="Media Attachments")

    def send_user_mail(self):
        self.env.ref('helpdesk.assignment_email_template'). \
            send_mail(self.id)

    def assign_to_me(self):
        self.write({'user_id': self.env.user.id})

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.partner_name = self.partner_id.name
            self.partner_email = self.partner_id.email

    # ---------------------------------------------------
    # CRUD
    # ---------------------------------------------------

    @api.model
    def create(self, vals):
        if vals.get('number', '/') == '/':
            vals['number'] = self.env['ir.sequence'].next_by_code(
                'helpdesk.ticket.sequence'
            ) or '/'
        res = super().create(vals)

        # Check if mail to the user has to be sent
        if vals.get('user_id') and res:
            res.send_user_mail()

        if vals.get('partner_id'):
            if (not vals.get('message_follower_ids', False)):
                vals['message_follower_ids'] = []
            vals['message_follower_ids'].append((4, vals['partner_id']))

        return res

    @api.multi
    def write(self, vals):
        for ticket in self:
            now = fields.Datetime.now()
            if vals.get('stage_id'):
                stage_obj = self.env['helpdesk.ticket.stage'].browse(
                    [vals['stage_id']])
                vals['last_stage_update'] = now
                if stage_obj.closed:
                    vals['closed_date'] = now
            if vals.get('user_id'):
                vals['assigned_date'] = now
        if vals.get('partner_id'):
            if (not vals.get('message_follower_ids', False)):
                vals['message_follower_ids'] = []
            vals['message_follower_ids'].append((4, vals['partner_id']))
        res = super(HelpdeskTicket, self).write(vals)

        # Check if mail to the user has to be sent
        for ticket in self:
            if vals.get('user_id'):
                ticket.send_user_mail()
        return res

    # ---------------------------------------------------
    # Mail gateway
    # ---------------------------------------------------

    @api.multi
    def _track_template(self, tracking):
        res = super(HelpdeskTicket, self)._track_template(tracking)
        test_task = self[0]
        changes, tracking_value = tracking[test_task.id]
        if "stage_id" in changes and test_task.stage_id.mail_template_id:
            res['stage_id'] = (test_task.stage_id.mail_template_id,
                               {"composition_mode": "mass_mail"})

        return res


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
