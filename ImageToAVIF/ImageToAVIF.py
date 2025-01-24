import sys
import os
from PIL import Image
import pillow_avif


def imageToAVI(image_path):
    if image_path.lower().endswith(('jpg', 'png', 'jpeg')):
        # 打开图片（支持JPG、PNG等格式）
        with Image.open(image_path) as img:
            # 如果不是RGBA或RGB模式，需要转换
            if img.mode not in ("RGBA", "RGB"):
                img = img.convert("RGBA")
            # 保存为AVIF格式
            img.save(image_path, "AVIF")
            return True
    return False


def readAllImage(folder):
    changed_list_file = f'{folder}/had_changed_to_avif_list.txt'
    changed_list = []
    if not os.path.exists(changed_list_file):
        open(changed_list_file, 'w').close()
    else:
        with open(changed_list_file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            changed_list.append(line.replace('\n', ''))
    if not os.path.exists(folder):
        print("文件夹不存在(Directory does not exist)")
        return
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file in changed_list or file == 'had_changed_to_avif_list.txt':
                continue
            if imageToAVI(root + '/' + file):
                with open(changed_list_file, 'a') as f:
                    f.write(file + '\n')
            else:
                print(f"{file}转换失败(Conversion failed)")


def main():
    argv_list = list(sys.argv)
    if len(argv_list) > 1:
        readAllImage(argv_list[1])
    else:
        readAllImage(r"./image")


if __name__ == '__main__':
    main()
