(function () {
    'use strict';

    $('ul li').removeClass('active');
    $('ul li').each(function () {
    	if ($(this).text() === 'Ayuda') {
    		$(this).addClass('active');
    	}
    });
})();