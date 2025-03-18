# 《英文书翻译脚本使用说明》

## 一、概述
本脚本的主要功能是将英文书籍的 TXT 文件翻译成中文，并以 Markdown 格式输出。它通过调用火山引擎的大模型，实现了文件分割、翻译和合并的自动化流程。

## 二、环境准备
1. **安装依赖库**：在运行脚本之前，需要确保已经安装了以下 Python 库：
    - `tkinter`：用于创建图形用户界面（GUI）对话框。
    - `re`：用于正则表达式匹配。
    - `volcenginesdkarkruntime`：火山引擎的 SDK，用于调用大模型进行翻译。
    - `natsort`：用于自然排序。
    - `shutil`：用于文件和文件夹的操作。

你可以使用以下命令安装缺失的库：
```bash
pip install volcenginesdkarkruntime natsort
```

2. **获取火山引擎 API Key**：你需要在火山引擎平台上注册并创建应用，获取 `Ark API Key`。这个密钥将用于调用火山引擎的大模型进行翻译。

## 三、使用步骤
1. **运行脚本**：在命令行中执行以下命令来运行脚本：
```bash
python translate2.py
```

2. **输入 API Key**：脚本会弹出一个对话框，要求你输入 `Ark API Key`。请输入你在火山引擎平台上获取的 API Key，然后点击“确定”。如果不输入 API Key，程序将退出。

3. **选择输入文件**：接下来，会弹出一个文件选择对话框，要求你选择要翻译的英文 TXT 文件。请选择对应的文件，然后点击“打开”。如果不选择文件，程序将退出。

4. **等待翻译过程**：脚本会自动完成以下步骤：
    - **文件分割**：将大的 TXT 文件分割成多个小文件，每个文件的单词或汉字数量不超过 3000 个。分割后的文件将保存在输入文件所在目录下的 `split_files` 文件夹中。
    - **文件翻译**：对分割后的每个小文件进行翻译，并将翻译结果保存为 Markdown 文件。翻译后的文件将保存在输入文件所在目录下的 `translated_files` 文件夹中。
    - **文件合并**：将所有翻译后的 Markdown 文件合并成一个文件，保存为 `merged.md`，并放置在输入文件所在目录下。

5. **选择是否保留过程文件**：翻译完成后，会弹出一个对话框询问你是否保留过程文件（即 `split_files` 和 `translated_files` 文件夹）。如果你选择“是”，这些文件夹将被保留；如果你选择“否”，脚本将自动删除这些文件夹。

## 四、注意事项
- **文件格式**：输入文件必须是 TXT 格式，且编码为 UTF-8。
- **API Key 安全**：请妥善保管你的 `Ark API Key`，不要泄露给他人。
- **网络连接**：确保你的计算机可以正常访问火山引擎的 API 服务，否则翻译过程可能会失败。
- **性能问题**：如果输入文件非常大，分割和翻译过程可能会比较耗时，请耐心等待。

通过以上步骤，你就可以轻松地将英文书籍翻译成中文，并得到一个格式规范的 Markdown 文件。

MIT License

Copyright (c) [2025] maxiaovo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
