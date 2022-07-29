# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

import ast
from odoo.osv import expression

import logging

_logger = logging.getLogger(__name__)



class OpenReport(models.TransientModel):
    _name = 'open.report.wizard'
    _description = 'Open Report'


    report_id = fields.Many2one('ir.actions.report', domain=[('report_type', '!=', 'qweb-text')])
    report_type = fields.Selection([('html', 'HTML'), ('pdf', 'PDF')], default='pdf')
    report_name = fields.Char(related='report_id.report_name')
    res_model = fields.Char("Res Model")
    model_id = fields.Many2one('ir.model', compute='_compute_model')
    res_id = fields.Integer(string="Res ID")
    rec_name = fields.Char(string="Record", compute='_compute_name')


    @api.onchange('res_model')
    def onchange_model(self):
        if self.res_model:
            self.res_id = self.env[self.res_model].search([], limit=1).id or False
            

    @api.onchange('report_id')
    def onchange_report(self):
        if self.report_id:
            self.report_type = self.report_id.report_type.split('-')[-1] or False


    @api.depends('res_model')
    def _compute_model(self):
        for record in self:
            if not record.res_model:
                record.model_id = False
                continue

            record.model_id = self.env['ir.model'].search([('model', '=', record.res_model)], limit=1).id or False


    @api.depends('res_model', 'res_id')
    def _compute_name(self):
        for record in self:
            if record.res_model and record.res_id:
                try:
                    res = self.env[record.res_model].browse(record.res_id)
                    record.rec_name = res.name if res else ""
                except:
                    record.rec_name = ""
            else:
                record.rec_name = ""


    def action_open(self):
        if not self.report_id:
            return False

        action = {
            'type': 'ir.actions.act_url',
            'url': "/report/{}/{}/{}".format(self.report_type, self.report_id.report_name, self.res_id),
            'target': 'new',
        }
        return action


    def action_view(self):
        if not self.report_id:
            return False

        action = {
            'res_model': 'ir.actions.report',
            'res_id': self.report_id.id,
            'name': self.rec_name,
            'type': "ir.actions.act_window",
            'views': [[False, "form"]],
            'view_mode': "form",
        }
        return action        