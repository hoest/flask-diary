// var Aloha = window.Aloha || (window.Aloha = {});
// Aloha.settings = {
//   locale: 'nl',
//   plugins: {
//     format: {
//       // all elements with no specific configuration get this configuration
//       config : [  'b', 'i', 'p', 'sub', 'sup', 'h3', 'h4', 'h5', 'pre', 'removeFormat' ],
//       editables : {
//         // no formatting allowed for title
//         '#title' : [  ]
//       },
//       sidebar: {
//         disabled: true
//       }
//     }
//   }
// };

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

  // Aloha.ready(function() {
  //   var $ = Aloha.jQuery;
  //   $('#body').aloha();
  // });
});

function getParameterByName(name) {
  var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
  return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}
