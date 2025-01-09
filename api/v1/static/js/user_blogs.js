const email = localStorage.getItem('email');
console.log(email);

function deleteBlog(blogId) {
    console.log('Deleting Blog with Blog Id', blogId)
    if (confirm('Are you sure you want to delete?')) {
        $.ajax({
            url: `/api/v1/${email}/blogs/${blogId}`,
            type: 'DELETE',
            success: function() {
                $(`#blogs .blog-card:has(a[href="/blogs/${blogId}"])`).remove();
            },
            error: function(xhr, status, error) {
                alert('Error deleting blog: ' + error);
            }
        });
    }
}
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
                        <button
                            class="delete-button"
                            onclick="deleteBlog('${blog.id}')"
                        >
                            Delete
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
