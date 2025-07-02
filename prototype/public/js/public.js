/********************** Modules **********************/
import { get_videos } from "./api.js";
import { insert_video_carousel, insert_video_section, insert_video_search, get_query_params, build_query_params } from "./utils.js";

/********************** API **********************/
const current_page = document.querySelector("[data-page]").getAttribute("data-page");
const sidebar_links = document.querySelectorAll("[data-sidebar-link]");

/*** Sidebar ***/
sidebar_links.forEach((link) => {
        if (link.getAttribute("data-sidebar-link") == current_page) link.classList.add("sidebar-link-container-active");
});

if (current_page == "home") {
    /*** Videos ***/
    let i = 0; // DEBUG
    const video_contents_container = document.querySelectorAll("[data-videos-content]");
    video_contents_container.forEach(async (container) => {
        const video_section = container.getAttribute("data-videos-content");
        
        const params = {
            "section": video_section,
            "_limit": 10,
            "_start": 10 * i, // DEBUG
        };
        i++; // DEBUG

        container.innerHTML = "";
        
        const videos = await get_videos(params);
        insert_video_carousel(videos, container);
    });
} else if (current_page == "trending" || current_page == "explore") {
    /*** Videos ***/
    const content_container = document.getElementById("content");
    const video_contents_container = document.getElementById("content-section-videos");
    const video_section = content_container.getAttribute("data-page");
    
    const params = {
        "section": video_section,
        "_limit": 25,
    };

    video_contents_container.innerHTML = "";
        
    const videos = await get_videos(params);
    insert_video_section(videos, video_contents_container);
} else if (current_page == "search") {
    /*** Videos ***/
    const content_search_section = document.getElementById("content-search-section");
    const title_search_result_text = document.getElementById("title-search-result-text");
    
    const content_container = document.getElementById("content");
    const video_section = content_container.getAttribute("data-page");
    
    const url_params = get_query_params();
    title_search_result_text.textContent = url_params.query;

    const params = {
        "section": video_section,
        "query": url_params.query,
        "_limit": 25,
        "_start": 0,
    };
    
    content_search_section.innerHTML = "";
    const videos = await get_videos(params);
    insert_video_search(videos, content_search_section);
}

/********************** Media Queries **********************/
window.addEventListener("resize", () => {
    const window_size = window.innerWidth;

    /*** Sidebar controller ***/
    const icon = document.getElementById("sidebar-toggle-icon");
    const sidebar = document.getElementById("sidebar");
    const content = document.getElementById("content");

    function reset_sidebar() {
        if (sidebar.classList.contains("sidebar-hide")) sidebar.classList.remove("sidebar-hide");
        if (content.classList.contains("content-shide")) content.classList.remove("content-shide");
    }

    /*** Actions ***/
    if (window_size <= 600) {

    } else if (window_size <= 768) {

    } else if (window_size <= 992) {

    } else if (window_size <= 1200) {
        /* Sidebar controller */
        if (icon.textContent == "notes") icon.textContent = "menu";
        reset_sidebar();
    } else {
        /* Sidebar controller */
        if (icon.textContent == "menu") icon.textContent = "notes";
        reset_sidebar();
    }
});

/********************** Search **********************/
const search_btn = document.getElementById("search-btn");
const search_backdrop = document.getElementById("search-backdrop");
const search_container = document.getElementById("search-results");
const search_result_input = document.getElementById("search-result-input");
const search_result_links_container = document.getElementById("search-results");

document.getElementById("search-result-input")?.addEventListener("input", (e) => {
    if (e.target.value == "") search_container.classList.add("hidden");
    else {
        if (search_container.classList.contains("hidden")) search_container.classList.remove("hidden");

        const link_input = document.getElementById("search-result-link-input");
        link_input.textContent = e.target.value;
    }
});

document.getElementById("search-result-input")?.addEventListener("focusout", (e) => {
    setTimeout(() => {
        search_container.classList.add("hidden");
    }, 150);
});

search_btn?.addEventListener("click", () => {
    search_backdrop.classList.toggle("hidden");
    search_result_input.classList.toggle("show");
    search_result_input.classList.toggle("scale-in-center");
});

search_backdrop?.addEventListener("click", () => {
    search_result_input.classList.remove("scale-in-center");
    search_result_input.classList.toggle("scale-out-center");

    setTimeout(() => {
        search_backdrop.classList.toggle("hidden");
        search_result_input.classList.toggle("show");
        search_result_input.classList.remove("scale-out-center");
    }, 500);
});

search_result_links_container.addEventListener("click", (e) => {
    if (e.target.matches(".search-result-text")) {
        const params = {"query": e.target.textContent};
        const query = build_query_params(params);
        window.location.href = "search.html" + query // LINK
    }
});

// <a href="#search-result" class="search-result-text">Lorem ipsum dolor</a> TEMPLATE

/********************** Sidebar controller **********************/
document.getElementById("sidebar-button")?.addEventListener("click", () => {
    const icon = document.getElementById("sidebar-toggle-icon");
    const sidebar = document.getElementById("sidebar");
    const content = document.getElementById("content");

    sidebar.classList.toggle("sidebar-hide");
    content.classList.toggle("content-shide");

    if (icon.textContent == "notes") icon.textContent = "menu";
    else icon.textContent = "notes";
});

/********************** Sign in and Sign up controllers **********************/
const navbar_actions = document.getElementById("navbar-actions");
const sidebar_actions = document.getElementById("sidebar-actions");

const modal_container = document.getElementById("modal");
const modal_close = document.getElementById("modal-close");
const modal_actions = document.getElementById("modal-actions");
const modal_content = document.getElementById("modal-content");
const modal_title = document.getElementById("modal-title-text");
const modal_backdrop = document.getElementById("modal-backdrop");

const sign_in_template = `
<div class="modal-input-container">
    <label for="email" class="modal-label">Email</label>
    <input type="email" id="email" class="modal-input" name="email" placeholder="Email address" required>
</div>
<div class="modal-input-container">
    <label for="password" class="modal-label">Password</label>
    <input type="password" id="password" class="modal-input" name="password" placeholder="************" required>
</div>
<button class="btn modal-input-button">Sign in</button>
`;

const sign_up_template = `
<div class="modal-input-container">
    <label for="username" class="modal-label">Username</label>
    <input type="text" id="username" class="modal-input" name="username" placeholder="Username" required>
</div>
<div class="modal-input-container">
    <label for="email" class="modal-label">Email</label>
    <input type="email" id="email" class="modal-input" name="email" placeholder="Email address" required>
</div>
<div class="modal-input-container">
    <label for="password" class="modal-label">Password</label>
    <input type="password" id="password" class="modal-input" name="password" placeholder="************" required>
</div>
<div class="modal-input-container">
    <label for="confirm_password" class="modal-label">Confirm password</label>
    <input type="password" id="confirm_password" class="modal-input" name="confirm_password" placeholder="************" required>
</div>
<div class="modal-input-container">
    <label for="birth" class="modal-label">Date of birth</label>
    <input type="text" id="birth" class="modal-input" name="birth" placeholder="mm/dd/yyyy" required>
</div>
<button class="btn modal-input-button">Sign up</button>
`;

function user_modal(type) {
    // Content
    if (type == "signin") {
        modal_actions.innerHTML = sign_in_template;
        modal_title.textContent = "Sign in";
        modal_actions.action = "#signin"
    } else if (type == "signup") {
        modal_actions.innerHTML = sign_up_template;
        modal_title.textContent = "Sign up";
        modal_actions.action = "#signup"
    }

    // Animation
    modal_container.classList.toggle("hidden");
    modal_content.classList.add("slide-in-top")
    modal_content.classList.remove("slide-out-top");
}

navbar_actions?.addEventListener("click", (e) => {
    const btn = e.target.closest(".modal-btn");

    if (btn) {
        const modal_type = btn.getAttribute("data-modal");
        if (modal_type == "signin") user_modal(modal_type);
        else if (modal_type == "signup") user_modal(modal_type);
    }

});

sidebar_actions?.addEventListener("click", (e) => {
    const btn = e.target.closest(".modal-btn");

    if (btn) {
        const modal_type = btn.getAttribute("data-modal");
        if (modal_type == "signin") user_modal(modal_type);
        else if (modal_type == "signup") user_modal(modal_type);
    }

});

modal_close?.addEventListener("click", () => {
    modal_content.classList.remove("slide-in-top")
    modal_content.classList.add("slide-out-top");
    setTimeout(() => {
        modal_container.classList.toggle("hidden");
    }, 500);
});

modal_backdrop?.addEventListener("click", () => {
    modal_content.classList.remove("slide-in-top")
    modal_content.classList.add("slide-out-top");
    setTimeout(() => {
        modal_container.classList.toggle("hidden");
    }, 500);
});