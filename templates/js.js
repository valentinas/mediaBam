jQuery(function(){
    jQuery("select.download").change(function(){
        jQuery.ajax({
            'url': jQuery(this).val(),
            'success': function(result){
                result = jQuery.parseJSON(result)
                if(result.success===true){
                    jQuery('#' + result.rowId + ' .downloadContainer').html('Downloading!').addClass('green bold')
                }
             }
        })
    })
})
