import os
import json

def labelme_to_yolo(json_file, image_width, image_height):
    with open(json_file, 'r') as f:
        data = json.load(f)

    annotations = data['shapes']
    yolo_annotations = []

    for annotation in annotations:
        label = annotation['label']
        points = annotation['points']

        x_min = min(points[0][0], points[1][0])
        y_min = min(points[0][1], points[1][1])
        x_max = max(points[0][0], points[1][0])
        y_max = max(points[0][1], points[1][1])

        x_center = (x_min + x_max) / (2 * image_width)
        y_center = (y_min + y_max) / (2 * image_height)
        width = (x_max - x_min) / image_width
        height = (y_max - y_min) / image_height

        yolo_annotations.append(f"{label} {x_center} {y_center} {width} {height}")

    return yolo_annotations

# 遍历目录中的JSON文件并进行转换
json_dir = '/home/lostye/桌面/protect_traning/705-904_label'
image_width = 1024
image_height = 682

output_dir = '/home/lostye/桌面/protect_traning/705-904_label'
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(json_dir):
    if filename.endswith('.json'):
        json_file = os.path.join(json_dir, filename)
        yolo_annotations = labelme_to_yolo(json_file, image_width, image_height)

        # 将yolo_annotations写入TXT文件
        txt_file = os.path.splitext(filename)[0] + '.txt'
        output_file = os.path.join(output_dir, txt_file)

        with open(output_file, 'w') as f:
            for annotation in yolo_annotations:
                f.write(annotation + '\n')
