# Mubu-To-MarkDown-Converter

将 幕布 导出 的 html 文件转化为 markdown 格式。

主要基于 markdownify 库：[python-markdownify](https://github.com/matthewwithanm/python-markdownify/)

在此基础上预处理了 LaTex 公式，以及幕布 html 文档 的其他特殊部分。

## Installation

```shell
git clone https://github.com/cjlworld/mubu-to-md-converter.git
```

## Usage

将幕布导出的 html 文件转换为 markdown：

```shell
python mubu_converter.py < your_mubu_export_file.html > md_name.md
```

或者您可以 导入 MubuConverter 类：

```python
from mubu_converter import MubuConverter

MubuConverter().convert(html_content)
```

## Testing

On Windows

```
./runtests.bat
```

## TODO

- 处理公式中的 `_` 以及 `*`
