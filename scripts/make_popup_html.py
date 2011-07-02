import os.path
from jinja2 import Template, Environment, FileSystemLoader
import unicodedata



#ENV = Environment( loader=FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')))
#template = ENV.get_template(os.path.join('chrome_popup_template.html'))
#template.render(all_symbols)

DINGBATS_RANGE = (0x2701, 0x27FF)
ARROWS_RANGE = (0x2190, 0x21FF)
MATH_OPERATORS_RANGE = (0x2200, 0x22FF)


outfile = "../unicode-symbols/popup.html"


def make_symbols(unicode_range):
    start, stop = unicode_range
    symbols = list()
    for i in range(start, stop+1):
        try:
            name = unicodedata.name(unichr(i))
            symbols.append((name, i))
        except ValueError:
            # skip the non mapped codepoints
            pass

    return symbols


if __name__=="__main__":
    dingbats_symbols = make_symbols(DINGBATS_RANGE)
    arrow_symbols = make_symbols(ARROWS_RANGE)
    math_symbols = make_symbols(MATH_OPERATORS_RANGE)

    all_symbols = [
        ('dingbats', dingbats_symbols),
        ('arrows', arrow_symbols),
        ('math-operators', math_symbols)
    ]


    ENV = Environment( loader=FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')))
    template = ENV.get_template(os.path.join('chrome_popup_template.html'))
    print all_symbols
    chrome_popup_html = template.render(all_symbols=all_symbols)

    with open(outfile, 'w') as f:
        f.write(chrome_popup_html)