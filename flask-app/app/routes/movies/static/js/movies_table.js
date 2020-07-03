//
var moviesTable = {};
// var deleteRow = function () {
// };
//
$(document).ready(function () {
    moviesTable = $('#movies-table').DataTable();
});
//
// $(document).on("click", ".delete-movie-btn", function () {
//     // var movieTableRow = $(this).closest("tr").get(0);
//     // console.log(movieTableRow);
//     // find the row
//     const movieId = $(this).data('id');
//     const movieTitle = $(this).data('title');
//     var movieModalEl = $("#delete-movie-modal");
//     var deleteMovieButton = movieModalEl.find("#movie-delete-button");
//     // $("#delete-movie-modal #movie-id").val( movieId );
//     movieModalEl.find("#movie-id").val(movieId);
//     movieModalEl.find("#movie-title").html(movieTitle);
//
//     // deleteRow = function () {
//     //     moviesTable
//     //         .row(movieTableRow)
//     //         .remove()
//     //         .draw();
//     // }
//
//     var succHandler = function () {
//         location.reload();
//     }
//
//     var data = {
//         title: movieTitle
//     }
//     console.log("EEEE");
//     deleteMovieButton.off("click");
//     deleteMovieButton.on("click", deleteMovieHandler(data, succHandler));
// });
//
//
// var deleteMovieHandler = function (data, callbackSuccess) {
//     return function () {
//         $.ajax({
//             url: 'api/v1/movies',
//             type: 'DELETE',
//             dataType: 'json',
//             contentType: 'application/json',
//             timeout: 5000,
//             data: JSON.stringify(data),
//             // statusCode: {
//             //     403: function () {
//             //         console.log("unatho");
//             //     }
//             // },
//             success: function (data, status, xhr) {
//                 if (xhr.status === 200) {
//                     if (callbackSuccess) {
//                         console.log("success!!!");
//                         callbackSuccess();
//                     }
//                 } else {
//                     console.log("error");
//                 }
//             },
//             fail: function (xhr, textStatus, errorThrown) {
//                 console.log(textStatus);
//                 console.log(errorThrown);
//                 console.log("error");
//             },
//
//         });
//     }
// }