import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL was not found in the .env file."
        )

    return psycopg.connect(database_url)


def create_tables():
    query = """
    CREATE TABLE IF NOT EXISTS asteroid_approaches (
        id SERIAL PRIMARY KEY,
        neo_id VARCHAR(50) NOT NULL,
        name VARCHAR(255) NOT NULL,
        approach_date DATE NOT NULL,
        diameter_m DOUBLE PRECISION NOT NULL,
        velocity_kmh DOUBLE PRECISION NOT NULL,
        miss_distance_km DOUBLE PRECISION NOT NULL,
        hazardous BOOLEAN NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        UNIQUE (neo_id, approach_date)
    );
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)


def save_asteroid(asteroid):
    query = """
    INSERT INTO asteroid_approaches (
        neo_id,
        name,
        approach_date,
        diameter_m,
        velocity_kmh,
        miss_distance_km,
        hazardous
    )
    VALUES (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    )
    ON CONFLICT (neo_id, approach_date)
    DO UPDATE SET
        name = EXCLUDED.name,
        diameter_m = EXCLUDED.diameter_m,
        velocity_kmh = EXCLUDED.velocity_kmh,
        miss_distance_km = EXCLUDED.miss_distance_km,
        hazardous = EXCLUDED.hazardous;
    """

    values = (
        asteroid["neo_id"],
        asteroid["name"],
        asteroid["approach_date"],
        asteroid["diameter"],
        asteroid["velocity"],
        asteroid["miss_distance"],
        asteroid["hazardous"]
    )

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, values)


def save_asteroids(asteroids):
    for asteroid in asteroids:
        save_asteroid(asteroid)


def get_asteroid_count():
    query = """
    SELECT COUNT(*)
    FROM asteroid_approaches;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)

            result = cursor.fetchone()

    return result[0]


def get_recent_asteroids(limit=10):
    query = """
    SELECT
        name,
        approach_date,
        diameter_m,
        velocity_kmh,
        miss_distance_km,
        hazardous
    FROM asteroid_approaches
    ORDER BY approach_date DESC, miss_distance_km ASC
    LIMIT %s;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (limit,))

            rows = cursor.fetchall()

    return rows

def get_closest_ever():
    query = """
    SELECT
        name,
        approach_date,
        miss_distance_km
    FROM asteroid_approaches
    ORDER BY miss_distance_km ASC
    LIMIT 1;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()

    return result

def get_fastest_ever():
    query = """
    SELECT
        name,
        approach_date,
        velocity_kmh
    FROM asteroid_approaches
    ORDER BY velocity_kmh DESC
    LIMIT 1;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()

    return result


def get_largest_ever():
    query = """
    SELECT
        name,
        approach_date,
        diameter_m
    FROM asteroid_approaches
    ORDER BY diameter_m DESC
    LIMIT 1;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()

    return result


def get_hazardous_count():
    query = """
    SELECT COUNT(*)
    FROM asteroid_approaches
    WHERE hazardous = TRUE;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()

    return result[0]

def get_today_asteroids():
    query = """
    SELECT
        name,
        approach_date,
        diameter_m,
        velocity_kmh,
        miss_distance_km,
        hazardous
    FROM asteroid_approaches
    WHERE approach_date = CURRENT_DATE
    ORDER BY miss_distance_km ASC;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

    return rows

def get_upcoming_asteroids(days=7):
    query = """
        SELECT
            name,
            approach_date,
            diameter_m,
            velocity_kmh,
            miss_distance_km,
            hazardous
        FROM asteroid_approaches
        WHERE approach_date > CURRENT_DATE
          AND approach_date <= CURRENT_DATE + %s
        ORDER BY approach_date ASC, miss_distance_km ASC;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (days,))
            rows = cursor.fetchall()

    return rows