import os
import re

def extract_dialogue(file_path):
    with open(file_path, 'r', encoding='utf-16') as file:  # Use UTF-16 as detected
        lines = file.readlines()

    dialogue_lines = []
    for line in lines:
        if line.strip().startswith('Dialogue:'):  # Only lines starting with 'Dialogue:' contain subtitles
            # Extract the actual dialogue part by splitting after the 9th comma
            dialogue_parts = line.split(',', 9)
            if len(dialogue_parts) > 9:
                dialogue = dialogue_parts[9].strip()  # The actual text part of the dialogue
                # Clean the dialogue text by removing style formatting and tags
                cleaned_dialogue = re.sub(r'\{[^}]*\}|\\[Nnh]|\\[a-zA-Z]|\(.*?\)|<.*?>', '', dialogue).strip()
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
