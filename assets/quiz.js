// מבחן תרגול ובוחן השבוע - קורס קציני הסברה 2026
(function () {
  var CATEGORIES = {
    role: "תפקיד קצין ההסברה",
    theory: "עקרונות ותורת ההסברה",
    guidelines: "הנחיות ומדיניות ההתגוננות",
    authority: "הרשות המקומית ומטה החירום",
    population: "מערך האוכלוסייה וכלים"
  };

  // type: "concept" (ידע/מושג) או "scenario" (יישום התו"ל - מקרה בוחן)
  var QUESTIONS = [
    {
      cat: "role", type: "concept",
      q: 'מי מוסמך לקבוע את תוכן המסרים וההנחיות הרשמיות של פיקוד העורף?',
      options: ['קצין ההסברה ביקל"ר', 'דובר הרשות המקומית', 'יחידת ההסברה הפיקודית בלבד', 'מכלול מידע לציבור'],
      correct: 2,
      explain: 'הסמכות לקביעת תוכן המסרים וההנחיות הרשמיות היא בלעדית ליחידת ההסברה הפיקודית. אסור להפיץ או לערוך מסרי פקע"ר ברמת מחוז/נפה/יקל"ר ללא אישור פיקודי - גם לא סרטונים מהשטח.'
    },
    {
      cat: "role", type: "scenario",
      q: 'קצין הסברה ביקל"ר צילם סרטון קצר ומוצלח מהשטח המסביר הנחיית מיגון, ורוצה להעלות אותו מיד לעמוד הפייסבוק של הרשות. מה הפעולה הנכונה?',
      options: ['להעלות מיד - זה מידע מועיל לציבור', 'להעלות רק לאחר אישור פיקודי לתוכן', 'לשלוח לדובר הרשות בלבד, בלי אישור נוסף', 'לא להעלות תוכן מהשטח בשום מקרה'],
      correct: 1,
      explain: 'גם תוכן טוב ומועיל מהשטח טעון אישור פיקודי לפני פרסום - הסמכות לתוכן מסרים נשארת בלעדית ליחידת ההסברה הפיקודית, ללא קשר לאיכות התוצר או לכוונה הטובה.'
    },
    {
      cat: "role", type: "concept",
      q: 'מהו הממשק המרכזי ביותר שעל קצין ההסברה ביקל"ר לבנות בו אמון ועבודת שגרה?',
      options: ['מוקד 104', 'דובר הרשות המקומית', "קה\"א הארצי", 'יחידת ההסברה הפיקודית'],
      correct: 1,
      explain: 'דובר הרשות המקומית הוא הממשק המרכזי ביותר של קצין ההסברה ביקל"ר - נדרשת היכרות הדוקה ועבודה בשגרה על בניית אמון ותיאום מוקדם, עוד לפני שפורץ אירוע.'
    },
    {
      cat: "role", type: "scenario",
      q: 'קצינת הסברה חדשה ברשות דוחה את פגישת ההיכרות עם מפקד היקל"ר ודובר הרשות ל"אחרי האירוע הראשון", כדי "להתמקד בדברים הדחופים". מה הבעיה בגישה הזו?',
      options: ['אין בעיה - זה תעדוף נכון של זמן', 'ההיכרות עם בעלי התפקידים צריכה לקרות לפני אירוע ולא בזמנו - זה בדיוק מה שהבדיל בין המודל האקטיבי לפסיבי בדוגמאות מהשטח', 'פגישות היכרות הן רק פרוטוקול מיותר', 'מפקד היקל"ר אינו גורם רלוונטי לעבודת קצין ההסברה'],
      correct: 1,
      explain: 'בהשוואת "גילי" (המודל האקטיבי) מול "שירה" (הכנה מוגבלת) - ההבדל המכריע היה תיאום ציפיות ובניית ממשקים בשגרה, לפני שיש אירוע לנהל. דחיית ההיכרות היא בדיוק הדפוס הפסיבי שמוביל לנתק מקצועי.'
    },
    {
      cat: "role", type: "concept",
      q: 'מי אחראי לגבש ולתחזק תמונת מצב הסברה ברמת המאקרו (אזורים גיאוגרפיים וקהילות) במחוז?',
      options: ['קצין הסברה ביקל"ר', 'קצין הסברה במחוז', 'דובר הרשות המקומית', "קה\"א בנפה"],
      correct: 1,
      explain: 'קצין ההסברה במחוז מחזיק ומתקף תיק נתונים מחוזי כללי ברמת ניתוח אוכלוסייה מאקרו, בעוד שהיקל"ר מדייק את תמונת המצב ברמה המקומית הספציפית.'
    },
    {
      cat: "role", type: "concept",
      q: 'מהו ההבדל המהותי בין "דוברות" ל"הסברה"?',
      options: ['אין הבדל אמיתי - זה אותו תפקיד בשני שמות', 'דוברות מכוונת למיצוב ואמון הציבור בצה"ל; הסברה מכוונת להצלת חיים באמצעות הנעה להתנהגות לפי הנחיות פיקוד העורף', 'דוברות עוסקת רק ברשתות חברתיות, הסברה רק בטלוויזיה', 'דוברות היא תפקיד של קצין הסברה ביקל"ר'],
      correct: 1,
      explain: 'דוברות עוסקת במיצוב התודעה ובחיזוק אמון הציבור והלגיטימציה לפעולות צה"ל; הסברה עוסקת בהנעת הציבור האזרחי להתנהגות מצילת חיים לפי הנחיות פיקוד העורף. אלו שתי מערכות שונות לגמרי, עם מטרות שונות ודרכי פעולה שונות.'
    },
    {
      cat: "role", type: "scenario",
      q: 'עיתונאי פונה לקצין הסברה ביקל"ר ומבקש תגובה על אירוע ביטחוני שקרה הלילה ברשות. מה הפעולה הנכונה?',
      options: ['למסור תגובה קצרה וזהירה, כי זה עניין ציבורי', 'להפנות את העיתונאי לדובר צה"ל ולא למסור תגובה עצמאית', 'להתייעץ עם דובר הרשות ולענות יחד איתו לעיתונאי', 'להתעלם מהפנייה לגמרי'],
      correct: 1,
      explain: 'קצין הסברה אינו דובר צה"ל ואינו מוסמך להתראיין בשם הצבא או למסור תגובה לתקשורת - גם לא ברשתות חברתיות. פנייה מעיתונאי מחייבת הפניה לדובר צה"ל, לעולם לא תגובה עצמאית.'
    },
    {
      cat: "role", type: "concept",
      q: 'מי מוסמך להתראיין או להתבטא בתפקיד/במדים מול עיתונאים?',
      options: ['כל קצין הסברה, בכפוף לשיקול דעתו', 'רק מי שקיבל אישור מפורש מדובר צה"ל', 'רק קציני מחוז ומעלה', 'כל מי שמחזיק תעודת עיתונאי צבאי'],
      correct: 1,
      explain: 'כלל הברזל: אין להתראיין או להתבטא בתפקיד או במדים עם עיתונאים ללא אישור דובר צה"ל - גם ברשתות חברתיות. הכלל חל על כל דרג, כולל קציני הסברה.'
    },
    {
      cat: "theory", type: "concept",
      q: 'לפי "המעגל הזהוב" (Golden Circle), מאיזו שאלה יש להתחיל כדי לבנות הסברה אפקטיבית?',
      options: ['"מה" - מה אנחנו עושים', '"איך" - איך אנחנו עושים את זה', '"למה" - למה אנחנו עושים את זה', 'אין סדר מועדף, הכול נכתב יחד'],
      correct: 2,
      explain: 'המודל מתחיל תמיד מה"למה" (התכלית, הרציונל) וממשיך כלפי "איך" ולבסוף "מה" - התוכן המוחשי. חשיבה שמתחילה מה"מה" (ההנחיה עצמה) בלי להסביר את הרציונל פחות אפקטיבית.'
    },
    {
      cat: "theory", type: "concept",
      q: 'מהו עקרון היסוד שחוזר לאורך כל חומרי הקורס לגבי חשיפת מידע לציבור בחירום?',
      options: ['חשיפת מידע תמיד מייצרת פאניקה, ולכן יש למעט בה', 'מידע מניע את הציבור להיערך ולהינצל - ולא חושף אותו לפאניקה', 'יש להימנע ממתן הנחיות לא נעימות', 'רק קצינים בכירים רשאים למסור מידע לציבור'],
      correct: 1,
      explain: 'עקרון מרכזי: מידע מניע את הציבור להיערך ובכך לנצל - ההנחה השגויה ש"חשיפת מידע מכניסה לפאניקה" היא בדיוק מה שהקורס מבקש לתקן.'
    },
    {
      cat: "theory", type: "scenario",
      q: 'תושב שואל קצין הסברה: "למה אני צריך לשכב על הקרקע ברחוב ולכסות את הראש, ולא פשוט לרוץ למרחב המוגן?" מהי התגובה הנכונה לפי עקרון "תמיד להתחיל מה\'למה\'"?',
      options: ['"כי ככה נאמר - תעשה מה שאומרים לך"', 'להסביר את הרציונל: הסיכון האמיתי הוא משברי ירוט שעלולים לפגוע גם במי שלא נפגע ישירות, ולכן יש ערך מציל-חיים בפעולה גם אם היא לא נוחה', 'להתעלם מהשאלה ולעבור הלאה', 'להפנות אותו למוקד 104 בלבד בלי לענות'],
      correct: 1,
      explain: 'בדיוק כמו בדוגמאות ההתנגדות שתועדו בשטח ("זה מביך", "זה מלכלך את הבגדים") - המענה הנכון הוא תמיד לפתוח בהסבר ה"למה" לפני ה"מה", כדי שהציבור יבין את הרציונל ולא רק יקבל פקודה.'
    },
    {
      cat: "theory", type: "concept",
      q: 'מהו סדר השלבים הנכון בתהליך ההסברה השלם המוביל להנעה לפעולה?',
      options: ['יישום ← הבנה ← קבלה ← צריכה ← חשיפה', 'חשיפה ← צריכה ← קבלה ← הבנה ← יישום', 'צריכה ← חשיפה ← יישום ← הבנה ← קבלה', 'קבלה ← חשיפה ← צריכה ← יישום ← הבנה'],
      correct: 1,
      explain: 'התהליך הוא רצף: חשיפה (האם האזרח נחשף להנחיה) ← צריכה (מה המידע שצרך) ← קבלה (איך הוא מגיב למסר) ← הבנה (האם הבין) ← יישום (האם הוא מתנהג בהתאם).'
    },
    {
      cat: "theory", type: "scenario",
      q: 'סקר שבוצע אחרי אירוע הראה כי 90% מהציבור נחשפו להנחיות העדכניות, אך בפועל רק מיעוט מהם יישמו אותן נכון. לפי מודל שלבי ההנעה לפעולה, היכן קרוב לוודאי הפער?',
      options: ['בשלב החשיפה - המידע כלל לא הגיע', 'בין שלב ההבנה לשלב היישום', 'אין כאן פער אמיתי, התוצאה תקינה', 'בשלב הצריכה בלבד'],
      correct: 1,
      explain: 'חשיפה גבוהה (90%) מצביעה על כך שהמידע הגיע. הפער בין "שמעו" לבין "פעלו נכון" ממוקם בדרך כלל בין הבנת ההנחיה ליישומה בפועל - שם צריך להתמקד המענה ההסברתי הבא.'
    },
    {
      cat: "guidelines", type: "concept",
      q: 'מהו ההבדל המרכזי בין "הנחיה מצילת חיים" ל"מדיניות ההתגוננות"?',
      options: ['אין הבדל מהותי - אלה שני כינויים לאותו דבר', 'הנחיה מצילת חיים היא הכלל הקבוע (למשל זמן הכניסה למרחב המוגן); מדיניות ההתגוננות היא ההחלטה המשתנה על היקף הפעילות (מדרג הצבעים)', 'מדיניות ההתגוננות חלה רק על מוסדות חינוך', 'הנחיה מצילת חיים נקבעת ע"י הרשות המקומית בלבד'],
      correct: 1,
      explain: 'אלו שני כלים שונים לגמרי במטרה: ההנחיה המצילת חיים קבועה וידועה מראש (איך להתגונן), ואילו מדיניות ההתגוננות היא ההחלטה המשתנה יום-יום על היקף הפעילות המותר.'
    },
    {
      cat: "guidelines", type: "concept",
      q: 'כמה מדרגי מדיניות התגוננות (צבעים) קיימים?',
      options: ['שניים', 'שלושה', 'ארבעה', 'שישה'],
      correct: 2,
      explain: 'ארבעה מדרגים: ירוק (פעילות מלאה), צהוב (פעילות חלקית), כתום (פעילות מצומצמת), אדום (פעילות הכרחית בלבד).'
    },
    {
      cat: "guidelines", type: "scenario",
      q: 'ראש רשות מקומית מבקש לפרסם הנחיה חדשה משלו, שלא אושרה ע"י פיקוד העורף, כי "זה הגיוני ודחוף". מה על קצין ההסברה לעשות?',
      options: ['לאשר מיד - ראש הרשות הוא הגורם המוסמך ביותר באזורו', 'להסביר שאסור לפרסם הנחיה עצמאית ללא אישור פיקודי, ולהעלות את הבקשה לערוץ הפיקודי הרלוונטי', 'להתעלם מהבקשה ולא להגיב', 'לפרסם את ההנחיה בלי לציין שהיא מטעם הרשות'],
      correct: 1,
      explain: 'גם כשההנחיה נראית הגיונית ודחופה, הסמכות לקביעת תוכן הנחיות היא פיקודית בלבד. התפקיד של קצין ההסברה הוא להסביר זאת ולהעלות את הצורך לערוץ הנכון - לא לאשר בעצמו.'
    },
    {
      cat: "guidelines", type: "concept",
      q: 'מי מוסמך לקבוע את מדרג מדיניות ההתגוננות היומי?',
      options: ['דובר הרשות המקומית', 'יחידת ההסברה הפיקודית / פיקוד העורף בלבד', 'קצין הסברה ביקל"ר', 'מועצת העיר'],
      correct: 1,
      explain: 'קביעת מדרג מדיניות ההתגוננות, בדיוק כמו תוכן המסרים, היא בסמכות פיקודית בלעדית ואינה ניתנת להחלטה ברמת הרשות המקומית.'
    },
    {
      cat: "authority", type: "concept",
      q: 'כמה מכלולים עיקריים פועלים ברשות מקומית בחירום, לפי המודל שהוצג בקורס?',
      options: ['שלושה', 'ארבעה', 'שישה', 'שמונה'],
      correct: 2,
      explain: 'שישה מכלולים: אוכלוסייה, חינוך, מידע לציבור, הנדסה ותשתיות, לוגיסטיקה ותפעול, ומנהל כללי ומשא"ן.'
    },
    {
      cat: "authority", type: "concept",
      q: 'מהו הממשק המרכזי ביותר של קצין ההסברה בתוך מכלול מידע לציבור ברשות?',
      options: ['מכלול הנדסה ותשתיות', 'דובר הרשות ומנהל מכלול המידע לציבור', 'מכלול לוגיסטיקה ותפעול', 'מוקד 106 בלבד'],
      correct: 1,
      explain: 'דובר הרשות ומנהל מכלול המידע לציבור הם הממשק המרכזי שקצין ההסברה עובד מולו באופן שוטף בתוך מכלול מידע לציבור.'
    },
    {
      cat: "authority", type: "scenario",
      q: 'מוקד 106 ברשות מקבל גל פניות חוזרות על אי-בהירות לגבי מיקום המרחב המוגן הציבורי הקרוב. מה תפקידו של קצין ההסברה במצב הזה?',
      options: ['להתעלם - זה לא בתחום אחריותו', 'לנטר את מוקד 106 כסנסור להלכי רוח ולפערי מידע, ולפעול בהתאם - להעלות צורך או לעדכן מסרים', 'לסגור את המוקד עד להבהרה', 'להפנות את כל הפונים לרשות שכנה'],
      correct: 1,
      explain: 'ניטור מוקד 106 והפלטפורמות המקומיות כסנסור להלכי רוח ולפערי מידע הוא חלק מהצ\'קליסט הבסיסי של קצין ההסברה - הפערים שעולים משם צריכים להיות מועלים הלאה בזמן אמת.'
    },
    {
      cat: "population", type: "concept",
      q: 'מהו תפקידו של קה"א (קצין התנהגות אוכלוסייה)?',
      options: ['אחראי בלעדי על תוכן ההסברה', 'קצין מטה מקצועי לנושא התנהגות האוכלוסייה בחירום - שותף תפקיד מרכזי של קצין ההסברה', 'מחליף את קצין ההסברה בעת הצורך', 'אחראי רק על לוגיסטיקה ברשות'],
      correct: 1,
      explain: 'קה"א הוא קצין מטה מקצועי (פיקוד/מחוז/נפה/יקל"ר) לתחום התנהגות האוכלוסייה בחירום, ומשלים את קצין ההסברה בידע ובכלים - לא מחליף אותו.'
    },
    {
      cat: "population", type: "scenario",
      q: 'קצין הסברה ביקל"ר מזהה שבקרב אוכלוסיית הקשישים במרחבו יש שיעור גבוה של אי-הבנת ההנחיות. מהי הפעולה המקצועית הנכונה?',
      options: ['להתעלם - זו אוכלוסייה קטנה יחסית', "להתייעץ עם הקה\"א ולבנות יחד מענה הסברתי מותאם לאוכלוסייה עם צרכים מיוחדים", 'להמתין שהבעיה תיפתר מעצמה', 'להפסיק להפיץ הנחיות לכלל הציבור'],
      correct: 1,
      explain: 'זיהוי צרכים ייחודיים של אוכלוסיות עם רגישות מוגברת (כמו קשישים) הוא בדיוק המקרה שבו שיתוף הפעולה בין קצין ההסברה לקה"א יוצר ערך מוסף - מענה מותאם במקום מענה גנרי.'
    },
    {
      cat: "population", type: "concept",
      q: 'מהו מוקד המענה הטלפוני לאזרח הפתוח 24/7, המוזכר כערוץ מרכזי בחומרי הקורס?',
      options: ['מוקד 100', 'מוקד 104', 'מוקד 101', 'מוקד 112'],
      correct: 1,
      explain: 'מוקד 104 הוא מרכז המענה לאזרח הפועל 24/7 במספר שפות, ומהווה ערוץ מרכזי להפצת מידע ולקבלת שו"ת מהציבור.'
    },
    {
      cat: "theory", type: "scenario",
      q: 'באמצע מערכה ממושכת, ניכר שהציבור מתעייף מהישמעות להנחיית נסיעה ברכב ("עצרו בצד הדרך"). מהי הגישה הנכונה של מערך ההסברה?',
      options: ['להפסיק להזכיר את ההנחיה - היא כבר נאמרה בעבר', 'למקד מחדש את ההסברה ברציונל שמאחורי ההנחיה ("למה") כדי לחזק את ההישמעות מול השחיקה', 'להטיל סנקציות על מי שלא נשמע', 'להחליף את ההנחיה בהנחיה אחרת כדי לגוון'],
      correct: 1,
      explain: 'שחיקה במערכה ממושכת היא תופעה מוכרת. המענה שתועד בפועל הוא הפצת סרטוני שטח וחיזוק ההסבר על הרציונל שמאחורי ההנחיה - לא ויתור עליה ולא ענישה.'
    },
    {
      cat: "role", type: "scenario",
      q: 'בשכונה עם מקלטים משותפים מתגלה שאחד המקלטים נעול ו"הושתלט" עליו ע"י חלק מהדיירים. לפי מודל "מי קהל היעד / מה הצרכים / מה המסר / מהם ערוצי ההפצה", מה הצעד ההסברתי הראשון המתאים?',
      options: ['לקרוא למשטרה באופן מיידי ללא בדיקה נוספת', 'לזהות את קהל היעד (דיירי הבניין), ולבנות מסר שמעודד אחריות דיירים לפתיחת המקלט וניקויו, דרך ערוץ הפצה מתאים (למשל קבוצת וואטסאפ שכונתית)', 'להתעלם - זו בעיה הנדסית ולא הסברתית', 'לפנות את הבניין כולו'],
      correct: 1,
      explain: 'זהו בדיוק יישום של המודל בן ארבע השאלות: קודם מזהים את קהל היעד הספציפי, מבינים את הצורך האמיתי (לא רק "המקלט נעול" אלא גם מודעות ואחריות דיירים), ואז בוחרים מסר וערוץ מתאימים - לא קופצים ישר לפתרון כפייתי.'
    },
    {
      cat: "guidelines", type: "scenario",
      q: 'דובר רשות מפרסם סרטון הסברה עצמאי, בלי סמל הרשות ובלי אישור פיקודי, בנימוק ש"המצב דחוף מדי לחכות לאישור". כיצד על קצין ההסברה ביקל"ר לנהוג?',
      options: ['לשבח את היוזמה המהירה', 'לעצור את הפרסום ולהבהיר שזו חריגה אסורה - גם בדחיפות אין לפרסם ללא אישור פיקודי ותחת סמל הרשות', 'להצטרף לצילום סרטון דומה', 'זה לא בתחום אחריותו ואין צורך להתערב'],
      correct: 1,
      explain: 'אחד העקרונות החוזרים לאורך כל חומרי הקורס: לעולם אל תאשר תוכן עצמאי שלא תחת סמל הרשות וללא אישור פיקודי - גם לא במצבי דחיפות. זו בדיוק נקודת הכשל שהצ\'קליסט נועד למנוע.'
    }
  ];

  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  // מערבב גם את סדר האפשרויות, תוך שמירה על אינדקס התשובה הנכונה
  function shuffleOptions(question) {
    var idxs = shuffle([0, 1, 2, 3]);
    var newOptions = idxs.map(function (i) { return question.options[i]; });
    var newCorrect = idxs.indexOf(question.correct);
    return {
      cat: question.cat, type: question.type, q: question.q,
      options: newOptions, correct: newCorrect, explain: question.explain
    };
  }

  function el(tag, attrs, html) {
    var e = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    }
    if (html !== undefined) e.innerHTML = html;
    return e;
  }

  // מנוע מבחן גנרי - משותף למצב "תרגול חופשי" ולמצב "בוחן השבוע",
  // כל אחד עם ה-root ו-state משלו (כדי ששני המצבים יוכלו לדור זה לצד זה באותו עמוד).
  function makeQuizEngine(root) {
    var state = { questions: [], current: 0, score: 0, byCat: {} };
    var opts = {};

    function start(questions, options) {
      opts = options || {};
      state.questions = shuffle(questions).map(shuffleOptions);
      state.current = 0;
      state.score = 0;
      state.byCat = {};
      renderQuestion();
    }

    function renderQuestion() {
      var q = state.questions[state.current];
      root.innerHTML = "";

      var progress = el("div", { class: "quiz-progress" },
        "שאלה " + (state.current + 1) + " מתוך " + state.questions.length +
        ' <span class="quiz-cat-badge">' + CATEGORIES[q.cat] + (q.type === "scenario" ? " · מקרה בוחן" : "") + "</span>");
      root.appendChild(progress);

      var box = el("div", { class: "qr-card quiz-question-card" });
      box.appendChild(el("h3", {}, q.q));

      var optsWrap = el("div", { class: "quiz-options" });
      q.options.forEach(function (opt, idx) {
        var btn = el("button", { type: "button", class: "quiz-option" }, opt);
        btn.addEventListener("click", function () {
          if (optsWrap.classList.contains("answered")) return;
          optsWrap.classList.add("answered");
          var correct = idx === q.correct;
          if (correct) state.score++;
          if (!state.byCat[q.cat]) state.byCat[q.cat] = { correct: 0, total: 0 };
          state.byCat[q.cat].total++;
          if (correct) state.byCat[q.cat].correct++;

          Array.prototype.forEach.call(optsWrap.children, function (b, i) {
            b.classList.add("locked");
            if (i === q.correct) b.classList.add("correct");
            else if (i === idx) b.classList.add("wrong");
          });

          var explain = el("div", { class: "quiz-explain " + (correct ? "ok" : "no") },
            (correct ? "✓ נכון. " : "✗ לא מדויק. ") + q.explain);
          box.appendChild(explain);

          var nextBtn = el("button", { type: "button", class: "quiz-next-btn" },
            state.current < state.questions.length - 1 ? "השאלה הבאה ←" : "לסיכום התוצאה ←");
          nextBtn.addEventListener("click", function () {
            if (state.current < state.questions.length - 1) {
              state.current++;
              renderQuestion();
            } else {
              renderResult();
            }
          });
          box.appendChild(nextBtn);
        });
        optsWrap.appendChild(btn);
      });
      box.appendChild(optsWrap);
      root.appendChild(box);
    }

    function renderResult() {
      root.innerHTML = "";
      var total = state.questions.length;
      var pct = Math.round((state.score / total) * 100);
      var box = el("div", { class: "qr-card quiz-result-card" });
      box.appendChild(el("h3", {}, "התוצאה שלכם"));
      box.appendChild(el("div", { class: "quiz-score" }, state.score + " / " + total + '<span class="quiz-pct">(' + pct + "%)</span>"));

      if (opts.showCatBreakdown) {
        var table = el("table", { class: "compact" });
        var thead = el("thead", {}, "<tr><th>נושא</th><th>תשובות נכונות</th></tr>");
        table.appendChild(thead);
        var tbody = el("tbody");
        Object.keys(state.byCat).forEach(function (cat) {
          var row = state.byCat[cat];
          var tr = el("tr", {}, "<td>" + CATEGORIES[cat] + "</td><td>" + row.correct + " / " + row.total + "</td>");
          tbody.appendChild(tr);
        });
        table.appendChild(tbody);
        var tableScroll = el("div", { class: "table-scroll" });
        tableScroll.appendChild(table);
        box.appendChild(tableScroll);
      }

      var retryBtn = el("button", { type: "button", class: "quiz-start-btn" }, opts.restartLabel || "נסו שוב ←");
      retryBtn.addEventListener("click", function () {
        if (opts.onRestart) opts.onRestart();
      });
      box.appendChild(retryBtn);
      root.appendChild(box);
    }

    return { start: start };
  }

  // ===== מצב "תרגול חופשי לפי קטגוריה" (קיים, ללא שינוי בתפקוד) =====
  function initFreePractice() {
    var root = document.getElementById("quiz-app");
    if (!root) return null;
    var engine = makeQuizEngine(root);

    function renderStart() {
      root.innerHTML = "";
      var box = el("div", { class: "qr-card" });
      var title = el("h3", {}, "בחרו נושאים למבחן");
      box.appendChild(title);
      var chipsWrap = el("div", { class: "quiz-chips", id: "quiz-chips" });
      var selected = {};
      Object.keys(CATEGORIES).forEach(function (key) {
        selected[key] = true;
        var chip = el("button", { type: "button", class: "quiz-chip active", "data-cat": key }, CATEGORIES[key]);
        chip.addEventListener("click", function () {
          selected[key] = !selected[key];
          chip.classList.toggle("active", selected[key]);
        });
        chipsWrap.appendChild(chip);
      });
      box.appendChild(chipsWrap);
      var p = el("p", { style: "color:var(--text-muted);font-size:0.88rem;margin-top:14px;" },
        "המבחן כולל שאלות ידע וגם שאלות יישום (מקרי בוחן) - מה הייתם עושים בפועל במצב נתון.");
      box.appendChild(p);
      var startBtn = el("button", { type: "button", class: "quiz-start-btn" }, "התחילו מבחן");
      startBtn.addEventListener("click", function () {
        var cats = Object.keys(selected).filter(function (k) { return selected[k]; });
        if (!cats.length) { cats = Object.keys(CATEGORIES); }
        startWithCats(cats);
      });
      box.appendChild(startBtn);
      root.appendChild(box);
    }

    function startWithCats(cats) {
      var pool = QUESTIONS.filter(function (q) { return cats.indexOf(q.cat) !== -1; });
      engine.start(pool, { showCatBreakdown: true, onRestart: renderStart, restartLabel: "נסו שוב ←" });
    }

    var urlCat = null;
    try {
      var params = new URLSearchParams(window.location.search);
      var catParam = params.get("cat");
      if (catParam && CATEGORIES[catParam]) urlCat = catParam;
    } catch (e) { /* no-op */ }

    if (urlCat) {
      startWithCats([urlCat]);
    } else {
      renderStart();
    }

    return { hasUrlCat: !!urlCat };
  }

  // ===== מצב "בוחן השבוע" =====
  function getCurrentWeek(weeks) {
    if (!weeks || !weeks.length) return null;
    var today = new Date(); today.setHours(0, 0, 0, 0);
    var best = null;
    weeks.forEach(function (w) {
      var d = new Date(w.date + "T00:00:00");
      if (d <= today && (!best || d > new Date(best.date + "T00:00:00"))) best = w;
    });
    if (!best) {
      best = weeks.slice().sort(function (a, b) { return new Date(a.date) - new Date(b.date); })[0];
    }
    return best;
  }

  function formatDateRange(startDateStr) {
    var start = new Date(startDateStr + "T00:00:00");
    var end = new Date(start.getTime() + 6 * 24 * 60 * 60 * 1000);
    function fmt(d) {
      var dd = String(d.getDate()).padStart(2, "0");
      var mm = String(d.getMonth() + 1).padStart(2, "0");
      return dd + "." + mm;
    }
    return fmt(start) + " - " + fmt(end) + "." + end.getFullYear();
  }

  function initSelfQuizWeek() {
    var root = document.getElementById("quiz-week-app");
    if (!root) return;
    var weeks = window.SELF_QUIZ_WEEKS || [];
    var week = getCurrentWeek(weeks);
    var engine = makeQuizEngine(root);

    function renderIntro() {
      root.innerHTML = "";
      if (!week) {
        root.appendChild(el("div", { class: "qr-card" }, "<p>בוחן השבוע עדיין לא פורסם. חזרו בקרוב.</p>"));
        return;
      }
      var cats = [];
      week.questions.forEach(function (q) { if (cats.indexOf(q.cat) === -1) cats.push(q.cat); });
      var hasScenario = week.questions.some(function (q) { return q.type === "scenario"; });

      var card = el("div", { class: "week-card" });
      card.appendChild(el("span", { class: "week-date-pill" },
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4.5" width="18" height="16" rx="2.5"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/></svg>שבוע ' + formatDateRange(week.date)));
      card.appendChild(el("h2", {}, "בוחן השבוע" + (week.title ? ": " + week.title : "")));
      card.appendChild(el("p", { class: "lede" },
        week.questions.length + " שאלות, מיקס קטגוריות" + (hasScenario ? " + תרחיש מהשטח" : "") + ". בשבוע הבא - בוחן חדש לגמרי."));

      var meta = el("div", { class: "week-meta" });
      meta.appendChild(el("span", { class: "week-meta-item" },
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8v4l3 2"/><circle cx="12" cy="12" r="9"/></svg>כ-<b>' + Math.max(2, Math.round(week.questions.length * 0.7)) + '</b> דקות'));
      meta.appendChild(el("span", { class: "week-meta-item" },
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3 7-7"/><path d="M20 12v6a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h10"/></svg><b>' + week.questions.length + '</b> שאלות'));
      if (hasScenario) {
        meta.appendChild(el("span", { class: "week-meta-item" },
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.6 19.6 5.4V11c0 4.9-3.2 8.4-7.6 10-4.4-1.6-7.6-5.1-7.6-10V5.4L12 2.6z"/></svg>כולל תרחיש שטח'));
      }
      card.appendChild(meta);

      var catsWrap = el("div", { class: "week-cats" });
      cats.forEach(function (c) { catsWrap.appendChild(el("span", { class: "week-cat-chip" }, CATEGORIES[c])); });
      card.appendChild(catsWrap);

      var startBtn = el("button", { type: "button", class: "week-start-btn" },
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 4l14 8-14 8V4z" fill="currentColor" stroke="none"/></svg>התחילו את בוחן השבוע');
      startBtn.addEventListener("click", function () {
        engine.start(week.questions, { showCatBreakdown: false, onRestart: renderIntro, restartLabel: "חזרה לבוחן השבוע ←" });
      });
      card.appendChild(startBtn);
      root.appendChild(card);

      root.appendChild(el("p", { class: "week-footnote" },
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16h.01"/></svg>בוחן חדש מתפרסם כל שבוע ומחליף את הקודם - אין חזרה אוטומטית על שאלות משבוע שעבר.'));
    }

    renderIntro();
  }

  // ===== מעבר בין הטאבים "בוחן השבוע" / "תרגול חופשי" =====
  function initModeTabs(defaultTarget) {
    var tabs = document.querySelectorAll(".mode-tab");
    if (!tabs.length) return;
    function activate(target) {
      tabs.forEach(function (t) {
        var on = t.getAttribute("data-target") === target;
        t.setAttribute("aria-selected", on ? "true" : "false");
      });
      document.querySelectorAll(".quiz-panel").forEach(function (p) {
        p.hidden = p.getAttribute("data-panel") !== target;
      });
    }
    tabs.forEach(function (t) {
      t.addEventListener("click", function () { activate(t.getAttribute("data-target")); });
    });
    activate(defaultTarget);
  }

  function init() {
    var freeState = initFreePractice();
    if (document.getElementById("quiz-week-app")) {
      initSelfQuizWeek();
      initModeTabs(freeState && freeState.hasUrlCat ? "free" : "week");
    }
  }

  document.addEventListener("DOMContentLoaded", init);
})();
