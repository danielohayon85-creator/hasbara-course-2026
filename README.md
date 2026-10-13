# המסבירון - קורס קציני הסברה 2026

אתר סטטי (HTML/CSS/JS) עם חומר הדרכה מאורגן לקורס קציני הסברה: תפקיד הקצין, עקרונות ותורת ההסברה, הנחיות מצילות חיים ומדיניות ההתגוננות, הרשות המקומית ומערך האוכלוסייה.

## מבנה

- `index.html`, `quick-ref.html`, `acronyms.html` - עמודי שער
- `digests/` - 5 עמודי סיכום מאוחדים (נקודת הכניסה המומלצת)
- `topics/` - ארכיון 17 המצגות המקוריות, שקף אחרי שקף
- `content-source/` - התמלולים הגולמיים (Markdown) שמהם נוצרים עמודי `topics/`
- `assets/` - CSS ו-JS
- `build.py` - מייצר את `topics/*.html` ו-`index.html` מתוך `content-source/*.md`. הרצה: `python3 build.py`
- `serve.py` - שרת Flask קטן להגשת האתר (לפריסה ב-Render וכדומה)

## פריסה

**Render:** מחובר ל-`render.yaml` בשורש הריפו - שירות Python שמריץ `gunicorn serve:app`.

**Netlify / כל אחסון סטטי אחר:** אין צורך ב-`serve.py` - פשוט מעלים את כל התוכן (למעט `content-source/`, `build.py`, `serve.py`, `render.yaml`, `requirements.txt` שאינם נחוצים להגשה).

לשימוש פנימי בלבד.
