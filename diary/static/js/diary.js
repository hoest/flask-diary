$(function() {
  post_id = getParameterByName('post_id');
  if(post_id && post_id !== '') {
    $('html, body').animate({
      scrollTop: $('#post_' + post_id).offset().top
    }, 500);
  }

  $('.alert-block').delay(1000).slideUp();

  $('.edit-buttons li a').each(function() {
    $(this).attr('title', $(this).text());
  });

  $('.delete-image').each(function() {
    $(this).attr('title', $(this).text());
  });

  if (!Modernizr.inputtypes.date) {
    $('#date').datepicker({ dateFormat: 'yy-mm-dd' });
  }

  $(".fancybox").fancybox();
});

var getParameterByName = function(name) {
  var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
  return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
};
