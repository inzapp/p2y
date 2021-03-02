import os
from glob import glob

import xmltodict as xd
from tqdm import tqdm

pascal_voc_annotation_path = r'.'
use_pre_saved_classes_txt = False
class_names = []


def parse_to_yolo(o, img_width, img_height):
    global use_pre_saved_classes_txt, class_names
    class_name = o['name']
    b = o['bndbox']
    x1, y1, x2, y2 = int(b['xmin']), int(b['ymin']), int(b['xmax']), int(b['ymax'])
    w, h = x2 - x1, y2 - y1
    cx, cy = x1 + w / 2.0, y1 + h / 2.0
    cx, cy, w, h = cx / float(img_width), cy / float(img_height), w / float(img_width), h / float(img_height)
    if use_pre_saved_classes_txt:
        class_index = class_names.index(class_name)
    else:
        try:
            class_index = class_names.index(class_name)
        except ValueError:
            class_names.append(class_name)
            class_index = class_names.index(class_name)
    return f'{class_index} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}\n'


def load_pre_saved_classes_txt():
    global use_pre_saved_classes_txt
    classes_txt_path = f'{pascal_voc_annotation_path}/classes.txt'
    if os.path.exists(classes_txt_path) and os.path.isfile(classes_txt_path):
        if os.path.getsize(classes_txt_path) > 0:
            with open(classes_txt_path, 'rt') as f:
                print('classes.txt found.')
                lines = f.readlines()
                for i in range(len(lines)):
                    class_name = lines[i].replace('\n', '')
                    class_names.append(class_name)
                    print(class_name)
            use_pre_saved_classes_txt = True


def p2y():
    global use_pre_saved_classes_txt
    load_pre_saved_classes_txt()
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

    if use_pre_saved_classes_txt:
        return
    classes_file_content = ''
    for i in range(len(class_names)):
        classes_file_content += f'{class_names[i]}\n'
    with open(rf'{pascal_voc_annotation_path}/classes.txt', 'wt') as classes_file:
        classes_file.write(classes_file_content)


def safe_delete_all_xml_files():
    xml_paths = glob(rf'{pascal_voc_annotation_path}\*.xml')
    for xml_path in xml_paths:
        if os.path.isfile(xml_path):
            yolo_label_path = f'{xml_path[:-4]}.txt'
            if os.path.isfile(yolo_label_path):
                if os.path.getsize(yolo_label_path) > 0:
                    os.remove(xml_path)
                    

def make_empty_label():
    paths = glob('*.jpg')
    for path in paths:
        label_path = f'{path[:-4]}.txt'
        if os.path.exists(label_path):
            continue
        with open(label_path, 'wt') as f:
            pass


if __name__ == '__main__':
    p2y()
    safe_delete_all_xml_files()
    make_empty_label()
