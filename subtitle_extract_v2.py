import os
import re

def extract_dialogues(file_path):
    """从.ass文件中提取对白"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='utf-16') as file:
                lines = file.readlines()
        except UnicodeDecodeError:
            print(f"无法读取文件 {file_path}，请检查文件编码。")
            return []

    dialogues = []
    dialogue_started = False
    
    for line in lines:
        # 检查是否到达[Events]部分
        if '[Events]' in line:
            dialogue_started = True
            continue
        
        # 如果已经到达对白部分，开始提取
        if dialogue_started and line.startswith('Dialogue:'):
            # 提取对白部分
            match = re.match(r'Dialogue: [^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,(.*)', line)
            if match:
                dialogue = match.group(1).strip()
                # 清理ASS标签
                dialogue = re.sub(r'\{[^}]*\}', '', dialogue)
                if dialogue:
                    dialogues.append(dialogue)

    return dialogues

def process_folder(folder_path):
    """处理文件夹中的所有.ass文件"""
    for filename in os.listdir(folder_path):
        if filename.endswith('.ass'):
            file_path = os.path.join(folder_path, filename)
            print(f'正在处理 {filename}...')
            
            # 提取对白
            dialogues = extract_dialogues(file_path)
            
            # 创建输出文件
            output_filename = os.path.splitext(filename)[0] + '_dialogues.txt'
            output_path = os.path.join(folder_path, output_filename)
            
            # 写入对白到文件
            with open(output_path, 'w', encoding='utf-8') as output_file:
                for dialogue in dialogues:
                    output_file.write(dialogue + '\n')
            
            print(f'已生成 {output_filename}')

if __name__ == "__main__":
    folder_path = input("请输入包含ass文件的文件夹地址: ").strip()
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        process_folder(folder_path)
        print("\n所有文件处理完毕。")
    else:
        print("无效的文件夹路径，请检查后重试。")
