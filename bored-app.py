import requests as rs
from argparse import ArgumentParser
from enum import Enum
import sys


class Color(Enum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    WHITE = 37


class Style(Enum):
    NONE = 0
    BOLD = 1
    UNDERLINE = 2
    NEGATIVE1 = 3
    NEGATIVE2 = 5


class Background(Enum):
    BLACK = 29


def color_format_text(color, style, background):
    return f"\033[{style.value};{color.value};{background.value}m"


def prettify_response(res):
    if "error" in res:
        error_prefix = color_format_text(Color.RED, Style.NONE, Background.BLACK)
        print(error_prefix, file=sys.stderr, end="")
        print(f"Couldn't retrieve the activity: {res['error']}", file=sys.stderr)
        return
    
    header_prefix = color_format_text(Color.GREEN, Style.NONE, Background.BLACK)
    body_prefix = color_format_text(Color.WHITE, Style.UNDERLINE, Background.BLACK)
    items_prefix = color_format_text(Color.BLUE, Style.NONE, Background.BLACK)

    print(header_prefix, end="")
    print(res["activity"])

    print(body_prefix, end="")
    print(f"type: ", end="")
    print(items_prefix, end="")
    print(res['type'])

    print(body_prefix, end="")
    print(f"participants: ", end="")
    print(items_prefix, end="")
    print(res['participants'])


    print(body_prefix, end="")
    print(f"price: ", end="")
    print(items_prefix, end="")
    print(res['price'])

    print(body_prefix, end="")
    print(f"accessibility: ", end="")
    print(items_prefix, end="")
    print(res['accessibility'])

    if res['link'] != "":
        print(body_prefix, end="")
        print(f"link: ", end="")
        print(items_prefix, end="")
        print(res['link'])

    print(body_prefix, end="")
    print(f"key: ", end="")
    print(items_prefix, end="")
    print(res['key'])


def get_response(args):
    params = {}
    if args.key is not None:
        params["key"] = args.key
    if args.type is not None:
        params["type"] = args.type
    if args.participants is not None:
        params["participants"] = args.participants
    if args.price_range is not None:
        params["minprice"] = args.price_range[0]
        params["maxprice"] = args.price_range[1]
    if args.accessibility_range is not None:
        params["minaccessibility"] = args.accessibility_range[0]
        params["maxaccessibility"] = args.accessibility_range[1]

    return rs.get('http://www.boredapi.com/api/activity', params=params)

    print(res)


def args_parser():
    parser = ArgumentParser(description='Bored app - implementation of Bored API')
    parser.add_argument('-k', '--key', metavar='KEY',
                        help='key of the activity')
    parser.add_argument('-t', '--type', metavar='TYPE',
                        choices=['education', 'recreational', 'social', 'diy', 'charity',
                                 'cooking', 'relaxation', 'music', 'busywork'],
                        help='type of the activity')
    parser.add_argument('-p', '--participants', type=int,
                        help='number of people involved in the activity')
    parser.add_argument('--price-range', nargs=2, metavar=('MIN', 'MAX'),
                        help='price range of how much the activity should cost \
                              on scale from 0 to 1')
    parser.add_argument('--accessibility-range', nargs=2, metavar=('MIN', 'MAX'),
                        help='accessibility range of how much the activity \
                              should be accessible on scale from 0 to 1')
    return parser


if __name__ == "__main__":
    parser = args_parser()
    args = parser.parse_args()
    res = get_response(args)
    prettify_response(res.json())
