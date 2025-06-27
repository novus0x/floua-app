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

document.getElementById("signin-button")?.addEventListener("click", () => {    
    // Content
    modal_actions.innerHTML = sign_in_dom;
    modal_title.textContent = "Sign in";
    modal_actions.action = "#signin"

    // Animation
    modal_container.classList.toggle("hidden");
    modal_content.classList.add("slide-in-top")
    modal_content.classList.remove("slide-out-top");
});

document.getElementById("signup-button")?.addEventListener("click", () => {
    // Content
    modal_actions.innerHTML = sign_up_dom;
    modal_title.textContent = "Sign up";
    modal_actions.action = "#signup"

    // Animation
    modal_container.classList.toggle("hidden");
    modal_content.classList.add("slide-in-top")
    modal_content.classList.remove("slide-out-top");
});

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