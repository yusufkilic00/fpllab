# FPL LAB — Revision 2026/27

> هذه النسخة تتضمن مراجعة UX كاملة للـOverview وTactical Board وFDR وMatchup XI وPlayer Intelligence وChart Studio، مع اختبار Desktop وMobile فعلي. راجع `CHANGELOG_REVISION.md` و`QA_REVISION.md` للتفاصيل.

# FPL LAB — Premier League Football Intelligence 2026/27

نسخة محلية نهائية مرشحة للتجربة، مبنية على ملفات الموسم التي وفرتها. البيانات التحليلية الحالية تغطي **GW1–GW9**، مع الاحتفاظ بجدول الموسم الكامل **380 مباراة** للتخطيط للمواجهات القادمة.

## التشغيل

### Windows
فك ضغط الملف بالكامل ثم افتح `START_WINDOWS.bat`.

### macOS / Linux
افتح Terminal داخل مجلد المشروع ثم شغّل:

```bash
sh START_MAC_LINUX.sh
```

### تشغيل يدوي
يتطلب Python 3.10+ فقط، ولا يحتاج npm أو حزم Python إضافية:

```bash
python server.py --open
```

يفتح التطبيق محليًا على `http://127.0.0.1:8765/`. لا تنقل `index.html` وحده؛ اترك الملفات والمجلدات معًا.

## ما يحتويه المنتج

### Overview
- ملخص الموسم والـFPL form.
- النتائج المتاحة وجدول الدوري المحسوب من المباريات المكتملة.
- تنقل مباشر لمساحات العمل.

### Tactical Board
- Sidebar رئيسية على اليسار في سطح المكتب، وBottom Navigation على الشاشات الصغيرة.
- فلاتر منظمة في Categories بدل قائمة مسطحة.
- Gameweek picker: All / Last 3 / Last 5 / Range / Custom.
- Minute range يدعم الوقت بدل الضائع حتى أقصى دقيقة فعلية في المصدر (103 حاليًا).
- Event Layers مصنفة إلى Possession / Finishing / Defending / Duels & Discipline، مع أشكال بصرية مختلفة للأحداث.
- Pitch zones، custom rectangle، density، timeline، outcomes، body-part filters وغيرها.
- تبويبات داخلية: Pitch / Matchup / Matchup XI / Fixture Difficulty / Sequences.

### Matchup Intelligence
- يحلل نشاط الفريق مقابل ما يسمح به المنافس عبر مباريات الجولات المختارة، وليس المواجهة المباشرة فقط.
- Event families مستقلة: Shots / Bad touches / Crosses / Headers / Final-third passes.
- الأرقام لا تُدمج في Activity score غامض؛ كل نوع يظهر منفصلًا.
- League Vulnerability Matrix تستخدم **Raw Totals داخل الجولات المختارة فقط**.
- كل Metric لها Rank مستقل ثابت؛ تغيير عمود الفرز لا يغير Rank الأعمدة الأخرى. تغيير نطاق الجولات يعيد حساب جميع الرانكات.
- Own Goals مستبعدة من attacking shots.

### Crosses & Headers
- Crosses delivered.
- Crosses completed.
- Header shots.
- Headers on target.
- Header goals.
- أهم منفذي العرضيات وأهم مسددي الرأسيات، مع تقسيم مناطق العرضيات.

**مهم:** التحليل يعرض علاقة تجميعية بين العرضيات والرأسيات، ولا يدّعي أن Header محددة جاءت من Cross محددة لأن الملفات المستوردة لا توفر علاقة event-to-event موثقة لذلك.

### Matchup XI Builder
- إضافة لاعب مباشرة من Matchup Intelligence.
- حفظ سبب الاختيار: الفريق/المنافس/الجولات/المنطقة/نوع النشاط.
- تشكيلات فعلية: 3-4-3، 3-5-2، 4-3-3، 4-4-2، 4-5-1، 5-3-2، 5-4-1.
- 11 Slot حقيقية على الملعب.
- تغيير الدور، إزالة واستبدال اللاعب، وإرجاع اللاعبين إلى أدوارهم الطبيعية.
- اللاعبين الزائدون على شكل الخطة يظهرون في Unplaced بدل كسر التشكيلة.
- التشكيلة والتكوين محفوظان محليًا.

### Fixture Difficulty Planner
- تقييم يدوي من المستخدم لكل فريق في Home وAway من 1 إلى 5.
- Presets متعددة + سجل للتعديلات.
- جدول الموسم الكامل 380 مباراة.
- اختيار Next 3 / 5 / 6 / 8 / 10 جولات قادمة.
- ترتيب الفرق تلقائيًا من الأسهل إلى الأصعب طبقًا لتقييماتك وعدد الجولات المختار.
- الـAnalysis Snapshot يحتفظ بنسخة التقييمات المستخدمة وقت حفظ التحليل، وليس اسم الـPreset فقط.

### Player Intelligence
- **146 Metric قابلة للاستخدام** بعد حذف الحقول الفارغة بالكامل وغير الصالحة للتحليل.
- Taxonomy موحدة للمقاييس، Search، Filters، Table columns، Scatter، Profiles، Comparisons.
- Comparison Category تعرض المقاييس التابعة لها مباشرة بدون الحاجة إلى Search.
- Historical club mapping حسب الجولة، لذلك اللاعب المنتقل يُنسب لناديه الصحيح في الـGW التاريخية.

### Chart Studio
- Performance Landscape موجود هنا بدل تكراره داخل Player Intelligence.
- Bar / Line / Area / Scatter / Bubble / Histogram / Radar / Heatmap / Quadrant / Box / Donut بحسب توافق نوع المقياس.
- Bubble Size Metric مستقلة.
- Radar يدعم 3–8 Metrics يختارها المستخدم ويستخدم Cohort مناسب للمركز.
- المحاور والقيم السالبة وBox Plot تم تصحيح منطقها.
- Themes تتضمن Club Crest identity للشارتات.
- Gameweek وMetric categories منظمة بنفس نظام بقية المنتج.

### Appearance
- Auto / Light / Dark / AMOLED.
- Full workspace palettes: Graphite / Midnight / Carbon / Violet / Slate وغيرها.
- Solid / Transparent / Glass.
- تحكم في Surface opacity وBlur.
- Pitch branding: Off / Wordmark / Logo / Logo + Wordmark مع التحكم في الشفافية.
- الإعدادات تحفظ محليًا.

### Analysis Sessions
- Autosave للـworkspace الحالي.
- Named snapshots.
- حفظ Tactical filters، Matchup context، XI، Fixture Difficulty snapshot، Player Intelligence، وChart Studio configuration.
- New Analysis يبدأ مساحة جديدة بدون مسح إعدادات المظهر أو Presets.

## البيانات وصحة الحسابات

النسخة الحالية مبنية على:
- **670 لاعبًا**.
- **90 مباراة مكتملة** عبر GW1–GW9.
- **380 مباراة** في جدول الموسم الكامل.
- **154,956 صف حدث خام** من أرشيف الأحداث.
- **130,459 حدثًا تحليليًا مفهرسًا** من الأنواع المستخدمة في المنتج.
- **146 Metric قابلة للاستخدام**.
- **453 من 454 Provider Player IDs** مرتبطة بثقة.
- **99.95%** من الأحداث التحليلية مرتبطة بلاعبين.

تمت مراجعة منطق Opta المستخدم في المنتج، ومن الإصلاحات المهمة:
- Own Goals منفصلة عن attacking shots.
- Crosses لا تُحسب Passes.
- Event type 61 يعرض كـBad touch وليس Total touches.
- Header يعني Header shot وليس Aerial duel.
- الشوط يحدد من Period وليس من الدقيقة فقط.
- الوقت بدل الضائع محفوظ.
- Percentages وTop Speed والمقاييس المختلفة لها aggregation مناسب لطبيعتها بدل قاعدة تجميع واحدة.
- المقاييس الموسمية Snapshot يتم تمييزها عن مقاييس الفترة المختارة.

بعد استبعاد Own Goals بالطريقة الصحيحة، تطابق Raw Opta shot totals مع Match total shots في **180/180 team-sides** ضمن المباريات الحالية.

## ملاحظات تفسير مهمة

- `Bad touch` ليس Total Touches مكانيًا؛ المصدر لا يقدم Spatial Total Touches مباشرة بالشكل المطلوب.
- Shot Sequence تعني أحداثًا زمنية سابقة للتسديدة داخل نفس المباراة/الفريق/الشوط، وليست Possession sequence مؤكدة ما لم يوفر المصدر معرف استحواذ موثوقًا.
- بعض FPL snapshot metrics مثل `total_points` و`form` هي حالة موسمية عند آخر GW مختارة وليست مجموعًا مستقلًا للجولات المتفرقة.
- مصادر مختلفة قد تستخدم تعريفات مختلفة للـAssists أو xG/xA؛ المنتج يحتفظ بتمييز المصدر بدل دمج التعريفات بلا توضيح.
- الشعارات الخارجية لها fallback. يمكن استيراد Crest ZIP محلي؛ للحفاظ على حدود تخزين المتصفح يتم تخطي الصورة الأكبر من 120KB أو عند امتلاء التخزين المحلي.

## تحديث البيانات

من Data Studio يمكنك رفع Performance ZIP وEvents ZIP وتشغيل `Validate & apply`.

**أول تحديث بعد فك النسخة:** ارفع الأرشيفين معًا. بعد نجاح أول تحديث يحتفظ الخادم بنسخة منهما داخل `source_archives`، وبعدها يمكن تحديث أرشيف واحد مع استخدام الآخر المحفوظ.

الـrebuild يراجع التعارضات والملفات المنطقية المكررة، ويعيد بناء `data.js` فقط بعد نجاح التحقق. يحتفظ الخادم بنسخة احتياطية من البيانات السابقة داخل `backups` قبل الاستبدال.

التحديث التلقائي من الإنترنت غير مفعل؛ يحتاج مصدر بيانات مرخص ومهيأ.

## الملفات المهمة

- `index.html` — الواجهة.
- `styles.css` — التصميم والـresponsive system.
- `app.js` — منطق المنتج والتحليلات.
- `data.js` — البيانات المبنية محليًا.
- `server.py` — الخادم المحلي والتحديثات.
- `tools/rebuild.py` — validation + data rebuild.
- `QA_FINAL.md` — اختبارات النسخة النهائية وحدود بيئة الاختبار.
- `CHANGELOG_FINAL.md` — ملخص الإصلاحات والإضافات النهائية.
- `REBUILD_INFO.json` — بيانات آخر rebuild مرفق.

هذه نسخة تحليل محلية مبنية على الملفات المقدمة، وليست بديلًا رسميًا لخدمات Opta أو Fantasy Premier League.
