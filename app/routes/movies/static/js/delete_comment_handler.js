$(".comment-delete-img").click(deleteCommentHandler);

function deleteCommentHandler() {
    var img = $(this);
    var userId = img.data('user');
    var movieId = window.location.pathname.split("/").pop();
    var options = {
        payload: {
            user_id: userId,
        },
        movie_id: movieId,
        $el: img.closest(".comment")
    }

    commentDeleteRequest(options);
}


function commentDeleteRequest(options) {

    $.ajax({
        url: '/api/v1/movies/' + options.movie_id + '/comments',
        type: 'DELETE',
        dataType: 'json',
        contentType: 'application/json',
        timeout: 5000,
        data: JSON.stringify(options.payload),
        success: function (data, status, xhr) {
            if (xhr.status === 200) {
                options.$el.remove();
                Swal.fire('Comment Deleted', "Deleted Succ", 'success');

            } else if (xhr.status === 500) {
                var error = "There was an error";
                if (data.error) {
                    error = data.error
                }
                Swal.fire('Error', error, 'error')
            }
        },
        fail: function () {
            Swal.fire('Error', "There was an error.", 'error')
        },

    });
}

