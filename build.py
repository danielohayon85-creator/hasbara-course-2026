#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
בונה את המסבירון (אתר סטטי) מתוך content-source/*.md
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
    {"id": "role", "title": "תפקיד קצין ההסברה", "icon": "role",
     "desc": "מי קצין ההסברה, מה תפקידו בכל דרג, וכיצד הוא פועל מול הרשות המקומית."},
    {"id": "theory", "title": "עקרונות ותורת ההסברה", "icon": "theory",
     "desc": "מהי הסברה, המודלים המרכזיים, עקרונות היסוד ולקחים מהשטח."},
    {"id": "guidelines", "title": "הנחיות מצילות חיים ומדיניות ההתגוננות", "icon": "guidelines",
     "desc": "ההבדל בין הנחיה מצילת חיים למדיניות התגוננות, מדרגי המדיניות וההגדרות המחייבות."},
    {"id": "authority", "title": "הרשות המקומית ומטה החירום", "icon": "authority",
     "desc": "מבנה הרשות המקומית, המכלולים, ומכלול המידע לציבור."},
    {"id": "population", "title": "מערך האוכלוסייה, כלים ופלטפורמות", "icon": "population",
     "desc": "מבנה מערך האוכלוסייה בפיקוד העורף, הקה\"א, והכלים הטכנולוגיים העומדים לרשות ההסברה."},
]

# doc_id -> (category_id, icon, order_in_category, short description)
DOC_META = {
    "01": ("population", "people", 3, "תפקיד הקה\"א, מערך התנהגות אוכלוסייה, אוכלוסיות עם צרכים מיוחדים וקהילה בחירום."),
    "02": ("guidelines", "alert", 1, "מהי הנחיה מצילת חיים, פלטפורמות ההפצה ותרחישים לדוגמה."),
    "03": ("theory", "megaphone", 1, "תשתית התנהגותית, המעגל הזהוב, מודל 4 השלבים ודוגמאות הנעה לפעולה."),
    "04": ("guidelines", "scale", 2, "הסמכות החוקית, מדרגי ההתגוננות וקריטריונים לקביעת המדיניות היומית."),
    "05": ("population", "puzzle", 1, "ייעוד ומבנה מערך האוכלוסייה, נתוני \"שאגת האריה\" ועקרונות ההסברה."),
    "06": ("authority", "authority", 1, "אחריות, מבנה ארגוני, כשירויות וכלים להכנת הרשות המקומית לחירום."),
    "07": ("population", "population", 2, "מרכז המענה 104, פלטפורמות דיגיטליות, דסקים ייעודיים וניטור ברשות."),
    "08": ("authority", "phone", 2, "מבנה מכלול המידע לציבור, איוש, משימות וממשקים מול קצין ההסברה ביקל\"ר."),
    "10": ("theory", "target", 2, "שמונת עקרונות ההסברה, מודל האסטרטגיה, תיאום ציפיות וסמכויות הפצה."),
    "11": ("theory", "swords", 4, "לקחים מ\"עם כלביא\" ו\"שאגת האריה\": מוכנות, דיוק ותוצאה בשטח."),
    "12": ("role", "role", 2, "תפקיד קצין ההסברה במחוז, בנפה וביקל\"ר: ניתוח אוכלוסייה, תיעדוף מאמץ ההסברה ומענה אופרטיבי בכל דרג."),
    "13": ("theory", "checkcircle", 3, "עשרה עקרונות יסוד תמציתיים לדוברי רשויות ומנהלי מכלולי מידע לציבור."),
    "14": ("guidelines", "clipboard", 3, "מסמך המדיניות המלא: הגדרות, מדרגים לפי תחום, ונספחי הפעלה."),
    "09": ("role", "compass", 1, "ייעוד ומבנה מערך ההסברה האורכי - מיחידת ההסברה הפיקודית ועד קצין ההסברה ביקל\"ר."),
}

DIGESTS = [
    {"id": "role", "icon": "role", "title": "תפקיד קצין ההסברה",
     "desc": "מי קצין ההסברה, מה תפקידו בכל דרג, מודל אקטיבי מול פסיבי, וצ'קליסט.",
     "url": "digests/role.html"},
    {"id": "theory", "icon": "theory", "title": "עקרונות ותורת ההסברה",
     "desc": "הגדרת הסברה, המעגל הזהוב, עקרונות היסוד ומודל ההנעה לפעולה.",
     "url": "digests/theory.html"},
    {"id": "guidelines", "icon": "guidelines", "title": "הנחיות ומדיניות ההתגוננות",
     "desc": "ההבדל בין הנחיה מצילת חיים למדיניות, הסמכות החוקית, ותהליך קביעת המדיניות היומי.",
     "url": "digests/guidelines.html"},
    {"id": "authority", "icon": "authority", "title": "הרשות המקומית ומטה החירום",
     "desc": "שישה המכלולים, ומכלול המידע לציבור בפירוט - הממשק המרכזי שלך.",
     "url": "digests/authority.html"},
    {"id": "population", "icon": "population", "title": "מערך האוכלוסייה וכלים",
     "desc": "מבנה מערך האוכלוסייה, תפקיד הקה\"א, והכלים העומדים לרשות ההסברה.",
     "url": "digests/population.html"},
]

MD = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "toc"],
                        extension_configs={"toc": {"permalink": False}})

# ספריית אייקוני SVG אחידה (קו, currentColor) שמחליפה את האימוג'ים -
# אותו שפה ויזואלית בכל מקום באתר, במקום תמהיל אקראי של סמלי מערכת ההפעלה.
ICON_PATHS = {
    "role": '<path d="M12 2.6 19.6 5.4V11c0 4.9-3.2 8.4-7.6 10-4.4-1.6-7.6-5.1-7.6-10V5.4L12 2.6z"/>'
            '<path d="M12 7.4l1.2 2.5 2.8.4-2 1.9.5 2.8-2.5-1.3-2.5 1.3.5-2.8-2-1.9 2.8-.4L12 7.4z" fill="currentColor" stroke="none"/>',
    "theory": '<path d="M4 5.6c1.8-1 4.3-1 8 .6 3.7-1.6 6.2-1.6 8-.6v13c-1.8-1-4.3-1-8 .6-3.7-1.6-6.2-1.6-8-.6v-13z"/><path d="M12 6.2v13"/>',
    "guidelines": '<path d="M12 2.6 19.6 5.4V11c0 4.9-3.2 8.4-7.6 10-4.4-1.6-7.6-5.1-7.6-10V5.4L12 2.6z"/><path d="M8.6 11.6l2.3 2.3 4.4-4.6"/>',
    "authority": '<path d="M3 9.2 12 4l9 5.2"/><path d="M4.3 9.6V20M19.7 9.6V20"/><path d="M7.6 9.6V20M11 9.6V20M13 9.6V20M16.4 9.6V20"/><path d="M3 20h18"/>',
    "population": '<rect x="3" y="9.5" width="18" height="10" rx="1.5"/><path d="M8.2 9.5V6.8A1.8 1.8 0 0 1 10 5h4a1.8 1.8 0 0 1 1.8 1.8v2.7"/><path d="M3 14h18"/>',
    "people": '<circle cx="9" cy="8.2" r="2.4"/><path d="M3.8 19c0-3 2.3-5.2 5.2-5.2s5.2 2.2 5.2 5.2"/><circle cx="17" cy="9.4" r="2"/><path d="M14.8 19c.2-2.4 1.7-4.2 3.6-4.6"/>',
    "alert": '<path d="M12 4.2 21 20H3L12 4.2z"/><path d="M12 10.2v3.8"/><circle cx="12" cy="16.6" r="0.9" fill="currentColor" stroke="none"/>',
    "megaphone": '<path d="M3 10v4h3l9 4V6l-9 4H3z"/><path d="M18.2 9a4.2 4.2 0 0 1 0 6"/>',
    "scale": '<path d="M12 3v18"/><path d="M6.5 7h11"/><path d="M8.6 21h6.8"/><path d="M6.5 7l-3 5.6a3 3 0 0 0 6 0L6.5 7z"/><path d="M17.5 7l-3 5.6a3 3 0 0 0 6 0L17.5 7z"/>',
    "puzzle": '<path d="M4 9h3.3a1.5 1.5 0 1 1 0 3H4v6h6v-3.3a1.5 1.5 0 1 1 3 0V18h6v-6h-3.3a1.5 1.5 0 1 1 0-3H19V4h-6v3.3a1.5 1.5 0 1 1-3 0V4H4v5z"/>',
    "phone": '<path d="M5 4h3.2l1.3 4.4-2 1.6a12 12 0 0 0 6.5 6.5l1.6-2 4.4 1.3V19a2 2 0 0 1-2 2C10.8 21 3 13.2 3 6a2 2 0 0 1 2-2z"/>',
    "target": '<circle cx="12" cy="12" r="8.6"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="currentColor" stroke="none"/>',
    "swords": '<path d="M4 4l16 16M20 4L4 20"/><path d="M4 4l2.6.3M20 4l-2.6.3M4 20l2.6-.3M20 20l-2.6-.3"/>',
    "checkcircle": '<circle cx="12" cy="12" r="9"/><path d="M7.5 12.4l3 3 6-6.4"/>',
    "clipboard": '<rect x="5" y="4.6" width="14" height="17" rx="2"/><rect x="9" y="3" width="6" height="3" rx="1"/><path d="M8.5 11h7M8.5 14.5h7M8.5 18h4.5"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.4 8.6l-2 5-5 2 2-5 5-2z" fill="currentColor" stroke="none"/>',
    "pulse": '<path d="M3 12h4l2-6.5 4 13 2-6.5h6"/>',
    "monitor": '<rect x="3" y="4.2" width="18" height="12.4" rx="1.5"/><path d="M8 20h8M12 16.6v3.4"/>',
    "mobile": '<rect x="7.3" y="2.5" width="9.4" height="19" rx="2"/><path d="M11 18.2h2"/>',
    "media": '<rect x="3" y="7" width="13" height="11" rx="1.5"/><path d="M16 10.4l5-2.4v9l-5-2.4"/>',
    "printer": '<path d="M6.2 9V4.2h11.6V9"/><rect x="4.5" y="9" width="15" height="7" rx="1.5"/><rect x="7" y="14" width="10" height="7" rx="1"/>',
    "pin": '<path d="M12 2a5 5 0 0 0-5 5c0 3.5 5 10 5 10s5-6.5 5-10a5 5 0 0 0-5-5z"/><circle cx="12" cy="7" r="1.8" fill="currentColor" stroke="none"/>',
    "home": '<path d="M4 11.2 12 4l8 7.2"/><path d="M6 10v10h5v-6h2v6h5V10"/>',
    "star": '<path d="M12 3.5l2.4 5 5.5.6-4.1 3.8 1.1 5.4L12 15.8l-4.9 2.5 1.1-5.4-4.1-3.8 5.5-.6L12 3.5z" fill="currentColor" stroke="none"/>',
}


def icon(name, size=None):
    style = f' style="width:{size};height:{size}"' if size else ""
    return (f'<svg class="icn" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"{style} aria-hidden="true">'
            f'{ICON_PATHS[name]}</svg>')

def header_html(root, active_cat=None):
    tabs = "\n      ".join(
        f'<a href="{root}digests/{d["id"]}.html" class="{"active" if d["id"] == active_cat else ""}">{icon(d["icon"])} {d["title"]}</a>'
        for d in DIGESTS
    )
    return f"""<div class="site-head-wrap">
<header class="site-header">
  <div class="container bar">
    <a class="brand" href="{root}index.html">
      <span class="badge"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M12 2.6 19.6 5.4V11c0 4.9-3.2 8.4-7.6 10-4.4-1.6-7.6-5.1-7.6-10V5.4L12 2.6z"/><path d="M12 7.4l1.2 2.5 2.8.4-2 1.9.5 2.8-2.5-1.3-2.5 1.3.5-2.8-2-1.9 2.8-.4L12 7.4z" fill="currentColor" stroke="none"/></svg></span>
      <span>המסבירון<br><small>קורס קציני הסברה 2026</small></span>
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
<title>{title} | המסבירון - קורס קציני הסברה 2026</title>
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
        <button data-print>{icon_print} הדפס / שמור כ-PDF</button>
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
    המסבירון - אתר הידע הפנימי לקורס קציני הסברה 2026 &middot; מבוסס על חומרי ההדרכה של המכללה הלאומית לאיתנות ישראלית ופיקוד העורף &middot; לשימוש פנימי בלבד
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
        cat_id, icon_key, order, short_desc = DOC_META[doc_id]
        docs.append({
            "id": doc_id, "title": title, "source_pages": source_pages,
            "cat_id": cat_id, "icon": icon_key, "order": order, "short_desc": short_desc,
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
            cat_icon=icon(cat["icon"]),
            icon_print=icon("printer"),
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
            "title": d["title"], "url": d["url"], "section": "סיכום",
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
<title>המסבירון - קורס קציני הסברה 2026</title>
<meta name="description" content="המסבירון - אתר הידע הפנימי לקורס קציני הסברה 2026 - עקרונות הסברה, הנחיות מצילות חיים, מדיניות ההתגוננות, מבנה הרשות המקומית ומערך האוכלוסייה.">
<link rel="stylesheet" href="assets/style.css">
</head>
<body data-root="./">
{header}

<div class="hero">
  <div class="container">
    <h1>כל מה שקצין הסברה צריך לדעת - במקום אחד</h1>
    <p>חמש סיכומים ממוקדים - מה שבאמת צריך לדעת. לעיון מעמיק בכל שקף מהמקור, ראו את ארכיון המצגות בתחתית העמוד.</p>
    <div class="stats">
      <div class="stat"><b>5</b><span>סיכומים מאוחדים</span></div>
      <div class="stat"><b>{n_docs}</b><span>מצגות מקור בארכיון</span></div>
      <div class="stat"><b>{n_sections}</b><span>סעיפים חיפושיים</span></div>
    </div>
    <div class="quicklinks">
      <a href="quick-ref.html">{icon_pin} מדריך מהיר</a>
      <a href="acronyms.html">{icon_book} מילון קיצורים</a>
      <a href="digests/role.html">{icon_role} תפקיד הקצין</a>
      <a href="digests/guidelines.html">{icon_guidelines} הנחיות ומדיניות</a>
    </div>
  </div>
</div>

<main class="container">
  <h2 class="section-title" id="digests"><span class="n">{icon_star}</span>התחילו כאן: חמש סיכומים</h2>
  <p style="color:var(--text-muted);margin-top:-8px;max-width:760px;">לכל סיכום 2-4 מצגות מקור, מאוחדות לעמוד אחד קצר וממוקד, עם קישור למקורות המלאים בתחתית העמוד.</p>
  <div class="cards-grid">
    {digest_cards}
  </div>

  <a class="spotlight-card" href="topics/03.html">
    <div class="spotlight-badge">{icon_star_badge} הרצאה מומלצת</div>
    <h3>הסברה בחירום - אתגרים והנעה לפעולה</h3>
    <p class="spotlight-author">סא"ל (במיל') שירן שמחי</p>
    <p class="spotlight-desc">מודל מובנה בארבע שאלות להנעה לפעולה - מי קהל היעד, מה הצרכים, מה המסר ואילו ערוצי הפצה - עם דוגמאות אמיתיות מהשטח, שכונה אחר שכונה.</p>
    <span class="spotlight-link">צפו בהרצאה המלאה ←</span>
  </a>

  <h2 class="section-title" id="archive" style="margin-top:56px;">{icon_book2} ארכיון מצגות המקור</h2>
  <p style="color:var(--text-muted);margin-top:-8px;max-width:760px;">14 המצגות המקוריות, שקף אחרי שקף - לעיון מעמיק, אימות ציטוט מדויק או הכנת שיעור. לקריאה ראשונה מומלץ להתחיל בסיכומים שלמעלה.</p>
  {categories}
</main>

<footer class="site-footer">
  <div class="container">
    המסבירון - אתר הידע הפנימי לקורס קציני הסברה 2026 &middot; מבוסס על חומרי ההדרכה של המכללה הלאומית לאיתנות ישראלית ופיקוד העורף &middot; לשימוש פנימי בלבד
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
  <span class="card-link">קרא את הסיכום ←</span>
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
            CARD_TEMPLATE.format(id=d["id"], icon=icon(d["icon"]), title=d["title"],
                                  desc=d["short_desc"], pages=d["source_pages"])
            for d in docs
        )
        body_id = f"archive-body-{c['id']}"
        cat_blocks.append(f"""
  <div class="archive-group" id="cat-{c['id']}">
    <button class="archive-toggle" aria-expanded="false" aria-controls="{body_id}">
      <span class="n" style="background:var(--navy);">{idx}</span>
      <span>{icon(c['icon'])} {c['title']}</span>
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
        DIGEST_CARD_TEMPLATE.format(url=d["url"], icon=icon(d["icon"]), title=d["title"], desc=d["desc"])
        for d in DIGESTS
    )

    html = INDEX_TEMPLATE.format(
        n_docs=n_docs,
        n_sections=search_index_len,
        digest_cards=digest_cards,
        categories="\n".join(cat_blocks),
        header=header_html("./"),
        icon_pin=icon("pin"),
        icon_book=icon("theory"),
        icon_role=icon("role"),
        icon_guidelines=icon("guidelines"),
        icon_star=icon("star", size="13px"),
        icon_star_badge=icon("star", size="14px"),
        icon_book2=icon("theory"),
    )
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote index.html")


if __name__ == "__main__":
    build()
