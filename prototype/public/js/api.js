/********************** Settings **********************/
const BASE_URL = "https://jsonplaceholder.typicode.com"; // Simulating API

/********************** Utilities **********************/
import { get_cookie, active_session, build_query_params } from "./utils.js";


/********************** GET videos **********************/
export async function get_videos(parameters) {
    try {
        let params = {};

        if (active_session()) params = {...parameters, token: active_session()};
        else params = {...parameters};

        const query = build_query_params(params); // Search query
        const response = await fetch(`${BASE_URL}/posts${query}`);

        if (!response.ok) throw new Error(`API error: ${response.status}`);
        console.log(`[DEBUG] URL --> ${BASE_URL}/posts${query}`) // DEBUG

        const data = await response.json();
        return data;
    } catch (err) {
        console.log(err);
    }
}