import asyncio
import os
import platform
import random
import subprocess
import zipfile
from datetime import datetime

from rubka import Robot
from config import (
    BOT_TOKEN,
    GROUP_ID,
    SOURCE_FOLDERS,
    MAX_FILES,
    MAX_TOTAL_SIZE_MB,
)


# ==================================================
# تنظیمات
# ==================================================

EXCLUDED_DIR_NAMES = {
    ".thumbnails",
    ".cache",
    "cache",
    "thumbnails",
}

SKIP_HIDDEN_FILES = True


# ==================================================
# اطلاعات دستگاه
# ==================================================

def get_android_property(name):
    try:
        result = subprocess.run(
            ["getprop", name],
            capture_output=True,
            text=True,
            timeout=5
        )

        value = result.stdout.strip()

        if value:
            return value

    except Exception:
        pass

    return "Unknown"


def get_device_info():
    manufacturer = get_android_property(
        "ro.product.manufacturer"
    )

    model = get_android_property(
        "ro.product.model"
    )

    android_version = get_android_property(
        "ro.build.version.release"
    )

    if manufacturer == "Unknown":
        manufacturer = platform.system()

    if model == "Unknown":
        model = platform.machine()

    return {
        "manufacturer": manufacturer,
        "model": model,
        "android": android_version,
    }


# ==================================================
# پیدا کردن فایل‌ها
# ==================================================

def collect_files():
    all_files = []
    existing_sources = []

    for source in SOURCE_FOLDERS:

        if not os.path.isdir(source):
            print("[-] Folder not found:")
            print(source)
            continue

        existing_sources.append(source)

        for root, dirs, files in os.walk(source):

            # حذف پوشه‌های اضافی
            dirs[:] = [
                directory
                for directory in dirs
                if directory.lower() not in EXCLUDED_DIR_NAMES
                and not (
                    directory.startswith(".")
                    and directory != "."
                )
            ]

            for filename in files:

                # حذف فایل‌های مخفی
                if SKIP_HIDDEN_FILES and filename.startswith("."):
                    continue

                full_path = os.path.join(
                    root,
                    filename
                )

                if os.path.isfile(full_path):
                    all_files.append(full_path)

    return existing_sources, all_files


# ==================================================
# اندازه فایل
# ==================================================

def get_file_size_bytes(file_path):
    try:
        return os.path.getsize(file_path)
    except Exception:
        return 0


def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"

    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"

    if size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"

    return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


# ==================================================
# انتخاب فایل‌ها با محدودیت تعداد و حجم
# ==================================================

def select_files(files):

    max_size_bytes = (
        MAX_TOTAL_SIZE_MB * 1024 * 1024
    )

    random.shuffle(files)

    selected_files = []
    total_size = 0

    for file_path in files:

        if len(selected_files) >= MAX_FILES:
            break

        file_size = get_file_size_bytes(
            file_path
        )

        # اگر فایل به تنهایی از سقف بزرگ‌تر باشد
        if file_size > max_size_bytes:
            print(
                f"[-] Skipping large file: "
                f"{os.path.basename(file_path)} "
                f"({format_size(file_size)})"
            )
            continue

        # اگر با این فایل از سقف عبور کنیم
        if total_size + file_size > max_size_bytes:
            continue

        selected_files.append(file_path)
        total_size += file_size

        if total_size >= max_size_bytes:
            break

    return selected_files, total_size


# ==================================================
# مسیر فایل داخل ZIP
# ==================================================

def get_archive_path(file_path):

    normalized_file = os.path.normpath(
        file_path
    )

    for source in SOURCE_FOLDERS:

        normalized_source = os.path.normpath(
            source
        )

        if (
            normalized_file == normalized_source
            or normalized_file.startswith(
                normalized_source + os.sep
            )
        ):

            relative_path = os.path.relpath(
                normalized_file,
                normalized_source
            )

            source_name = os.path.basename(
                normalized_source
            )

            return os.path.join(
                source_name,
                relative_path
            )

    return os.path.basename(
        normalized_file
    )


# ==================================================
# گزارش اجرا
# ==================================================

def build_report(
    user_name,
    phone_number,
    device_info,
    existing_sources,
    found_count,
    selected_count,
    total_size,
    start_time
):

    source_text = "\n".join(
        f"📂 {path}"
        for path in existing_sources
    )

    return f"""
🚀 SENDER STARTED

👤 User: {user_name}
📞 Phone: {phone_number}

📱 Device Model: {device_info['model']}
🏭 Manufacturer: {device_info['manufacturer']}
🤖 Android: {device_info['android']}

🕐 Time: {start_time}

📁 Sources:
{source_text}

📦 Files found: {found_count}
📤 Files selected: {selected_count}
💾 Selected size: {format_size(total_size)}

📦 Maximum files: {MAX_FILES}
💾 Maximum input size: {MAX_TOTAL_SIZE_MB} MB

📦 Delivery method:
ZIP archive
""".strip()


# ==================================================
# ساخت ZIP
# ==================================================

def create_zip(
    files,
    report_text,
    zip_path
):

    if os.path.exists(zip_path):
        os.remove(zip_path)

    added_count = 0
    failed_count = 0
    added_size = 0

    with zipfile.ZipFile(
        zip_path,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=6,
        allowZip64=True
    ) as zip_file:

        # ------------------------------------------
        # گزارش
        # ------------------------------------------

        zip_file.writestr(
            "SENDER_REPORT.txt",
            report_text
        )

        # ------------------------------------------
        # فایل‌ها
        # ------------------------------------------

        for index, file_path in enumerate(
            files,
            start=1
        ):

            archive_path = get_archive_path(
                file_path
            )

            print(
                f"[{index}/{len(files)}] "
                f"Adding: {archive_path}"
            )

            try:

                zip_file.write(
                    file_path,
                    archive_path
                )

                added_count += 1
                added_size += get_file_size_bytes(
                    file_path
                )

            except Exception as e:

                failed_count += 1

                print(
                    "[-] Could not add file:"
                )

                print(file_path)

                print(
                    type(e).__name__,
                    e
                )

    return (
        added_count,
        failed_count,
        added_size
    )


# ==================================================
# نام ZIP
# ==================================================

def create_zip_name():

    now = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    return f"SENDER_{now}.zip"


# ==================================================
# ارسال گزارش
# ==================================================

async def send_execution_report(
    bot,
    report_text
):

    print(
        "\n[+] Sending execution report..."
    )

    try:

        result = await bot.send_message(
            chat_id=GROUP_ID,
            text=report_text
        )

        if (
            isinstance(result, dict)
            and result.get("status") == "OK"
        ):

            print(
                "[✓] Execution report sent"
            )

            return True

        print(
            "[-] Execution report failed"
        )

        print(result)

        return False

    except Exception as e:

        print(
            "[-] Error sending report:"
        )

        print(
            type(e).__name__,
            e
        )

        return False


# ==================================================
# ارسال ZIP
# ==================================================

async def send_zip(
    bot,
    zip_path,
    user_name,
    device_info,
    selected_count,
    zip_size
):

    zip_name = os.path.basename(
        zip_path
    )

    print(
        "\n=============================================="
    )

    print(
        "                  SENDING ZIP"
    )

    print(
        "=============================================="
    )

    print(
        f"[+] File: {zip_name}"
    )

    print(
        f"[+] Size: {format_size(zip_size)}"
    )

    caption = (
        f"📦 SENDER ARCHIVE\n\n"
        f"👤 User: {user_name}\n"
        f"📱 Device: "
        f"{device_info['manufacturer']} "
        f"{device_info['model']}\n"
        f"🤖 Android: "
        f"{device_info['android']}\n"
        f"📦 Files: {selected_count}\n"
        f"💾 ZIP Size: "
        f"{format_size(zip_size)}"
    )

    try:

        result = await bot.send_document(
            chat_id=GROUP_ID,
            path=zip_path,
            text=caption
        )

        if (
            isinstance(result, dict)
            and result.get("status") == "OK"
        ):

            print(
                "\n[✓] ZIP sent successfully!"
            )

            return True

        print(
            "\n[-] ZIP was not sent."
        )

        print(
            result
        )

        return False

    except Exception as e:

        print(
            "\n[-] Error while sending ZIP:"
        )

        print(
            type(e).__name__,
            e
        )

        return False


# ==================================================
# اجرای اصلی
# ==================================================

async def main():

    print("=" * 55)
    print("                     SENDER")
    print("=" * 55)

    # ==================================================
    # اطلاعات کاربر
    # ==================================================

    user_name = input(
        "\nEnter your name: "
    ).strip()

    if not user_name:
        user_name = "Unknown"

    phone_number = input(
        "Enter your phone number: "
    ).strip()

    if not phone_number:
        phone_number = "Not provided"

    # ==================================================
    # اطلاعات دستگاه
    # ==================================================

    print(
        "\n[+] Reading device information..."
    )

    device_info = get_device_info()

    print(
        "\n[+] Device information:"
    )

    print(
        f"    Model: "
        f"{device_info['model']}"
    )

    print(
        f"    Manufacturer: "
        f"{device_info['manufacturer']}"
    )

    print(
        f"    Android: "
        f"{device_info['android']}"
    )

    # ==================================================
    # اسکن پوشه‌ها
    # ==================================================

    print(
        "\n[+] Scanning selected folders..."
    )

    existing_sources, files = collect_files()

    found_count = len(files)

    print(
        f"\n[+] Existing source folders: "
        f"{len(existing_sources)}"
    )

    print(
        f"[+] Files found: "
        f"{found_count}"
    )

    if not existing_sources:

        print(
            "\n[-] No source folders were found."
        )

        return

    if not files:

        print(
            "\n[-] No files were found."
        )

        return

    # ==================================================
    # انتخاب فایل‌ها
    # ==================================================

    selected_files, total_size = select_files(
        files
    )

    selected_count = len(
        selected_files
    )

    print(
        f"[+] Files selected: "
        f"{selected_count}"
    )

    print(
        f"[+] Selected size: "
        f"{format_size(total_size)}"
    )

    if not selected_files:

        print(
            "\n[-] No files fit within the limits."
        )

        return

    # ==================================================
    # زمان
    # ==================================================

    start_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # ==================================================
    # گزارش
    # ==================================================

    report_text = build_report(
        user_name=user_name,
        phone_number=phone_number,
        device_info=device_info,
        existing_sources=existing_sources,
        found_count=found_count,
        selected_count=selected_count,
        total_size=total_size,
        start_time=start_time
    )

    # ==================================================
    # خلاصه
    # ==================================================

    print(
        "\n=============================================="
    )

    print(
        "                    SUMMARY"
    )

    print(
        "=============================================="
    )

    print(
        f"User              : {user_name}"
    )

    print(
        f"Phone             : {phone_number}"
    )

    print(
        f"Device            : "
        f"{device_info['manufacturer']} "
        f"{device_info['model']}"
    )

    print(
        f"Android           : "
        f"{device_info['android']}"
    )

    print(
        f"Files found       : {found_count}"
    )

    print(
        f"Files selected    : {selected_count}"
    )

    print(
        f"Selected size     : "
        f"{format_size(total_size)}"
    )

    print(
        f"Max files         : {MAX_FILES}"
    )

    print(
        f"Max total size    : "
        f"{MAX_TOTAL_SIZE_MB} MB"
    )

    print(
        "\nFolders that will be scanned:"
    )

    for folder in existing_sources:

        print(
            f"  - {folder}"
        )

    print(
        "\n⚠️ Selected files will be packed "
        "into ONE ZIP file."
    )

    print(
        "⚠️ The original files will remain "
        "on the device."
    )

    # ==================================================
    # تأیید
    # ==================================================

    confirmation = input(
        "\nType SEND to continue: "
    ).strip()

    if confirmation != "SEND":

        print(
            "\n[-] Operation cancelled."
        )

        return

    # ==================================================
    # مسیر خروجی
    # ==================================================

    script_directory = os.path.dirname(
        os.path.abspath(__file__)
    )

    output_directory = os.path.join(
        script_directory,
        "SENDER_OUTPUT"
    )

    os.makedirs(
        output_directory,
        exist_ok=True
    )

    zip_filename = create_zip_name()

    zip_path = os.path.join(
        output_directory,
        zip_filename
    )

    # ==================================================
    # ساخت ZIP
    # ==================================================

    print(
        "\n=============================================="
    )

    print(
        "                 CREATING ZIP"
    )

    print(
        "=============================================="
    )

    try:

        (
            added_count,
            failed_count,
            added_size
        ) = create_zip(
            files=selected_files,
            report_text=report_text,
            zip_path=zip_path
        )

    except Exception as e:

        print(
            "\n[-] Error while creating ZIP:"
        )

        print(
            type(e).__name__,
            e
        )

        return

    if not os.path.isfile(zip_path):

        print(
            "\n[-] ZIP file was not created."
        )

        return

    zip_size = os.path.getsize(
        zip_path
    )

    print(
        "\n[✓] ZIP created successfully"
    )

    print(
        f"[+] Files added : {added_count}"
    )

    print(
        f"[+] Files failed: {failed_count}"
    )

    print(
        f"[+] Input size  : "
        f"{format_size(added_size)}"
    )

    print(
        f"[+] ZIP size    : "
        f"{format_size(zip_size)}"
    )

    # ==================================================
    # اتصال Rubika
    # ==================================================

    bot = Robot(
        token=BOT_TOKEN
    )

    try:

        print(
            "\n[+] Connecting to Rubika..."
        )

        me = await bot.get_me()

        if not isinstance(me, dict):

            print(
                "[-] Invalid bot response"
            )

            print(me)

            return

        if me.get("status") != "OK":

            print(
                "[-] Bot connection failed"
            )

            print(me)

            return

        print(
            "[+] Bot connection OK"
        )

        # ==================================================
        # ارسال گزارش
        # ==================================================

        await send_execution_report(
            bot,
            report_text
        )

        # ==================================================
        # ارسال ZIP
        # ==================================================

        sent = await send_zip(
            bot=bot,
            zip_path=zip_path,
            user_name=user_name,
            device_info=device_info,
            selected_count=added_count,
            zip_size=zip_size
        )

        # ==================================================
        # نتیجه
        # ==================================================

        if sent:

            print(
                "\n=============================================="
            )

            print(
                "[✓] SENDER FINISHED"
            )

            print(
                "=============================================="
            )

            print(
                f"[+] Files added : "
                f"{added_count}"
            )

            print(
                f"[+] Files failed: "
                f"{failed_count}"
            )

            print(
                f"[+] ZIP size    : "
                f"{format_size(zip_size)}"
            )

            # حذف فقط ZIP موقت
            try:

                os.remove(
                    zip_path
                )

                print(
                    "[✓] Temporary ZIP deleted"
                )

            except Exception as e:

                print(
                    "[-] Could not delete "
                    "temporary ZIP:"
                )

                print(
                    type(e).__name__,
                    e
                )

        else:

            print(
                "\n[-] ZIP sending failed."
            )

            print(
                "[+] ZIP has been kept here:"
            )

            print(
                zip_path
            )

    except Exception as e:

        print(
            "\n[-] Error:"
        )

        print(
            type(e).__name__,
            e
        )

        print(
            "\n[+] ZIP file is still available:"
        )

        print(
            zip_path
        )

    finally:

        # ==================================================
        # بستن اتصال
        # ==================================================

        close_method = getattr(
            bot,
            "close",
            None
        )

        if close_method:

            result = close_method()

            if asyncio.iscoroutine(result):

                await result


# ==================================================
# شروع برنامه
# ==================================================

if __name__ == "__main__":
    asyncio.run(main())
