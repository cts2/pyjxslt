import sys
import os
import argparse

from pyjxslt import Gateway

test_xml = """<doc name='foo'><entry>Page 1</entry></doc>"""

test_xsl = os.path.join(os.path.dirname(__file__), "test.xsl")


def main(argv):
    parser = argparse.ArgumentParser(description="Test the XSLT Gateway process")
    parser.add_argument("--port", help="Gateway process port (default: 25333", type=int, default=25333)
    opts = parser.parse_args(argv)
    gw = Gateway(port=opts.port)
    if gw.gateway_connected():
        print()
        print("XML to JSON")
        print("=" * 10)
        print(gw.to_json(test_xml))
        print()
        print("XML to HTML via XSLT")
        print("=" * 10)
        gw.add_transform("test", test_xsl)
        print(gw.transform("test", test_xml))
    else:
        print("XSLT Gateway not available on port %d" % opts.port)


if __name__ == '__main__':
    main(sys.argv[1:])
