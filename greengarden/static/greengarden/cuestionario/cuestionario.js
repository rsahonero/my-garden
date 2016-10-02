(function () {
    'use strict';

    $('.btn-default').on('mousedown', function () {
        $(this).css('background-color', '#009688');
        $(this).css('border-color', '#009688');
        $(this).css('color', '#FFF');
    });

    $('#cuestionario').submit(function (e) {
        var valor = $('input[name=valor]:checked').val();
        if (valor) {
            return true;
        } else {
            return false;
        }
    });
})();