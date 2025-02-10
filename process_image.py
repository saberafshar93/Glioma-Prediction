import os
from ultralytics import YOLO
import shutil

def process_image(image_path):
    # بارگذاری مدل آموزش‌دیده
    model = YOLO("/content/runs/segment/train/weights/best.pt")  # مسیر فایل مدل آموزش‌دیده

    # پیش‌بینی روی تصویر آپلود شده
    results = model.predict(source=image_path, save=True)  # پیش‌بینی و ذخیره نتیجه

    # results ممکن است لیستی از نتایج باشد، به همین دلیل باید به اولین نتیجه دسترسی پیدا کنید
    output_dir = results[0].save_dir  # استخراج مسیر ذخیره‌سازی از اولین نتیجه
    output_image_path = os.path.join(output_dir, os.path.basename(image_path))  # مسیر کامل تصویر خروجی

    # بررسی اینکه آیا تصویر خروجی ذخیره شده است یا خیر
    if os.path.exists(output_image_path):
        # انتقال تصویر پردازش‌شده به پوشه results
        result_path = os.path.join("static", "results", os.path.basename(image_path))
        shutil.move(output_image_path, result_path)
        return result_path
    else:
        raise Exception(f"خطا: تصویر خروجی در مسیر {output_image_path} یافت نشد.")