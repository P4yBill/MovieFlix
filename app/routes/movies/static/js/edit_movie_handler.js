var movieForm = $("#edit-movie-form");
movieForm.find("#edit-movie-button").click(deleteMovieHandler);

function showErrorDialog(message) {
    Swal.fire('Error', message, 'error')
        .then(function () {
            location.reload();
        })
}

function deleteMovieHandler() {
    var movieId = window.location.pathname.split("/").pop();
    var movieTitle = movieForm.find("#input-title").val();
    var movieDescription = movieForm.find("#input-description").val();
    var movieYear = movieForm.find("#input-year").val();
    var movieActors = movieForm.find("#input-actors").val();


    var data = {
        movie_id: movieId,
        title: movieTitle,
        description: movieDescription,
        year: movieYear,
        actors: movieActors,
    };

    if (checkParams(data)) {
        movieEditRequest(data)
    } else {
        showErrorDialog('Please check your input.')
    }
}

function movieEditRequest(data) {
    var params = new FormData();

    for (var key in data) {
        params.append(key, data[key]);
    }

    $axios.put('/movies', params, {
        'Content-Type': "application/x-www-form-urlencoded"
    })
        .then(function (response) {
            console.log(response);
            Swal.fire({
                position: 'center',
                icon: 'success',
                title: 'Movie successfully changed',
                showConfirmButton: false,
                timer: 1000
            }).then(function () {
                location.reload();
            })
        })
        .catch(function (error) {
            console.log(error.response.data.error);
            var message = "An error occured. Please try again.";

            if (error.response.data.error) {
                message = error.response.data.error;

            }

            showErrorDialog(message)
        });
}

function checkParams(data) {
    if (!data.title && data.title === "") {
        return false;
    }

    if (!data.actors && data.actors === "") {
        return false;
    }


    return true
}

