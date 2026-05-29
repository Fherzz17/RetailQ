import pandas as pd
import streamlit as st

from retailiq import analytics
from retailiq.database import SessionLocal, init_db
from retailiq.seed import seed_database


st.set_page_config(page_title="RetailIQ", page_icon=":bar_chart:", layout="wide")


@st.cache_data(show_spinner=False)
def load_dashboard_data() -> dict:
    init_db()
    with SessionLocal() as session:
        return {
            "overview": analytics.overview(session),
            "monthly_revenue": analytics.revenue_by_month(session),
            "top_products": analytics.top_products(session, limit=10),
            "low_stock": analytics.low_stock_products(session),
            "stock_risk": analytics.stock_risk_forecast(session),
        }


st.title("RetailIQ")
st.caption("Sales analytics and inventory forecasting for small retail businesses")

with st.sidebar:
    st.header("Demo Data")
    if st.button("Create / refresh sample data"):
        seed_database(reset=True)
        st.cache_data.clear()
        st.success("Sample data loaded.")

data = load_dashboard_data()
overview = data["overview"]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"Rs {overview['total_revenue']:,.2f}")
col2.metric("Units Sold", f"{overview['total_units_sold']:,}")
col3.metric("Orders", f"{overview['total_orders']:,}")
col4.metric("Low Stock Items", overview["low_stock_products"])

st.subheader("Revenue Trend")
monthly_df = pd.DataFrame(data["monthly_revenue"])
if monthly_df.empty:
    st.info("No sales data yet. Create demo data from the sidebar.")
else:
    st.line_chart(monthly_df, x="month", y="revenue")

left, right = st.columns(2)

with left:
    st.subheader("Top Products")
    top_products_df = pd.DataFrame(data["top_products"])
    if top_products_df.empty:
        st.info("No product sales yet.")
    else:
        st.dataframe(top_products_df, use_container_width=True, hide_index=True)

with right:
    st.subheader("Low Stock Products")
    low_stock_df = pd.DataFrame(data["low_stock"])
    if low_stock_df.empty:
        st.success("No low-stock products right now.")
    else:
        st.dataframe(low_stock_df, use_container_width=True, hide_index=True)

st.subheader("Stock Risk Forecast")
forecast_df = pd.DataFrame(data["stock_risk"])
if forecast_df.empty:
    st.info("No products available for forecasting.")
else:
    st.dataframe(forecast_df, use_container_width=True, hide_index=True)
