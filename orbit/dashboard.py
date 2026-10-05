from nasa import (
    get_asteroid_data,
    get_asteroid_data_range
)
from asteroids import get_asteroids, process_asteroids
from database import save_asteroids
import pandas as pd
from datetime import date
import altair as alt
import streamlit as st
from database import (
    get_asteroid_count,
    get_closest_ever,
    get_fastest_ever,
    get_largest_ever,
    get_hazardous_count,
    get_recent_asteroids,
    get_today_asteroids,
    get_upcoming_asteroids
)

st.set_page_config(
    page_title="ORBIT",
    page_icon="☄️",
    layout="wide"
)

st.title("ORBIT")
st.subheader("Space Observation & Mission Intelligence System")

st.write("Near-Earth Monitor dashboard is online.")

forecast_days = st.selectbox(
    "Forecast Window",
    [7, 14, 30],
    format_func=lambda days: f"Next {days} days"
)

if st.button(
    "Refresh NASA Data",
    type="primary"
):
    with st.spinner(
        f"Retrieving the next {forecast_days} days from NASA..."
    ):

        nasa_data = get_asteroid_data_range(
            forecast_days
        )

        raw_asteroids = get_asteroids(
            nasa_data
        )

        refreshed_asteroids = (
            process_asteroids(
                raw_asteroids
            )
        )

        save_asteroids(
            refreshed_asteroids
        )

    st.success(
        f"ORBIT updated successfully — "
        f"{len(refreshed_asteroids)} "
        f"asteroid approaches processed."
    )

    st.rerun()

database_count = get_asteroid_count()

database_count = get_asteroid_count()
closest_ever = get_closest_ever()
fastest_ever = get_fastest_ever()
largest_ever = get_largest_ever()
hazardous_count = get_hazardous_count()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Approaches Stored",
        database_count
    )

with col2:
    st.metric(
        "Closest Approach",
        f"{closest_ever[2]:,.0f} km"
    )

with col3:
    st.metric(
        "Fastest Object",
        f"{fastest_ever[2]:,.0f} km/h"
    )

with col4:
    st.metric(
        "Hazardous Approaches",
        hazardous_count
    )

today_tab, history_tab = st.tabs([
    "TODAY",
    "HISTORICAL DATA"
])

with today_tab:
    st.subheader("Today's Near-Earth Objects")

    today_asteroids = get_today_asteroids()

    st.write(f"{len(today_asteroids)} objects detected today")

    today_hazardous = [
    asteroid
    for asteroid in today_asteroids
    if asteroid[5]
    ]

if today_hazardous:
    st.warning(
        f"ATTENTION — {len(today_hazardous)} potentially hazardous object(s) detected."
    )
else:
    st.success(
        "STATUS: NOMINAL — No potentially hazardous objects detected."
    )
    for asteroid in today_asteroids:
        name = asteroid[0]
        diameter = asteroid[2]
        velocity = asteroid[3]
        miss_distance = asteroid[4]
        hazardous = asteroid[5]

        with st.container(border=True):
            st.subheader(name)

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.metric(
                "Estimated Diameter",
                f"{diameter:,.2f} m"
            )

        with col_b:
            st.metric(
                "Velocity",
                f"{velocity:,.2f} km/h"
            )

        with col_c:
            st.metric(
                "Miss Distance",
                f"{miss_distance:,.2f} km"
            )

        if hazardous:
            st.warning("POTENTIALLY HAZARDOUS")
        else:
            st.success("SAFE")
st.divider()

st.subheader("Upcoming Approaches")

upcoming_asteroids = get_upcoming_asteroids(
    forecast_days
)

upcoming_asteroids = get_upcoming_asteroids(forecast_days)

if upcoming_asteroids:
    for asteroid in upcoming_asteroids:
        name = asteroid[0]
        approach_date = asteroid[1]
        diameter = asteroid[2]
        velocity = asteroid[3]
        miss_distance = asteroid[4]
        hazardous = asteroid[5]
        days_away = (approach_date - date.today()).days

        with st.container(border=True):
            st.subheader(name)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Approach Date",
                    str(approach_date),
                    f"{days_away} day{'s' if days_away != 1 else ''} away"
                )

            with col2:
                st.metric(
                    "Estimated Diameter",
                    f"{diameter:,.2f} m"
                )

            with col3:
                st.metric(
                    "Miss Distance",
                    f"{miss_distance:,.2f} km"
                )

            st.write(f"**Velocity:** {velocity:,.2f} km/h")

            if hazardous:
                st.warning("POTENTIALLY HAZARDOUS")
            else:
                st.success("SAFE")

else:
    st.info("No upcoming asteroid approaches found.")

if upcoming_asteroids:
    st.divider()
    st.subheader("Upcoming Analysis")

    closest_upcoming = min(
        upcoming_asteroids,
        key=lambda asteroid: asteroid[4]
    )

    fastest_upcoming = max(
        upcoming_asteroids,
        key=lambda asteroid: asteroid[3]
    )

    largest_upcoming = max(
        upcoming_asteroids,
        key=lambda asteroid: asteroid[2]
    )

    hazardous_upcoming = sum(
        1
        for asteroid in upcoming_asteroids
        if asteroid[5]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Closest Upcoming",
            f"{closest_upcoming[4]:,.0f} km"
        )
        st.caption(closest_upcoming[0])

    with col2:
        st.metric(
            "Fastest Upcoming",
            f"{fastest_upcoming[3]:,.0f} km/h"
        )
        st.caption(fastest_upcoming[0])

    with col3:
        st.metric(
            "Largest Upcoming",
            f"{largest_upcoming[2]:,.2f} m"
        )
        st.caption(largest_upcoming[0])

    with col4:
        st.metric(
            "Hazardous Upcoming",
            hazardous_upcoming
        )

st.divider()
st.subheader("Today's Analysis")

if today_asteroids:
    closest_today = min(today_asteroids, key=lambda asteroid: asteroid[4])
    fastest_today = max(today_asteroids, key=lambda asteroid: asteroid[3])
    largest_today = max(today_asteroids, key=lambda asteroid: asteroid[2])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
        "Closest Object",
        f"{closest_today[4]:,.2f} km"
    )
        st.caption(closest_today[0])

    with col2:
        st.metric(
        "Fastest Object",
        f"{fastest_today[3]:,.2f} km/h"
    )
        st.caption(fastest_today[0])

    with col3:
        st.metric(
        "Largest Object",
        f"{largest_today[2]:,.2f} m"
    )
        st.caption(largest_today[0])

st.divider()
st.subheader("Today's Miss Distance Comparison")

today_chart_df = pd.DataFrame(
    today_asteroids,
    columns=[
        "Asteroid",
        "Approach Date",
        "Diameter (m)",
        "Velocity (km/h)",
        "Miss Distance (km)",
        "Hazardous"
    ]
)

today_chart_df["Miss Distance (km)"] = (
    today_chart_df["Miss Distance (km)"].round(2)
)

chart_data = today_chart_df.set_index("Asteroid")[
    "Miss Distance (km)"
]

miss_distance_chart = (
    alt.Chart(today_chart_df)
    .mark_bar(color="#FF7A00", cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
    .encode(
        x=alt.X(
            "Asteroid:N",
            title="Asteroid",
            sort="-y"
        ),
        y=alt.Y(
            "Miss Distance (km):Q",
            title="Miss Distance (km)"
        ),
        tooltip=[
            alt.Tooltip("Asteroid:N", title="Asteroid"),
            alt.Tooltip(
                "Miss Distance (km):Q",
                title="Miss Distance",
                format=",.2f"
            )
        ]
    )
    .properties(height=400)
)

st.altair_chart(miss_distance_chart, use_container_width=True)

st.divider()
st.subheader("Distance Context")

MOON_DISTANCE_KM = 384400

distance_context = today_chart_df[
    ["Asteroid", "Miss Distance (km)"]
].copy()

distance_context["Lunar Distances"] = (
    distance_context["Miss Distance (km)"] / MOON_DISTANCE_KM
).round(1)

st.dataframe(
    distance_context[
        ["Asteroid", "Miss Distance (km)", "Lunar Distances"]
    ],
    width="stretch",
    hide_index=True
)

st.caption(
    "1 lunar distance = approximately 384,400 km, the average distance from Earth to the Moon."
)

with history_tab:
    st.subheader("Recent Asteroid Approaches")

    recent_asteroids = get_recent_asteroids(10)

    df = pd.DataFrame(
        recent_asteroids,
        columns=[
            "Asteroid",
            "Approach Date",
            "Diameter (m)",
            "Velocity (km/h)",
            "Miss Distance (km)",
            "Hazardous"
        ]
    )

    df["Diameter (m)"] = df["Diameter (m)"].round(2)
    df["Velocity (km/h)"] = df["Velocity (km/h)"].round(2)
    df["Miss Distance (km)"] = df["Miss Distance (km)"].round(2)

df["Hazardous"] = df["Hazardous"].apply(
lambda value: "HAZARDOUS" if value else "SAFE"
)

st.subheader("Data Filters")

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    hazardous_only = st.toggle(
        "Potentially hazardous only"
    )

with filter_col2:
    sort_option = st.selectbox(
        "Sort by",
        [
            "Most Recent",
            "Closest Approach",
            "Fastest",
            "Largest"
        ]
    )

filtered_df = df.copy()

if hazardous_only:
    filtered_df = filtered_df[
        filtered_df["Hazardous"] == "HAZARDOUS"
    ]

if sort_option == "Closest Approach":
    filtered_df = filtered_df.sort_values(
        "Miss Distance (km)",
        ascending=True
    )

elif sort_option == "Fastest":
    filtered_df = filtered_df.sort_values(
        "Velocity (km/h)",
        ascending=False
    )

elif sort_option == "Largest":
    filtered_df = filtered_df.sort_values(
        "Diameter (m)",
        ascending=False
    )

elif sort_option == "Most Recent":
    filtered_df = filtered_df.sort_values(
        "Approach Date",
        ascending=False
    )

st.dataframe(
    filtered_df,
    width="stretch",
    hide_index=True
)

st.divider()

st.subheader("Miss Distance by Asteroid")

history_chart = (
    alt.Chart(filtered_df)
    .mark_bar(
        color="#FF7A00",
        cornerRadiusTopLeft=4,
        cornerRadiusTopRight=4
    )
    .encode(
        x=alt.X(
            "Asteroid:N",
            title="Asteroid"
        ),
        y=alt.Y(
            "Miss Distance (km):Q",
            title="Miss Distance (km)"
        ),
        tooltip=[
            alt.Tooltip("Asteroid:N", title="Asteroid"),
            alt.Tooltip(
                "Miss Distance (km):Q",
                title="Miss Distance",
                format=",.2f"
            )
        ]
    )
    .properties(height=400)
)

st.altair_chart(
    history_chart,
    use_container_width=True
)

st.divider()
st.subheader("Asteroid Search")

search_term = st.text_input(
    "Search stored asteroids",
    placeholder="Example: 2017 AV3"
)

if search_term:
    search_results = df[
        df["Asteroid"].str.contains(
            search_term,
            case=False,
            na=False
        )
    ]

    if search_results.empty:
        st.warning("No stored asteroid matches that search.")
    else:
        searched_asteroid = search_results.iloc[0]

        st.success(f"OBJECT FOUND — {searched_asteroid['Asteroid']}")

        st.subheader(searched_asteroid["Asteroid"])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
            "Estimated Diameter",
            f"{searched_asteroid['Diameter (m)']:,.2f} m"
        )

        with col2:
            st.metric(
            "Velocity",
            f"{searched_asteroid['Velocity (km/h)']:,.2f} km/h"
        )

        with col3:
            st.metric(
            "Miss Distance",
            f"{searched_asteroid['Miss Distance (km)']:,.2f} km"
        )

        lunar_distance = searched_asteroid["Miss Distance (km)"] / 384400

        st.write(
            f"**Distance from Earth:** "
            f"{lunar_distance:,.1f} lunar distances"
)
        st.write(f"**Approach Date:** {searched_asteroid['Approach Date']}")

        if searched_asteroid["Hazardous"] == "HAZARDOUS":
            st.warning("STATUS: POTENTIALLY HAZARDOUS")
        else:
            st.success("STATUS: SAFE")
    st.divider()
    st.subheader("ORBIT Risk Assessment")

    miss_distance = searched_asteroid["Miss Distance (km)"]
    diameter = searched_asteroid["Diameter (m)"]
    velocity = searched_asteroid["Velocity (km/h)"]
    hazardous = searched_asteroid["Hazardous"]

    if hazardous == "HAZARDOUS":
        risk_level = "ELEVATED"
        explanation = (
            "This object is classified as potentially hazardous. "
            "Continued monitoring is recommended."
        )

    elif miss_distance < 7_500_000:
        risk_level = "MONITOR"
        explanation = (
            "This object is making a relatively close approach to Earth, "
            "but is not currently classified as potentially hazardous."
        )

    else:
        risk_level = "LOW"
        explanation = (
            "This object is not classified as potentially hazardous and "
            f"will pass approximately {lunar_distance:,.1f} lunar distances from Earth."
        )

        if risk_level == "ELEVATED":
            st.error(f"RISK LEVEL: {risk_level}")
        elif risk_level == "MONITOR":
            st.warning(f"RISK LEVEL: {risk_level}")
        else:
            st.success(f"RISK LEVEL: {risk_level}")

        st.write(explanation)

if upcoming_asteroids:

    st.divider()
    st.subheader("Upcoming Analysis")

    closest_upcoming = min(
        upcoming_asteroids,
        key=lambda asteroid: asteroid[4]
    )

    fastest_upcoming = max(
        upcoming_asteroids,
        key=lambda asteroid: asteroid[3]
    )

    largest_upcoming = max(
        upcoming_asteroids,
        key=lambda asteroid: asteroid[2]
    )

    hazardous_upcoming = sum(
        1
        for asteroid in upcoming_asteroids
        if asteroid[5]
    )

    up_col1, up_col2, up_col3, up_col4 = (
        st.columns(4)
    )

    with up_col1:
        st.metric(
            "Closest Upcoming",
            f"{closest_upcoming[4]:,.0f} km"
        )
        st.caption(
            closest_upcoming[0]
        )

    with up_col2:
        st.metric(
            "Fastest Upcoming",
            f"{fastest_upcoming[3]:,.0f} km/h"
        )
        st.caption(
            fastest_upcoming[0]
        )

    with up_col3:
        st.metric(
            "Largest Upcoming",
            f"{largest_upcoming[2]:,.2f} m"
        )
        st.caption(
            largest_upcoming[0]
        )

    with up_col4:
        st.metric(
            "Hazardous Upcoming",
            hazardous_upcoming
        )