#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
בונה את אתר הידע הסטטי מתוך content-source/*.md
מריץ: python3 build.py
"""
import json
import os
import re
import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "content-source")
TOPICS_OUT = os.path.join(ROOT, "topics")

CATEGORIES = [
    {"id": "role", "title": "תפקיד קצין ההסברה", "icon": "🎖️",
     "desc": "מי קצין ההסברה, מה תפקידו בכל דרג, וכיצד הוא פועל מול הרשות המקומית."},
    {"id": "theory", "title": "עקרונות ותורת ההסברה", "icon": "📚",
     "desc": "מהי הסברה, המודלים המרכזיים, עקרונות היסוד ולקחים מהשטח."},
    {"id": "guidelines", "title": "הנחיות מצילות חיים ומדיניות ההתגוננות", "icon": "🛡️",
     "desc": "ההבדל בין הנחיה מצילת חיים למדיניות התגוננות, מדרגי המדיניות וההגדרות המחייבות."},
    {"id": "authority", "title": "הרשות המקומית ומטה החירום", "icon": "🏛️",
     "desc": "מבנה הרשות המקומית, המכלולים, ומכלול המידע לציבור."},
    {"id": "population", "title": "מערך האוכלוסייה, כלים ופלטפורמות", "icon": "🧰",
     "desc": "מבנה מערך האוכלוסייה בפיקוד העורף, הקה\"א, והכלים הטכנולוגיים העומדים לרשות ההסברה."},
]

# doc_id -> (category_id, icon, order_in_category, short description)
DOC_META = {
    "01": ("population", "👥", 3, "תפקיד הקה\"א, מערך התנהגות אוכלוסייה, אוכלוסיות עם צרכים מיוחדים וקהילה בחירום."),
    "02": ("guidelines", "🚨", 1, "מהי הנחיה מצילת חיים, פלטפורמות ההפצה ותרחישים לדוגמה."),
    "03": ("theory", "📣", 1, "תשתית התנהגותית, המעגל הזהוב, מודל 4 השלבים ודוגמאות הנעה לפעולה."),
    "04": ("guidelines", "⚖️", 2, "הסמכות החוקית, מדרגי ההתגוננות וקריטריונים לקביעת המדיניות היומית."),
    "05": ("population", "🧩", 1, "ייעוד ומבנה מערך האוכלוסייה, נתוני \"שאגת האריה\" ועקרונות ההסברה."),
    "06": ("authority", "🏛️", 1, "אחריות, מבנה ארגוני, כשירויות וכלים להכנת הרשות המקומית לחירום."),
    "07": ("population", "🧰", 2, "מרכז המענה 104, פלטפורמות דיגיטליות, דסקים ייעודיים וניטור ברשות."),
    "08": ("authority", "📞", 2, "מבנה מכלול המידע לציבור, איוש, משימות וממשקים מול קצין ההסברה ביקל\"ר."),
    "10": ("theory", "🎯", 2, "שמונת עקרונות ההסברה, מודל האסטרטגיה, תיאום ציפיות וסמכויות הפצה."),
    "11": ("theory", "⚔️", 4, "לקחים מ\"עם כלביא\" ו\"שאגת האריה\": מוכנות, דיוק ותוצאה בשטח."),
    "12": ("role", "🎖️", 2, "תפקיד קצין ההסברה במחוז, בנפה וביקל\"ר: ניתוח אוכלוסייה, תיעדוף מאמץ ההסברה ומענה אופרטיבי בכל דרג."),
    "13": ("theory", "✅", 3, "עשרה עקרונות יסוד תמציתיים לדוברי רשויות ומנהלי מכלולי מידע לציבור."),
    "14": ("guidelines", "📋", 3, "מסמך המדיניות המלא: הגדרות, מדרגים לפי תחום, ונספחי הפעלה."),
    "09": ("role", "🧭", 1, "ייעוד ומבנה מערך ההסברה האורכי - מיחידת ההסברה הפיקודית ועד קצין ההסברה ביקל\"ר."),
}

DIGESTS = [
    {"id": "role", "icon": "🎖️", "title": "תפקיד קצין ההסברה",
     "desc": "מי קצין ההסברה, מה תפקידו בכל דרג, מודל אקטיבי מול פסיבי, וצ'קליסט.",
     "url": "digests/role.html"},
    {"id": "theory", "icon": "📚", "title": "עקרונות ותורת ההסברה",
     "desc": "הגדרת הסברה, המעגל הזהוב, עקרונות היסוד (גרסה מאוחדת) ומודל ההנעה לפעולה.",
     "url": "digests/theory.html"},
    {"id": "guidelines", "icon": "🛡️", "title": "הנחיות ומדיניות ההתגוננות",
     "desc": "ההבדל בין הנחיה מצילת חיים למדיניות, הסמכות החוקית, ותהליך קביעת המדיניות היומי.",
     "url": "digests/guidelines.html"},
    {"id": "authority", "icon": "🏛️", "title": "הרשות המקומית ומטה החירום",
     "desc": "שישה המכלולים, ומכלול המידע לציבור בפירוט - הממשק המרכזי שלך.",
     "url": "digests/authority.html"},
    {"id": "population", "icon": "🧰", "title": "מערך האוכלוסייה וכלים",
     "desc": "מבנה מערך האוכלוסייה, תפקיד הקה\"א, והכלים העומדים לרשות ההסברה.",
     "url": "digests/population.html"},
]

MD = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "toc"],
                        extension_configs={"toc": {"permalink": False}})

def header_html(root, active_cat=None):
    tabs = "\n      ".join(
        f'<a href="{root}digests/{d["id"]}.html" class="{"active" if d["id"] == active_cat else ""}">{d["icon"]} {d["title"]}</a>'
        for d in DIGESTS
    )
    return f"""<div class="site-head-wrap">
<header class="site-header">
  <div class="container bar">
    <a class="brand" href="{root}index.html">
      <span class="badge"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M12 2.6 19.6 5.4V11c0 4.9-3.2 8.4-7.6 10-4.4-1.6-7.6-5.1-7.6-10V5.4L12 2.6z"/><path d="M12 7.4l1.2 2.5 2.8.4-2 1.9.5 2.8-2.5-1.3-2.5 1.3.5-2.8-2-1.9 2.8-.4L12 7.4z" fill="currentColor" stroke="none"/></svg></span>
      <span>אתר הידע<br><small>קורס קציני הסברה 2026</small></span>
    </a>
    <nav class="main-nav">
      <a href="{root}index.html">בית</a>
      <a href="{root}quick-ref.html">מדריך מהיר</a>
      <a href="{root}acronyms.html">מילון קיצורים</a>
    </nav>
    <button class="nav-toggle" id="nav-toggle" aria-label="תפריט" aria-expanded="false">☰</button>
    <div class="search-box">
      <input id="site-search" type="text" placeholder='חיפוש באתר... (למשל: ממ"ד, מדרג כתום, קה"א)' autocomplete="off">
      <div id="search-results"></div>
    </div>
  </div>
</header>
<nav class="cat-tabs"><div class="inner">
      {tabs}
</div></nav>
</div>
<nav class="mobile-menu" id="mobile-menu"></nav>"""


TOPIC_TEMPLATE = """<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@500;700;900&display=swap" rel="stylesheet">
<link rel="icon" href="data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A//www.w3.org/2000/svg%27%20viewBox%3D%270%200%2024%2024%27%3E%3Crect%20width%3D%2724%27%20height%3D%2724%27%20rx%3D%275%27%20fill%3D%27%230e1f38%27/%3E%3Cpath%20d%3D%27M12%203.6%2018.4%206V11c0%204.3-2.8%207.3-6.4%208.7C8.4%2018.3%205.6%2015.3%205.6%2011V6L12%203.6z%27%20fill%3D%27none%27%20stroke%3D%27%23c0922f%27%20stroke-width%3D%271.3%27/%3E%3Cpath%20d%3D%27M12%207.8l1%202.1%202.3.3-1.7%201.6.4%202.3-2-1.1-2%201.1.4-2.3-1.7-1.6%202.3-.3%201-2.1z%27%20fill%3D%27%23c0922f%27/%3E%3C/svg%3E">
<title>{title} | אתר הידע - קורס קציני הסברה 2026</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body data-root="../">
{header}

<main class="container">
  <div class="breadcrumb"><a href="../index.html">בית</a> ← <a href="../index.html#cat-{cat_id}">{cat_title}</a> ← {title}</div>

  <div class="topic-layout">
    <aside class="topic-toc">
      <h4>בעמוד זה</h4>
      <ul>
        {toc}
      </ul>
    </aside>

    <article class="topic-content">
      <div class="topic-meta">
        <span class="pill">{cat_icon} {cat_title}</span>
        <span class="pill orange">{source_pages} שקפי מקור</span>
      </div>
      <div class="page-actions">
        <button data-print>🖨️ הדפס / שמור כ-PDF</button>
      </div>
      {body}

      <div class="topic-nav-footer">
        {prev_link}
        {next_link}
      </div>
    </article>
  </div>
</main>

<footer class="site-footer">
  <div class="container">
    אתר ידע פנימי לקורס קציני הסברה 2026 &middot; מבוסס על חומרי ההדרכה של המכללה הלאומית לאיתנות ישראלית ופיקוד העורף &middot; לשימוש פנימי בלבד
  </div>
</footer>
<script src="../assets/app.js"></script>
</body>
</html>
"""


def wrap_tables(html_body):
    return re.sub(r"(<table>.*?</table>)", r'<div class="table-scroll">\1</div>', html_body, flags=re.S)


def flatten_toc(tokens):
    flat = []
    for tok in tokens:
        flat.append(tok)
        if tok.get("children"):
            flat.extend(flatten_toc(tok["children"]))
    return flat


def slugify_anchor(text, used):
    base = re.sub(r"[^\w֐-׿\- ]", "", text).strip().replace(" ", "-")
    base = base or "section"
    slug = base
    i = 2
    while slug in used:
        slug = f"{base}-{i}"
        i += 1
    used.add(slug)
    return slug


def parse_doc(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    meta = {}
    body = raw
    if m:
        front, body = m.group(1), m.group(2)
        for line in front.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    return meta, body.strip()


def build():
    doc_ids = sorted(DOC_META.keys())
    docs = []
    for doc_id in doc_ids:
        path = os.path.join(SRC, f"{doc_id}-doc.md")
        if not os.path.exists(path):
            print(f"!! missing source for {doc_id}, skipping")
            continue
        meta, body = parse_doc(path)
        title = meta.get("title", f"מסמך {doc_id}")
        source_pages = meta.get("source_pages", "?")
        cat_id, icon, order, short_desc = DOC_META[doc_id]
        docs.append({
            "id": doc_id, "title": title, "source_pages": source_pages,
            "cat_id": cat_id, "icon": icon, "order": order, "short_desc": short_desc,
            "body_md": body,
        })

    # order within category
    docs.sort(key=lambda d: (d["cat_id"], d["order"]))

    cat_docs = {c["id"]: [] for c in CATEGORIES}
    for d in docs:
        cat_docs[d["cat_id"]].append(d)

    search_index = []

    os.makedirs(TOPICS_OUT, exist_ok=True)

    doc_list_in_order = docs  # for prev/next across whole site, grouped by category order

    for i, d in enumerate(doc_list_in_order):
        MD.reset()
        html_body = MD.convert(d["body_md"])
        toc_tokens = flatten_toc(MD.toc_tokens)

        used_anchors = set()
        toc_html_items = []
        # re-render anchors consistently: python-markdown toc already injects ids;
        # just read them from toc_tokens (level 2 and 3 only)
        for tok in toc_tokens:
            if tok["level"] not in (2, 3):
                continue
            indent_class = ' style="padding-right:14px;font-size:0.8rem;"' if tok["level"] == 3 else ""
            toc_html_items.append(
                f'<li{indent_class}><a href="#{tok["id"]}">{tok["name"]}</a></li>'
            )
            search_index.append({
                "title": tok["name"],
                "url": f"topics/{d['id']}.html#{tok['id']}",
                "section": d["title"],
                "docTitle": d["title"],
                "text": tok["name"],
            })

        cat = next(c for c in CATEGORIES if c["id"] == d["cat_id"])

        prev_link = ""
        next_link = ""
        if i > 0:
            p = doc_list_in_order[i - 1]
            prev_link = f'<a href="{p["id"]}.html">→ הקודם: {p["title"]}</a>'
        if i < len(doc_list_in_order) - 1:
            n = doc_list_in_order[i + 1]
            next_link = f'<a href="{n["id"]}.html">הבא: {n["title"]} ←</a>'

        html = TOPIC_TEMPLATE.format(
            title=d["title"],
            desc=d["short_desc"],
            cat_id=cat["id"],
            cat_title=cat["title"],
            cat_icon=cat["icon"],
            source_pages=d["source_pages"],
            toc="\n        ".join(toc_html_items),
            body=wrap_tables(html_body),
            prev_link=prev_link,
            next_link=next_link,
            header=header_html("../", active_cat=cat["id"]),
        )
        out_path = os.path.join(TOPICS_OUT, f"{d['id']}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"wrote {out_path}")

        # also index the doc title itself
        search_index.append({
            "title": d["title"],
            "url": f"topics/{d['id']}.html",
            "section": cat["title"],
            "docTitle": d["title"],
            "text": d["title"] + " " + d["short_desc"],
        })

    # index the hand-authored digest pages too
    for d in DIGESTS:
        path = os.path.join(ROOT, d["url"])
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            digest_html = f.read()
        search_index.append({
            "title": d["title"], "url": d["url"], "section": "תמצית",
            "docTitle": d["title"], "text": d["title"] + " " + d["desc"],
        })
        for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', digest_html, re.S):
            heading = re.sub(r"<[^>]+>", "", m.group(2)).strip()
            search_index.append({
                "title": heading, "url": f"{d['url']}#{m.group(1)}",
                "section": d["title"], "docTitle": d["title"], "text": heading,
            })

    # index the acronyms glossary page
    acr_path = os.path.join(ROOT, "acronyms.html")
    if os.path.exists(acr_path):
        with open(acr_path, encoding="utf-8") as f:
            acr_html = f.read()
        search_index.append({
            "title": "מילון ראשי תיבות", "url": "acronyms.html", "section": "מילון",
            "docTitle": "מילון ראשי תיבות", "text": "מילון ראשי תיבות קיצורים פקע\"ר יקל\"ר ממ\"ד",
        })
        for m in re.finditer(r'<h3 id="([^"]+)">(.*?)</h3>', acr_html, re.S):
            heading = re.sub(r"<[^>]+>", "", m.group(2)).strip()
            search_index.append({
                "title": heading, "url": f"acronyms.html#{m.group(1)}",
                "section": "מילון ראשי תיבות", "docTitle": "מילון ראשי תיבות", "text": heading,
            })
        for m in re.finditer(r"<td><b>(.*?)</b></td><td>(.*?)</td>", acr_html.replace("\n", "")):
            abbr = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            mean = re.sub(r"<[^>]+>", "", m.group(2)).strip()
            search_index.append({
                "title": f"{abbr} - {mean}", "url": "acronyms.html",
                "section": "מילון ראשי תיבות", "docTitle": "מילון ראשי תיבות", "text": abbr + " " + mean,
            })

    with open(os.path.join(ROOT, "search-index.json"), "w", encoding="utf-8") as f:
        json.dump(search_index, f, ensure_ascii=False)
    print(f"wrote search-index.json ({len(search_index)} entries)")

    write_index(CATEGORIES, cat_docs, len(docs))

    return CATEGORIES, cat_docs


INDEX_TEMPLATE = """<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@500;700;900&display=swap" rel="stylesheet">
<link rel="icon" href="data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A//www.w3.org/2000/svg%27%20viewBox%3D%270%200%2024%2024%27%3E%3Crect%20width%3D%2724%27%20height%3D%2724%27%20rx%3D%275%27%20fill%3D%27%230e1f38%27/%3E%3Cpath%20d%3D%27M12%203.6%2018.4%206V11c0%204.3-2.8%207.3-6.4%208.7C8.4%2018.3%205.6%2015.3%205.6%2011V6L12%203.6z%27%20fill%3D%27none%27%20stroke%3D%27%23c0922f%27%20stroke-width%3D%271.3%27/%3E%3Cpath%20d%3D%27M12%207.8l1%202.1%202.3.3-1.7%201.6.4%202.3-2-1.1-2%201.1.4-2.3-1.7-1.6%202.3-.3%201-2.1z%27%20fill%3D%27%23c0922f%27/%3E%3C/svg%3E">
<title>אתר הידע - קורס קציני הסברה 2026</title>
<meta name="description" content="אתר ידע פנימי לקורס קציני הסברה 2026 - עקרונות הסברה, הנחיות מצילות חיים, מדיניות ההתגוננות, מבנה הרשות המקומית ומערך האוכלוסייה.">
<link rel="stylesheet" href="assets/style.css">
</head>
<body data-root="./">
{header}

<div class="hero">
  <div class="container">
    <h1>חומר הדרכה לקורס קציני הסברה 2026</h1>
    <p>חמש תמציות ממוקדות - מה שבאמת צריך לדעת. לעיון מעמיק בכל שקף מהמקור, ראו את ארכיון המצגות בתחתית העמוד.</p>
    <div class="stats">
      <div class="stat"><b>5</b><span>תמציות מאוחדות</span></div>
      <div class="stat"><b>{n_docs}</b><span>מצגות מקור בארכיון</span></div>
      <div class="stat"><b>{n_sections}</b><span>סעיפים חיפושיים</span></div>
    </div>
    <div class="quicklinks">
      <a href="quick-ref.html">📌 מדריך מהיר</a>
      <a href="acronyms.html">📖 מילון קיצורים</a>
      <a href="digests/role.html">🎖️ תפקיד הקצין</a>
      <a href="digests/guidelines.html">🛡️ הנחיות ומדיניות</a>
    </div>
  </div>
</div>

<main class="container">
  <h2 class="section-title" id="digests"><span class="n">★</span>תמציות - התחילו כאן</h2>
  <p style="color:var(--text-muted);margin-top:-8px;max-width:760px;">לכל תמצית 2-4 מצגות מקור, מאוחדות לעמוד אחד קצר וממוקד, עם קישור למקורות המלאים בתחתית העמוד.</p>
  <div class="cards-grid">
    {digest_cards}
  </div>

  <h2 class="section-title" id="archive" style="margin-top:56px;">📚 ארכיון מצגות המקור</h2>
  <p style="color:var(--text-muted);margin-top:-8px;max-width:760px;">14 המצגות המקוריות, שקף אחרי שקף - לעיון מעמיק, אימות ציטוט מדויק או הכנת שיעור. לקריאה ראשונה מומלץ להתחיל בתמציות שלמעלה.</p>
  {categories}
</main>

<footer class="site-footer">
  <div class="container">
    אתר ידע פנימי לקורס קציני הסברה 2026 &middot; מבוסס על חומרי ההדרכה של המכללה הלאומית לאיתנות ישראלית ופיקוד העורף &middot; לשימוש פנימי בלבד
  </div>
</footer>
<script src="assets/app.js"></script>
</body>
</html>
"""

CARD_TEMPLATE = """<a class="card-link-wrap" href="topics/{id}.html" style="text-decoration:none;color:inherit;">
<div class="card" style="opacity:0.88;">
  <div class="icon">{icon}</div>
  <h3 style="font-size:0.96rem;">{title}</h3>
  <p style="font-size:0.82rem;">{desc}</p>
  <div class="meta">{pages} שקפי מקור · מקור מלא</div>
  <span class="card-link">פתח מקור ←</span>
</div>
</a>"""

DIGEST_CARD_TEMPLATE = """<a class="card-link-wrap" href="{url}" style="text-decoration:none;color:inherit;">
<div class="card" style="border-right:4px solid var(--orange);">
  <div class="icon">{icon}</div>
  <h3>{title}</h3>
  <p>{desc}</p>
  <span class="card-link">קרא את התמצית ←</span>
</div>
</a>"""


def write_index(categories, cat_docs, n_docs):
    search_index_len = 0
    si_path = os.path.join(ROOT, "search-index.json")
    if os.path.exists(si_path):
        with open(si_path, encoding="utf-8") as f:
            search_index_len = len(json.load(f))

    cat_blocks = []
    for idx, c in enumerate(categories, start=1):
        docs = cat_docs.get(c["id"], [])
        if not docs:
            continue
        cards = "\n".join(
            CARD_TEMPLATE.format(id=d["id"], icon=d["icon"], title=d["title"],
                                  desc=d["short_desc"], pages=d["source_pages"])
            for d in docs
        )
        body_id = f"archive-body-{c['id']}"
        cat_blocks.append(f"""
  <div class="archive-group" id="cat-{c['id']}">
    <button class="archive-toggle" aria-expanded="false" aria-controls="{body_id}">
      <span class="n" style="background:var(--navy);">{idx}</span>
      <span>{c['icon']} {c['title']}</span>
      <span class="chev">▾</span>
    </button>
    <div class="archive-body" id="{body_id}">
      <p style="color:var(--text-muted);margin-top:0;max-width:760px;">{c['desc']}</p>
      <div class="cards-grid">
        {cards}
      </div>
    </div>
  </div>
""")

    digest_cards = "\n".join(
        DIGEST_CARD_TEMPLATE.format(url=d["url"], icon=d["icon"], title=d["title"], desc=d["desc"])
        for d in DIGESTS
    )

    html = INDEX_TEMPLATE.format(
        n_docs=n_docs,
        n_sections=search_index_len,
        digest_cards=digest_cards,
        categories="\n".join(cat_blocks),
        header=header_html("./"),
    )
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote index.html")


if __name__ == "__main__":
    build()
