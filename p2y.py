import os
from glob import glob

import xmltodict as xd
from tqdm import tqdm

pascal_voc_annotation_path = r'.'
yolo_label_save_path = r'.'

class_names = []


def parse_to_yolo(o, img_width, img_height):
    global class_names
    class_name = o['name']
    b = o['bndbox']
    x1, y1, x2, y2 = int(b['xmin']), int(b['ymin']), int(b['xmax']), int(b['ymax'])
    w, h = x2 - x1, y2 - y1
    cx, cy = x1 + w / 2.0, y1 + h / 2.0
    cx, cy, w, h = cx / float(img_width), cy / float(img_height), w / float(img_width), h / float(img_height)
    try:
        class_index = class_names.index(class_name)
    except ValueError:
        class_names.append(class_name)
        class_index = class_names.index(class_name)
    return f'{class_index} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}\n'


def p2y():
    xml_paths = glob(rf'{pascal_voc_annotation_path}\*.xml')
    for xml_path in tqdm(xml_paths):
        with open(xml_path, 'rt') as f:
            xml_string = f.read().strip()
        res = xd.parse(xml_string)
        width = int(res['annotation']['size']['width'])
        height = int(res['annotation']['size']['height'])
        dict_or_dicts = res['annotation']['object']
        yolo_label = ''
        if isinstance(dict_or_dicts, list):
            for obj in dict_or_dicts:
                yolo_label += parse_to_yolo(obj, width, height)
        else:
            yolo_label += parse_to_yolo(dict_or_dicts, width, height)
        with open(rf'{xml_path[:-4]}.txt', 'wt') as yolo_label_file:
            yolo_label_file.write(yolo_label)

    classes_file_content = ''
    for i in range(len(class_names)):
        classes_file_content += f'{class_names[i]}\n'
    with open(rf'{yolo_label_save_path}\classes.txt', 'wt') as classes_file:
        classes_file.write(classes_file_content)


def safe_delete_all_xml_files():
    xml_paths = glob(rf'{pascal_voc_annotation_path}\*.xml')
    for xml_path in xml_paths:
        if os.path.isfile(xml_path):
            yolo_label_path = f'{xml_path[:-4]}.txt'
            if os.path.isfile(yolo_label_path):
                if os.path.getsize(yolo_label_path) > 0:
                    os.remove(xml_path)


if __name__ == '__main__':
    p2y()
    safe_delete_all_xml_files()

