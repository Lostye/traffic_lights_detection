import os

def replace_labels(input_file, output_file):
    label_mapping = {
        "red": "0",
        "green": "1",
        "blank": "2",
        "yellow": "3"
    }

    with open(input_file, 'r') as f:
        lines = f.readlines()

    with open(output_file, 'w') as f:
        for line in lines:
            label, *rest = line.split(' ')
            if label in label_mapping:
                label = label_mapping[label]
            new_line = ' '.join([label] + rest)
            f.write(new_line)

# 遍历目录中的TXT文件并进行替换
txt_dir = '/home/lostye/桌面/protect_traning/1107-1305_label'
output_dir = '/home/lostye/桌面/protect_traning/1107-1305_labels'
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(txt_dir):
    if filename.endswith('.txt'):
        input_file = os.path.join(txt_dir, filename)
        output_file = os.path.join(output_dir, filename)
        replace_labels(input_file, output_file)
