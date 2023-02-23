  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    var el = document.querySelectorAll('.tabs');
    M.Modal.init(elems, {});
    M.Tabs.init(el, {});
  });