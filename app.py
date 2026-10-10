import streamlit as st

import pandas as pd

import plotly.express as px

from pathlib import Path



st.set_page_config(

    page_title="Sales Analytics Dashboard",

    page_icon="📊",

    layout="wide"

)



st.title("📊 Sales Analytics Dashboard")

st.caption("Sales performance overview")



# Load the analysis results

BASE_DIR = Path(__file__).parent

RESULTS_DIR = BASE_DIR / "results"



@st.cache_data

def load_data():

    category = pd.read_csv(RESULTS_DIR / "revenue_by_category.csv")

    hourly = pd.read_csv(RESULTS_DIR / "orders_per_hour.csv")

    regions = pd.read_csv(RESULTS_DIR / "region_summary.csv")

    cancellations = pd.read_csv(

        RESULTS_DIR / "cancellation_summary.csv"

    )

    average = pd.read_csv(

        RESULTS_DIR / "average_order_value.csv"

    )

    return category, hourly, regions, cancellations, average



try:

    category, hourly, regions, cancellations, average = load_data()



    # Key metrics

    total_revenue = category["total_revenue"].sum()

    total_orders = regions["total_orders"].sum()

    cancellation_rate = (

        cancellations["cancelled_orders"].sum()

        / cancellations["total_orders"].sum() * 100

    )

    avg_order_value = float(average["average_order_value"].iloc[0])



    col1, col2, col3, col4 = st.columns(4)



    col1.metric("Delivered Revenue", f"₱{total_revenue:,.2f}")

    col2.metric("Orders", f"{total_orders:,}")

    col3.metric("Cancellation Rate", f"{cancellation_rate:.2f}%")

    col4.metric("Average Order Value", f"₱{avg_order_value:,.2f}")



    st.divider()



    # Revenue by category

    st.subheader("Revenue by Product Category")

    fig_category = px.bar(

        category,

        x="category",

        y="total_revenue",

        labels={

            "category": "Category",

            "total_revenue": "Revenue (₱)"

        },

        text_auto=".2s"

    )

    st.plotly_chart(fig_category, use_container_width=True)



    # Orders per hour

    st.subheader("Orders by Hour")

    fig_hourly = px.line(

        hourly,

        x="hour",

        y="total_orders",

        markers=True,

        labels={

            "hour": "Hour of Day",

            "total_orders": "Number of Orders"

        }

    )

    fig_hourly.update_xaxes(dtick=1)

    st.plotly_chart(fig_hourly, use_container_width=True)



    # Region filter

    st.subheader("Regional Sales Analysis")

    region_options = ["All Regions"] + sorted(

        regions["region"].dropna().unique().tolist()

    )

    selected_region = st.selectbox(

        "Filter by Region",

        region_options

    )



    filtered_regions = regions.copy()

    if selected_region != "All Regions":

        filtered_regions = filtered_regions[

            filtered_regions["region"] == selected_region

        ]



    st.dataframe(filtered_regions, use_container_width=True)



    # Cancellation breakdown

    st.subheader("Cancellation Rate by Payment Method")

    fig_cancel = px.bar(

        cancellations,

        x="payment_method",

        y="cancellation_rate_pct",

        labels={

            "payment_method": "Payment Method",

            "cancellation_rate_pct": "Cancellation Rate (%)"

        },

        text_auto=".2f"

    )

    st.plotly_chart(fig_cancel, use_container_width=True)



except FileNotFoundError as error:

    st.error(f"Missing file: {error}")

    st.info(

        "Upload all five CSV files into the repository's results/ folder."

    )
