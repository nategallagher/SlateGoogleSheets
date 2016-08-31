function init_hidden_datapickers(){
    $('.hidden-datefield-div').each(function() {
        var $this = $(this);
        var $span = $this.find("span.datefield-text")
        var $dateinput = $this.find(".hidden-datefield");
        $dateinput.datepicker({
            showOn: 'button',
            buttonImage: '/static/common/img/calendar.png',
            buttonImageOnly: true,
            dateFormat: ShareDateFormat.datepicker_format,
            onSelect: function() {
                var date = $(this).datepicker('getDate');
                $span.text(date.format(ShareDateFormat.date_format));
                $dateinput.trigger('change');

                // Hack - trigger for hidden fields, doesn't triggered after getting data by ajax.
                $("#is_modified").val(1);
            }
        });

    });
}
