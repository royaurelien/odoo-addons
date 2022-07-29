/** @odoo-module **/

import { registry } from "@web/core/registry";

const { tags } = owl;

const debugRegistry = registry.category("debug");


function viewReports({ action, env }) {
    if (!action.res_model) {
        return null;
    }
    const description = env._t("View Reports");
    return {
        type: "item",
        description,
        callback: async () => {
            // const modelId = (
            //     await env.services.orm.search("ir.model", [["model", "=", action.res_model]], {
            //         limit: 1,
            //     })
            // )[0];
            env.services.action.doAction({
                res_model: "open.report.wizard",
                name: description,
                views: [
                    [false, "form"],
                ],
                type: "ir.actions.act_window",
                view_mode: "form",
                target: "new",
                flags: { action_buttons: true, headless: true },                
                context: {
                    default_res_model: action.res_model,
                },
            });
        },
        sequence: 301,
    };
}

export function analyzeView({ accessRights, component, env }) {
    if (!accessRights.canEditView) {
        return null;
    }
    let { viewId, viewType: type } = component.env.config || {}; // fallback is there for legacy
    if ("viewInfo" in component.props) {
        // legacy
        viewId = component.props.viewInfo.view_id;
        type = component.props.viewInfo.type;
        type = type === "tree" ? "list" : type;
    }
    const displayName = type[0].toUpperCase() + type.slice(1);
    const description = env._t("Analyze View: ") + displayName;
    return {
        type: "item",
        description,
        callback: () => {
            // editModelDebug(env, description, "ir.ui.view", viewId);
            env.services.action.doAction({
                res_model: "analyze.view.wizard",
                name: description,
                views: [
                    [false, "form"],
                ],
                type: "ir.actions.act_window",
                view_mode: "form",
                target: "new",
                flags: { action_buttons: true, headless: true },                
                context: {
                    default_view_id: viewId,
                },
            });            
        },
        sequence: 350,
    };
}

debugRegistry
    .category("view")
    .add("viewReports", viewReports)
    .add("analyzeView", analyzeView)