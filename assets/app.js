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

  // אותה ספריית SVG שמוגדרת ב-build.py (ICON_PATHS) - מוטבעת גם כאן כי
  // תפריט הנייד נבנה בצד הלקוח, לא בזמן ה-build.
  var ICN = {
    home: '<path d="M4 11.2 12 4l8 7.2"/><path d="M6 10v10h5v-6h2v6h5V10"/>',
    pin: '<path d="M12 2a5 5 0 0 0-5 5c0 3.5 5 10 5 10s5-6.5 5-10a5 5 0 0 0-5-5z"/><circle cx="12" cy="7" r="1.8" fill="currentColor" stroke="none"/>',
    theory: '<path d="M4 5.6c1.8-1 4.3-1 8 .6 3.7-1.6 6.2-1.6 8-.6v13c-1.8-1-4.3-1-8 .6-3.7-1.6-6.2-1.6-8-.6v-13z"/><path d="M12 6.2v13"/>',
    role: '<path d="M12 2.6 19.6 5.4V11c0 4.9-3.2 8.4-7.6 10-4.4-1.6-7.6-5.1-7.6-10V5.4L12 2.6z"/><path d="M12 7.4l1.2 2.5 2.8.4-2 1.9.5 2.8-2.5-1.3-2.5 1.3.5-2.8-2-1.9 2.8-.4L12 7.4z" fill="currentColor" stroke="none"/>',
    guidelines: '<path d="M12 2.6 19.6 5.4V11c0 4.9-3.2 8.4-7.6 10-4.4-1.6-7.6-5.1-7.6-10V5.4L12 2.6z"/><path d="M8.6 11.6l2.3 2.3 4.4-4.6"/>',
    authority: '<path d="M3 9.2 12 4l9 5.2"/><path d="M4.3 9.6V20M19.7 9.6V20"/><path d="M7.6 9.6V20M11 9.6V20M13 9.6V20M16.4 9.6V20"/><path d="M3 20h18"/>',
    population: '<rect x="3" y="9.5" width="18" height="10" rx="1.5"/><path d="M8.2 9.5V6.8A1.8 1.8 0 0 1 10 5h4a1.8 1.8 0 0 1 1.8 1.8v2.7"/><path d="M3 14h18"/>',
    quiz: '<circle cx="12" cy="12" r="9"/><path d="M9.2 9.3a2.8 2.8 0 1 1 3.8 2.6c-.7.3-1 .8-1 1.6"/><circle cx="12" cy="17" r="0.9" fill="currentColor" stroke="none"/>'
  };
  function svgIcon(name) {
    return '<svg class="icn" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" ' +
      'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICN[name] + "</svg>";
  }

  function initMobileMenu() {
    var toggle = document.getElementById("nav-toggle");
    var menu = document.getElementById("mobile-menu");
    if (!toggle || !menu) return;
    var root = rootPath();
    var items = [
      { href: root + "index.html", label: svgIcon("home") + " בית" },
      { href: root + "quick-ref.html", label: svgIcon("pin") + " מדריך מהיר" },
      { href: root + "acronyms.html", label: svgIcon("theory") + " מילון קיצורים" },
      { href: root + "quiz.html", label: svgIcon("quiz") + " מבחן תרגול" },
      { divider: "סיכומים" },
      { href: root + "digests/role.html", label: svgIcon("role") + " תפקיד קצין ההסברה" },
      { href: root + "digests/theory.html", label: svgIcon("theory") + " עקרונות ותורת ההסברה" },
      { href: root + "digests/guidelines.html", label: svgIcon("guidelines") + " הנחיות ומדיניות" },
      { href: root + "digests/authority.html", label: svgIcon("authority") + " הרשות המקומית" },
      { href: root + "digests/population.html", label: svgIcon("population") + " מערך האוכלוסייה וכלים" },
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
