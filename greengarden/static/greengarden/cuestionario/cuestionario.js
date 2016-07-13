(function(){
    'use strict';

    $('#form-cuestionario input:checkbox').each(function () {
        $(this).click(function () {
            if (this.checked) {
                $('#memoria').append('<li class="list-group-item">'+ $(this).parent().text() +'</li>');
            } else {
                $('#memoria li').remove(":contains('"+ $(this).parent().text() +"')");
            }
        });
    });

    $('.navbar-nav li').each(function () {
        if ($(this).children().text() === 'Cuestionario') {
            $(this).addClass('active');
        } else {
            $(this).removeClass('active');
        }
    });
})();