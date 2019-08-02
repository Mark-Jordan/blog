$(document).ready(function() {

    var $showTarget=$('#div_id_content');
    var $title=$('#div_id_title');
    setInterval(function () {
         let $target=$('#div_id_display_type>.controls>.selectize-control>.selectize-input>.item');
        if ($target.attr('data-value')!="1"){
            $showTarget.hide();
            $title.hide();
        }else {
            $showTarget.show();
            $title.show();
        }
    },220);
});
