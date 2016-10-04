(function () {
    'use strict';

    $('#condiciones-atmosfericas').submit(function (event) {
        event.preventDefault();
        $.ajax({
            type: 'GET',
            url: '/greengarden/actualizar/',
            success: function (data) {
                $('#info-actualizacion').show();
            }
        });
    });

    $('.alert .close').click(function () {
        $(this).parent().hide();
    });

    $('.btn-default').on('mousedown', function () {
        $(this).css('background-color', '#009688');
        $(this).css('border-color', '#009688');
        $(this).css('color', '#FFF');
    });
})();