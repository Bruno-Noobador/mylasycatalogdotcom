$('.cc-number').on('keyup change', function(){
    if ($(this).val().length == 4) {
      $(this).next().focus();
    } else if ($(this).val().length == 0) {
      $(this).prev().focus();
    }
});

$(".button-cart").on('click', function(e){
  e.stopPropagation();
  $(".cont-product").addClass("slide-right");
  $(".container").addClass("slide-cont-left");
  $(this).addClass("btn-hiding");
  setTimeout(function(){
       $(".cont-product").addClass("zindex");
   }, 300);
});

$(".product").on('click', function(e){
  e.stopPropagation();
  $(".cont-options").removeClass("slideup");
  $(".product").removeClass("active");
  $(this).addClass("active");
  $(this).find(".cont-options").addClass("slideup");
});

$(window).on( "click", function(){
  $(".product").removeClass("active");
  $(".cont-product").removeClass("zindex");
  $(".cont-product").removeClass("slide-right");
  $(".container").removeClass("slide-cont-left");
  $(".button-cart").removeClass("btn-hiding");
  $(".cont-options").removeClass("slideup");
});