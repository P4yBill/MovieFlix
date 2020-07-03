$(document).ready(function () {
    $('#users-table').DataTable({
        "columnDefs": [
            {"width": "40%", "targets": 0},
            {"width": "40%", "targets": 1},
            {"width": "20%", "targets": 2},
        ]
    });
});
