$(document).ready(function() {
    // Toggle between forms
    $('.toggle-form').click(function(e) {
        e.preventDefault();
        $('#loginForm, #registerForm').toggle();
        $('#error').text('');
    });

    // Login form submission
    $('#loginFormSubmit').submit(function(e) {
        e.preventDefault();
        $.ajax({
            url: '/api/v1/auth/login',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                email: $('#loginEmail').val(),
                password: $('#loginPassword').val()
            }),
            success: function(response) {
                localStorage.setItem('token', response.token);
                window.location.href = '/dashboard.html';
            },
            error: function(xhr) {
                $('#error').text(xhr.responseJSON.message);
            }
        });
    });

    // Register form submission
    $('#registerFormSubmit').submit(function(e) {
        e.preventDefault();
        $.ajax({
            url: '/api/v1/auth/register',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                email: $('#registerEmail').val(),
                username: $('#registerUsername').val(),
                password: $('#registerPassword').val()
            }),
            success: function(response) {
                localStorage.setItem('token', response.token);
                window.location.href = '../templates/dashboard.html';
            },
            error: function(xhr) {
                $('#error').text(xhr.responseJSON.message);
            }
        });
    });
});
