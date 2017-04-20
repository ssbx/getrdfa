#!/usr/bin/env python

# Copyright (C) 2014 Dan Scott <dscott@laurentian.ca>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#
# from https://github.com/dbs/schema-unioncat
#

import logging
import sys

try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
    from urllib import urlopen

from xml.dom.minidom import parse
from rdflib.graph import ConjunctiveGraph
from rdflib.namespace import RDF, RDFS, OWL, XSD
from rdflib.parser import Parser
from rdflib.serializer import Serializer

logging.basicConfig()

def url_value(url):
    "Get the URL value from a given <loc> element"
    locs = url.getElementsByTagName('loc')
    if len(locs) > 1:
        raise Exception('More than 1 loc in url %s' % url.nodeValue)
    if len(locs) < 1:
        raise Exception('No loc in url %s' % url.nodeValue)
    for node in locs[0].childNodes:
        if node.nodeType == node.TEXT_NODE:
            return node.nodeValue

def extract_rdfa(url, outfile=sys.stdout, parser="rdfa", serializer="n3"):
    """
    Extract RDFa from a given URL

    Parsers are listed at https://rdflib.readthedocs.org/en/4.1.0/plugin_parsers.html
    Serializers are listed at https://rdflib.readthedocs.org/en/4.1.0/plugin_serializers.html
    """
    store = None
    graph = ConjunctiveGraph()
    graph.parse(url, format=parser)
    graph.serialize(destination=outfile, format=serializer)

def main():
    import argparse
    import pprint
    import traceback

    parser = argparse.ArgumentParser(
        description="Crawl a sitemap.xml and extract RDFa from the documents")
    parser.add_argument('-o', '--output', required=True,
        help='Path / filename for the output')
    parser.add_argument('-p', '--parser', default='rdfa1.1',
        help='Parser to use for the input format ("rdfa", "microdata", etc)')
    parser.add_argument('-u', '--url', required=True,
        help='The url to parse')
    parser.add_argument('-t', '--serializer', default='n3',
        help='Serializer to use for the output format ("n3", "nt", "turtle", "xml", etc)')
    args = parser.parse_args()

    errors = []
    outfile = open(args.output, 'wb')

    try:
        print "try to get " + args.url
        extract_rdfa(args.url, outfile, args.parser, args.serializer)
    except Exception as e:
        traceback.print_exc()

if __name__ == '__main__':
    main()
