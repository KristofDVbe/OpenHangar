(function () {
  function init() {
    var modal = document.getElementById('docModal');
    if (!modal || modal.dataset.ohInited) return;
    modal.dataset.ohInited = '1';
    modal.addEventListener('show.bs.modal', function (e) {
      var btn = e.relatedTarget;
      var url = btn.getAttribute('data-url');
      var mime = btn.getAttribute('data-mime') || '';
      var title = btn.getAttribute('data-title') || '';
      document.getElementById('docModalLabel').textContent = title;
      var downloadLink = document.getElementById('docModalDownload');
      if (downloadLink) downloadLink.href = url;
      var body = document.getElementById('docModalBody');
      body.innerHTML = '';
      if (mime.startsWith('image/')) {
        var img = document.createElement('img');
        img.src = url;
        img.className = 'doc-modal-image img-fluid d-block mx-auto p-2';
        body.appendChild(img);
      } else {
        var iframe = document.createElement('iframe');
        iframe.src = url;
        iframe.className = 'doc-modal-frame';
        body.appendChild(iframe);
      }
    });
    modal.addEventListener('hidden.bs.modal', function () {
      document.getElementById('docModalBody').innerHTML = '';
    });
  }
  document.addEventListener('DOMContentLoaded', init);
  document.addEventListener('htmx:afterSettle', init);
})();
