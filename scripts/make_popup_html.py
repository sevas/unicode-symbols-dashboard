import os.path
import unicodedata
from jinja2 import Template, Environment, FileSystemLoader


MOST_USED_NAMES = ['WHITE STAR', 'BLACK STAR',
                   'CHECK MARK', 'HEAVY CHECK MARK',
                   'BALLOT X', 'HEAVY BALLOT X',
                   'HEAVY BLACK HEART', 'CIRCLED WHITE STAR',
                   'MEDIUM WHITE CIRCLE', 'MEDIUM BLACK CIRCLE',
                   'HOT SPRINGS',

                   'QUARTER NOTE', 'EIGHTH NOTE',
                   'BEAMED EIGHTH NOTES', 'BEAMED SIXTEENTH NOTES',

                   'WHITE SMILING FACE', 'BLACK SMILING FACE',
                   'WHITE FROWNING FACE',

                   'SKULL AND CROSSBONES',
                   'RADIOACTIVE SIGN', 'BIOHAZARD SIGN',
                   'ATOM SYMBOL', 'HIGH VOLTAGE SIGN', 'WARNING SIGN',

                   'WHITE SUN WITH RAYS',
                   'FIRST QUARTER MOON', 'LAST QUARTER MOON',
                   'BLACK SUN WITH RAYS', 'CLOUD',
                   'UMBRELLA', 'SNOWMAN', 'COMET',

                   'CADUCEUS', 'ANKH', 'STAR AND CRESCENT',
                   'HAMMER AND SICKLE', 'PEACE SYMBOL',
                   'YIN YANG',


                   'COPYRIGHT SIGN', 'TRADE MARK SIGN',
                   'OPTION KEY', 'PLACE OF INTEREST SIGN', 'UPWARDS WHITE ARROW']

DINGBATS_RANGE = (0x2701, 0x27FF)
MISC_SYMBOLS_RANGE = (0x2600, 0x26FF)
ARROWS_RANGE = (0x2190, 0x21FF)
MATH_OPERATORS_RANGE = (0x2200, 0x22FF)
SHAPES_RANGE = (0x25A0, 0x25FF)
GREEK_LETTERS_RANGE = (0x0370, 0x03FF)

COMBOS = [('LOOK OF DISAPPROVAL', (0x0CA0, 0x5F, 0x0CA0))]





def make_symbols_from_range(unicode_range):
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


def make_symbols_from_names(unicode_names):
    symbols = list()
    for name in unicode_names:
        unicode_point_value = ord(unicodedata.lookup(name))
        symbols.append((name, unicode_point_value))

    return symbols


def make_html_entity_strings_from_combos(combos):
    out = list()
    for name, values in combos:
        html_string = ''.join(['&#{0};'.format(v) for v in values])
        out.append((name, html_string))
    return out



def main(outfile):
    most_used_symbols = make_symbols_from_names(MOST_USED_NAMES)
    dingbats_symbols = make_symbols_from_range(DINGBATS_RANGE)
    misc_symbols = make_symbols_from_range(MISC_SYMBOLS_RANGE)
    arrow_symbols = make_symbols_from_range(ARROWS_RANGE)
    math_symbols = make_symbols_from_range(MATH_OPERATORS_RANGE)
    shape_symbols = make_symbols_from_range(SHAPES_RANGE)
    greek_symbols = make_symbols_from_range(GREEK_LETTERS_RANGE)


    all_symbols = [
            ('dingbats', dingbats_symbols),
            ('misc-symbols', misc_symbols),
            ('arrows', arrow_symbols),
            ('math-operators', math_symbols),
            ('shapes', shape_symbols),
    ]


    

    ENV = Environment( loader=FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')))
    template = ENV.get_template(os.path.join('chrome_popup_template.html'))

    print('Generating chrome extension')
    chrome_popup_html = template.render(all_symbols=all_symbols,
                                        most_used=most_used_symbols,
                                        combos=make_html_entity_strings_from_combos(COMBOS))

    with open(outfile, 'w') as f:
        print('Saving generated html to {0}'.format(outfile))
        f.write(chrome_popup_html)


if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(description='create the popup.html file for the chrome extension')
    parser.add_argument('--outfile', dest='outfile', type=str, required=True, help='path to output file')

    args = parser.parse_args()
    main(args.outfile)