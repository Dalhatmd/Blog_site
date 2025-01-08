$(document).ready(function() {
    // Get blog ID from URL
    const blogId = window.location.pathname.split('/')[2];
    const email = localStorage.getItem('email');
    
    // Load blog content
    $.ajax({
        url: `/api/v1/${email}/blogs/${blogId}`,
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        success: function(blog) {
            $('#loading').hide();
            $('#editBlogForm').show();
            
            // Populate form with blog data
            $('#title').val(blog.title);
            $('#content').val(blog.content);
        },
        error: function(xhr) {
            $('#loading').hide();
            $('#error').show().text('Error loading blog: ' + 
                xhr.responseJSON?.message || 'Unknown error');
        }
    });
    
    // Handle form submission
    $('#editBlogForm').on('submit', function(e) {
        e.preventDefault();
        
        const updatedBlog = {
            title: $('#title').val(),
            content: $('#content').val()
        };
        
        $.ajax({
            url: `/api/v1/${email}/blogs/${blogId}`,
            method: 'PUT',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
                'Content-Type': 'application/json'
            },
            data: JSON.stringify(updatedBlog),
            success: function() {
                // Redirect back to blogs list on success
                window.location.href = '/home';
            },
            error: function(xhr) {
                $('#error').show().text('Error saving blog: ' + 
                    xhr.responseJSON?.message || 'Unknown error');
            }
        });
    });
});
