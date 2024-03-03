import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# membuat helper function
def create_workingday_users_df(all_df):

    workingday_users_df = all_df.groupby(by="workingday").agg({
        "casual": "sum", 
        "registered": "sum", 
        "cnt": "sum"
    })

    workingday_users_df = workingday_users_df.reset_index()
    workingday_users_df['workingday'] = workingday_users_df['workingday'].replace({False: 'Hari Libur', True: 'Hari Kerja'})

    workingday_users_df = pd.melt(workingday_users_df,
                            id_vars=["workingday"],
                            value_vars=["casual", "registered"],
                            var_name="categories",
                            value_name="count")
    
    return workingday_users_df

def create_season_users_df(all_df):
    season_users_df = all_df.groupby(by="season").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum",
    })

    season_users_df = season_users_df.reset_index()
    season_users_df = pd.melt(season_users_df,
                           id_vars=["season"],
                           value_vars=["casual", "registered"],
                           var_name="categories",
                           value_name="count")

    return season_users_df

# load berkas all_data.csv
all_df = pd.read_csv("https://raw.githubusercontent.com/afifahrahma22/project-bike-sharing/main/data/all_data.csv") 

# memastikan kolom dteday bertipe data datetime untuk keperluan filter
all_df['dteday'] = pd.to_datetime(all_df['dteday'])

# membuat komponen filter (diletakkan di sidebar)
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

# sidebar
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/afifahrahma22/project-bike-sharing/main/image/Capital_BikeShare.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Filter berdasarkan Tanggal', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# menyimpan data dari filter
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

# memanggil helper function
workingday_users_df = create_workingday_users_df(main_df)
season_users_df = create_season_users_df(main_df)

# melengkapi dashboard dengan visualisasi
st.header("Bike-Sharing Dashboard \U0001F6B4")

# informasi pengguna
st.subheader('Informai Pengguna')
 
col1, col2, col3 = st.columns(3)
 
with col1:
    casual_users = main_df['casual'].sum()
    st.metric("Pengguna Biasa", value=casual_users)
 
with col2:
    registred_users = main_df['registered'].sum() 
    st.metric("Pengguna Terdaftar", value=registred_users)

with col3:
    total_users = main_df['cnt'].sum()
    st.metric("Total Pengguna", value=total_users)

# visualisasi pengguna layanan bike sharing per hari
fig, ax = plt.subplots(figsize=(16,8))

sns.lineplot(x="dteday", y="cnt", data=main_df, color="#72BCD4")
ax.set_title("Jumlah Pengguna Bike Sharing per Hari", loc="center", fontsize=20)
ax.set_xlabel("Tanggal", fontsize=15)
ax.set_ylabel("Jumlah Pengguna", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)

st.pyplot(fig)

# visualisasi pengguna layanan bike sharing di hari kerja dan hari libur
fig, ax = plt.subplots(figsize=(16,8))

sns.barplot(x="workingday", y="count", data=workingday_users_df, hue="categories")
ax.set_title("Jumlah Pengguna berdasarkan Hari Kerja dan Hari Libur (Tanpa Weekend)", loc="center", fontsize=20)
ax.set_xlabel("Kategori Hari", fontsize=15)
ax.set_ylabel("Jumlah Pengguna", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)

st.pyplot(fig)

# visualisasi pengguna layanan bike sharing berdasarkan musim
fig, ax = plt.subplots(figsize=(16,8))

sns.barplot(x="season", y="count", data=season_users_df, color="#72BCD4")
ax.set_title("Jumlah Pengguna Bike Sharing Berdasarkan Musim", loc="center", fontsize=20)
ax.set_xlabel("Musim", fontsize=15)
ax.set_ylabel("Jumlah Pengguna", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)

st.pyplot(fig)

# visualisasi kategori pengguna layanan bike sharing berdasarkan musim
fig, ax = plt.subplots(figsize=(16,8))

sns.barplot(x="season", y="count", data=season_users_df, hue="categories")
ax.set_title("Jumlah Pengguna Bike Sharing Berdasarkan Musim", loc="center", fontsize=20)
ax.set_xlabel("Musim", fontsize=15)
ax.set_ylabel("Jumlah Pengguna", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)

st.pyplot(fig)

st.caption('Created by afifahrahma22')