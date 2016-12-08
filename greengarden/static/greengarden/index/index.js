(function () {
    'use strict';

    $('#condiciones-atmosfericas').submit(function (event) {
        event.preventDefault();
        $.ajax({
            type: 'GET',
            url: '/greengarden/actualizar/',
            success: function (data) {

                var monthNames = [
                    "Enero", "Febrero", "Marzo",
                    "Abril", "Mayo", "Junio", "Julio",
                    "Agosto", "Septiembre", "Octubre",
                    "Noviembre", "Diciembre"
                ];

                var date = new Date(data.tiempo_actual);
                var day = date.getDate();
                var monthIndex = date.getMonth();
                var year = date.getFullYear();
                var fechaFormateada = day + ' de ' + monthNames[monthIndex] + ' de ' + year;
                var tiempoFormateado = date.getHours() + ':' + date.getMinutes();
                $('#ultimo-escaneo').html(fechaFormateada + ' a las ' + tiempoFormateado);
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