#Fernando Michael Hebert Siregar
#Bangkit Machine Learning 2024
#ML-67
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime

sns.set_theme(style='dark')


# Membuat function yang menampilkan dataframe untuk membuat Grafik
# Bike rent total berisi total dari registered + count (colomn = cnt)
def bike_rent_total_df(df):
    daily_rent_df = df.groupby(by='date').agg({
        'cnt': 'sum'
    }).reset_index()
    return daily_rent_df

# Bike rent Casual berisi jumlah pelanggan casual
def bike_rent_casual(df):
    daily_casual_rent_df = df.groupby(by='date').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Bike rent regis berisi jumlah pelanggan registered
def bike_rent_regis(df):
    daily_registered_rent_df = df.groupby(by='date').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df

# Bike monthly berisi total pelanggan dalam setiap bulan
def bike_montly_df(df):
    monthly_df = df.groupby(by="month").agg({
        "cnt": "mean"
    }).reset_index() 
    return monthly_df

# Bike hourly berisi keterangan libur dan juga jam dalam sehari
def bike_hourly_df(df):
    hourly_df = df.groupby(by=["holiday", "hour"]).agg({
        "cnt": "mean"
    }).reset_index() 
    return hourly_df

# Bike weather berisi total pelanggan dalam kelompok cuaca
def bike_weather_df(df):
    weather_df = df.groupby(by="weather").agg({
        "cnt": "sum"
    }).reset_index() 
    return weather_df

# Mengimport data dari csv
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Mengubah tipe data datetime, dan juga merubah beberapa nama kolom pada day_df
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df.rename(columns={
    "dteday" : "date",
    "yr" : "year",
    "mnth" : "month",
    "workingday" : "workday",
    "weathersit" : "weather",
}, inplace=True)
day_df.info()

# Mengubah tipe data datetime, dan juga merubah beberapa nama kolom pada hour_df
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
hour_df.rename(columns={
    "dteday" : "date",
    "yr" : "year",
    "mnth" : "month",
    "hr" : "hour",
    "workingday" : "workday",
    "weathersit" : "weather",
}, inplace=True)
hour_df.info()

# Membuat variabel min_date dan max_date sebagai batasan dalam tanggal dashboard
min_date = day_df["date"].min()
max_date = day_df["date"].max()

with st.sidebar:
    # Menambahkan logo dan namas
    st.write("Fernando's Bike Sharing")
    st.image("https://i.pinimg.com/originals/85/ac/a3/85aca3de21e181e86293cb913f56b9bf.jpg")
    # Menginisialisasi start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Mendeklarasikan tanggal awal dan akhir pada data day dan hour
day_data_df = day_df[(day_df["date"] >= str(start_date)) & 
                       (day_df["date"] <= str(end_date))]

hour_data_df = hour_df[(hour_df["date"] >= str(start_date)) & 
                       (hour_df["date"] <= str(end_date))]


# Menyiapkan berbagai dataframe dengan memanggil func yang dubuat sebelumnya
daily_rent_df = bike_rent_total_df(day_data_df)
daily_casual_rent_df = bike_rent_casual(day_data_df)
daily_registered_rent_df = bike_rent_regis(day_data_df)
monthly_df = bike_montly_df(day_data_df)
hourly_df = bike_hourly_df(hour_data_df)
weather_df_1 = bike_weather_df(day_data_df)
weather_df_2 = bike_weather_df(hour_data_df)

# Membuat judul Dashboard
st.title('Dashboard Penyewaan Sepeda Thn. 2011 - 2012')

st.markdown("-------")

# Menampilkan Bagaimana tren terakhir terkait jumlah pengguna baru dengan pengguna casual dalam beberapa tahun terakhir
st.subheader('Daftar Pelanggan')
col1, col2, col3 = st.columns(3)
with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual', value= daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered', value= daily_rent_registered)
 
with col3:
    daily_rent_total = daily_rent_df['cnt'].sum()
    st.metric('Total', value= daily_rent_total)

st.markdown("-------")

# pola yang terjadi pada jumlah total penyewaan sepeda berdasarkan Cuaca
plt.style.use('dark_background')
st.subheader("Penyewaan sepeda berdasarkan Cuaca")
fig, ax = plt.subplots(2,1, figsize=(15,10))
sns.barplot(x="weather", y="cnt", data=weather_df_1.sort_values(by="cnt", ascending=False), palette="viridis", ax=ax[0])
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)
ax[0].set_title("Penyewaan sepeda berdasarkan cuaca pada data harian", loc="center", fontsize=15)

sns.barplot(x="weather", y="cnt", data=weather_df_2.sort_values(by="cnt", ascending=False), palette="viridis", ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Penyewaan sepeda berdasarkan cuaca  data dalam jam", loc="center", fontsize=15)

plt.tight_layout()
st.pyplot(fig)
with st.expander('Penjelasan'):
    st.write(
        """
        1 : Cerah, Berawan
        
        2 : Berkabut, Berawan
        
        3 : Hujan Kecil, Salju Kecil

        4 : Hujan deras, Badai
        """
    )

st.markdown("-------")

# pola yang terjadi pada jumlah total penyewaan sepeda berdasarkan bulan 
st.subheader("Penyewaan Sepeda Berdasarkan Bulan")
fig, ax = plt.subplots()
sns.barplot(x="month", y="cnt", data=monthly_df, palette="viridis")
plt.xlabel("Bulan Ke - ")
plt.ylabel("Jumlah Pelanggan")
plt.title(None)
plt.tight_layout()
st.pyplot(fig)

st.markdown("-------")

# Grafik garis perbedaan penggunaan sepeda pada hari kerja dan libur setiap jam nya
st.subheader("Penyewaan sepeda pada hari kerja dan libur tiap jamnya")
fig, ax = plt.subplots()
sns.lineplot(x="hour", y="cnt", data=hourly_df, hue="holiday", palette="viridis")
plt.xlabel("Jam Ke - ")
plt.ylabel("Jumlah")
plt.legend(title="Ket", loc="upper right")  
plt.xticks(ticks=hourly_df["hour"], labels=hourly_df["hour"])
plt.tight_layout()
st.pyplot(fig)

with st.expander('Keterangan'):
    st.write(
        """
        0 : Tidak Libur / Kerja
        
        1 : Libur
        """
    )
st.caption("Copyright by Fernando Michael Hebert Siregar (2024)")