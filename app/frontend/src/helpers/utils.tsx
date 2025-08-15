'use client';

/********************** Modules **********************/
import { settings } from "./settings";

/********************** Create params **********************/
export function create_params(obj: Record<string, any>): string {
    const params = new URLSearchParams();

    Object.entries(obj).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
            if (Array.isArray(value)) {
                value.forEach(v => params.append(key, v));
            } else {
                params.append(key, value.toString());
            }
        }
    });

    return `?${params.toString()}`;
}

/********************** Set Cookie **********************/
export function set_cookie(cookie_value: string) {
    document.cookie = `${settings.token_name}=${cookie_value}; path=/`;
}

/********************** Get Cookie **********************/
export function get_cookie() {
    const value = `; ${document.cookie}`;
    const arr = value.split(`; ${settings.token_name}=`);
    if (arr.length === 2) return arr.pop()?.split(';').shift();
    return null;
}

/********************** Delete Cookie **********************/
export function delete_cookie() {
    document.cookie = `${settings.token_name}=; Max-Age=0; path=/`;
}
