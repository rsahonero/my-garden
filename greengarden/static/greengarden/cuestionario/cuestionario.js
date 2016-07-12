(function(){
    'use strict';
    var items = [];

    $('#form-cuestionario input:checkbox').each(function () {
        $(this).click(function () {
            if (this.checked) {
                items.push($(this).parent().text())
                $('#memoria').append('<li class="list-group-item">'+ $(this).parent().text() +'</li>');
            } else {
                var index = items.indexOf($(this).parent().text())
                items.splice(index, 1);
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