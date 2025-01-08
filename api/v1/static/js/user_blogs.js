const email = localStorage.getItem('email');
console.log(email);
        
$(document).ready(function() {
    $.ajax({
        url: `/api/v1/${email}/blogs`,
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        success: function(blogs) {
            $('#loading').hide();
                    
            if (blogs.length === 0) {
                $('#blogs').html('<p>No blogs found</p>');
                return;
            }

            blogs.forEach(blog => {
                $('#blogs').append(`
                    <div class="blog-card">
                        <div class="blog-title">
                            <a href=/blogs/${blog.id}>${blog.title}</a>
                        </div>
                        <div class="blog-meta">
                            Posted on: ${blog.formatted_date}
                        </div>
                        <button 
                            class="edit-button" 
                            onclick="window.location.href='/blogs/${blog.id}/edit'"
                        >
                            Edit
                        </button>
                    </div>
                `);
            });
        },
        error: function(xhr) {
            $('#loading').hide();
            $('#error').show().text('Error loading blogs: ' + 
                xhr.responseJSON?.message || 'Unknown error');
        }
    });
});
