import osm2gmns as og
import os

# net = og.getNetFromOSMFile('asu', network_type=('auto'), POIs=True, default_lanes = True, default_speed = True)
net = og.getNetFromOSMFile('map', network_type=('railway'), POIs =True)
og.outputNetToCSV(net)

# check and modify (if necessary) network files before complex intersection consolidation
net = og.getNetFromCSV()
og.consolidateComplexIntersections(net)
og.outputNetToCSV(net, output_folder='consolidated')

