  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    M.Modal.init(elems, {});
    elems  = document.querySelectorAll('.tabs');
    M.Tabs.init(elems, {});
    elems = document.querySelectorAll('.sidenav');
    M.Sidenav.init(elems, {});
    console.log('toto')
  });