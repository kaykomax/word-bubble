import os
import json
import platform
import ctypes
import random

SETTINGS_FILE = "settings.json"
DATA_FOLDER = "word_lists"
FONTS_FOLDER = "fonts"
ICON_FOLDER = "icon"

os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(FONTS_FOLDER, exist_ok=True)
os.makedirs(ICON_FOLDER, exist_ok=True)

TRANSLATIONS = {
    "fa": {
        "window_title": "حباب لغت",
        "settings_btn": "تنظیمات",
        "manage_btn": "مدیریت لغات و لیست‌ها",
        "select_list_btn": "انتخاب لیست",
        "play_mode_btn": "نحوه پخش",
        "toggle_play": {"play": "   پخش ", "pause": "    توقف"},
        "dark_mode_label": "حالت شب",
        "selected_list_label": "لیست انتخابی: {list_name}",
        "no_list_selected": "لیست انتخابی: هیچ لیستی انتخاب نشده",
        "manage_title": "مدیریت لغات و لیست‌ها",
        "select_list": "انتخاب لیست:",
        "words_label": "لغات:",
        "add_word_btn": "افزودن لغت",
        "edit_word_btn": "ویرایش لغت",
        "delete_word_btn": "حذف لغت",
        "new_list_btn": "لیست جدید",
        "rename_list_btn": "تغییر نام لیست",
        "delete_list_btn": "حذف لیست",
        "import_list_btn": "وارد کردن لیست",
        "no_list_error": "هیچ لیستی موجود نیست",
        "add_word_title": "لغت جدید",
        "add_word_prompt": "لغت را وارد کنید:",
        "add_meaning_prompt": "معنی را وارد کنید:",
        "edit_word_title": "ویرایش لغت",
        "edit_meaning_prompt": "معنی:",
        "delete_word_confirm": "آیا مطمئن هستید؟",
        "new_list_title": "لیست جدید",
        "new_list_prompt": "نام لیست:",
        "rename_list_title": "تغییر نام لیست",
        "rename_list_prompt": "نام جدید:",
        "delete_list_confirm": "آیا مطمئن هستید؟ این کار تمام لغات این لیست را حذف می‌کند.",
        "list_exists_error": "لیستی با این نام وجود دارد.",
        "import_list_title": "وارد کردن لیست",
        "import_list_prompt": "نام لیست جدید:",
        "import_list_replace": "لیستی با نام '{name}' وجود دارد. آیا می‌خواهید آن را جایگزین کنید؟",
        "import_list_invalid": "فایل انتخاب‌شده معتبر نیست. لطفاً فایلی با فرمت صحیح (word::meaning) انتخاب کنید.",
        "import_list_empty": "فایل انتخاب‌شده خالی است یا هیچ لغت معتبری ندارد。",
        "select_list_title": "انتخاب لیست",
        "select_list_prompt": "یک لیست را انتخاب کنید:",
        "no_lists_found": "هیچ لیستی یافت نشد。",
        "settings_title": "تنظیمات",
        "bubble_duration": "مدت نمایش حباب",
        "bubble_interval": "فاصله بین حباب‌ها",
        "font_size": "اندازه فونت",
        "word_color": "رنگ لغت",
        "meaning_color": "رنگ معنی",
        "bg_color": "رنگ پس‌زمینه",
        "opacity": "شفافیت پس‌زمینه",
        "top_most": "جایگاه نمایش",
        "top_most_options": ["فقط روی دسکتاپ", "روی همه برنامه‌ها"],
        "alignment": "ترازبندی متن",
        "alignment_options": ["راست‌چین", "چپ‌چین", "وسط‌چین"],
        "font_select": "انتخاب فونت",
        "import_font_btn": "وارد کردن فونت",
        "import_font_title": "انتخاب فایل فونت",
        "font_exists_replace": "فونت '{name}' قبلاً وجود دارد. آیا می‌خواهید آن را جایگزین کنید؟",
        "import_font_error": "فایل انتخاب‌شده معتبر نیست. لطفاً فایل فونت با فرمت .ttf یا .otf انتخاب کنید。",
        "bubble_position": "مکان حباب",
        "bubble_position_options": [
            "تصادفی", "بالا چپ", "بالا راست", "پایین چپ", "پایین راست", "وسط",
            "آبشاری (بالا چپ)", "آبشاری (بالا راست)", "آبشاری (بالا وسط)",
            "چپ به راست (بالا چپ)", "چپ به راست (پایین چپ)",
            "راست به چپ (بالا راست)", "راست به چپ (پایین راست)",
            "آبشاری راست به چپ (بالا راست)", "آبشاری چپ به راست (بالا چپ)",
            "آبشاری راست به چپ (پایین راست)", "آبشاری چپ به راست (پایین چپ)",
            "بالا به پایین (بالا چپ)", "بالا به پایین (بالا وسط)", "بالا به پایین (بالا راست)"
        ],
        "no_fonts_found": "هیچ فونتی یافت نشد",
        "preview_btn": "پیش‌نمایش حباب",
        "save_btn": "ذخیره تنظیمات",
        "language_select": "انتخاب زبان",
        "language_options": ["فارسی", "انگلیسی"],
        "play_mode_title": "نحوه پخش",
        "play_mode_prompt": "نحوه پخش را انتخاب کنید:",
        "play_mode_options": ["پخش پشت سر هم", "پخش رندوم"],
        "seconds": "{value} ثانیه",
        "preview_word": "پیش‌نمایش",
        "preview_meaning": "نمایش آزمایشی",
        "already_running": "برنامه در حال اجرا است!"
    },
    "en": {
        "window_title": "Word Bubble",
        "settings_btn": "Settings",
        "manage_btn": "Manage Words and Lists",
        "select_list_btn": "Select List",
        "play_mode_btn": "Play Mode",
        "toggle_play": {"play": "    Play", "pause": "  Pause"},
        "dark_mode_label": "Dark Mode",
        "selected_list_label": "Selected List: {list_name}",
        "no_list_selected": "Selected List: No list selected",
        "manage_title": "Manage Words and Lists",
        "select_list": "Select List:",
        "words_label": "Words:",
        "add_word_btn": "Add Word",
        "edit_word_btn": "Edit Word",
        "delete_word_btn": "Delete Word",
        "new_list_btn": "New List",
        "rename_list_btn": "Rename List",
        "delete_list_btn": "Delete List",
        "import_list_btn": "Import List",
        "no_list_error": "No lists available",
        "add_word_title": "New Word",
        "add_word_prompt": "Enter the word:",
        "add_meaning_prompt": "Enter the meaning:",
        "edit_word_title": "Edit Word",
        "edit_meaning_prompt": "Meaning:",
        "delete_word_confirm": "Are you sure?",
        "new_list_title": "New List",
        "new_list_prompt": "List name:",
        "rename_list_title": "Rename List",
        "rename_list_prompt": "New name:",
        "delete_list_confirm": "Are you sure? This will delete all words in this list.",
        "list_exists_error": "A list with this name already exists.",
        "import_list_title": "Import List",
        "import_list_prompt": "Enter the new list name:",
        "import_list_replace": "A list named '{name}' already exists. Do you want to replace it?",
        "import_list_invalid": "The selected file is invalid. Please select a file with the correct format (word::meaning).",
        "import_list_empty": "The selected file is empty or contains no valid words.",
        "select_list_title": "Select List",
        "select_list_prompt": "Choose list:",
        "no_lists_found": "No lists found.",
        "settings_title": "Settings",
        "bubble_duration": "Bubble Display Time",
        "bubble_interval": "Bubble Interval",
        "font_size": "Font Size",
        "word_color": "Word Color",
        "meaning_color": "Meaning Color",
        "bg_color": "Background Color",
        "opacity": "Background Opacity",
        "top_most": "Display Position",
        "top_most_options": ["Desktop Only", "Above All Apps"],
        "alignment": "Text Alignment",
        "alignment_options": ["Right", "Left", "Center"],
        "font_select": "Select Font",
        "import_font_btn": "Import Font",
        "import_font_title": "Select Font File",
        "font_exists_replace": "Font '{name}' already exists. Do you want to replace it?",
        "import_font_error": "The selected file is invalid. Please select a font file with .ttf or .otf format.",
        "bubble_position": "Bubble Position",
        "bubble_position_options": [
            "Random", "Top Left", "Top Right", "Bottom Left", "Bottom Right", "Center",
            "Cascade (Top Left)", "Cascade (Top Right)", "Cascade (Top Center)",
            "Left to Right (Top Left)", "Left to Right (Bottom Left)",
            "Right to Left (Top Right)", "Right to Left (Bottom Right)",
            "Cascade Right to Left (Top Right)", "Cascade Left to Right (Top Left)",
            "Cascade Right to Left (Bottom Right)", "Cascade Left to Right (Bottom Left)",
            "Top to Bottom (Top Left)", "Top to Bottom (Top Center)", "Top to Bottom (Top Right)"
        ],
        "no_fonts_found": "No fonts found",
        "preview_btn": "Preview Bubble",
        "save_btn": "Save Settings",
        "language_select": "Select Language",
        "language_options": ["Persian", "English"],
        "play_mode_title": "Play Mode",
        "play_mode_prompt": "Select play mode:",
        "play_mode_options": ["Sequential", "Random"],
        "seconds": "{value} seconds",
        "preview_word": "Preview",
        "preview_meaning": "Test Display",
        "already_running": "Application is already running!"
    }
}

def load_settings():
    default_settings = {
        "selected_file": "",
        "bubble_duration": 5,
        "bubble_interval": 15,
        "font_size": 13,
        "word_color": "#000000",
        "meaning_color": "#0000FF",
        "bg_color": "#CCFFFF",
        "opacity": 0.9,
        "top_most": True,
        "text_alignment": "right",
        "selected_font": "Vazir.ttf",
        "language": "fa",
        "play_mode": "random",
        "bubble_position": "random",
        "dark_mode": False
    }
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                loaded_settings = json.load(f)
                default_settings.update(loaded_settings)
        except Exception:
            pass
    return default_settings

def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

def list_word_files():
    return [f for f in os.listdir(DATA_FOLDER) if f.endswith(".txt")]

def load_words_from_file(file_name):
    words = []
    file_path = os.path.join(DATA_FOLDER, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and "::" in line:
                    word, meaning = line.split("::", 1)
                    word = word.strip()
                    meaning = meaning.strip()
                    if word and meaning:
                        words.append((word, meaning))
    return words

def save_words_to_file(file_name, words):
    file_path = os.path.join(DATA_FOLDER, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        for word, meaning in words:
            f.write(f"{word}::{meaning}\n")

def list_font_files():
    return [f for f in os.listdir(FONTS_FOLDER) if f.lower().endswith((".ttf", ".otf"))]

def is_rtl(text):
    if not text:
        return False
    first_char = text[0]
    return ord(first_char) >= 0x0600 and ord(first_char) <= 0x06FF

def set_window_title_bar_theme(window, dark_mode):
    if platform.system() == "Windows":
        try:
            hwnd = window.winId().__int__()
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            value = 1 if dark_mode else 0
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(ctypes.c_int(value)),
                ctypes.sizeof(ctypes.c_int)
            )
        except Exception:
            pass