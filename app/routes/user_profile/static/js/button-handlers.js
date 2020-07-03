$("#delete-account").click(deleteAccountHandler);

function deleteAccountHandler() {
    var userId = $(this).data('id');
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Yes!'
    }).then((result) => {
        if (result.value) {
            deleteAccountRequest(userId);
        }
    })
};

function deleteAccountRequest(userId) {
    $axios.delete('/users', {
        headers: {
            'Content-Type': 'application/json',
        },
        data: {
            email: userId
        },
    })
        .then(function (response) {
            console.log(response);
            Swal.fire({
                position: 'center',
                icon: 'success',
                title: 'Account deleted',
                showConfirmButton: false,
                timer: 1000
            }).then(function () {
                window.location.reload(true);
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