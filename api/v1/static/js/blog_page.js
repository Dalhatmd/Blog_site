$(document).ready(function () {
    // Bind a keypress event to the "Add Comment" textarea
    $('#comment').on('keypress', function (e) {
        if (e.which === 13 && !e.shiftKey) { // Submit on Enter key without Shift
            e.preventDefault();

            const token = localStorage.getItem('token');
            if (!token) {
                alert('You must be logged in to comment');
                window.location.href = '/login';
                return;
            }
            console.log(token);

            const blogId = window.location.pathname.split('/')[2];
            console.log('Blog ID:', blogId);

            const commentContent = $(this).val().trim();
            if (commentContent === '') {
                alert('Comment cannot be empty!');
                return;
            }
            console.log(commentContent);

            // Make an AJAX POST request to add the comment
            $.ajax({
                url: `/api/v1/blogs/${blogId}/comments`,
                method: 'POST',
                contentType: 'application/json',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                data: JSON.stringify({ content: commentContent }),
                success: function (response) {
                    // Append the new comment to the comments section
                    $('.comments').append(`
                        <div class="comment">
                            <p>${response.content}</p>
                            <small>At: ${response.created_at}</small>
                        </div>
                    `);
                    $('#comment').val(''); // Clear the textarea
                },
                error: function (xhr, status, error) {
                    console.error('AJAX Error:', xhr, status, error); // Log full error
                    alert(`Error: ${xhr.responseText || 'Failed to add comment.'}`);
                }
            });
        }
    });
});
