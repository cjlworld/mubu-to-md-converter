from bs4 import BeautifulSoup, Tag
from markdownify import MarkdownConverter
import sys

class MubuConverter:
    def convert(self, html: str) -> str:
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        return self.convert_soup(soup)
    
    def convert_soup(self, soup: BeautifulSoup) -> str:
        # Convert LaTeX blocks
        # MarkdownConverter 不能处理公式快，需要预处理
        for latex_tag in soup.find_all("span", attrs={"class": "formula", "data-raw": True}): 
            latex_tag.string = f'${latex_tag.find("annotation").string}$'

        # 删除 head, head 中包含大量的 style 文件, 且 MarkdownConverter 会识别错误
        head_tag = soup.find("head")
        if type(head_tag) is Tag:
            head_tag.clear()
            
        # 删除 "以上内容整理于 幕布文档"
        publish_tag = soup.find("div", attrs={"class": "publish"})
        if type(publish_tag) is Tag:
            publish_tag.clear()

        # Convert parsed content to Markdown using markdownify
        # TODO：目前有个小问题，就是 LaTeX 中有 _, 为了避免将 _ 换成 \_， 必须开启 escape_underscores
        # 但这个操作会影响其余部分
        md_content = MarkdownConverter(escape_underscores=False, escape_asterisks=False, bullets='-').convert_soup(soup)
        
        # 清除多余的换行符
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