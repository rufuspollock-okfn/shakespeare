jQuery(document).ready(function($) {
  var $mydiv = $('#latest-annotations');
  var mytmpl = '<li><a href="${uri}">${work}</a>: ${snippet}</li>';
  var url = 'http://annotateit.org/api/search?limit=5';
  $.getJSON(url, function(data) {
    $.each(data.rows, function(idx, row) {
      var _t = row['text'];
      row['snippet'] =  _t.length < 75 ? _t : _t.slice(0, 75) + '...';
      var _name = row['uri'].split('/');
      var _name = _name[_name.length-1];
      row['work'] = _name[0].toUpperCase() + _name.slice(1).replace(/_/g, ' ');
    });
    $mydiv.find('.total').html(data.total);
    $mydiv.find('ul').html($.tmpl(mytmpl, data.rows));
  });
});
