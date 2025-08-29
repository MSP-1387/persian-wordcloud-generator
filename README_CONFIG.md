# Persian Word Cloud Generator - Configuration Guide

## 📋 فایل تنظیمات (config.json)

این پروژه از فایل `config.json` برای تنظیم تمام پارامترها استفاده می‌کند. بدون نیاز به تغییر کد، می‌توانید خروجی مورد نظرتان را تنظیم کنید.

## 🎨 تنظیمات رنگ

### 1. رنگ‌های سفارشی (Custom Colors)
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
- **hue**: رنگ پایه (0-360)
  - 0: قرمز
  - 120: سبز
  - 240: آبی
  - 30: نارنجی
- **saturation**: اشباع رنگ (0-100)
- **lightness_range**: محدوده روشنایی [کمترین, بیشترین]

### 2. رنگ از تصویر (Image Colors)
```json
{
    "color_mode": "image_colors",
    "mask_path": "your_image.png"
}
```
رنگ‌ها از تصویر ماسک استخراج می‌شوند.

### 3. رنگ‌های پیش‌فرض (Colormap)
```json
{
    "color_mode": "colormap",
    "colormap": "plasma"
}
```
گزینه‌های colormap: `plasma`, `viridis`, `Set3`, `tab10`, `hsv`

## 🖼️ تنظیمات ماسک

### بدون ماسک (مستطیل)
```json
{
    "mask_path": null
}
```

### با ماسک سفارشی
```json
{
    "mask_path": "your_mask.png"
}
```

## 📏 تنظیمات اندازه

```json
{
    "width": 1000,
    "height": 800,
    "max_words": 1000,
    "min_font_size": 8,
    "max_font_size": 300,
    "dpi": 300
}
```

## 🎯 تنظیمات چیدمان

```json
{
    "relative_scaling": 1.0,
    "prefer_horizontal": 0.3,
    "random_state": 42,
    "collocations": false,
    "repeat": true
}
```

- **relative_scaling**: نسبت اندازه کلمات (0.5-1.0)
- **prefer_horizontal**: ترجیح کلمات افقی (0.0-1.0)
- **random_state**: عدد ثابت برای چیدمان ثابت
- **collocations**: اجازه تکرار کلمات
- **repeat**: تکرار کلمات برای پر کردن فضا

## 🚫 کلمات حذف شده (Stopwords)

```json
{
    "stopwords": [
        "و", "که", "در", "به", "از", "با", "برای", "این", "آن", "را",
        "است", "بود", "شد", "خواهد", "دارد"
    ]
}
```

## 📊 سایزبندی هوشمند

```json
{
    "smart_sizing": {
        "extra_large_multiplier": 8,
        "large_multiplier": 6,
        "medium_multiplier": 4,
        "small_multiplier": 2
    }
}
```

## 🔤 تنظیمات فونت

```json
{
    "font_paths": [
        "fonts/Vazir-Regular.ttf",
        "fonts/Vazir-Medium.ttf",
        "fonts/Vazir-Bold.ttf"
    ]
}
```

## 📝 مثال‌های کامل

### مثال 1: ابر کلمات نارنجی بدون ماسک
```json
{
    "output_file": "orange_wordcloud.png",
    "width": 1200,
    "height": 800,
    "background_color": "white",
    "mask_path": null,
    "color_mode": "custom_colors",
    "custom_colors": {
        "hue": 30,
        "saturation": 80,
        "lightness_range": [40, 80]
    },
    "max_words": 500,
    "random_state": 42
}
```

### مثال 2: ابر کلمات با رنگ از تصویر
```json
{
    "output_file": "image_colored_wordcloud.png",
    "width": 1000,
    "height": 1000,
    "background_color": "black",
    "mask_path": "heart_mask.png",
    "color_mode": "image_colors",
    "max_words": 800,
    "min_font_size": 12,
    "max_font_size": 200
}
```

### مثال 3: ابر کلمات آبی با چیدمان ثابت
```json
{
    "output_file": "blue_fixed_wordcloud.png",
    "width": 800,
    "height": 600,
    "background_color": "white",
    "mask_path": null,
    "color_mode": "custom_colors",
    "custom_colors": {
        "hue": 240,
        "saturation": 70,
        "lightness_range": [30, 70]
    },
    "random_state": 123,
    "relative_scaling": 0.8,
    "prefer_horizontal": 0.7
}
```

## 🚀 نحوه استفاده

1. فایل `config.json` را ویرایش کنید
2. کد را اجرا کنید:
```bash
python3 wordcloud_generator.py
```

## 📋 تمام تنظیمات موجود

| تنظیم | نوع | پیش‌فرض | توضیح |
|-------|-----|---------|-------|
| `output_file` | string | "wordcloud.png" | نام فایل خروجی |
| `width` | integer | 800 | عرض تصویر |
| `height` | integer | 600 | ارتفاع تصویر |
| `background_color` | string | "white" | رنگ پس‌زمینه |
| `mask_path` | string/null | null | مسیر فایل ماسک |
| `max_words` | integer | 1000 | حداکثر تعداد کلمات |
| `min_font_size` | integer | 8 | حداقل اندازه فونت |
| `max_font_size` | integer | 300 | حداکثر اندازه فونت |
| `relative_scaling` | float | 1.0 | نسبت اندازه کلمات |
| `prefer_horizontal` | float | 0.3 | ترجیح کلمات افقی |
| `random_state` | integer | 42 | عدد ثابت برای چیدمان |
| `collocations` | boolean | false | اجازه تکرار کلمات |
| `repeat` | boolean | true | تکرار کلمات |
| `colormap` | string | "plasma" | نقشه رنگ |
| `mode` | string | "RGBA" | حالت رنگ |
| `dpi` | integer | 300 | کیفیت تصویر |
| `color_mode` | string | "colormap" | حالت رنگ |
| `custom_colors` | object | {} | تنظیمات رنگ سفارشی |
| `stopwords` | array | [] | کلمات حذف شده |
| `font_paths` | array | [] | مسیرهای فونت |
| `smart_sizing` | object | {} | تنظیمات سایزبندی |

## 💡 نکات مهم

1. **فایل ماسک**: اگر `mask_path` null باشد، ابر کلمات مستطیلی ساخته می‌شود
2. **رنگ‌های سفارشی**: با HSL کنترل می‌شوند
3. **چیدمان ثابت**: با `random_state` ثابت می‌شود
4. **کلمات حذف شده**: کلمات بی‌معنی را حذف می‌کند
5. **سایزبندی هوشمند**: کلمات را به 4 دسته تقسیم می‌کند
