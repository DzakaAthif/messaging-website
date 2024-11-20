//window.alert("JS TEST!")
const h_link = document.querySelector('#home-link');
const a_link = document.querySelector('#about-link');

const p_link = document.querySelector('#profile-link');
const c_link = document.querySelector('#chat-link');
const t_link = document.querySelector('#test-link');
const l_link = document.querySelector('#logout-link');

const r_link = document.querySelector('#register-link');
const login_link = document.querySelector('#login-link');

const is_hidden = localStorage.getItem("hidden");
console.log("inside scriptheadjs");
if (is_hidden !== null) {
    if (is_hidden === "false") {
        p_link.classList.remove('is-hidden');
        c_link.classList.remove('is-hidden');
        t_link.classList.remove('is-hidden');
        l_link.classList.remove('is-hidden');
        
        r_link.classList.add('is-hidden');
        login_link.classList.add('is-hidden');
    } else {
        p_link.classList.add('is-hidden');
        c_link.classList.add('is-hidden');
        t_link.classList.add('is-hidden');
        l_link.classList.add('is-hidden');
    }
}

//modal
const modal_bg = document.querySelector(".modal-background");
const modal = document.querySelector(".modal");

l_link.addEventListener('click', () => {
    modal.classList.add("is-active");
});

modal_bg.addEventListener('click', () => {
    modal.classList.remove("is-active");
});

//yes no button in the modal
const yes_button = document.querySelector("#yes-button");
const no_button = document.querySelector("#no-button");

yes_button.addEventListener('click', () => {
    window.location.replace("/logout");
});

no_button.addEventListener('click', () => {
    modal.classList.remove("is-active");
});