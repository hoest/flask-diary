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

  $('#body-editor').hallo({
    plugins: {
      'halloformat': {},
      'halloheadings': {
        formatBlocks: ['p', 'h3']
      },
      'halloreundo': {},
      'halloblacklist': {
        tags: ['div', 'span', 'h1', 'h2', 'a', 'font']
      }
    },
    toolbar: 'halloToolbarContextual'
  });

  $('#body-editor').bind('hallomodified', function(event, data) {
    showSource(data.content);
  });
  $('#body').bind('keyup', function() {
    updateHtml(this.val());
  }).hide();
  updateHtml($('#body').val());
});

var converter = new Showdown.converter();
var htmlize = function(content) {
  return converter.makeHtml(content);
};

var updateHtml = function(content) {
  if (markdownize($('#body-editor').html()) == content) {
    return;
  }

  var html = htmlize(content);
  $('#body-editor').html(html);
};

// optional options w/defaults
var options = {
    link_list:  true,    // render links as references, create link list as appendix
    h1_setext:  true,     // underline h1 headers
    h2_setext:  true,     // underline h2 headers
    h_atx_suf:  false,    // header suffixes (###)
    gfm_code:   true,    // gfm code blocks (```)
    li_bullet:  "*",      // list item bullet style
    hr_char:    "-",      // hr style
    indnt_str:  "    ",   // indentation string
    bold_char:  "*",      // char used for strong
    emph_char:  "_",      // char used for em
    gfm_del:    true,     // ~~strikeout~~ for <del>strikeout</del>
    gfm_tbls:   true,     // markdown-extra tables
    tbl_edges:  false,    // show side edges on tables
    hash_lnks:  false,    // anchors w/hash hrefs as links
    br_only:    false    // avoid using "  " as line break indicator
};

var reMarker = new reMarked(options);

var markdownize = function(content) {
  var html = content.split("\n").map($.trim).filter(function(line) {
    return line !== "";
  }).join("\n");
  return reMarker.render(html);
};

var showSource = function(content) {
  var markdown = markdownize(content);
  if ($('#body').get(0).value == markdown) {
    return;
  }
  $('#body').get(0).value = markdown;
};

var getParameterByName = function(name) {
  var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
  return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
};
