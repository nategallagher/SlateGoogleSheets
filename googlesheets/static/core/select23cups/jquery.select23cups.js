(function($){
    $.fn.select23cups = function(options){
        var opts = $.extend({}, $.fn.select23cups.defaults, options);
        $.fn.select23cups.opts = opts;

        return this.each(function() {
            var container = $(this);
            var main = container.find('select').hide();

            var wrapper = $('<div class="select23cups_wrapper"/>');
            var select1 = get_select('select23cups_select1', opts.select1_title);
            var select2 = get_select('select23cups_select2', opts.select2_title, true);
            var select3 = get_select('select23cups_select3', opts.select3_title, true);
            var buttons = $('<div class="select23cups_buttons"/>');

            wrapper.append(select1.container)
                   .append(select2.container);

            container.append(wrapper)
                     .append(buttons)
                     .append(select3.container);

            button = {
                add: get_button(opts.button_add),
                add_all: get_button(opts.button_add_all),
                del: get_button(opts.button_del),
                del_all: get_button(opts.button_del_all)
            };

            buttons.append(button.add)
                   .append(button.add_all)
                   .append(button.del)
                   .append(button.del_all);

            select1 = select1.select;
            select2 = select2.select;
            select3 = select3.select;

            main.find('optgroup').each(function() {
               var option = $('<option/>')
               option.html(this.label);
               select1.append(option);
            });
           // Bug fix for IE OnChange behavior (should use live, but this is more portable)
           if ($.browser.msie) {
               select1.unbind('click');
               select1.bind('click', function() {
                   $(this).trigger('change');
               });
           }

           // New change handler
            select1.change(function() {
                $(".select23cups_select1 option:selected").each(function () {
                    element = $(this);
                    group = main.find('optgroup[label=' + element.text() + ']');
                    group_list = group.find('option:not(:selected)');
                    //------------------- add options --------------
                    select2[0].options.length = 0;
                    group_list.each(function(){
                        // ------------- check option ---------
                        var not_enable_move = false;
                        for(var i =0; i < select3[0].options.length; i++){
                            if($(this)[0].value == select3[0][i].value){
                                not_enable_move=true;
                            }
                        }
                        if(!not_enable_move){
                            select2[0].options[select2[0].options.length] = new Option($(this)[0].text, $(this)[0].value);
                        }
                    });
                    //------------------- add options --------------
                    select2.trigger('change');
                });
            });

            select3.append(main.find('option:selected').clone().attr('selected', ''));

            //------------- buttons event ---------------
            button.add.click(function() {
                options = select2.find('option');
                if (options.length>0) {
                    if ( select2[0].selectedIndex != -1)
                    {
                        select2_change_move(select2[0].options[select2[0].selectedIndex], select2[0].selectedIndex);
                    }
                }
                return false;
            });

            button.add_all.click(function() {
                var opt_length = select2[0].options.length;
                for(var i = 0; i < opt_length; i++){
                    select3[0].options[select3[0].options.length] = new Option(select2[0].options[i].text, select2[0].options[i].value);
                    main.find('option[value=' + $(select2[0].options[i]).val() + ']').attr('selected', 'selected')
                }
                select2[0].options.length = 0;

                return false;
            });

            button.del.click(function() {
                options = select3.find('option');
                if (options.length>0) {
                    if ( select3[0].selectedIndex != -1)
                    {
                        select3_change_move(select3[0].options[select3[0].selectedIndex], select3[0].selectedIndex);
                    }
                }
                return false;
            });

            button.del_all.click(function() {
               var opt_length = select3[0].options.length;
                for(var i = 0; i < opt_length; i++){
                    select2[0].options[select2[0].options.length] = new Option(select3[0].options[i].text, select3[0].options[i].value);
                    main.find('option[value=' + $(select3[0].options[i]).val() + ']').attr('selected', '')
                }
                select3[0].options.length = 0;

                return false;
            })

            select2.change(function() {
                options = select2.find('option');
                if (options.length>0) {                    
                    options.dblclick(function() {
                        options = select2.find('option');
                        if (options.length>0) {
                            if ( select2[0].selectedIndex != -1)
                            {
                                select2_change_move(select2[0].options[select2[0].selectedIndex], select2[0].selectedIndex);
                            }
                        }
                        return false;
                    });
                }
            });

            select3.change(function() {
                options = select3.find('option');
                if (options.length>0) {                    
                    options.dblclick(function() {
                        options = select3.find('option');
                        if (options.length>0) {
                            if ( select3[0].selectedIndex != -1)
                            {
                                select3_change_move(select3[0].options[select3[0].selectedIndex], select3[0].selectedIndex);
                            }
                        }
                        return false;

                        //select3_change(this);
                    });
                }
            });

            select2.trigger('change');
            select3.trigger('change');           

            function get_button(button) {
                return $('<a href="#"/>').html(button.text).attr('title', button.title);
            }

            function get_select(class_, title, multiple) {
                var container = $('<div/>').addClass(class_);
                var title = $('<b/>').html(title);
                var select  = $('<select size="8">');
                if (multiple != undefined) {
                    select.attr('multiple', 'multiple');
                }
                container.append(title)
                         .append(select);

                return {container: container, select: select};
            }            

            function select2_change_move(element, index){
                select3[0].options[select3[0].options.length] = new Option(element.text, element.value);
                main.find('option[value=' + $(element).val() + ']').attr('selected', 'selected')
                select2[0].remove(index);
            }

            function select3_change_move(element, index){
                select2[0].options[select2[0].options.length] = new Option(element.text, element.value);
                main.find('option[value=' + $(element).val() + ']').attr('selected', '')
                select3[0].remove(index);
            }            
        });
    };

    $.fn.select23cups.defaults = {
        select1_title: 'Groups',
        select2_title: 'Individuals',
        select3_title: 'Selected Individuals',
        button_add: {text: '&rsaquo;', title: 'Add Selected'},
        button_add_all: {text: '&raquo;', title: 'Add All'},
        button_del: {text: '&lsaquo;', title: 'Remove Selected'},
        button_del_all: {text: '&laquo;', title: 'Remove All'}
    }

})(jQuery);
