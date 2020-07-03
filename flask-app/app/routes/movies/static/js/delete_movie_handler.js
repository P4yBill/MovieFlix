var deleteMovieForm = $("#delete-movie-form");
deleteMovieForm.find("#delete-movie-button").on("click", deleteMovieHandler);
console.log(deleteMovieForm.find("#delete-movie-button"));

function deleteMovieHandler() {
    var movieTitle = deleteMovieForm.find("#input-title-delete").val();
    var data = {
        title: movieTitle
    };
    if (checkParams(data)) {
        movieDeleteRequest(data)
    } else {
        Swal.fire('Error', 'Please give a valid title.', 'error')
    }
}

function movieDeleteRequest(data) {
    $.ajax({
        url: 'api/v1/movies',
        type: 'DELETE',
        dataType: 'json',
        contentType: 'application/json',
        timeout: 5000,
        data: JSON.stringify(data),
        success: function (data, status, xhr) {
            if (xhr.status === 200) {
                location.reload();
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

function checkParams(data) {
    if (data.title && data.title !== "") {
        return true;
    } else {
        return false;
    }
}

