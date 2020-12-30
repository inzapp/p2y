from glob import glob

import xmltodict as xd
from tqdm import tqdm

annotation_path = r'.'
yolo_label_save_path = r'.'

class_names = []


def parse_to_yolo(o, img_width, img_height):
    global class_names
    class_name = o['name']
    b = o['bndbox']
    x1, y1, x2, y2 = int(b['xmin']), int(b['ymin']), int(b['xmax']), int(b['ymax'])
    w, h = x2 - x1, y2 - y1
    cx, cy = x1 + w / 2, y1 + h / 2
    cx, cy, w, h = cx / img_width, cy / img_height, w / img_width, h / img_height
    try:
        class_index = class_names.index(class_name)
    except ValueError:
        class_names.append(class_name)
        class_index = class_names.index(class_name)
    return f'{class_index} {cx} {cy} {w} {h}\n'


def a2y():
    file_paths = glob(rf'{annotation_path}\*.xml')
    for file_path in tqdm(file_paths):
        with open(file_path, 'rt') as f:
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
        with open(rf'{file_path[:-4]}.txt', 'wt') as yolo_label_file:
            yolo_label_file.write(yolo_label)

    classes_file_content = ''
    for i in range(len(class_names)):
        classes_file_content += f'{class_names[i]}\n'
    with open(rf'{yolo_label_save_path}\classes.txt', 'wt') as classes_file:
        classes_file.write(classes_file_content)


if __name__ == '__main__':
    a2y()
