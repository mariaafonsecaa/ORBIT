from nasa import get_asteroid_data

from asteroids import (
    get_asteroids,
    process_asteroids,
    find_closest_asteroid,
    find_fastest_asteroid,
    find_largest_asteroid,
    count_hazardous_asteroids
)

from database import (
    create_tables,
    save_asteroids,
    get_asteroid_count,
    get_closest_ever,
    get_fastest_ever,
    get_largest_ever,
    get_hazardous_count
)

from report import (
    build_report,
    save_report
)


def main():
    print("ORBIT starting...")

    create_tables()

    # TODAY'S DATA
    today_data = get_asteroid_data()

    today_raw_asteroids = get_asteroids(today_data)

    processed_asteroids = process_asteroids(
    today_raw_asteroids
    )

    if not processed_asteroids:
        print("No asteroid approaches found today.")
        return

    save_asteroids(processed_asteroids)

    # UPCOMING 7-DAY DATA
    upcoming_data = get_asteroid_data(7)

    upcoming_raw_asteroids = get_asteroids(upcoming_data)

    upcoming_processed_asteroids = process_asteroids(
    upcoming_raw_asteroids
    )

    save_asteroids(upcoming_processed_asteroids)

    closest_asteroid = find_closest_asteroid(
        processed_asteroids
    )

    fastest_asteroid = find_fastest_asteroid(
        processed_asteroids
    )

    largest_asteroid = find_largest_asteroid(
        processed_asteroids
    )

    hazardous_count = count_hazardous_asteroids(
        processed_asteroids
    )

    database_count = get_asteroid_count()

    report = build_report(
        processed_asteroids,
        closest_asteroid,
        fastest_asteroid,
        largest_asteroid,
        hazardous_count,
        database_count
    )

    print(report)

    filename = save_report(report)

    print(f"Report saved to: {filename}")
    print(f"\nDatabase contains {database_count} asteroid approaches.")

    closest_ever = get_closest_ever()
    fastest_ever = get_fastest_ever()
    largest_ever = get_largest_ever()
    historical_hazardous_count = get_hazardous_count()

    print("\n--- HISTORICAL RECORDS ---")

    print(f"Closest stored asteroid: {closest_ever[0]}")
    print(f"Approach date: {closest_ever[1]}")
    print(f"Miss distance: {closest_ever[2]:,.2f} km")

    print()

    print(f"Fastest stored asteroid: {fastest_ever[0]}")
    print(f"Approach date: {fastest_ever[1]}")
    print(f"Velocity: {fastest_ever[2]:,.2f} km/h")

    print()

    print(f"Largest stored asteroid: {largest_ever[0]}")
    print(f"Approach date: {largest_ever[1]}")
    print(f"Estimated diameter: {largest_ever[2]:,.2f} m")

    print()

    print(f"Potentially hazardous approaches stored: {historical_hazardous_count}")

print("\nORBIT complete.")


if __name__ == "__main__":
    main()