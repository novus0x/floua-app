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
})

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

const sign_in_dom = `
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

const sign_up_dom = `
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
        modal_actions.innerHTML = sign_in_dom;
        modal_title.textContent = "Sign in";
        modal_actions.action = "#signin"
    } else if (type == "signup") {
        modal_actions.innerHTML = sign_up_dom;
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
        console.log("ok");
        const modal_type = btn.getAttribute("data-modal");
        if (modal_type == "signin") user_modal(modal_type);
        else if (modal_type == "signup") user_modal(modal_type);
    }

})

sidebar_actions?.addEventListener("click", (e) => {
    const btn = e.target.closest(".modal-btn");

    if (btn) {
        console.log("ok");
        const modal_type = btn.getAttribute("data-modal");
        if (modal_type == "signin") user_modal(modal_type);
        else if (modal_type == "signup") user_modal(modal_type);
    }

})

modal_close?.addEventListener("click", () => {
    modal_content.classList.remove("slide-in-top")
    modal_content.classList.add("slide-out-top");
    setTimeout(() => {
        modal_container.classList.toggle("hidden");
    }, 500);
})

modal_backdrop?.addEventListener("click", () => {
    modal_content.classList.remove("slide-in-top")
    modal_content.classList.add("slide-out-top");
    setTimeout(() => {
        modal_container.classList.toggle("hidden");
    }, 500);
})