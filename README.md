<div dir="ltr">

<p align="center">
  <img src="./asset/1.png" alt="المقدمة: بسم الله الرحمن الرحيم" />
</p>

# مستودع تفاسير القرآن الكريم

هذا المستودع يضم مجموعة منظمة من بيانات تفاسير القرآن الكريم بصيغة `JSON`، مرتبة بطريقة واضحة لتسهيل قراءتها، مراجعتها، واستخدامها في التطبيقات الإسلامية، مواقع القرآن الكريم، واجهات البرمجة `API`، والمشاريع التعليمية والبحثية.

نسأل الله تعالى أن يجعل هذا العمل نافعا، وأن يكون عونا لمن يريد خدمة كتاب الله عز وجل وعلومه باحترام وأمانة.

**الإصدار الحالي:** v1.0 | **آخر تحديث:** يونيو 2026

---

## جدول المحتويات

1. [معاينة](#معاينة)
2. [البدء السريع](#البدء-السريع)
3. [محتويات المستودع](#محتويات-المستودع)
4. [التفاسير المتوفرة](#التفاسير-المتوفرة)
5. [صيغة ملفات JSON](#صيغة-ملفات-json)
6. [اتفاقيات تسمية الملفات](#اتفاقيات-تسمية-الملفات)
7. [ملفات الصور والأغلفة](#ملفات-الصور-والأغلفة)
8. [الوصول عبر CDN](#الوصول-عبر-cdn)
9. [أمثلة البرمجة](#أمثلة-البرمجة)
10. [ملاحظات مهمة](#ملاحظات-مهمة)

---

## معاينة


<p align="center">
  <img src="./asset/2.png" alt="معاينة إضافية لبيانات التفاسير" />
</p>

---

## البدء السريع

### 🚀 الحالات الشائعة للاستخدام

**الحالة 1: الحصول على تفسير آية واحدة**
```json
// المسار المحلي:
tafsir/ar-tafsir-muyassar/1/1.json

// القراءة البرمجية:
{
  "text": "نص التفسير",
  "ayah": 1,
  "surah": 1
}
```

**الحالة 2: الحصول على تفاسير سورة كاملة**
```json
// المسار المحلي:
tafsir-complete/ar-tafsir-muyassar/1.json

// البيانات:
{
  "ayahs": [
    {"ayah": 1, "surah": 1, "text": "..."},
    {"ayah": 2, "surah": 1, "text": "..."}
  ]
}
```

**الحالة 3: الوصول عبر CDN (بدون تحميل محلي)**
```
https://cdn.jsdelivr.net/gh/quranapp006-boop/tafsir-the-Holy-Quran@main/tafsir/ar-tafsir-muyassar/1/1.json
```

---

## محتويات المستودع

يحتوي المستودع على صورتين أساسيتين من البيانات:

1. `tafsir/`

   بيانات مفصلة، حيث يكون كل تفسير مقسما حسب رقم السورة، ثم حسب رقم الآية.

   مثال:

   ```text
   tafsir/ar-tafsir-muyassar/1/1.json
   ```

   هذا الملف يمثل تفسير الآية رقم `1` من السورة رقم `1` في التفسير الميسر.

2. `tafsir-complete/`

   بيانات مجمعة، حيث يكون لكل سورة ملف واحد يحتوي آيات السورة وتفسيرها.

   مثال:

   ```text
   tafsir-complete/ar-tafsir-muyassar/1.json
   ```

   هذا الملف يمثل تفسير سورة الفاتحة كاملة في التفسير الميسر.

---

## التفاسير المتوفرة

المجلدات التالية موجودة داخل `tafsir/`، وكل مجلد منها يحتوي `114` مجلدا للسور:

```text
tafsir/
├── ar-tafseer-al-qurtubi
├── ar-tafseer-al-saddi
├── ar-tafseer-tanwir-al-miqbas
├── ar-tafsir-al-baghawi
├── ar-tafsir-al-tabari
├── ar-tafsir-al-wasit
├── ar-tafsir-ibn-kathir
└── ar-tafsir-muyassar
```

وتوجد النسخ المجمعة داخل `tafsir-complete/`، وكل مجلد منها يحتوي `114` ملفا بصيغة `JSON`:

```text
tafsir-complete/
├── ar-tafseer-al-qurtubi
├── ar-tafseer-al-saddi
├── ar-tafseer-tanwir-al-miqbas
├── ar-tafsir-al-baghawi
├── ar-tafsir-al-tabari
├── ar-tafsir-al-wasit
├── ar-tafsir-ibn-kathir
├── ar-tafsir-muyassar
└── ar-tafsir-muyassar2
```

---

## صيغة ملفات JSON

### صيغة ملف الآية الواحدة

المسار:

```text
tafsir/ar-tafsir-muyassar/1/1.json
```

الشكل العام:

```json
{
  "text": "نص التفسير",
  "ayah": 1,
  "surah": 1
}
```

المعاني:

- `text`: نص التفسير.
- `ayah`: رقم الآية.
- `surah`: رقم السورة.

### صيغة ملف السورة الكاملة

المسار:

```text
tafsir-complete/ar-tafsir-muyassar/1.json
```

الشكل العام:

```json
{
  "ayahs": [
    {
      "ayah": 1,
      "surah": 1,
      "text": "نص التفسير"
    }
  ]
}
```

المعاني:

- `ayahs`: قائمة آيات السورة مع تفسير كل آية.
- `ayah`: رقم الآية داخل السورة.
- `surah`: رقم السورة.
- `text`: نص التفسير الخاص بالآية.

---

## اتفاقيات تسمية الملفات

### 📁 نمط المسار في `tafsir/` (التفصيلي)

```
tafsir/
└── {اسم-التفسير}/
    └── {رقم-السورة}/
        └── {رقم-الآية}.json
```

| العنصر | الوصف | أمثلة |
|--------|-------|-------|
| **اسم-التفسير** | اسم مصدر التفسير (بدون مسافات) | `ar-tafsir-muyassar`, `ar-tafsir-ibn-kathir` |
| **رقم-السورة** | من 1 إلى 114 | `1`, `2`, `114` |
| **رقم-الآية** | رقم الآية داخل السورة | `1`, `2`, `286` |

**أمثلة عملية:**
- `tafsir/ar-tafsir-muyassar/1/1.json` → الآية الأولى من سورة الفاتحة (التفسير الميسر)
- `tafsir/ar-tafsir-ibn-kathir/2/100.json` → الآية 100 من سورة البقرة (ابن كثير)
- `tafsir/ar-tafseer-al-qurtubi/114/6.json` → الآية الأخيرة من سورة الناس (القرطبي)

### 📁 نمط المسار في `tafsir-complete/` (المجمع)

```
tafsir-complete/
└── {اسم-التفسير}/
    └── {رقم-السورة}.json
```

| العنصر | الوصف | ملاحظات |
|--------|-------|--------|
| **اسم-التفسير** | اسم مصدر التفسير (بدون مسافات) | نفس الأسماء المستخدمة في `tafsir/` |
| **رقم-السورة** | من 1 إلى 114 | الملف يحتوي جميع آيات السورة |

**أمثلة عملية:**
- `tafsir-complete/ar-tafsir-muyassar/1.json` → جميع آيات سورة الفاتحة (التفسير الميسر)
- `tafsir-complete/ar-tafsir-ibn-kathir/2.json` → جميع آيات سورة البقرة (ابن كثير)
- `tafsir-complete/ar-tafseer-al-qurtubi/114.json` → جميع آيات سورة الناس (القرطبي)

### ✅ قائمة أسماء التفاسير الصحيحة

استخدم هذه الأسماء بالضبط عند بناء الروابط:

```
ar-tafseer-al-qurtubi
ar-tafseer-al-saddi
ar-tafseer-tanwir-al-miqbas
ar-tafsir-al-baghawi
ar-tafsir-al-tabari
ar-tafsir-al-wasit
ar-tafsir-ibn-kathir
ar-tafsir-muyassar
ar-tafsir-muyassar2  (متوفر فقط في tafsir-complete/)
```

---

## ملفات الصور والأغلفة

توجد الصور المستخدمة في README داخل:

```text
asset/
├── 1.png
└── 2.png
```

وتوجد أغلفة الكتب داخل:

```text
assets/book-covers/
├── png
├── png-large
├── svg
└── svg-large
```

كما يوجد مجلد خاص بالأغلفة الخلفية:

```text
assets/book-back-covers/
```

---

## الوصول عبر CDN

إذا كان المستودع منشورا على GitHub، يمكن الوصول إلى جميع الملفات مباشرة عبر **jsDelivr CDN** دون الحاجة لتحميل المستودع محليا:

### 🌐 روابط الوصول المباشر

**1. صور المعاينة:**
```
https://cdn.jsdelivr.net/gh/quranapp006-boop/tafsir-the-Holy-Quran@main/asset/1.png
https://cdn.jsdelivr.net/gh/quranapp006-boop/tafsir-the-Holy-Quran@main/asset/2.png
```

**2. ملف تفسير آية واحدة:**
```
https://cdn.jsdelivr.net/gh/quranapp006-boop/tafsir-the-Holy-Quran@main/tafsir/ar-tafsir-muyassar/1/1.json
```
يمكن استبدال:
- `ar-tafsir-muyassar` باسم أي تفسير آخر
- `1/1` برقم السورة والآية المطلوبة

**3. ملف تفسير سورة كاملة:**
```
https://cdn.jsdelivr.net/gh/quranapp006-boop/tafsir-the-Holy-Quran@main/tafsir-complete/ar-tafsir-muyassar/1.json
```
يمكن استبدال:
- `ar-tafsir-muyassar` باسم أي تفسير آخر
- `1` برقم السورة المطلوبة

**4. مجلد أغلفة الكتب:**
```
https://github.com/quranapp006-boop/tafsir-the-Holy-Quran/tree/main/assets/book-covers
```

### 💡 ملاحظة حول الأداء
- استخدام CDN مفيد للتطبيقات الويب والأنظمة التي تريد الوصول المباشر
- للمشاريع الكبيرة، يفضل تحميل البيانات محليا لتجنب تأخر الشبكة

---

## أمثلة البرمجة

### 📖 مثال 1: استدعاء تفسير آية واحدة (JavaScript)

```javascript
async function getTafisrAyah(tafsirName, surah, ayah) {
  const url = `https://cdn.jsdelivr.net/gh/quranapp006-boop/tafsir-the-Holy-Quran@main/tafsir/${tafsirName}/${surah}/${ayah}.json`;
  
  try {
    const response = await fetch(url);
    const data = await response.json();
    console.log(`السورة ${data.surah}, الآية ${data.ayah}:`);
    console.log(data.text);
  } catch (error) {
    console.error('خطأ في جلب البيانات:', error);
  }
}

// الاستخدام:
getTafisrAyah('ar-tafsir-muyassar', 1, 1);
```

### 📖 مثال 2: استدعاء سورة كاملة (Python)

```python
import requests
import json

def get_surah_tafsir(tafsir_name, surah_number):
    url = f"https://cdn.jsdelivr.net/gh/quranapp006-boop/tafsir-the-Holy-Quran@main/tafsir-complete/{tafsir_name}/{surah_number}.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        print(f"عدد الآيات: {len(data['ayahs'])}")
        for ayah in data['ayahs'][:3]:  # عرض أول 3 آيات
            print(f"الآية {ayah['ayah']}: {ayah['text'][:50]}...")
            
    except requests.exceptions.RequestException as e:
        print(f'خطأ: {e}')

# الاستخدام:
get_surah_tafsir('ar-tafsir-muyassar', 1)
```

### 📖 مثال 3: تحميل البيانات محليا (Node.js)

```javascript
const fs = require('fs');
const path = require('path');

function readLocalTafsir(tafsirName, surah, ayah) {
  const filePath = path.join(__dirname, 'tafsir', tafsirName, String(surah), `${ayah}.json`);
  
  try {
    const data = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(data);
  } catch (error) {
    console.error('خطأ في قراءة الملف:', error.message);
    return null;
  }
}

// الاستخدام:
const tafsir = readLocalTafsir('ar-tafsir-muyassar', 1, 1);
if (tafsir) {
  console.log(tafsir.text);
}
```

---

## قواعد البيانات (Databases)

### 📊 ما هي قواعد البيانات؟

بيانات التفاسير متوفرة أيضاً في صيغ قواعد بيانات مختلفة (بالإضافة إلى ملفات JSON). هذا يسهل الاستخدام في التطبيقات المختلفة.

### 🗂️ التنسيقات المتاحة

يمكن تحويل بيانات JSON إلى:

| التنسيق | الملف | الاستخدام |
|---------|-------|----------|
| **SQLite** | `.db` | التطبيقات المحمولة وسطح المكتب |
| **MySQL/PostgreSQL** | `.sql` | الخوادم والويب |
| **CSV** | `.csv` | Excel والتحليل الإحصائي |
| **JSON** | `.bin` | تطبيقات الويب |
| **XML** | `.xml` | التطبيقات المؤسسية |
| **YAML** | `.yaml` | التكوينات |

### 🛠️ كيفية إنشاء قواعد البيانات

استخدم أداة `scripts/import_tafsir_to_sqlite.py`:

```powershell
# إنشاء قاعدة بيانات SQLite
python scripts/import_tafsir_to_sqlite.py tafsir -o databases -f db

# تصدير إلى CSV
python scripts/import_tafsir_to_sqlite.py tafsir -o databases -f csv

# تصدير إلى XML
python scripts/import_tafsir_to_sqlite.py tafsir -o databases -f xml
```

**النتيجة:** ملفات في `databases/<format>/`

### 📚 بنية قاعدة البيانات

جميع قواعد البيانات تحتوي على **جدول واحد** يسمى `tafsir`:

| العمود | النوع | الوصف |
|--------|--------|-------|
| **surah** | رقم | رقم السورة (1-114) |
| **ayah** | رقم | رقم الآية |
| **text** | نص | نص التفسير |

### 📖 أمثلة استخدام سريعة

**Python - قراءة من SQLite:**
```python
import sqlite3

conn = sqlite3.connect('databases/db/ar-tafsir-muyassar.db')
cursor = conn.cursor()

# الحصول على تفسير آية
cursor.execute('SELECT text FROM tafsir WHERE surah = 1 AND ayah = 1')
print(cursor.fetchone()[0])

conn.close()
```

**JavaScript - قراءة من JSON:**
```javascript
const tafsir = require('./databases/json/ar-tafsir-muyassar.bin');
const ayah = tafsir.find(e => e.surah === 1 && e.ayah === 1);
console.log(ayah.text);
```

### 📘 معلومات تفصيلية

لمعلومات كاملة عن:
- بنية الجداول بالتفصيل
- أمثلة استعلامات متقدمة
- أداء وتحسينات الاستعلامات
- مقارنة شاملة بين التنسيقات

**راجع:** [دليل قواعد البيانات](scripts/README-en.md#قواعد-البيانات-والجداول)

---

## أدوات التطوير

### ⚠️ نقاط حاسمة

- **أرقام السور:** تبدأ من `1` وتنتهي عند `114`
- **استخدام أسماء التفاسير:** استخدم الأسماء بالضبط كما هي مدرجة (بما فيها الأحرف والواصلات)
- **ترميز الملفات:** جميع ملفات JSON بترميز UTF-8
- **عدم وجود بيانات فارغة:** جميع الآيات لها تفسير (لا توجد ملفات فارغة)

### 📐 معلومات البيانات

| المعيار | القيمة |
|--------|--------|
| عدد السور | 114 |
| عدد التفاسير المتوفرة (tafsir/) | 8 |
| عدد التفاسير المتوفرة (tafsir-complete/) | 9 |
| صيغة البيانات | JSON |
| الترميز | UTF-8 |
| ترخيص الاستخدام | عام (للأغراض الخيرية) |

### 🔧 التطبيقات المدعومة

البيانات مهيأة وجاهزة للاستخدام في:

- ✅ تطبيقات Android و iOS
- ✅ مواقع الويب (HTML, React, Vue, Angular)
- ✅ خدمات الخلفية (Backend)
- ✅ قواعد البيانات
- ✅ أنظمة البحث والفهرسة
- ✅ تطبيقات سطح المكتب
- ✅ البرامج التعليمية والبحثية

### 📝 الخطوات الأساسية للاستخدام

**1. اختر طريقة الوصول:**
- محلي: قم بتحميل المستودع
- CDN: استخدم الروابط المباشرة

**2. حدد التفسير:**
- اختر من قائمة التفاسير المتوفرة

**3. حدد السورة والآية:**
- السورة: 1-114
- الآية: حسب عدد آيات السورة

**4. استدعي البيانات:**
- عبر API (CDN)
- أو من الملفات المحلية

---

<p align="center">
تم إعداد هذا المستودع لخدمة القرآن الكريم وعلومه، ونسأل الله القبول والنفع.

**جزاكم الله خيرا** 🌙
</p>

</div>
