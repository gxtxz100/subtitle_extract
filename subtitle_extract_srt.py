import os
import re
from typing import List, Tuple

def try_read_file(file_path: str) -> str:
    """尝试使用不同的编码读取文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件内容字符串，如果所有编码都失败则返回空字符串
    """
    encodings = ['utf-8', 'utf-16', 'gbk', 'gb2312', 'big5', 'latin1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
                # 验证内容是否包含有效的字幕格式
                if re.search(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', content):
                    print(f"成功使用 {encoding} 编码读取文件")
                    return content
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"使用 {encoding} 编码读取时发生错误: {str(e)}")
            continue
    
    print(f"无法使用支持的编码读取文件 {file_path}")
    return ""

def extract_subtitles(file_path: str) -> List[Tuple[str, str]]:
    """从.srt文件中提取中英字幕对
    
    Args:
        file_path: SRT文件路径
        
    Returns:
        包含(中文字幕, 英文字幕)元组的列表
    """
    content = try_read_file(file_path)
    if not content:
        return []

    # 分割字幕块
    subtitle_blocks = re.split(r'\n\s*\n', content.strip())
    subtitle_pairs = []
    
    for block in subtitle_blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:  # 跳过无效的字幕块
            continue
            
        # 跳过序号和时间码行，只处理字幕文本
        text_lines = [line.strip() for line in lines[2:] if line.strip()]
        
        if len(text_lines) >= 2:
            # 假设第一行是中文，第二行是英文
            chinese = text_lines[0]
            english = text_lines[1]
            # 清理可能的HTML标签
            chinese = re.sub(r'<[^>]+>', '', chinese)
            english = re.sub(r'<[^>]+>', '', english)
            subtitle_pairs.append((chinese, english))
        elif len(text_lines) == 1:
            # 如果只有一行，可能是单语言字幕
            text = re.sub(r'<[^>]+>', '', text_lines[0])
            subtitle_pairs.append((text, ""))

    return subtitle_pairs

def process_folder(folder_path: str):
    """处理文件夹中的所有SRT文件
    
    Args:
        folder_path: 包含SRT文件的文件夹路径
    """
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print("无效的文件夹路径，请检查后重试。")
        return

    # 获取文件夹中所有的SRT文件
    srt_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.srt')]
    
    if not srt_files:
        print("文件夹中没有找到SRT文件。")
        return

    print(f"找到 {len(srt_files)} 个SRT文件。")
    
    for srt_file in srt_files:
        file_path = os.path.join(folder_path, srt_file)
        print(f'正在处理 {srt_file}...')
        
        # 提取字幕对
        subtitle_pairs = extract_subtitles(file_path)
        
        if not subtitle_pairs:
            print(f"警告：未能从 {srt_file} 提取到任何字幕")
            continue
            
        # 创建输出文件
        output_filename = os.path.splitext(srt_file)[0] + '_subtitles.txt'
        output_path = os.path.join(folder_path, output_filename)
        
        # 写入字幕对到文件
        try:
            with open(output_path, 'w', encoding='utf-8') as output_file:
                for chinese, english in subtitle_pairs:
                    output_file.write(f"{chinese}\n{english}\n\n")
            print(f'已生成 {output_filename}，包含 {len(subtitle_pairs)} 条字幕')
        except Exception as e:
            print(f"写入文件 {output_filename} 时发生错误: {str(e)}")

if __name__ == "__main__":
    folder_path = input("请输入包含SRT文件的文件夹地址: ").strip()
    process_folder(folder_path)
    print("\n所有文件处理完毕。") 