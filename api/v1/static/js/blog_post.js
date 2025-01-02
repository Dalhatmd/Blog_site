$(document).ready(function() {
    $('#blogForm').submit(function(e) {
        e.preventDefault();

        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = '/login';
            return;
        }

        $.ajax({
            url: '/api/v1/blogs',
            method: 'POST',
            contentType: 'application/json',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            data: JSON.stringify({
                title: $('#title').val(),
                content: $('#content').val()
            }),
            success: function(response) {
                window.location.href = '/home';
            },
            error: function(xhr) {
                $('#error').text(xhr.responseJSON.message);
            }
        });
    });
});
