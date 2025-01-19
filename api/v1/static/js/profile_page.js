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
            
            const email = data.Email;
            localStorage.setItem('email', email);
            
            // Add profile picture section at the top
            $('#profile').append('<div id="profile-picture-container"></div>');
            
            $.ajax({
                url: '/api/v1/get_profile_picture',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem('token')
                },
                success: function(picData) {
                    console.log('Profile picture data:', picData); // Debug log
                    if (picData.profile_pic) { 
                        var mainPath = picData.profile_pic;

                        imgPath = mainPath.substring(mainPath.indexOf('static'));
                        console.log('Image path:', imgPath);
                        $('#profile-picture-container').html(`
                            <div class="field">
                                <span class="field-label">Profile Picture</span>
                                <img src="${imgPath}" alt="Profile Picture" style="max-width: 200px;" onerror="this.src='/static/default.jpeg'">
                            </div>
                        `);
                    } else {
                        $('#profile-picture-container').html(`
                            <div class="field">
                                <span class="field-label">Profile Picture</span>
                                <img src="api/v1/static/default.jpeg" alt="Default Profile Picture" style="max-width: 200px;">
                            </div>
                        `);
                    }
                },
                error: function(xhr) {
                    console.log('Profile picture error:', xhr);
                    $('#profile-picture-container').html(`
                        <div class="field">
                            <span class="field-label">Profile Picture</span>
                            <img src="/static/default.jpeg" alt="Default Profile Picture" style="max-width: 200px;">
                        </div>
                    `);
                }
            });

            Object.entries(data).forEach(([key, value]) => {
                if (key !== 'profile_pic') {  // Changed from Profile_picture to match backend
                    $('#profile').append(`
                        <div class="field">
                            <span class="field-label">${key.replace('_', ' ')}</span>
                            <span>${value}</span>
                        </div>
                    `);
                }
            });
        },
        error: function(xhr) {
            $('#loading').hide();
            $('#error').show().text('Error loading profile: ' + xhr.responseJSON?.message || 'Unknown error');
        }
    });
});
