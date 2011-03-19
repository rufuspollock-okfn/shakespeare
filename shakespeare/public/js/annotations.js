jQuery(document).ready(function($) {
  var $mydiv = $('#latest-annotations');
  var mytmpl = '<li><a href="/work/annotate/${uri}">${work}</a>: ${snippet}</li>';
  var url = 'http://annotateit.org/api/search?limit=5&all_fields=1';
  $.getJSON(url, function(data) {
    $.each(data.rows, function(idx, row) {
      var _t = row['text'];
      row['snippet'] =  _t.length < 75 ? _t : _t.slice(0, 75) + '...';
      var _uri = row['uri'];
      row['work'] = _uri[0].toUpperCase() + _uri.slice(1).replace('_', ' ');
    });
    $mydiv.find('.total').html(data.total);
    $mydiv.find('ul').html($.tmpl(mytmpl, data.rows));
  });
});
