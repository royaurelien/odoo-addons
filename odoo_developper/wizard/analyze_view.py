# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

import ast
from odoo.osv import expression

import logging

_logger = logging.getLogger(__name__)


class IrModuleModule(models.Model):
    _inherit = 'ir.module.module'

    def button_immediate_upgrade2(self):
        _logger.error(self.env.context.get('active_model'))
        _logger.error(self.env.context.get('active_ids'))
        res = self.button_immediate_upgrade()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            'params': {'menu_id': 341},
        }


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    def _get_addons_from(self):
        return self.mapped('xml_id')[0].split('.')[0]

    def _analyze(self, top=False, items=[]):        
        if top and self.inherit_id:
            items = self.inherit_id._analyze()

        for child in self.inherit_children_ids:
            items += child._analyze()

        items.append(self._get_addons_from())
            

        return items

class AnalyzeView(models.TransientModel):
    _name = 'analyze.view.wizard'
    _description = 'Analyze View'


    view_id = fields.Many2one('ir.ui.view')
    addons = fields.Char(compute='_compute_children')
    addons_count = fields.Integer(compute='_compute_children')
    module_ids = fields.One2many(compute='_compute_children', comodel_name='ir.module.module')

    @api.depends('view_id')
    def _compute_children(self):
        for record in self:
            record.module_ids = False

            addons = list(set(record.view_id._analyze(True)))
            record.addons = ", ".join(addons)
            record.addons_count = len(addons)

            module_ids = self.env['ir.module.module'].sudo().search([('name', 'in', addons)])
            if module_ids:
                record.module_ids = module_ids
            # _logger.error(module_ids)
            
    




    def action_open(self):
        if not self.view_id:
            return False

        action = {
            'type': 'ir.actions.act_url',
            # 'url': "/report/{}/{}/{}".format(self.report_type, self.report_id.report_name, self.res_id),
            'target': 'new',
        }
        return action


    def action_view(self):
        if not self.view_id:
            return False

        action = {
            'res_model': 'ir.actions.report',
            # 'res_id': self.report_id.id,
            # 'name': self.rec_name,
            'type': "ir.actions.act_window",
            'views': [[False, "form"]],
            'view_mode': "form",
        }
        return action        