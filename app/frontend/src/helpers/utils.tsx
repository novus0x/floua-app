'use client';

/********************** Modules **********************/
import { settings } from "./settings";
import { routes } from "./routes";

interface User {
    role: string
}

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

/********************** Creator role **********************/
export function creators_only(user: User, notify?: (message: string, type: string) => void, message?: string) {
    if (!user) return window.location.href = routes.public.home;
    else if (user.role != "creator") {
        if (notify) notify(`${message}`, "info")
        setTimeout(() => {
            return window.location.href = routes.public.home;
        }, 2500)
    }

}

/********************** Set Cookie **********************/
export function set_cookie(cookie_name: string, cookie_value: string) {
    document.cookie = `${cookie_name}=${cookie_value}; path=/`;
}

/********************** Get Cookie **********************/
export function get_cookie(cookie_name: string) {
    const value = `; ${document.cookie}`;
    const arr = value.split(`; ${cookie_name}=`);
    if (arr.length === 2) return arr.pop()?.split(';').shift();
    return null;
}

/********************** Delete Cookie **********************/
export function delete_cookie() {
    document.cookie = `${settings.token_name}=; Max-Age=0; path=/`;
}
