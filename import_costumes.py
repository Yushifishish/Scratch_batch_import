#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import zipfile
import shutil
import tempfile
import hashlib
from PIL import Image
print("=" * 50)
print("作者/Author: FishishOuO")
print("Github: https://github.com/Yushifishish")
print("X: https://x.com/FishishOuO")
print("QQ: 3899512800")
print("Email: yushifishish@outlook.com")
print
print("=" * 50)
LANG_TEXTS = {
    "zh": {
        "select_lang": "请选择语言 (zh / en): ",
        "invalid_lang": "错误：不支持的语言，默认使用中文",
        "no_images_folder": "未找到 'images' 文件夹，将扫描当前目录下的图片文件。",
        "current_dir": "当前目录:",
        "input_sb3_name": "请输入 .sb3 文件名（例如 my_project.sb3）: ",
        "file_not_exist": "错误：文件 {} 不存在！",
        "input_role_name": "请输入目标角色名称（例如 角色1）: ",
        "scan_images": "[1/4] 扫描图片文件夹:",
        "no_image_found": "错误：未找到任何图片（支持 .png .jpg .jpeg .svg）",
        "found_images": "找到 {} 张图片，正在处理...",
        "img_convert": "  {} -> {} (中心: {:.1f}, {:.1f})",
        "modify_project": "[2/4] 修改项目文件 {} ...",
        "add_costume_success": "  已向角色 '{}' 添加 {} 个造型",
        "role_not_found": "错误：未找到名为 '{}' 的角色",
        "copy_images": "\n[3/4] 复制图片文件到项目内部...",
        "add_file": "  已添加 {}",
        "pack_project": "\n[4/4] 打包新项目: {}",
        "finish": "\n完成！新项目已保存为:"
    },
    "en": {
        "select_lang": "Please select language (zh / en): ",
        "invalid_lang": "Error: Unsupported language, use Chinese by default",
        "no_images_folder": "Folder 'images' not found, will scan images in current directory.",
        "current_dir": "Current directory:",
        "input_sb3_name": "Enter .sb3 file name (e.g. my_project.sb3): ",
        "file_not_exist": "Error: File {} does not exist!",
        "input_role_name": "Enter target sprite name (e.g. Sprite1): ",
        "scan_images": "[1/4] Scanning image folder:",
        "no_image_found": "Error: No images found (supports .png .jpg .jpeg .svg)",
        "found_images": "Found {} images, processing...",
        "img_convert": "  {} -> {} (Center: {:.1f}, {:.1f})",
        "modify_project": "[2/4] Modifying project file {} ...",
        "add_costume_success": "  Added {} costumes to sprite '{}'",
        "role_not_found": "Error: Sprite named '{}' not found",
        "copy_images": "\n[3/4] Copying images into project...",
        "add_file": "  Added {}",
        "pack_project": "\n[4/4] Packaging new project: {}",
        "finish": "\nDone! New project saved as:"
    }
}

# 选择语言
lang_choice = input(LANG_TEXTS["zh"]["select_lang"]).strip().lower()
if lang_choice not in ("zh", "en"):
    print(LANG_TEXTS["zh"]["invalid_lang"])
    USE_LANG = "zh"
else:
    USE_LANG = lang_choice
TEXT = LANG_TEXTS[USE_LANG]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(SCRIPT_DIR, "images")
if not os.path.exists(IMAGE_FOLDER):
    IMAGE_FOLDER = SCRIPT_DIR
    print(TEXT["no_images_folder"])

print(TEXT["current_dir"], SCRIPT_DIR)
sb3_name = input(TEXT["input_sb3_name"]).strip()
if not sb3_name.endswith('.sb3'):
    sb3_name += '.sb3'
SB3_FILE = os.path.join(SCRIPT_DIR, sb3_name)
if not os.path.exists(SB3_FILE):
    print(TEXT["file_not_exist"].format(SB3_FILE))
    exit(1)

TARGET_ROLE = input(TEXT["input_role_name"]).strip()
OUTPUT_SB3 = SB3_FILE.replace('.sb3', '_batch_import.sb3')


def md5_file(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_image_center(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext in ('.png', '.jpg', '.jpeg'):
        with Image.open(filepath) as img:
            w, h = img.size
            return w / 2.0, h / 2.0
    elif ext == '.svg':
        try:
            import xml.etree.ElementTree as ET
            ET.register_namespace('', 'http://www.w3.org/2000/svg')
            tree = ET.parse(filepath)
            root = tree.getroot()
            viewbox = root.get('viewBox')
            if viewbox:
                parts = viewbox.split()
                if len(parts) == 4:
                    w = float(parts[2])
                    h = float(parts[3])
                    return w / 2.0, h / 2.0
            w_attr = root.get('width')
            h_attr = root.get('height')
            if w_attr and h_attr:
                w = float(''.join(c for c in w_attr if c.isdigit() or c == '.'))
                h = float(''.join(c for c in h_attr if c.isdigit() or c == '.'))
                return w / 2.0, h / 2.0
        except Exception:
            pass
    return 0.0, 0.0


print("\n" + TEXT["scan_images"], IMAGE_FOLDER)
image_extensions = ('.png', '.jpg', '.jpeg', '.svg')
image_files = []
for f in os.listdir(IMAGE_FOLDER):
    if f.lower().endswith(image_extensions):
        image_files.append(os.path.join(IMAGE_FOLDER, f))

if not image_files:
    print(TEXT["no_image_found"])
    exit(1)

print(TEXT["found_images"].format(len(image_files)))
new_costumes = []
temp_images = {}

for img_path in image_files:
    original_name = os.path.basename(img_path)
    ext = os.path.splitext(img_path)[1].lower()
    data_format = ext[1:]
    file_md5 = md5_file(img_path)
    new_filename = f"{file_md5}{ext}"
    cx, cy = get_image_center(img_path)
    costume = {
        "name": os.path.splitext(original_name)[0],
        "bitmapResolution": 1,
        "dataFormat": data_format,
        "assetId": file_md5,
        "md5ext": new_filename,
        "rotationCenterX": cx,
        "rotationCenterY": cy
    }
    new_costumes.append(costume)
    temp_images[new_filename] = img_path
    print(TEXT["img_convert"].format(original_name, new_filename, cx, cy))


print(f"\n{TEXT['modify_project'].format(SB3_FILE)}")
temp_dir = tempfile.mkdtemp()
try:
    with zipfile.ZipFile(SB3_FILE, 'r') as zip_in:
        zip_in.extractall(temp_dir)

    proj_path = os.path.join(temp_dir, 'project.json')
    with open(proj_path, 'r', encoding='utf-8') as f:
        project = json.load(f)

    targets = project.get('targets', [])
    role_found = False
    for target in targets:
        if target.get('isStage') is False and target.get('name') == TARGET_ROLE:
            if 'costumes' not in target:
                target['costumes'] = []
            target['costumes'].extend(new_costumes)
            role_found = True
            print(TEXT["add_costume_success"].format(len(new_costumes), TARGET_ROLE))
            break

    if not role_found:
        print(TEXT["role_not_found"].format(TARGET_ROLE))
        exit(1)

    with open(proj_path, 'w', encoding='utf-8') as f:
        json.dump(project, f, indent=2, ensure_ascii=False)

    print(TEXT["copy_images"])
    for new_name, original_path in temp_images.items():
        dest = os.path.join(temp_dir, new_name)
        shutil.copy2(original_path, dest)
        print(TEXT["add_file"].format(new_name))

    print(f"\n{TEXT['pack_project'].format(OUTPUT_SB3)}")
    with zipfile.ZipFile(OUTPUT_SB3, 'w', zipfile.ZIP_DEFLATED) as zip_out:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, temp_dir)
                zip_out.write(full_path, arcname)

    print(f"\n{TEXT['finish']}", OUTPUT_SB3)

finally:
    shutil.rmtree(temp_dir, ignore_errors=True)
