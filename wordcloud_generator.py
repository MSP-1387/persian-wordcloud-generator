#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import re
from collections import Counter
import numpy as np
import os
import json
from PIL import Image, ImageDraw
import colorsys
import random

def load_config(config_file="config.json"):
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file {config_file} not found, using default settings")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing config file: {e}")
        return {}

def create_random_color_func(hue, saturation, lightness_range):
    """Create a random color function with HSL control"""
    def random_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        # Generate random lightness within the specified range
        lightness = random.uniform(lightness_range[0], lightness_range[1])
        # Convert HSL to RGB
        rgb = colorsys.hls_to_rgb(hue/360, lightness/100, saturation/100)
        # Convert to hex
        return f'#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}'
    return random_color_func

def process_mask_image(mask_path, debug=False):
    """
    Process mask image using the simple, working approach from wordcloud_with_mask.py
    Returns: (mask_array, image_colors, success_message)
    """
    if not mask_path or not os.path.exists(mask_path):
        return None, None, "Mask file not found"
    
    try:
        # Load mask image using the simple approach that works
        mask = np.array(Image.open(mask_path))
        print(f"Loading mask: {mask_path}, Shape: {mask.shape}")
        
        # Create image color generator for color extraction
        image_colors = ImageColorGenerator(mask)
        
        success_msg = f"Mask loaded successfully using simple approach"
        print(success_msg)
        
        return mask, image_colors, success_msg
        
    except Exception as e:
        error_msg = f"Error loading mask from {mask_path}: {e}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return None, None, error_msg

def create_persian_wordcloud(text_array, config_file="config.json", output_file=None):
    """
    Create a Persian word cloud from an array of strings
    Complete version with external configuration
    """
    
    # Load configuration
    config = load_config(config_file)
    
    # Use provided output_file or config default
    if output_file is None:
        output_file = config.get("output_file", "wordcloud.png")
    
    # Get configuration values with defaults
    width = config.get("width", 800)
    height = config.get("height", 600)
    background_color = config.get("background_color", "white")
    mask_path = config.get("mask_path")
    max_words = config.get("max_words", 1000)
    min_font_size = config.get("min_font_size", 8)
    max_font_size = config.get("max_font_size", 300)
    relative_scaling = config.get("relative_scaling", 1.0)
    prefer_horizontal = config.get("prefer_horizontal", 0.3)
    random_state = config.get("random_state", 42)
    collocations = config.get("collocations", False)
    repeat = config.get("repeat", True)
    colormap = config.get("colormap", "plasma")
    mode = config.get("mode", "RGBA")
    dpi = config.get("dpi", 300)
    color_mode = config.get("color_mode", "colormap")
    custom_colors = config.get("custom_colors", {})
    stopwords = set(config.get("stopwords", []))
    font_paths = config.get("font_paths", [])
    smart_sizing_config = config.get("smart_sizing", {})
    
    # Join all strings and clean the text
    full_text = ' '.join(text_array)
    
    # Remove special characters and normalize Persian text
    persian_pattern = r'[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\s\d]'
    cleaned_text = re.sub(persian_pattern, ' ', full_text)
    
    # Split into words and filter out empty strings, short words, and stopwords
    words = cleaned_text.split()
    words = [word.strip() for word in words if len(word.strip()) > 1 and word.strip() not in stopwords]
    
    # Count word frequencies
    word_freq = Counter(words)
    
    # Apply smart sizing for better distribution
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    total_words = len(sorted_words)
    
    # Calculate size distribution
    extra_large_count = max(1, total_words // 3)
    large_count = max(1, total_words // 3)
    medium_count = max(1, total_words // 4)
    small_count = total_words - extra_large_count - large_count - medium_count
    
    # Get multipliers from config
    extra_large_mult = smart_sizing_config.get("extra_large_multiplier", 8)
    large_mult = smart_sizing_config.get("large_multiplier", 6)
    medium_mult = smart_sizing_config.get("medium_multiplier", 4)
    small_mult = smart_sizing_config.get("small_multiplier", 2)
    
    # Create new frequency dict with smart sizing
    new_freq = {}
    for i, (word, freq) in enumerate(sorted_words):
        if i < extra_large_count:
            new_freq[word] = freq * extra_large_mult
        elif i < extra_large_count + large_count:
            new_freq[word] = freq * large_mult
        elif i < extra_large_count + large_count + medium_count:
            new_freq[word] = freq * medium_mult
        else:
            new_freq[word] = freq * small_mult
    
    word_freq = new_freq
    print(f"Smart sizing applied: {extra_large_count} extra-large, {large_count} large, {medium_count} medium, {small_count} small words")
    
    # Get font path
    font_path = None
    for font in font_paths:
        if os.path.exists(font):
            font_path = font
            print(f"Using font: {font}")
            break
    
    if font_path is None:
        print("Warning: No Persian font found. Using system default.")
    
    # Process mask with improved handling
    mask = None
    image_colors = None
    
    if mask_path:
        mask, image_colors, mask_status = process_mask_image(mask_path, debug=True)
        if mask is None:
            print(f"Mask processing failed: {mask_status}")
            print("Continuing without mask...")
    
    # Create color function based on mode
    color_func = None
    if color_mode == "custom_colors" and custom_colors:
        hue = custom_colors.get("hue", 30)
        saturation = custom_colors.get("saturation", 80)
        lightness_range = custom_colors.get("lightness_range", [40, 80])
        color_func = create_random_color_func(hue, saturation, lightness_range)
        print(f"Using custom color function with hue={hue}, saturation={saturation}")
    elif color_mode == "image_colors" and image_colors:
        color_func = image_colors
        print("Using image color generator")
    
    # Create word cloud with complete settings
    # Note: WordCloud uses mask differently - True areas are where words CAN be placed
    # For WordCloud: True = areas where words CAN be placed, False = areas where words CANNOT be placed
    wordcloud = WordCloud(
        width=width,
        height=height,
        background_color=background_color,
        colormap=colormap if color_func is None else None,
        color_func=color_func,
        font_path=font_path,
        mask=mask,
        max_words=max_words,
        min_font_size=min_font_size,
        max_font_size=max_font_size,
        relative_scaling=relative_scaling,
        prefer_horizontal=prefer_horizontal,
        random_state=random_state,
        collocations=collocations,
        repeat=repeat,
        mode=mode,
        contour_width=0,  # No contour
        contour_color='black'
    )
    
    # Generate word cloud from frequencies
    wordcloud.generate_from_frequencies(word_freq)
    
    # Create matplotlib figure
    plt.figure(figsize=(12, 8))
    
    # Show wordcloud with proper mask handling
    if mask is not None:
        # Show wordcloud normally - the mask is already applied during generation
        plt.imshow(wordcloud, interpolation='bilinear')
    else:
        # No mask, just show wordcloud normally
        plt.imshow(wordcloud, interpolation='bilinear')
    
    plt.axis('off')
    plt.tight_layout(pad=0)
    
    # Save the word cloud
    plt.savefig(output_file, dpi=dpi, bbox_inches='tight', 
                facecolor=background_color, edgecolor='none')
    plt.close()
    
    print(f"Word cloud saved as {output_file}")
    print(f"Total unique words: {len(word_freq)}")
    # Show most common words
    word_freq_counter = Counter(word_freq)
    print(f"Most common words: {word_freq_counter.most_common(10)}")
    
    return wordcloud

def main():
    """Example usage of the word cloud generator"""
    
    # Sample Persian text array - Much more data for better filling
    sample_texts = [
        # Technology and Programming
        "سلام دنیا", "این یک متن نمونه است", "ابر کلمات فارسی", "پایتون و پردازش متن",
        "یادگیری ماشین و هوش مصنوعی", "برنامه نویسی و توسعه نرم افزار", "داده کاوی و تحلیل اطلاعات",
        "وب و اینترنت", "موبایل و اپلیکیشن", "امنیت و رمزنگاری", "پایگاه داده و ذخیره اطلاعات",
        "الگوریتم و ساختار داده", "شبکه و ارتباطات", "سیستم عامل و نرم افزار", "گرافیک و طراحی",
        "بازی و سرگرمی", "آموزش و یادگیری", "تحقیق و پژوهش", "توسعه و پیشرفت", "فناوری و نوآوری",
        
        # Science and Education
        "علم و دانش", "تحقیقات علمی", "آزمایشگاه و پژوهش", "کتابخانه و مطالعه", "دانشگاه و تحصیل",
        "استاد و دانشجو", "کلاس درس", "امتحان و نمره", "تدریس و آموزش", "کتاب و مقاله",
        "مجله علمی", "کنفرانس و همایش", "پروژه تحقیقاتی", "نظریه و فرضیه", "تحلیل آماری",
        
        # Business and Economy
        "تجارت و بازرگانی", "اقتصاد و مالی", "سرمایه گذاری", "بازار و بورس", "شرکت و سازمان",
        "مدیریت و رهبری", "کارآفرینی", "استارتاپ", "بازاریابی", "فروش و درآمد",
        "سود و زیان", "قیمت و هزینه", "تولید و صنعت", "خدمات و مشتری", "رقابت و کیفیت",
        
        # Health and Medicine
        "سلامت و بهداشت", "پزشکی و درمان", "بیمارستان و کلینیک", "دکتر و پرستار", "دارو و درمان",
        "بیماری و سلامتی", "پیشگیری و واکسن", "جراحی و عمل", "تشخیص و آزمایش", "درمان و بهبود",
        
        # Culture and Arts
        "فرهنگ و هنر", "موسیقی و آواز", "سینما و فیلم", "تئاتر و نمایش", "ادبیات و شعر",
        "نقاشی و طراحی", "مجسمه سازی", "عکاسی و تصویر", "رقص و حرکات موزون", "کتاب و داستان",
        
        # Sports and Recreation
        "ورزش و بازی", "فوتبال و تیم", "کشتی و زورخانه", "شنا و استخر", "دو و میدانی",
        "بسکتبال و سبد", "تنیس و راکت", "والیبال و تور", "کوهنوردی و طبیعت", "سفر و گردشگری",
        
        # Food and Cooking
        "غذا و آشپزی", "پخت و پز", "دستور پخت", "مواد غذایی", "سبزیجات و میوه",
        "گوشت و مرغ", "برنج و نان", "شیرینی و دسر", "نوشیدنی و آب", "رستوران و کافه",
        
        # Family and Relationships
        "خانواده و عشق", "پدر و مادر", "فرزند و کودک", "برادر و خواهر", "دوست و همکار",
        "عشق و محبت", "ازدواج و زندگی", "خانه و خانواده", "محبت و مهربانی", "احترام و ادب",
        
        # Nature and Environment
        "طبیعت و محیط زیست", "درخت و جنگل", "دریا و اقیانوس", "کوه و دشت", "آب و هوا",
        "خورشید و ماه", "ستاره و آسمان", "گیاه و گل", "حیوان و پرنده", "محیط زیست و حفاظت",
        
        # Transportation and Travel
        "حمل و نقل", "ماشین و اتومبیل", "هواپیما و پرواز", "قطار و راه آهن", "اتوبوس و تاکسی",
        "سفر و مسافرت", "هتل و اقامت", "بلیط و رزرو", "مسیر و راه", "سفرنامه و خاطرات",
        
        # Communication and Media
        "ارتباطات و رسانه", "تلویزیون و رادیو", "اخبار و گزارش", "مصاحبه و گفتگو", "پیام و ایمیل",
        "تلفن و موبایل", "اینترنت و شبکه", "چت و پیامک", "ویدیو و عکس", "پادکست و وبلاگ",
        
        # Politics and Society
        "سیاست و حکومت", "انتخابات و رای", "قانون و حقوق", "عدالت و دادگاه", "پلیس و امنیت",
        "دولت و وزارتخانه", "نماینده و مجلس", "رئیس جمهور و نخست وزیر", "مردم و جامعه", "دموکراسی و آزادی",
        
        # Religion and Spirituality
        "دین و مذهب", "عبادت و نماز", "مسجد و معبد", "روزه و روزه داری", "حج و زیارت",
        "قرآن و کتاب مقدس", "امام و روحانی", "دعا و نیایش", "ایمان و اعتقاد", "اخلاق و معنویت",
        
        # Time and History
        "زمان و تاریخ", "گذشته و آینده", "تاریخ و وقایع", "قرن و سال", "ماه و هفته",
        "روز و شب", "ساعت و دقیقه", "تقویم و تاریخ", "خاطرات و یادها", "آثار تاریخی",
        
        # Emotions and Feelings
        "احساسات و عواطف", "شادی و خوشحالی", "غم و ناراحتی", "عشق و محبت", "ترس و اضطراب",
        "امید و آرزو", "نگرانی و دلهره", "خشم و عصبانیت", "تعجب و حیرت", "رضایت و خشنودی",
        
        # Work and Career
        "کار و شغل", "دفتر و شرکت", "همکار و رئیس", "پروژه و وظیفه", "مذاکره و جلسه",
        "ارتقا و پیشرفت", "حقوق و دستمزد", "ساعت کاری", "مرخصی و تعطیلات", "بازنشستگی",
        
        # Shopping and Fashion
        "خرید و فروش", "فروشگاه و مغازه", "لباس و مد", "کفش و کیف", "جواهرات و زیورآلات",
        "لوازم آرایش", "عطر و ادکلن", "ساعت و زیور", "پوشاک و البسه", "مد و استایل",
        
        # Home and Living
        "خانه و زندگی", "اتاق و مبلمان", "آشپزخانه و وسایل", "حمام و سرویس", "بالکن و حیاط",
        "گل و گیاه", "حیوان خانگی", "تعمیر و نگهداری", "دکوراسیون و تزئین", "آرامش و راحتی",
        
        # Language and Communication
        "زبان و گفتار", "کلمات و جملات", "معنی و مفهوم", "ترجمه و تفسیر", "دیکشنری و فرهنگ",
        "گرامر و دستور زبان", "تلفظ و لهجه", "مکالمه و گفتگو", "نامه و نامه نگاری", "سخنرانی و خطابه",
        
        # Additional words for better filling
        "کامپیوتر", "لپ تاپ", "تلفن همراه", "تبلت", "هدفون", "اسپیکر", "ماوس", "کیبورد",
        "مانیتور", "پرینتر", "اسکنر", "فلش", "هارد دیسک", "رم", "پردازنده", "کارت گرافیک",
        "مادربورد", "پاور", "کیس", "کولر", "فن", "کابل", "سوکت", "پورت", "یو اس بی",
        "وای فای", "بلوتوث", "جی پی اس", "دوربین", "میکروفون", "اسپیکر", "آمپلیفایر",
        "گیتار", "پیانو", "ویولن", "درام", "ساکسیفون", "ترومپت", "فلوت", "کلارینت",
        "آکاردئون", "هارمونیکا", "بانجو", "ماندولین", "عود", "تار", "سه تار", "کمانچه",
        "نی", "دف", "دایره", "تمبک", "سنج", "قاشقک", "چنگ", "سنتور", "قانون", "بربط"
    ]
    
    # Create word cloud with configuration
    create_persian_wordcloud(
        text_array=sample_texts,
        config_file="config.json"
    )

if __name__ == "__main__":
    main()
