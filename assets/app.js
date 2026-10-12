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
      { href: root + "acronyms.html", label: "📖 מילון קיצורים" },
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

  function initActiveTabScroll() {
    var active = document.querySelector(".cat-tabs a.active");
    if (active) active.scrollIntoView({ inline: "center", block: "nearest" });
  }

  function initTableScroll() {
    document.querySelectorAll(".table-scroll").forEach(function (wrap) {
      var table = wrap.querySelector("table");
      if (!table) return;
      var wrapWidth = wrap.clientWidth;
      if (!wrapWidth) return;

      // Measure the table's true single-line content width (how wide it
      // would need to be if nothing wrapped), independent of any min-width
      // already set in CSS, to decide whether this specific table actually
      // needs horizontal scrolling on this screen.
      var prevWhiteSpace = table.style.whiteSpace;
      var prevWidth = table.style.width;
      var prevMinWidth = table.style.minWidth;
      table.style.whiteSpace = "nowrap";
      table.style.width = "auto";
      table.style.minWidth = "0";
      var naturalWidth = table.scrollWidth;
      table.style.whiteSpace = prevWhiteSpace;

      if (naturalWidth <= wrapWidth + 2) {
        table.style.width = "100%";
        table.style.minWidth = "0";
        wrap.classList.remove("scrollable");
      } else {
        table.style.width = prevWidth;
        table.style.minWidth = Math.ceil(Math.min(naturalWidth, wrapWidth * 2)) + "px";
        wrap.classList.add("scrollable");

        var hint = wrap.previousElementSibling;
        if (!hint || !hint.classList || !hint.classList.contains("scroll-hint")) {
          hint = document.createElement("div");
          hint.className = "scroll-hint";
          hint.textContent = "⟷ ניתן לגלול בטבלה כדי לצפות בכל העמודות";
          wrap.parentNode.insertBefore(hint, wrap);
        }
        wrap.addEventListener("scroll", function onScroll() {
          if (Math.abs(wrap.scrollLeft) > 8) {
            hint.classList.add("hide");
            wrap.removeEventListener("scroll", onScroll);
          }
        });
      }
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initSearch();
    initMobileMenu();
    initPrintButtons();
    initArchiveAccordion();
    initActiveTabScroll();
    initTableScroll();
    window.addEventListener("resize", initTableScroll);
  });
})();
