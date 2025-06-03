import csv
import os
import argparse
from rdflib import Graph, Literal
from rdflib.namespace import GEO
from urllib.parse import urlparse

parser = argparse.ArgumentParser(description='Simple app replacing GML '
                                             'geometry representations with '
                                             'WKT in RDF graphs.')
parser.add_argument('-f', help='RDF file path', required=True)
parser.add_argument('-d', help='QGIS WKT-CSV files directory path', required=True)
parser.add_argument('--format', help='RDF file format', default="turtle")


args = parser.parse_args()


g = Graph()
g.parse(args.f)

gid_wkt = {}
gml_key = 'gml_id'
wkt_key = 'WKT'

for f in os.listdir(args.d):
  if f.endswith(".csv"):
    with open(os.path.join(os.path.abspath(args.d), f)) as cf:
      reader = csv.DictReader(cf, delimiter=',')
      for row in reader:
        if gml_key in row and wkt_key in row:
          gid_wkt[row[gml_key]] = row[wkt_key]

for s, p, o in g:
  if p == GEO.asGML:
    gmlid = urlparse(s.n3().replace('<', '').replace('>', '')).path.split('/')[
      -2]
    if gmlid in gid_wkt.keys():
      wkt = gid_wkt[gmlid]
      g.add((s, GEO.asWKT, Literal(wkt, datatype=GEO.wktLiteral)))
      g.remove((s, p, o))

new_file = args.f.split('.')[0] + '_wkt.ttl'

g.serialize(destination=new_file, format=args.format)
