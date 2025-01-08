$(document).ready(function() {
    let userId;
    $.ajax({
        url: '/api/v1/me',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        success: function(data) {
            $('#loading').hide();
            $('#profile').show();
            
           // const userId = data.id || data.user_id || data;
            //localStorage.setItem('userId', userId);
            //console.log("Stored userId:", userId);
            console.log('Input data', data);

            const email = data.Email;
            localStorage.setItem('email', email);
            console.log('Stored email', email);
            
            Object.entries(data).forEach(([key, value]) => {
                $('#profile').append(`
                    <div class="field">
                        <span class="field-label">${key.replace('_', ' ')}</span>
                        <span>${value}</span>
                    </div>
                `);
            });
        },
        error: function(xhr) {
            $('#loading').hide();
            $('#error').show().text('Error loading profile: ' + xhr.responseJSON?.message || 'Unknown error');
        }
    });
});
