'use client';

/********************** Set Cookie **********************/
export function set_cookie (cookie_value: string) {
    document.cookie = `Authorization=${cookie_value}; path=/`;
}

/********************** Get Cookie **********************/

/********************** Delete Cookie **********************/
