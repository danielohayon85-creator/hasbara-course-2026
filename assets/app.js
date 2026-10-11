// אתר ידע - קורס קציני הסברה 2026 - חיפוש וניווט

(function () {
  function rootPath() {
    // detect whether we're in /topics/ or root, to build correct relative path to search-index.json
    return document.body.getAttribute("data-root") || "./";
  }

  function initSearch() {
    var input = document.getElementById("site-search");
    var resultsBox = document.getElementById("search-results");
    if (!input || !resultsBox) return;

    var index = null;
    var indexUrl = rootPath() + "search-index.json";

    fetch(indexUrl)
      .then(function (r) { return r.json(); })
      .then(function (data) { index = data; })
      .catch(function () { index = []; });

    function render(matches, query) {
      if (!matches.length) {
        resultsBox.innerHTML = '<div class="sr-empty">אין תוצאות עבור "' + escapeHtml(query) + '"</div>';
        resultsBox.classList.add("open");
        return;
      }
      var html = matches.slice(0, 12).map(function (m) {
        return '<a href="' + rootPath() + m.url + '">' +
          '<div class="sr-title">' + escapeHtml(m.title) + '</div>' +
          '<div class="sr-path">' + escapeHtml(m.section || m.docTitle || "") + '</div>' +
          '</a>';
      }).join("");
      resultsBox.innerHTML = html;
      resultsBox.classList.add("open");
    }

    function escapeHtml(s) {
      return (s || "").replace(/[&<>"']/g, function (c) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
      });
    }

    function search(query) {
      if (!index || !query || query.trim().length < 2) {
        resultsBox.classList.remove("open");
        return;
      }
      var q = query.trim().toLowerCase();
      var matches = index.filter(function (item) {
        return (item.title && item.title.toLowerCase().indexOf(q) !== -1) ||
               (item.text && item.text.toLowerCase().indexOf(q) !== -1) ||
               (item.docTitle && item.docTitle.toLowerCase().indexOf(q) !== -1);
      });
      render(matches, query);
    }

    input.addEventListener("input", function () { search(input.value); });
    input.addEventListener("focus", function () { if (input.value) search(input.value); });
    document.addEventListener("click", function (e) {
      if (!resultsBox.contains(e.target) && e.target !== input) {
        resultsBox.classList.remove("open");
      }
    });
  }

  document.addEventListener("DOMContentLoaded", initSearch);
})();
