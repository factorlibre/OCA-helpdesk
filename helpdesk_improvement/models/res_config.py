from odoo import fields, models, api


class HelpdeskConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Getter / Setter Section
    @api.model
    def get_values(self):
        res = super().get_values()
        ir_config_sudo = self.env['ir.config_parameter'].sudo()
        number_of_minutes = ir_config_sudo.get_param(
            'helpdesk_improvement_number_of_minutes')
        number_of_tickets = ir_config_sudo.get_param(
            'helpdesk_improvement_number_of_tickets')
        res.update(
            helpdesk_improvement_number_of_minutes=int(
                number_of_minutes),
            helpdesk_improvement_number_of_tickets=int(
                number_of_tickets
            )
        )
        return res

    @api.multi
    def set_values(self):
        super().set_values()
        ir_config_sudo = self.env['ir.config_parameter'].sudo()
        if self.helpdesk_improvement_number_of_minutes:
            ir_config_sudo.set_param(
                'helpdesk_improvement_number_of_minutes',
                self.helpdesk_improvement_number_of_minutes
            )
        if self.helpdesk_improvement_number_of_tickets:
            ir_config_sudo.set_param(
                'helpdesk_improvement_number_of_tickets',
                self.helpdesk_improvement_number_of_tickets
            )

    helpdesk_improvement_number_of_tickets = fields.Integer(
        string='Number of tickets.')

    helpdesk_improvement_number_of_minutes = fields.Integer(
        string='Number of minutes.')
