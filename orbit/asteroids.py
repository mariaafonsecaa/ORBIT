def get_asteroids(data):
    near_earth_objects = data.get(
        "near_earth_objects",
        {}
    )

    asteroids = []

    for date_key in near_earth_objects:
        daily_asteroids = near_earth_objects[
            date_key
        ]

        asteroids.extend(daily_asteroids)

    return asteroids


def process_asteroid(asteroid):
    approach_data = asteroid["close_approach_data"]

    if not approach_data:
        return None

    approach = approach_data[0]

    estimated_diameter_min = asteroid[
        "estimated_diameter"
    ]["meters"]["estimated_diameter_min"]

    estimated_diameter_max = asteroid[
        "estimated_diameter"
    ]["meters"]["estimated_diameter_max"]

    diameter = (
        estimated_diameter_min
        + estimated_diameter_max
    ) / 2

    velocity = float(
        approach[
            "relative_velocity"
        ]["kilometers_per_hour"]
    )

    miss_distance = float(
        approach[
            "miss_distance"
        ]["kilometers"]
    )

    return {
        "neo_id": asteroid["id"],
        "name": asteroid["name"],
        "approach_date": approach["close_approach_date"],
        "diameter": diameter,
        "velocity": velocity,
        "miss_distance": miss_distance,
        "hazardous": asteroid[
            "is_potentially_hazardous_asteroid"
        ]
    }


def process_asteroids(asteroids):
    processed_asteroids = []

    for asteroid in asteroids:
        processed = process_asteroid(asteroid)

        if processed is not None:
            processed_asteroids.append(processed)

    return processed_asteroids


def find_closest_asteroid(processed_asteroids):
    return min(
        processed_asteroids,
        key=lambda asteroid: asteroid["miss_distance"]
    )


def find_fastest_asteroid(processed_asteroids):
    return max(
        processed_asteroids,
        key=lambda asteroid: asteroid["velocity"]
    )


def find_largest_asteroid(processed_asteroids):
    return max(
        processed_asteroids,
        key=lambda asteroid: asteroid["diameter"]
    )


def count_hazardous_asteroids(processed_asteroids):
    hazardous_count = 0

    for asteroid in processed_asteroids:
        if asteroid["hazardous"]:
            hazardous_count += 1

    return hazardous_count