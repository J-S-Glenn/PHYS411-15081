import simplekml
from datetime import datetime, timedelta
import random
import math

# We should implement this somewhere: https://geodesy.noaa.gov/api/gravd/gp?lat=40.0&lon=-80.0&eht=100.0
# This is the gravity API. It returns the gravity at a given lat, long, and height. We can use this to get the gravity constant for a given location.
default_icon = "http://maps.google.com/mapfiles/kml/shapes/donut.png"
GRAVITY_CONSTANT = 9.80
DEGREE_OF_RADIUS_LINE = 111139

def meters_to_lat_change(meters):
    """Converts meters to a change in latitude in degrees."""
    return meters / DEGREE_OF_RADIUS_LINE

def meters_to_long_change(meters, lat):
    """Converts meters to a change in longitude in degrees, given a latitude."""
    return meters / (DEGREE_OF_RADIUS_LINE * math.cos(math.radians(lat)))


class Object:
    def vector(name, lat, long, i, j, k1=0, k2=0):
        kml = simplekml.Kml()
        kml.document = simplekml.Folder(name = "Vectors")
        point = kml.newlinestring()
        point.name = name
        delta_lat = meters_to_lat_change(i)
        delta_long = meters_to_long_change(j, lat)
        print(str(lat + delta_lat) + ", " + str(long + delta_long))
        point.coords = [(long, lat, k1), (long + delta_long, lat + delta_lat, k2)]
        point.style.labelstyle.scale = 0.6
        point.style.iconstyle.icon.href = default_icon
        point.style.iconstyle.scale = 0.5
        point.altitudemode = simplekml.AltitudeMode.relativetoground
        kml.save(f"{name}.kml")
        # Need to implement recursion for vectors, pass an array of matrices and use recursion to get a resultant KML. This is just a placeholder.
        return lat + delta_lat, long + delta_long, k1, k2

    def freefall(lat, long, height, name, duration, intervals=100):
        kml = simplekml.Kml()
        kml.document = simplekml.Folder(name = "Freefall Points")
        start_time = datetime.utcnow()
        previous_time = None
        previous_height = None
        velocity = 0
        # Split the freefall into intervals
        for i in range(intervals + 1):
            fraction = i / intervals
            current_time = start_time + timedelta(seconds=duration * fraction)
            current_height = height - ((1/2) * GRAVITY_CONSTANT * (duration * fraction)**2)  # Simple linear interpolation
            # if (current_height < 0):
            #     current_height = 0
            #     return
            # Create a new point for each interval
            # Calculate velocity
            if previous_time and previous_height:
                velocity = (current_height - previous_height) / (current_time - previous_time).total_seconds()
            point = kml.newpoint()
            point.name = f"h: {current_height:.2f}m, v: {velocity:.2f} m/s"
            point.coords = [(long, lat, current_height)]
            point.style.labelstyle.scale = 0.6
            point.style.iconstyle.icon.href = default_icon
            point.style.iconstyle.scale = 0.5
            point.altitudemode = simplekml.AltitudeMode.relativetoground
            # point.timestamp.begin = start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            point.timestamp.when = current_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            previous_time = current_time
            previous_height = current_height
        kml.save(f"freefall_{name}.kml")

    def horizontal_projection(lat, long, height, name, duration):
        kml = simplekml.Kml()
        kml.document = simplekml.Folder(name = "kml_files")
        newPoint = kml.newpoint(name=name)
        newPoint.coords = [(lat, long, height)]
        newPoint.altitudemode = simplekml.AltitudeMode.relativetoground
         # Get current UTC time
        start_time = datetime.utcnow()
        # Calculate end time by adding duration
        end_time = start_time + timedelta(seconds=duration)

        # Format times into strings
        start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

        # Use TimeSpan for duration instead of TimeStamp
        newPoint.timespan.begin = start_time_str
        newPoint.timespan.end = end_time_str
        kml.save("/kml_files/horizontal_projection_" + name + ".kml")
    
start_lat = 38.66246307880478
start_long = -121.1256435949286

# For some reason these are switched. x gives a change in the value of the longitude, and y gives a change in the value of the latitude.
i = 10
j = 0
# Path: googleEarth.py
Object.freefall(start_lat, start_long, random.randrange(100), "Group 8", 10, 100)
# Need to implement recursion for vectors
vector_1_lat, vector_1_lon, vector_1_k1, vector_1_k2 = Object.vector("Vector 1", start_lat, start_long, i, j, 0, 25)
vector_2_lat, vector_2_lon, vector_2_k1, vector_2_k2 = Object.vector("Vector 2", vector_1_lat, vector_1_lon, i+5, j+100, vector_1_k2, 200)
vector_3_lat, vector_3_lon, vector_3_k1, vector_1_k2 = Object.vector("Vector 3", vector_2_lat, vector_2_lon, i-50, j-100, vector_2_k2, 100)

# Object.horizontal_projection(38.66226127273164, -121.1262282178109, 10, "Group 8", 10)
