# پرواز نفرین‌شده — Cursed Flight (Telegram Mini App)

بازی اصلی **دست‌نخورده و بدون هیچ تغییری** از فایل `game.html` اجرا می‌شود (بایت‌به‌بایت همان فایل اصلی بازی).

## ساختار
- `app.xhtml` — ورودی اصلی مینی‌اپ برای CDNهای jsDelivr (بازی از `game.html` خوانده و تمام‌صفحه اجرا می‌شود)
- `index.html` — ورودی GitHub Pages (نسخه iframe مستقیم)
- `game.html` — فایل اصلی بازی (بدون تغییر)
- `assets/` — تمام دارایی‌های اصلی بازی (تصاویر و صداها)

## لینک‌های اجرا
- **اصلی — jsDelivr (کش یک‌ساله، مناسب ایران):**
  `https://cdn.jsdelivr.net/gh/prauofi21-svg/cursed-flight-app@v3/app.xhtml`
- GitHub Pages:
  `https://prauofi21-svg.github.io/cursed-flight-app/`

## نکته فنی
برخی CDNها (مثل jsDelivr و Statically) فایلهای `.html` را به‌صورت متن ساده سرو می‌کنند؛ به همین دلیل ورودی اصلی با پسوند `.xhtml` ساخته شده که سورس بازی را از `game.html` (دست‌نخورده) می‌خواند و با `srcdoc` داخل قاب تمام‌صفحه اجرا می‌کند.

## بات تلگرام
`@Midnight_talebot` — دکمه «شروع بازی 🎮» در نوار پایین چت.
