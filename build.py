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

MD = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "toc"],
                        extension_configs={"toc": {"permalink": False}})

TOPIC_TEMPLATE = """<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | אתר הידע - קורס קציני הסברה 2026</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body data-root="../">
<header class="site-header">
  <div class="container bar">
    <a class="brand" href="../index.html">
      <span class="badge">🎖️</span>
      <span>אתר הידע<br><small>קורס קציני הסברה 2026</small></span>
    </a>
    <nav class="main-nav">
      <a href="../index.html">בית</a>
      <a href="../quick-ref.html">מדריך מהיר</a>
    </nav>
    <div class="search-box">
      <input id="site-search" type="text" placeholder="חיפוש באתר... (למשל: ממ\\"ד, מדרג כתום, קה\\"א)" autocomplete="off">
      <div id="search-results"></div>
    </div>
  </div>
</header>

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
            body=html_body,
            prev_link=prev_link,
            next_link=next_link,
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
<title>אתר הידע - קורס קציני הסברה 2026</title>
<meta name="description" content="אתר ידע פנימי לקורס קציני הסברה 2026 - עקרונות הסברה, הנחיות מצילות חיים, מדיניות ההתגוננות, מבנה הרשות המקומית ומערך האוכלוסייה.">
<link rel="stylesheet" href="assets/style.css">
</head>
<body data-root="./">
<header class="site-header">
  <div class="container bar">
    <a class="brand" href="index.html">
      <span class="badge">🎖️</span>
      <span>אתר הידע<br><small>קורס קציני הסברה 2026</small></span>
    </a>
    <nav class="main-nav">
      <a href="index.html" class="active">בית</a>
      <a href="quick-ref.html">מדריך מהיר</a>
    </nav>
    <div class="search-box">
      <input id="site-search" type="text" placeholder="חיפוש באתר... (למשל: ממ\\"ד, מדרג כתום, קה\\"א)" autocomplete="off">
      <div id="search-results"></div>
    </div>
  </div>
</header>

<div class="hero">
  <div class="container">
    <h1>חומר הדרכה לקורס קציני הסברה 2026</h1>
    <p>מרכז ידע אחד לכל חומרי ההדרכה: תפקיד קצין ההסברה, עקרונות ותורת ההסברה, הנחיות מצילות חיים ומדיניות ההתגוננות, הרשות המקומית ומערך האוכלוסייה בפיקוד העורף.</p>
    <div class="stats">
      <div class="stat"><b>{n_docs}</b><span>מצגות מקור</span></div>
      <div class="stat"><b>5</b><span>תחומי ידע</span></div>
      <div class="stat"><b>{n_sections}</b><span>סעיפים חיפושיים</span></div>
    </div>
    <div class="quicklinks">
      <a href="quick-ref.html">📌 מדריך מהיר / מילון מונחים</a>
      <a href="#cat-role">🎖️ תפקיד הקצין</a>
      <a href="#cat-guidelines">🛡️ הנחיות ומדיניות</a>
    </div>
  </div>
</div>

<main class="container">
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
<div class="card">
  <div class="icon">{icon}</div>
  <h3>{title}</h3>
  <p>{desc}</p>
  <div class="meta">{pages} שקפי מקור</div>
  <span class="card-link">קרא עוד ←</span>
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
        cat_blocks.append(f"""
  <h2 class="section-title" id="cat-{c['id']}"><span class="n">{idx}</span>{c['icon']} {c['title']}</h2>
  <p style="color:var(--text-muted);margin-top:-8px;max-width:760px;">{c['desc']}</p>
  <div class="cards-grid">
    {cards}
  </div>
""")

    html = INDEX_TEMPLATE.format(
        n_docs=n_docs,
        n_sections=search_index_len,
        categories="\n".join(cat_blocks),
    )
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote index.html")


if __name__ == "__main__":
    build()
