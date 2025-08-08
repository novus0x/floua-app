'use client';

/********************** Modules **********************/
import { settings } from "./settings";

/********************** GET Request **********************/
export async function get_data(
    endpoint: string, 
    headers: Record<string, string>,
    notify?: (message: string, type: string) => void
) {
    // Variables
    let i, details, values;

    // Request
    const res = await fetch(`${settings.api_url}${endpoint}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            ...headers,
        },
        credentials: "include",
    })

    // Get data
    const data = await res.json();

    // Check errors
    if (res.status == 400) {
        details = data.details;

        // Multiple errors
        if (details) {
            for (i = 0; i < details.length; i++) if (notify) notify(details[i].message, 'alert');
            return null;
        }

        // Unique error - General message
        if (notify) notify(data.message, 'alert');
        return null;
    }

    values = data?.data ?? {};
    return values;
}


/********************** POST Request **********************/
export async function send_data(
    endpoint: string, 
    headers: Record<string, string>, 
    body: Record<string, string>,
    notify: (message: string, type: string) => void
) {
    // Variables
    let i, details, values;

    // Request
    const res = await fetch(`${settings.api_url}${endpoint}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...headers,
        },
        body: JSON.stringify(body),
        credentials: "include",
    })

    // Get data
    console.log(res);
    const data = await res.json();
    console.log(data);

    // Check errors
    if (res.status == 400) {
        details = data.details;

        // Multiple errors
        if (details) {
            for (i = 0; i < details.length; i++) if (notify) notify(details[i].message, 'alert');
            return null;
        }

        // Unique error - General message
        if (notify) notify(data.message, 'alert');
        return null;
    }

    values = data?.data ?? {};

    // Success
    if(notify) notify(data.message, 'success');
    return values;
};
