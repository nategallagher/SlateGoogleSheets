function init_datapickers(){
    $('.datefield').datepicker({
        showOn: 'button',
        dateFormat: ShareDateFormat.datepicker_format,
        buttonImage: '/static/common/img/calendar.png',
        buttonImageOnly: true
    }); 
}
