# 📸 SENDER – Rubika Automatic Image Sender

[🇬🇧 English](#-english) | [🇮🇷 فارسی](#-فارسی)

---

# 🇬🇧 English

## 📌 About

**SENDER** is a Python-based Android tool designed to find images inside a specified device folder and automatically send a randomly selected image to a designated Rubika group through a Rubika bot.

The project is designed to work with explicitly selected folders and files rather than scanning the entire device, helping reduce unnecessary access to private data.

## ✨ Features

* 📂 Access to the device's `DCIM` directory
* 📁 Detect folders and subfolders
* 🖼️ Find available images
* 🎲 Randomly select a folder
* 🎯 Randomly select an image
* 🤖 Connect to a Rubika bot
* 📤 Automatically send the selected image to a specified group
* 🖥️ Display execution stages in the terminal
* 🔢 Show the number of discovered files
* 📊 Display execution information
* 👤 Support for user-provided name and phone number
* 📱 Display device model and manufacturer
* 🤖 Display Android version
* 🕐 Display execution date and time
* 🔌 Properly manage bot connection and disconnection
* 🧩 Designed for future support of additional specified folders

## ⚙️ How It Works

1. The application accesses the configured storage location.
2. The selected folder and its subfolders are scanned.
3. Available image files are detected.
4. A folder is selected randomly.
5. An image is selected randomly from the available files.
6. The application connects to the Rubika bot.
7. The selected image is sent to the configured group.
8. Execution information is displayed in the terminal.
9. The bot connection is properly closed.

## 📊 Device Information

Depending on the configured implementation, the application can display:

* 👤 User-provided name
* 📞 User-provided phone number
* 📱 Device model
* 🏭 Device manufacturer
* 🤖 Android version
* 🕐 Execution date and time
* 🖼️ Number of discovered files

## 🛡️ Privacy & Permissions

SENDER is designed to operate on **specified folders and files** rather than indiscriminately accessing all personal data on the device.

Before running the project, make sure the application has only the storage permissions it actually needs.

The user should also be aware of which image will be sent and which Rubika group will receive it.

## 🛠️ Technologies

* 🐍 Python
* 📱 Pydroid
* 🤖 Rubika Bot
* 💾 Android Storage
* 📂 File System
* 🎲 Random File Selection

## 🚀 Future Improvements

Possible improvements include:

* 📂 Manual folder selection
* ✅ User confirmation before sending
* 🖼️ Image preview before transmission
* ⏱️ Configurable sending intervals
* 📋 Support for multiple selected folders
* 📊 More detailed execution logs

---

# 🇮🇷 فارسی

## 📌 درباره پروژه

**SENDER** یک ابزار اندرویدی مبتنی بر Python است که تصاویر موجود در پوشه‌های مشخص‌شده دستگاه را پیدا کرده و پس از انتخاب تصادفی یک تصویر، آن را از طریق ربات روبیکا به گروه تعیین‌شده ارسال می‌کند.

این پروژه به‌جای بررسی بدون محدودیت کل حافظه دستگاه، برای کار با **پوشه‌ها و فایل‌های مشخص‌شده** طراحی شده تا دسترسی غیرضروری به اطلاعات خصوصی کاهش پیدا کند.

## ✨ قابلیت‌ها

* 📂 دسترسی به پوشه `DCIM`
* 📁 شناسایی پوشه‌ها و زیرپوشه‌ها
* 🖼️ پیدا کردن تصاویر موجود
* 🎲 انتخاب تصادفی یک پوشه
* 🎯 انتخاب تصادفی یک تصویر
* 🤖 اتصال به ربات روبیکا
* 📤 ارسال خودکار تصویر به گروه مشخص‌شده
* 🖥️ نمایش مراحل اجرای برنامه در ترمینال
* 🔢 نمایش تعداد فایل‌های پیدا‌شده
* 📊 نمایش اطلاعات اجرای برنامه
* 👤 دریافت نام واردشده توسط کاربر
* 📞 دریافت شماره واردشده توسط کاربر
* 📱 نمایش مدل دستگاه
* 🏭 نمایش سازنده دستگاه
* 🤖 نمایش نسخه اندروید
* 🕐 نمایش تاریخ و زمان اجرای برنامه
* 🔌 مدیریت صحیح اتصال و قطع اتصال ربات
* 🧩 قابلیت توسعه برای پشتیبانی از پوشه‌های مشخص دیگر

## ⚙️ نحوه عملکرد

1. برنامه به مسیر حافظه تعیین‌شده دسترسی پیدا می‌کند.
2. پوشه انتخاب‌شده و زیرپوشه‌های آن بررسی می‌شوند.
3. فایل‌های تصویری موجود شناسایی می‌شوند.
4. یک پوشه به‌صورت تصادفی انتخاب می‌شود.
5. یک تصویر از فایل‌های موجود به‌صورت تصادفی انتخاب می‌شود.
6. برنامه به ربات روبیکا متصل می‌شود.
7. تصویر انتخاب‌شده به گروه مشخص‌شده ارسال می‌شود.
8. اطلاعات مراحل اجرا در ترمینال نمایش داده می‌شود.
9. اتصال ربات به‌درستی بسته می‌شود.

## 📊 اطلاعات دستگاه

برنامه می‌تواند، بر اساس پیاده‌سازی و مجوزهای تعریف‌شده، اطلاعات زیر را نمایش دهد:

* 👤 نام واردشده توسط کاربر
* 📞 شماره واردشده توسط کاربر
* 📱 مدل دستگاه
* 🏭 سازنده دستگاه
* 🤖 نسخه اندروید
* 🕐 تاریخ و زمان اجرا
* 🖼️ تعداد فایل‌های پیدا‌شده

## 🛡️ حریم خصوصی و دسترسی‌ها

SENDER برای کار با **پوشه‌ها و فایل‌های مشخص‌شده** طراحی شده و هدف آن دسترسی بدون محدودیت به تمام اطلاعات شخصی دستگاه نیست.

قبل از اجرای پروژه، فقط مجوزهای ذخیره‌سازی موردنیاز برنامه را فعال کنید.

همچنین کاربر باید بداند چه تصویری قرار است ارسال شود و تصویر به کدام گروه روبیکا ارسال خواهد شد.

## 🛠️ تکنولوژی‌های استفاده‌شده

* 🐍 Python
* 📱 Pydroid
* 🤖 Rubika Bot
* 💾 Android Storage
* 📂 File System
* 🎲 Random File Selection

## 🚀 قابلیت‌های قابل توسعه

در نسخه‌های آینده می‌توان قابلیت‌های زیر را اضافه کرد:

* 📂 انتخاب دستی پوشه
* ✅ تأیید کاربر قبل از ارسال
* 🖼️ نمایش پیش‌نمایش تصویر
* ⏱️ تعیین فاصله زمانی ارسال
* 📋 پشتیبانی از چند پوشه انتخابی
* 📊 لاگ و گزارش دقیق‌تر اجرای برنامه

---

## 👨‍💻 Developer

**Mohammad**

⭐ اگر پروژه برایتان مفید بود، به Repository ستاره بدهید.
