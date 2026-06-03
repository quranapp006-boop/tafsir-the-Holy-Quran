<div dir="ltr">

<p align="center">
  <img src="./asset/1.png" alt="المقدمة: بسم الله الرحمن الرحيم" />
</p>

# مستودع تفاسير القرآن الكريم

هذا المستودع يضم مجموعة منظمة من بيانات تفاسير القرآن الكريم بصيغة `JSON`، مرتبة بطريقة واضحة لتسهيل قراءتها، مراجعتها، واستخدامها في التطبيقات الإسلامية، مواقع القرآن الكريم، واجهات البرمجة `API`، والمشاريع التعليمية والبحثية.

نسأل الله تعالى أن يجعل هذا العمل نافعا، وأن يكون عونا لمن يريد خدمة كتاب الله عز وجل وعلومه باحترام وأمانة.

---

## معاينة


<p align="center">
  <img src="./asset/2.png" alt="معاينة إضافية لبيانات التفاسير" />
</p>

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

## أمثلة للاستخدام عبر CDN

يمكن الوصول إلى الملفات مباشرة من خلال `jsDelivr` إذا كان المستودع منشورا على GitHub:

صورة المعاينة:

```text
https://cdn.jsdelivr.net/gh/quranapp006-boop/tafsir-the-Holy-Quran@main/asset/1.png
```

ملف تفسير آية واحدة:

```text
https://cdn.jsdelivr.net/gh/quranapp006-boop/tafsir-the-Holy-Quran@main/tafsir/ar-tafsir-muyassar/1/1.json
```

ملف تفسير سورة كاملة:

```text
https://cdn.jsdelivr.net/gh/quranapp006-boop/tafsir-the-Holy-Quran@main/tafsir-complete/ar-tafsir-muyassar/1.json
```

أغلفة الكتب:

```text
https://github.com/quranapp006-boop/tafsir-the-Holy-Quran/tree/main/assets/book-covers
```

---

## ملاحظات مهمة

- أرقام السور تبدأ من `1` وتنتهي عند `114`.
- في مجلد `tafsir/` يكون المسار على النمط التالي: `tafsir/{اسم-التفسير}/{رقم-السورة}/{رقم-الآية}.json`.
- في مجلد `tafsir-complete/` يكون المسار على النمط التالي: `tafsir-complete/{اسم-التفسير}/{رقم-السورة}.json`.
- أسماء المجلدات يجب استخدامها كما هي تماما عند بناء الروابط أو عند القراءة من داخل التطبيق.
- البيانات مهيأة لتكون سهلة الدمج داخل تطبيقات Android، مواقع الويب، خدمات الخلفية، أو أي مشروع يحتاج إلى نصوص تفسير منظمة.

---

## المساهمة

نرحب بكل مساهمة نافعة ومحترمة تساعد على تحسين هذا العمل، مثل:

- تصحيح خطأ في البيانات أو في ترتيب الملفات.
- تحسين التوثيق وشرح طريقة الاستخدام.
- إضافة أمثلة أو أدوات تساعد المطورين على قراءة البيانات.
- تحسين جودة الملفات مع المحافظة على البنية الحالية للمسارات.

يرجى عند المساهمة مراعاة مكانة القرآن الكريم وعلومه، والتحقق من أي تعديل قبل إرساله.

---

<p align="center">
تم إعداد هذا المستودع لخدمة القرآن الكريم وعلومه، ونسأل الله القبول والنفع.
</p>

</div>
