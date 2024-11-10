import os
import re

def extract_dialogue(file_path):
    try:
        with open(file_path, 'r', encoding='utf-16') as file:  # 尝试使用 UTF-16 编码
            lines = file.readlines()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='utf-8') as file:  # 如果失败，使用 UTF-8 编码
            lines = file.readlines()

    dialogue_lines = []  # 确保定义了 dialogue_lines
    for line in lines:
        # 假设你有某种逻辑来清理对话
        cleaned_dialogue = line.strip()  # 这是一个简单的例子
        if cleaned_dialogue:
            dialogue_lines.append(cleaned_dialogue)

    return '\n'.join(dialogue_lines)

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.ass'):
            file_path = os.path.join(folder_path, filename)
            print(f'Processing {filename}...')
            content = extract_dialogue(file_path)
            output_filename = filename.replace('.ass', '.txt')
            output_path = os.path.join(folder_path, output_filename)
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(content)
            print(f'Generated {output_filename}')

if __name__ == "__main__":
    folder_path = input("请输入包含ass文件的文件夹地址: ").strip()
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        process_folder(folder_path)
        print("\n所有文件已处理完毕。")
    else:
        print("无效的文件夹路径，请检查后重试。")
