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
            $('#error-cuestionario').hide();
            return true;
        } else {
            $('#error-cuestionario').show();
            return false;
        }
    });

    $('.alert .close').click(function () {
        $(this).parent().hide();
    });
})();