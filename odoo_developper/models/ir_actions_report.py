
# from email.policy import default
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)



class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'
        

    def action_open_report(self):
        res_id = self.env[self.model].search([],limit=1).id or 1
        action = {
            'type': 'ir.actions.act_url',
            'url': "/report/{}/{}/{}".format(self.report_type.split('-')[-1], self.report_name, res_id),
            'target': 'new',
        }
        return action        

            