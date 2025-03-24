from bs4 import BeautifulSoup, Tag
from markdownify import MarkdownConverter
import sys

class MubuConverter:
    def convert(self, html: str) -> str:       
        soup = BeautifulSoup(html, 'html.parser')
        return self.convert_soup(soup)

    def convert_soup(self, soup: BeautifulSoup) -> str:
        ## 0. 处理公式块
        # MarkdownConverter 不能处理公式块，需要预处理
        for latex_tag in soup.find_all("span", attrs={"class": "formula", "data-raw": True}): 
            latex_tag.string = f'${latex_tag.find("annotation").string}$'

        ## 1. 处理需要转义的字符
        # 转义对照表
        transfer_map = {
            "_": r'\_',
            "*": r'\*',
        }
        # 需要忽略的标签和类名
        ignore_map = {
            "span": ["formula", "codespan"],
        }
        
        # 处理需要转义的字符
        for text_node in soup.find_all(string=True):
            # 检查父节点是否在忽略列表中
            should_ignore = False
            for tag, classes in ignore_map.items():
                parent = text_node.find_parent(tag)
                if parent and any(cls in parent.get('class', []) for cls in classes):
                    should_ignore = True
                    break
                    
            if should_ignore:
                continue
                
            # 根据转义对照表进行替换
            replaced_text = text_node.string
            for char, escaped in transfer_map.items():
                replaced_text = replaced_text.replace(char, escaped)
            
            if replaced_text != text_node.string:
                text_node.replace_with(replaced_text)

        ## 2. 处理加粗, 斜体, 删除线, 行内代码
        deal_map = {
            "bold": "**",
            "italic": "*",
            "strikethrough": "~~",
            "codespan": "`"
        }
        for tag_name, tag_symbol in deal_map.items():
            for text_node in soup.find_all(class_=tag_name):
                text_node.string = f"{tag_symbol}{text_node.string}{tag_symbol}"
                
        ## 3. 删除 head, head 中包含大量的 style 文件, 且 MarkdownConverter 会识别错误
        head_tag = soup.find("head")
        if type(head_tag) is Tag:
            head_tag.clear()
            
        ## 4. 删除 "以上内容整理于 幕布文档"
        publish_tag = soup.find("div", attrs={"class": "publish"})
        if type(publish_tag) is Tag:
            publish_tag.clear()

        ## 5. 使用 markdownify 转换为 Markdown
        # 就是 LaTeX 中有 _, 为了避免将 _ 换成 \_， 必须开启 escape_underscores, escape_asterisks 同理
        # 转义在前面已经处理过了，这里不需要再处理
        md_content = MarkdownConverter(escape_underscores=False, escape_asterisks=False, bullets='-').convert_soup(soup)
        
        ## 6. 处理标题
        md_content = md_content.lstrip()
        if md_content.startswith('html'):
            md_content = md_content[4:]
            md_content = md_content.lstrip()
        # 加上标题 H1
        md_content = f"# {md_content}"
        return md_content


if __name__ == "__main__":
    """
    调用方式：
    1. python mubu_converter.py < xxx.html > yyy.md
    2. from mubu_converter import MubuConverter ...
    """
    mubu_to_md = MubuConverter()
    html_content = sys.stdin.read()
    md_content = mubu_to_md.convert(html_content)
    sys.stdout.write(md_content)