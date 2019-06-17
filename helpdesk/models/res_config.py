from odoo import fields, models, api


class SaleConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Getter / Setter Section
    @api.model
    def get_values(self):
        res = super(SaleConfigSettings, self).get_values()
        ir_config_sudo = self.env['ir.config_parameter'].sudo()
        number_of_minutes = ir_config_sudo.get_param(
            'crm_helpdesk_improvement_number_of_minutes')
        number_of_tickets = ir_config_sudo.get_param(
            'crm_helpdesk_improvement_number_of_tickets')
        res.update(
            crm_helpdesk_improvement_number_of_minutes=int(
                number_of_minutes),
            crm_helpdesk_improvement_number_of_tickets=int(
                number_of_tickets
            )
        )
        return res

    @api.multi
    def set_values(self):
        super(SaleConfigSettings, self).set_values()
        ir_config_sudo = self.env['ir.config_parameter'].sudo()
        if self.crm_helpdesk_improvement_number_of_minutes:
            ir_config_sudo.set_param(
                'crm_helpdesk_improvement_number_of_minutes',
                self.crm_helpdesk_improvement_number_of_minutes
            )
        if self.crm_helpdesk_improvement_number_of_tickets:
            ir_config_sudo.set_param(
                'crm_helpdesk_improvement_number_of_tickets',
                self.crm_helpdesk_improvement_number_of_tickets
            )

    crm_helpdesk_improvement_number_of_tickets = fields.Integer(
        string='Number of tickets.')

    crm_helpdesk_improvement_number_of_minutes = fields.Integer(
        string='Number of minutes.')
