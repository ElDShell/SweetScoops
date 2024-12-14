$(document).ready(function () {
    var page = 2;
    var loading = false;

    var loadMoreUrl = $('#load-more-btn').data('url');
    var csrfToken = $('meta[name="csrf-token"]').attr('content');


    if (!csrfToken) {
        console.error('CSRF token not found');
        return; 
    }
    console.log("CSRF Token:", csrfToken);  // Log CSRF token


    $('#load-more-btn').click(function () {
        if (loading) return;
        loading = true;

        $.ajax({
            url: loadMoreUrl,  
            data: {
                'page': page,
            },
            headers: {
                'X-CSRFToken': csrfToken 
            },
            success: function (response) {
                $('#product-list').append(response.products_html);

                if (response.has_next) {
                    page++;
                    $('#load-more-container').appendTo('#product-list');
                } else {
                    $('#load-more-container').hide();
                }
                loading = false;
            },
            error: function () {
                console.error('Error with the request');
                loading = false;
            }
        });
    });
});
