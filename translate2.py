import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import re
from volcenginesdkarkruntime import Ark
from natsort import natsorted
import shutil

def count_words(text):
    """统计文本中的单词或汉字数量"""
    words = re.findall(r'[\u4e00-\u9fff]|[a-zA-Z0-9]+', text)
    return len(words)

def split_txt_file(file_path, output_folder):
    """将大文本文件分割成小文件，每个文件不超过3000个单词或汉字"""
    os.makedirs(output_folder, exist_ok=True)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            paragraphs = content.split('\n\n')  # 按空行分割段落

            current_text = ""
            current_count = 0
            file_index = 1

            for paragraph in paragraphs:
                para_count = count_words(paragraph)
                if current_count + para_count > 3000:
                    output_file_path = os.path.join(output_folder, f'split_{file_index}.txt')
                    with open(output_file_path, 'w', encoding='utf-8') as output_file:
                        output_file.write(current_text.strip())
                    file_index += 1
                    current_text = paragraph
                    current_count = para_count
                else:
                    current_text += '\n\n' + paragraph if current_text else paragraph
                    current_count += para_count

            # 保存最后一部分文本
            if current_text:
                output_file_path = os.path.join(output_folder, f'split_{file_index}.txt')
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(current_text.strip())
        print(f"文件分割完成，分割文件保存在: {output_folder}")
        return True
    except Exception as e:
        print(f"分割文件时出错: {e}")
        return False

def translate_text_to_markdown_stream(text, client, source_lang="en", target_lang="zh"):
    """以流式方式翻译文本并返回Markdown格式的中文文本"""
    try:
        stream = client.chat.completions.create(
            model="doubao-1-5-pro-256k-250115",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"你是一个翻译助手，将 {source_lang} 翻译成 {target_lang}，"
                        "并根据内容结构输出为 Markdown 格式。识别标题、列表、段落等，"
                        "并使用合适的 Markdown 语法（如 #、-、换行等）。把引用的圣经都替换成和合本。"
                    )
                },
                {"role": "user", "content": text},
            ],
            stream=True,
        )
        
        translated_markdown = ""
        print("开始流式输出翻译结果：")
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                translated_markdown += content
                print(content, end="", flush=True)
        print("\n流式输出结束。")
        return translated_markdown
    except Exception as e:
        print(f"翻译时出错: {e}")
        return None

def translate_files(input_folder, output_folder, client, source_lang="en", target_lang="zh"):
    """翻译文件夹中的所有TXT文件并保存为MD文件"""
    os.makedirs(output_folder, exist_ok=True)
    
    for file in os.listdir(input_folder):
        if file.endswith(".txt"):
            input_file = os.path.join(input_folder, file)
            output_file = os.path.join(output_folder, file.replace(".txt", ".md"))
            print(f"\n开始翻译文件: {input_file}")
            try:
                with open(input_file, 'r', encoding='utf-8') as f:
                    text = f.read()
                translated_markdown = translate_text_to_markdown_stream(text, client, source_lang, target_lang)
                if translated_markdown:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(translated_markdown)
                    print(f"翻译完成: {input_file} -> {output_file}")
                else:
                    print(f"翻译失败: {input_file}")
            except Exception as e:
                print(f"处理文件 {input_file} 时出错: {e}")

def merge_md_files(input_folder, output_file):
    """合并文件夹中的所有MD文件到一个文件中"""
    md_files = [f for f in os.listdir(input_folder) if f.endswith('.md')]
    md_files = natsorted(md_files)  # 自然排序
    
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for md_file in md_files:
                file_path = os.path.join(input_folder, md_file)
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write('\n\n')  # 文件间添加空行
        print(f"文件合并完成，输出文件: {output_file}")
    except Exception as e:
        print(f"合并文件时出错: {e}")

def main():
    """主函数，协调整个翻译工作流程"""
    # 创建Tkinter窗口并隐藏
    root = tk.Tk()
    root.withdraw()

    # 弹出对话框让用户输入API Key
    api_key = simpledialog.askstring("API Key", "请输入Ark API Key:", parent=root)
    if not api_key:
        print("未输入API Key，程序退出。")
        return

    # 初始化 Ark 客户端
    client = Ark(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=api_key,
    )

    # 选择输入文件
    input_file = filedialog.askopenfilename(
        title="选择要翻译的TXT文件",
        filetypes=[("Text files", "*.txt")]
    )
    if not input_file:
        print("未选择文件，程序退出。")
        return

    # 设置工作目录和临时文件夹
    base_dir = os.path.dirname(input_file)
    split_folder = os.path.join(base_dir, "split_files")
    trans_folder = os.path.join(base_dir, "translated_files")
    output_file = os.path.join(base_dir, "merged.md")

    # 第一步：分割文件
    if not split_txt_file(input_file, split_folder):
        print("文件分割失败，程序退出。")
        return

    # 第二步：翻译文件
    translate_files(split_folder, trans_folder, client, source_lang="en", target_lang="zh")

    # 第三步：合并文件
    merge_md_files(trans_folder, output_file)

    # 弹出对话框询问是否保留过程文件
    if messagebox.askyesno("保留过程文件", "翻译完成！是否保留过程文件（split_files 和 translated_files 文件夹）？"):
        print("保留过程文件。")
    else:
        try:
            shutil.rmtree(split_folder)
            shutil.rmtree(trans_folder)
            print("过程文件已删除。")
        except Exception as e:
            print(f"删除过程文件时出错: {e}")

    print("翻译工作流程完成！")

if __name__ == "__main__":
    main()