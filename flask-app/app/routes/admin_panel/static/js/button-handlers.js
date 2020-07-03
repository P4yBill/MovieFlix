$(".delete-user-btn").click(function () {
    var userMail = $(this).data('id');
    var movieModalEl = $("#delete-user-modal");

    movieModalEl.find("#user-email").val(userMail);
    movieModalEl.find("#user-email-title").html(userMail);
});

$("#delete-user-modal").find("#user-delete-button").click(deleteUserHandler);

function deleteUserHandler() {
    var userEmail = $("#delete-user-modal").find("#user-email").val();
    console.log("Clicked");
    $.ajax({
        url: 'api/v1/users',
        type: 'DELETE',
        dataType: 'json',
        contentType: 'application/json',
        timeout: 5000,
        data: JSON.stringify({email: userEmail}),
        success: function (data, status, xhr) {
            if (xhr.status === 200) {
                location.reload();
            } else {
                Swal.fire('Error', data.error, 'error')
            }
        },
        fail: function () {
            Swal.fire('Error', "User could not be deleted. Please try again.", 'error')

        },

    });
}


// update user modal
$(".update-user-btn").click(function () {
    var userMail = $(this).data('id');
    var movieModalEl = $("#update-user-modal");

    movieModalEl.find("#user-update-email").val(userMail);
    movieModalEl.find("#user-update-email-title").html(userMail);
});

$("#update-user-modal").find("#user-update-button").click(updateUserModal);

function updateUserModal() {
    var userEmail = $("#update-user-modal").find("#user-update-email").val();
    $.ajax({
        url: 'api/v1/users',
        type: 'PUT',
        dataType: 'json',
        contentType: 'application/json',
        timeout: 5000,
        data: JSON.stringify({email: userEmail}),
        success: function (data, status, xhr) {
            if (xhr.status === 200) {
                location.reload();
            } else {
                Swal.fire('Error', data.error, 'error')
            }
        },
        fail: function () {
            Swal.fire('Error', "User could not be deleted. Please try again.", 'error')

        },

    });
}