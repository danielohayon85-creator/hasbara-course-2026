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

  function initMobileMenu() {
    var toggle = document.getElementById("nav-toggle");
    var menu = document.getElementById("mobile-menu");
    if (!toggle || !menu) return;
    var root = rootPath();
    var items = [
      { href: root + "index.html", label: "🏠 בית" },
      { href: root + "quick-ref.html", label: "📌 מדריך מהיר" },
      { divider: "תמציות" },
      { href: root + "digests/role.html", label: "🎖️ תפקיד קצין ההסברה" },
      { href: root + "digests/theory.html", label: "📚 עקרונות ותורת ההסברה" },
      { href: root + "digests/guidelines.html", label: "🛡️ הנחיות ומדיניות" },
      { href: root + "digests/authority.html", label: "🏛️ הרשות המקומית" },
      { href: root + "digests/population.html", label: "🧰 מערך האוכלוסייה וכלים" },
    ];
    menu.innerHTML = items.map(function (it) {
      if (it.divider) return '<div class="mobile-menu-divider">' + it.divider + "</div>";
      return '<a href="' + it.href + '">' + it.label + "</a>";
    }).join("");

    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "✕" : "☰";
      document.body.style.overflow = open ? "hidden" : "";
    });
    menu.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        menu.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.textContent = "☰";
        document.body.style.overflow = "";
      }
    });
  }

  function initPrintButtons() {
    document.querySelectorAll("[data-print]").forEach(function (btn) {
      btn.addEventListener("click", function () { window.print(); });
    });
  }

  function initArchiveAccordion() {
    document.querySelectorAll(".archive-toggle").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var body = document.getElementById(btn.getAttribute("aria-controls"));
        var open = body.classList.toggle("open");
        btn.setAttribute("aria-expanded", open ? "true" : "false");
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initSearch();
    initMobileMenu();
    initPrintButtons();
    initArchiveAccordion();
  });
})();
