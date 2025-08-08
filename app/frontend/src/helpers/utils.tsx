'use client';

/********************** Modules **********************/
import { settings } from "./settings";

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
