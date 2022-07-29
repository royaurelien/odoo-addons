/** @odoo-module **/

import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";

function odooDevelopper(env) {
    const newURL = "https://www.odoo.com/documentation/15.0";
    return {
        type: "item",
        id: "odoo_developper",
        description: env._t("Developper"),
        href: newURL,
        callback: () => {
            browser.open(newURL, "_blank");
        },
        sequence: 10,
    };
}

registry
    .category("user_menuitems")
    .add("odoo_developper", odooDevelopper)
