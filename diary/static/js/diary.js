$(function() {
  post_id = getParameterByName("post_id");
  if(post_id && post_id !== "") {
    $("html, body").animate({
      scrollTop: $("#post_" + post_id).offset().top
    }, 500);
  }

  $(".alert-block.alert-info").delay(5000).slideUp();

  $(".edit-buttons li a").each(function() {
    $(this).attr("title", $(this).text());
  });

  $(".delete-image").each(function() {
    $(this).attr("title", $(this).text());
  });

  $("a[class^=delete-], [class^=delete-] a").bind("click", function() {
    return confirm("Weet je het zeker?");
  });

  if (!Modernizr.inputtypes.date) {
    $("#date").datepicker({ dateFormat: "yy-mm-dd" });
  }

  $("#content").infinitescroll({
    navSelector: "div.pager", // selector for the paged navigation (it will be hidden)
    nextSelector: "div.pager a.old", // selector for the NEXT link (to page 2)
    itemSelector: "#content div.post", // selector for all items you"ll retrieve
    loading: {
      finishedMsg: "",
      msgText: "<p>Meer berichten laden...</p>"
    },
    prefill: true,
    extraScrollPx: 250,
    bufferPx: 75
  });

  $(".fancybox").fancybox();
});

var getParameterByName = function(name) {
  var match = RegExp("[?&]" + name + "=([^&]*)").exec(window.location.search);
  return match && decodeURIComponent(match[1].replace(/\+/g, " "));
};
