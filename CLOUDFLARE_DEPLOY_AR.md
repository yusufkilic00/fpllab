# FPL LAB — نسخة GitHub + Cloudflare

## المعمارية
- `data.js` = نسخة Admin محلية فقط، ولا ترفع إلى GitHub.
- `web_data/` = نسخة النشر المقسمة حسب Gameweek؛ هي التي ترفع إلى GitHub.
- `tools/build_cloudflare.py` يبني `dist/` من `web_data/` بدون الاعتماد على `data.js`.
- `functions/api/fpl/*` = Proxy للـOfficial FPL API حتى لا يعتمد المتصفح على CORS الخارجي.
- Data Studio Upload يظل متاحاً محلياً فقط؛ نسخة الإنترنت Read-only.

## تحديث الموسم
1. شغّل محلياً: `python server.py --open`
2. ارفع من Data Studio الملفين المعتادين:
   - `Premier-League-2026-2027.zip`
   - `EPL_2026_2027_English_Teams_By_Gameweek.zip`
3. `Validate & apply` يقوم الآن بتحديث الاثنين معاً:
   - `data.js` المحلي
   - `web_data/` الخاص بالنشر
4. اختبر:
   - Windows: `BUILD_CLOUDFLARE_WINDOWS.bat`
   - macOS/Linux: `./BUILD_CLOUDFLARE_MAC_LINUX.sh`
5. على GitHub اعمل commit لـ `web_data/` والكود فقط. `.gitignore` يمنع `data.js` وZIPs وbackups تلقائياً.

## لو عملت Clone جديد من GitHub وتريد النسخة المحلية
`data.js` غير موجود في Git عمداً. أنشئه من ملفات الويب:
```bash
python tools/restore_local_data.py
python server.py --open
```

## أول رفع على GitHub
```bash
git init
git add .
git commit -m "Cloudflare-ready FPL LAB"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/fpl-lab.git
git push -u origin main
```

## إعداد Cloudflare Pages
- Workers & Pages → Create → Pages → Import an existing Git repository
- Production branch: `main`
- Framework preset: `None`
- Build command: `python3 tools/build_cloudflare.py`
- Build output directory: `dist`

`functions/` يجب أن يظل في root للمشروع وليس داخل `dist/`.

## فحص قبل الـPush
```bash
python3 tools/build_cloudflare.py
python3 tools/qa_cloudflare.py
```

الـQA يفحص checksums لكل chunk، ويعيد تجميع الداتا، وإذا كان `data.js` المحلي موجوداً يقارن كل مفاتيح الداتا به.
