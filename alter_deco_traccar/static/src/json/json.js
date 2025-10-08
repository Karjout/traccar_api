/** @odoo-module */

import {_t} from '@web/core/l10n/translation';
import {Component, useRef, useEffect, useState} from '@odoo/owl';
import {registry} from '@web/core/registry';
import {standardFieldProps} from '@web/views/fields/standard_field_props';

function sortObjectKeysAlphabetically(obj) {
    if (typeof obj !== 'object' || obj === null) {
        return obj; // Return primitives and null as-is
    }

    if (Array.isArray(obj)) {
        // If it's an array, recursively sort each element
        return obj.map(sortObjectKeysAlphabetically);
    }

    // For objects, create a new object with sorted keys
    const sortedKeys = Object.keys(obj).sort();
    const sortedObj = {};

    for (const key of sortedKeys) {
        sortedObj[key] = sortObjectKeysAlphabetically(obj[key]);
    }

    return sortedObj;
}

export class FieldJSON extends Component {
    static template = 'web_field_json.JSON';
    static props = {
        ...standardFieldProps,
    }

    setup() {
        super.setup();
        this.viewerRef = useRef('json-viewer');
        this.state = useState({
            sort: false,
        });
        useEffect(() => {
            const jsonViewer = new JSONViewer();
            this.viewerRef.el.querySelector('.json-viewer')?.remove();
            this.viewerRef.el.appendChild(jsonViewer.getContainer());
            jsonViewer.showJSON(this.value, -1, -1);
        })
    }

    get value() {
        let value = this.props.record.data[this.props.name] || {};
        if (this.state.sort) {
            value = sortObjectKeysAlphabetically(value);
        }
        return value;
    }

}

export const fieldJSON = {
    component: FieldJSON,
    displayName: _t('JSON'),
    supportedTypes: ['html', 'text', 'jsonb'],
}

registry.category('fields').add('json', fieldJSON, {force: true});
