# Persian Word Cloud Generator

یک تولیدکننده ابر کلمات فارسی پیشرفته با قابلیت تنظیمات خارجی و ویژگی‌های متنوع.

## 🌟 ویژگی‌ها

- ✅ **پشتیبانی کامل از فارسی** - حروف فارسی و اعداد
- ✅ **تنظیمات خارجی** - بدون نیاز به تغییر کد
- ✅ **رنگ‌های سفارشی** - کنترل HSL برای رنگ‌ها
- ✅ **رنگ از تصویر** - استخراج رنگ از ماسک
- ✅ **حذف کلمات بی‌معنی** - stopwords فارسی و انگلیسی
- ✅ **چیدمان ثابت** - با random_state
- ✅ **سایزبندی هوشمند** - 4 دسته اندازه مختلف
- ✅ **پشتیبانی از ماسک** - شکل‌های سفارشی
- ✅ **کیفیت بالا** - 300 DPI

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها
```bash
pip install -r requirements.txt
```

### اجرا
```bash
python3 wordcloud_generator.py
```

## 📋 فایل‌های پروژه

- `wordcloud_generator.py` - کد اصلی
- `config.json` - فایل تنظیمات
- `README_CONFIG.md` - راهنمای کامل تنظیمات
- `requirements.txt` - وابستگی‌ها
- `fonts/` - پوشه فونت‌های فارسی

## ⚙️ تنظیمات سریع

فایل `config.json` را ویرایش کنید:

```json
{
    "output_file": "my_wordcloud.png",
    "width": 1000,
    "height": 800,
    "color_mode": "custom_colors",
    "custom_colors": {
        "hue": 30,
        "saturation": 80,
        "lightness_range": [40, 80]
    }
}
```

## 🎨 مثال‌های تنظیمات

### رنگ‌های نارنجی
```json
{
    "color_mode": "custom_colors",
    "custom_colors": {
        "hue": 30,
        "saturation": 80,
        "lightness_range": [40, 80]
    }
}
```

### رنگ از تصویر
```json
{
    "color_mode": "image_colors",
    "mask_path": "your_image.png"
}
```

### رنگ‌های پیش‌فرض
```json
{
    "color_mode": "colormap",
    "colormap": "plasma"
}
```

## 📖 مستندات کامل

برای اطلاعات بیشتر، فایل [README_CONFIG.md](README_CONFIG.md) را مطالعه کنید.

## 🤝 مشارکت

1. Fork کنید
2. Branch جدید بسازید (`git checkout -b feature/amazing-feature`)
3. تغییرات را commit کنید (`git commit -m 'Add amazing feature'`)
4. Push کنید (`git push origin feature/amazing-feature`)
5. Pull Request بسازید

## 📄 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.

## 🙏 تشکر

- فونت Vazir از [rastikerdar](https://github.com/rastikerdar/vazir-font)
- کتابخانه wordcloud از [amueller](https://github.com/amueller/word_cloud)
