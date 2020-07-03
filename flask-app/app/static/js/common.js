$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", MF.CSRF);
        }
    }
});


const config = {
    baseURL: "/api/v1/",
    withCredentials: true,
    timeout: 10000,
    responseType: 'json',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': MF.CSRF,
    },
};

var $axios = axios.create(config);