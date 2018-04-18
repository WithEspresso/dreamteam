$(function () {
 
  var $pickers = $('.mk-datepicker-trigger');
      $pickers.mkdatepicker();
      $pickers.on('change.mk-datepicker', function(e, date) {
          console.info('formatted date: ', this.value);
          console.info('raw date object: ', date);
      });
});
 
settings = {
    //Model Popup
    objModalPopupBtn: ".modalButton",
    objModalCloseBtn: ".overlay, .closeBtn",
    objModalDataAttr: "data-popup"
} 
  $(settings.objModalPopupBtn).bind("click", function () {
        if ($(this).attr(settings.objModalDataAttr)) {
 
            var strDataPopupName = $(this).attr(settings.objModalDataAttr);
 
           
            //Fade In Modal Pop Up
            $(".overlay, #" + strDataPopupName).fadeIn();
 
        }
    });
 
    //On clicking the modal background
    $(settings.objModalCloseBtn).bind("click", function () {
        $(".modal").fadeOut();
    });