import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# daily_order_df
def create_daily_orders_df(df):
    # Ensure 'review_creation_date' is a datetime type
    df['review_creation_date'] = pd.to_datetime(df['review_creation_date'], errors='coerce')

    # Now you can safely use `.resample()`
    monthly_orders_df = df.resample(rule='M', on='review_creation_date').agg({
        'order_id': 'count'
    })

    return monthly_orders_df

# sum_order_items_state_df
def create_sum_order_items_state_df(df):
    sum_order_items_state_df = df.groupby('seller_state').size().sort_values(ascending=False).reset_index(name='count')
    return sum_order_items_state_df.head(10)

# create_by_seller_City_df()
def create_by_seller_City_df(df):
    by_seller_City_df = df.groupby(by="seller_state").review_score.nunique().reset_index()
    by_seller_City_df.rename(columns={
        "review_id": "review_count"
    }, inplace=True)
    
    return by_seller_City_df

# Dataset
all_df = pd.read_csv("main_data.csv")

# MEMBUAT KOMPONEN FILTER
min_date = all_df["review_creation_date"].min()
max_date = all_df["review_creation_date"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    main_df = all_df[(all_df["review_creation_date"] >= str(start_date)) & 
                    (all_df["review_creation_date"] <= str(end_date))]
    
    monthly_orders_df = create_daily_orders_df(main_df)
    sum_order_items_df = create_sum_order_items_state_df(main_df)
    by_seller_City_df = create_by_seller_City_df(main_df)

# MELENGKAPI DASHBOARD DENGAN BERBAGAI VISUALISASI DATA
st.header('Dashboard E-Commerce :sparkles:')

########## VISUALISASI 1 ##########
st.subheader('Monthly Orders')

col1, col2 = st.columns(2)
 
with col1:
    total_orders = monthly_orders_df.count()
    st.metric("Total orders", value=total_orders)
 
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_orders_df.index,
    monthly_orders_df["order_id"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

########### VISUALISASI 2 ##########
st.title("Seller States")

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

fig, ax = plt.subplots(figsize=(12, 6))

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="count", y="seller_state", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Seller State", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="count", y="seller_state", data=sum_order_items_df.sort_values(by="count", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Seller State", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)


# VISUALISASI 3
st.subheader("Review Score State")

fig, ax = plt.subplots(figsize=(35, 25))
 
sns.barplot(
        y="review_score", 
        x="seller_state",
        data=by_seller_City_df.sort_values(by="review_score", ascending=False),
        palette=colors,
        ax=ax
    )
ax.set_title("Review Score berdasarkan negara", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)
 
# with col2:
#     fig, ax = plt.subplots(figsize=(20, 10))
    
#     colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
#     sns.barplot(
#         y="count", 
#         x="age_group",
#         data=by_seller_City_df.sort_values(by="age_group", ascending=False),
#         palette=colors,
#         ax=ax
#     )
#     ax.set_title("Number of Customer by Age", loc="center", fontsize=50)
#     ax.set_ylabel(None)
#     ax.set_xlabel(None)
#     ax.tick_params(axis='x', labelsize=35)
#     ax.tick_params(axis='y', labelsize=30)
#     st.pyplot(fig)
 

# st.pyplot(fig)
