jQuery(function(){
    jQuery("select.download").change(function(){
    jQuery.ajax({url:jQuery(this).val()})
    })
})
