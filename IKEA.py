import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

# Load an image (local file)
image = Image.open("Ikealogo1.jpg")

# Display it in the app
st.image(image, caption="Data Analysis for Ikea Company") 
st.title("IKea Dashboard")



st.set_page_config(layout="wide")



@st.cache_data
def load_data():
    df = pd.read_excel("IKEA_product_catalog.xlsx")

    return df

df=load_data()



# years = sorted(df["Year"].unique())

# selected_years = st.multiselect(
#     "Select Years",
#     options = years,
#     default = years
# )


sale_tag = sorted(df["sale_tag"].unique())

selected_sale_tag = st.multiselect(
    "sale tag",
    options=sale_tag,
    default=sale_tag
)

filtered_df = df[ df["sale_tag"].isin(selected_sale_tag) ]


countries = sorted(df["country"].unique())

selected_countries = st.multiselect(
    "Select Countries",
    options = countries,
    default = countries
)

filtered_df = filtered_df[ filtered_df["country"].isin(selected_countries) ]



# st.markdown("###  📌 KPI")

# total_sales = filtered_df["TotalSales"].sum()
# units_sold = filtered_df["Quantity"].sum()
# order_count = filtered_df["OrderID"].nunique()
# average_order_value = total_sales / order_count
# kpi1, kpi2, kpi3 = st.columns(3)

# with kpi1:
#     st.metric("💰 Total Sales",  f"{total_sales:,.0f}")

# with kpi2:
#     st.metric("Units Sold", f"{units_sold:,.0f}")

# with kpi3:
#     st.metric("Average Order Value", f"{average_order_value:,.0f}")
    
st.markdown("### 🗝️ KPI")

total_sales= filtered_df["price"].sum()
order_count = filtered_df["product_id"].nunique()
min_price = filtered_df["price"].min() 
max_price = filtered_df["price"].max()
filtered_df["product_rating"] = pd.to_numeric(filtered_df["product_rating"], errors='coerce')


rating_average = filtered_df["product_rating"].mean()


kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric(" Total Sales", f"{total_sales:,.0f}")

with kpi2:
    st.metric(" Order count", f"{order_count:,.0f}")

with kpi3:
    st.metric(" Min price", f"{min_price:,.0f}")

with kpi4:
    st.metric(" Max price", f"{max_price:,.0f}")

with kpi5:
    st.metric(" Rating average", f"{rating_average:,.0f}")


st.dataframe(
    filtered_df.head(100),
    use_container_width= True
)




st.markdown("### 📈 Charts")


sales_by_country = (
    filtered_df.groupby("country")["price"].sum()
    .reset_index()
    .sort_values(by="price", ascending= False)
)

sales_by_currency = (
    filtered_df.groupby("currency")["price"].sum()
    .reset_index()
    .sort_values(by="price", ascending= False)
)

sales_by_badge = (
    filtered_df.groupby("badge")["price"].sum()
    .reset_index()
    .sort_values(by="price", ascending= False)
)

sales_by_sale_tag = (
    filtered_df.groupby("sale_tag")["price"].sum()
    .reset_index()
    .sort_values(by="price", ascending= False)
)


top_products = (
    filtered_df.groupby("product_type")["product_rating"].mean()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)


fig1=px.bar(
        sales_by_country,
        y="price",
        x="country",
        # orientation="h",
        title="Sales By Country",
        text_auto= '.2s',
        color_discrete_sequence=["#0057ad"] 
    )

fig1.update_traces( textfont_color= "white", textposition = "outside")
st.plotly_chart(fig1, use_container_width= True)

# fig2=px.bar(
#         sales_by_currency,
#         y="price",
#         x="currency",
#         # orientation="h",
#         title="Sales By currency",
#         text_auto= '.2s'
#     )

# fig2.update_traces( textfont_color= "white", textposition = "outside")
# st.plotly_chart(fig2, use_container_width= True)


fig2 = px.line(
        sales_by_currency,
        x = "currency",
        y = "price",
        markers = True,
        title = "Sales By currency",
        # text_auto= '.2s'
        
    )


fig2.update_traces(textposition = "top center", texttemplate = '%{text:.01s}')
st.plotly_chart(fig2, use_container_width = True)

col1,col2,col3 = st.columns(3)


with col1:
    fig3 = px.bar(
        top_products,
        y="product_type",
        x="product_rating",
        orientation="h",
        title="Top Rated 5 Products",
        text_auto= '.2s',
        color_discrete_sequence=["#fbda0c"] 
    
    )

    fig3.update_traces( textfont_color = "white", textposition = "outside")
    st.plotly_chart(fig3, use_container_width=True)


with col2:
    fig4=px.pie(
        sales_by_sale_tag,
        names = "sale_tag",
        values = "price",
        title = "sales by sale_tag",
        hole = 0,
        color_discrete_sequence= px.colors.sequential.YlOrBr
    )

    fig4.update_traces(textinfo = "percent")
    st.plotly_chart(fig4, use_container_width= True)


with col3:
    fig5=px.pie(
        sales_by_badge,
        names = "badge",
        values = "price",
        title = "sales by badge",
        hole = 0.6,
        color_discrete_sequence= px.colors.sequential.YlOrBr
    )

    fig5.update_traces(textinfo = "percent")
    st.plotly_chart(fig5, use_container_width= True)
