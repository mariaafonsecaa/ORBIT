import os
from datetime import date


def build_report(
    processed_asteroids,
    closest_asteroid,
    fastest_asteroid,
    largest_asteroid,
    hazardous_count,
    database_count
):
    today = date.today().isoformat()

    return f"""
========================================
                 ORBIT
          NEAR-EARTH MONITOR
========================================

Date: {today}

Objects detected today: {len(processed_asteroids)}
Potentially hazardous objects: {hazardous_count}
Total approaches stored in database: {database_count}

----------------------------------------
CLOSEST OBJECT
----------------------------------------

Asteroid: {closest_asteroid['name']}
Miss distance: {closest_asteroid['miss_distance']:,.2f} km

----------------------------------------
FASTEST OBJECT
----------------------------------------

Asteroid: {fastest_asteroid['name']}
Velocity: {fastest_asteroid['velocity']:,.2f} km/h

----------------------------------------
LARGEST OBJECT
----------------------------------------

Asteroid: {largest_asteroid['name']}
Estimated diameter: {largest_asteroid['diameter']:,.2f} m

----------------------------------------
TODAY'S OBJECTS
----------------------------------------
""" + build_asteroid_list(processed_asteroids)


def build_asteroid_list(processed_asteroids):
    output = ""

    for asteroid in processed_asteroids:
        if asteroid["hazardous"]:
            status = "POTENTIALLY HAZARDOUS"
        else:
            status = "SAFE"

        output += f"""
{asteroid['name']}
Diameter: {asteroid['diameter']:,.2f} m
Velocity: {asteroid['velocity']:,.2f} km/h
Miss distance: {asteroid['miss_distance']:,.2f} km
Status: {status}

"""

    return output


def save_report(report):
    os.makedirs("reports", exist_ok=True)

    today = date.today().isoformat()

    filename = f"reports/orbit_report_{today}.txt"

    with open(filename, "w") as file:
        file.write(report)

    return filename