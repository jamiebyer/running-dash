from xml.etree import ElementTree as ET
from datetime import datetime
import pandas as pd
import numpy as np

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

# https://stackoverflow.com/questions/639695/how-to-convert-latitude-or-longitude-to-meters
def measure(lat1, lon1, lat2, lon2)
    R = 6378.137; # Radius of earth in KM
    dLat = lat2 * np.pi / 180 - lat1 * np.pi / 180;
    dLon = lon2 * np.pi / 180 - lon1 * np.pi / 180;
    a = np.sin(dLat/2) * np.sin(dLat/2) +
    np.cos(lat1 * np.pi / 180) * np.cos(lat2 * np.pi / 180) *
    np.sin(dLon/2) * np.sin(dLon/2)
    c = 2 * np.atan2(np.sqrt(a), np.sqrt(1-a))
    d = R * c
    return d * 1000 # meters

h_dist = measure(lat[:-2], lon[:-2], lat[1:], lon[1:])
dist = np.linalg.norm([h_dist, ele], axis=1)

vel = np.diff(dist)/np.diff(times)

df = pd.DataFrame(data=list(zip(ele, times, hr, cad, lat, lon, vel)), columns=["ele", "times", "hr", "cad", "lat", "lon", "vel"])
df.to_csv("data/running_data.csv")