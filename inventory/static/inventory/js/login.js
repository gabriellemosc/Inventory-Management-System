document.addEventListener("DOMContentLoaded", () => {
    const togglePassword = document.querySelector('.toggle-password');
    const passwordField = document.querySelector('#id_password');

    togglePassword.addEventListener('click', () =>{
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);
    });
});