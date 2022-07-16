from xml.etree import ElementTree as ET
from datetime import datetime

ns = {"n": "http://www.topografix.com/GPX/1/1", "ns3": "http://www.garmin.com/xmlschemas/TrackPointExtension/v1"}

tree = ET.parse("data/activity_9216447102.gpx")
root = tree.getroot()

metadata = root.find("n:metadata", ns)
track = root.find("n:trk", ns)

date = datetime.strptime(metadata.find("n:time", ns).text, "%Y-%m-%dT%H:%M:%S.000Z")

track_name = track.find("n:name", ns).text
track_type = track.find("n:type", ns).text
track_segment = track.find("n:trkseg", ns)

ele = []
times = []
hr = []
cad = []
lat = []
lon = []

for track_point in track_segment.findall("n:trkpt", ns):
    ele.append(float(track_point.find("n:ele", ns).text))
    times.append((datetime.strptime(track_point.find("n:time", ns).text, "%Y-%m-%dT%H:%M:%S.000Z")-date).total_seconds())
    hr.append(float(track_point.find("n:extensions/ns3:TrackPointExtension/ns3:hr", ns).text))
    cad.append(float(track_point.find("n:extensions/ns3:TrackPointExtension/ns3:cad", ns).text))
    lat.append(float(track_point.attrib["lat"]))
    lon.append(float(track_point.attrib["lon"]))
