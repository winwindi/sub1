import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime
import plotly.express as px


# Load cleaned data
day = pd.read_csv("day.csv")


#Rename column
day.rename(columns={'dteday':'date', 'yr':'year', 'mnth':'month', 'weekday':'day', 'weathersit':'weather',
                    'temp':'temperature', 'atemp':'temperature_feel', 'hum':'humidity', 'casual':'casual_user',
                    'registered':'registered_user', 'cnt':'total_user'}, inplace=True)


# Filter data
day["date"] = pd.to_datetime(day["date"])


with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")


#konversi Year
def konversi_year(x):
    if x == 0:
        return 2011
    else:
        return 2012

day['year'] = day['year'].apply(konversi_year)


konversi_day = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 4:'friday', 5:'saturday', 6:'sunday'}

day['day'] = day['day'].map(konversi_day)


#konversi season
def konversi_season(x):
    if x == 1:
        return 'spring'
    elif x == 2:
        return 'summer'
    elif x == 3:
        return 'fall'
    else:
        return 'winter'

day['season'] = day['season'].apply(konversi_season)


def konversi_weather(x):
    if x == 1:
        return 'clear'
    elif x == 2:
        return 'mist'
    elif x == 3:
        return 'snow'
    else:
        return 'heavy rain'

day['weather'] = day['weather'].apply(konversi_weather)


def konversi_workingday(x):
    if x == 0:
        return 'weekend/holiday'
    else:
        return 'working day'

day['workingday'] = day['workingday'].apply(konversi_workingday)


# Aggregasi Data
agg_day = day.groupby(by="day").agg({
    "date": "nunique",
    "casual_user": "sum",
    "registered_user": "sum",
    "total_user": ["max", "min", "mean", "sum"],
})

agg_month = day.groupby(by=["year", "month"]).agg({
    "date": "nunique",
    "casual_user": "sum",
    "registered_user": "sum",
    "total_user": ["max", "min", "mean", "sum"],
})

sum_casual_user = day.groupby("day").casual_user.sum().sort_values(ascending=False).reset_index()
sum_registered_user = day.groupby("day").registered_user.sum().sort_values(ascending=False).reset_index()

byweather = day.groupby("weather").total_user.sum().sort_values(ascending=False).reset_index()
byseason = day.groupby("season").total_user.sum().sort_values(ascending=False).reset_index()


plot_option = st.sidebar.radio(
    "pilihan pertanyaan untuk menampilkan visualisasi :",
    ["Bagaimana gambaran Trend penyewaan sepeda dalam 2 tahun?", "Bagaimana pola bike sharing saat weekday dan weekend perbulannya?", "Bagaimana pola penggunaan Bike dari user casual maupun registered setiap harinya?", 
     "Bagaimana pola penggunaan Bike sharing/rent berdasarkan musim dan cuaca ?", "Analisis RFM dalam rangka peningkatan revenue"]
)


st.title("Bike Sharing/Rent Dashboard")
st.write(
    """
    Dataset Bike Sharing ini terkait dengan catatan historis dua tahun yang mencakup tahun 2011 dan 2012 dari sistem Capital Bikeshare di Washington D.C., Amerika Serikat.
    """
)


if plot_option == "Bagaimana gambaran Trend penyewaan sepeda dalam 2 tahun?":
        
    fig, ax = plt.subplots(figsize=(22, 6))
    sns.lineplot(
    data=day,
    x='date',
    y='total_user',
    hue='year',
    palette='coolwarm',
    linewidth=2.5,
    ax=ax
    )

    # Menambahkan elemen
    ax.set_title('Tren bike sharing 2011-2012', fontsize=40, pad=18)
    ax.set_xlabel('Date', fontsize=16)
    ax.set_ylabel('Count of Bike Rent', fontsize=16)
    ax.tick_params(axis='x', labelsize=12, rotation=45)
    ax.tick_params(axis='y', labelsize=12)

    # Menambahkan grid
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # Menambahkan legend
    ax.legend(title='Year Sequence', loc='upper left', fontsize=12, title_fontsize=14)

    # Menampilkan chart di Streamlit
    st.pyplot(fig)

    st.markdown("tren penggunaan bike sharing tahun 2012 naik dibanding 2011")



elif plot_option == "Bagaimana pola bike sharing saat weekday dan weekend perbulannya?":
    # Pola Bike Sharing Saat Weekday dan Weekend Perbulan
    fig, ax = plt.subplots(figsize=(20, 5))
    sns.pointplot(
        data=day,
        x='month',
        y='total_user',
        hue='workingday',
        errorbar=None,
        ax=ax,
        palette="coolwarm",
        markers=["o", "s"]
    )

    # Setting the title and labels
    ax.set_title('Pola Bike Sharing Saat Weekday dan Weekend Perbulan', fontsize=40, pad=18)
    ax.set_ylabel('count', fontsize=14)
    ax.set_xlabel('month', fontsize=14)

    # Tampilkan plot di Streamlit
    st.pyplot(fig)
    st.markdown("penggunaan bike sharing dimulai dari bulan february dengan puncaknya di bulan agustus (saat weekday/working day) dan june&Sept (saat weekend/holiday) dan akan turun kembali menjelang desember (musim dingin)")


elif plot_option == "Bagaimana pola penggunaan Bike dari user casual maupun registered setiap harinya?":
    st.subheader("Pengguna bike sharing/rent dari tipe user casual dan register daily")
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
    # Warna untuk plot
    colors_casual = ["#FFA07A", "#FF7F50", "#FF6347", "#FF4500", "#FF0000", "#DC143C", "#B22222"]
    colors_registered = ["#4682B4", "#5F9EA0", "#6495ED", "#4169E1", "#1E90FF", "#00BFFF", "#87CEEB"]
    
    # Plot Casual Users
    sns.barplot(
        x="casual_user", 
        y="day", 
        data=sum_casual_user, 
        palette=colors_casual, 
        hue="day", 
        dodge=False, 
        ax=ax[0]
    )
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Casual User", loc="center", fontsize=30)
    ax[0].tick_params(axis='y', labelsize=20)

    # Plot Registered Users
    sns.barplot(
        x="registered_user", 
        y="day", 
        data=sum_registered_user, 
        palette=colors_registered, 
        hue="day", 
        dodge=False, 
        ax=ax[1]
    )
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Registered User", loc="center", fontsize=30)
    ax[1].tick_params(axis='y', labelsize=20)

    # Adjust layout
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("untuk casual user penggunaan bike sharing/rent paling banyak di hari minggu, dan paling sedikit di hari kamis, sedangkan untuk register user penggunaan bike sharing/rent paling banyak di hari jumat, dan paling sedikit di hari senin")


elif plot_option == "Bagaimana pola penggunaan Bike sharing/rent berdasarkan musim dan cuaca ?":
    st.subheader("pola penggunaan Bike sharing/rent berdasarkan musim dan cuaca")
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
    # Warna untuk plot
    colors_weather = ["#FFA07A", "#FF7F50", "#FF6347", "#FF4500", "#FF0000", "#DC143C", "#B22222"]
    colors_season = ["#4682B4", "#5F9EA0", "#6495ED", "#4169E1", "#1E90FF", "#00BFFF", "#87CEEB"]
    
    # Plot weather
    sns.barplot(
        x="total_user", 
        y="weather", 
        data=byweather, 
        palette=colors_weather, 
        hue="weather", 
        dodge=False, 
        ax=ax[0]
    )
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Number of User by Weather", loc="center", fontsize=30)
    ax[0].tick_params(axis='y', labelsize=20)

    # Plot season
    sns.barplot(
        x="total_user", 
        y="season", 
        data=byseason, 
        palette=colors_season, 
        hue="season", 
        dodge=False, 
        ax=ax[1]
    )
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Number of User by Season", loc="center", fontsize=30)
    ax[1].tick_params(axis='y', labelsize=20)

    # Adjust layout
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("berdasarkan kondisi cuaca, penggunaan bike sharing paling banyak pada cuaca cerah, sedangkan paling rendah saat cuaca bersalju ataupun hujan deras. Bila berdasarkan musim, penggunaan bike sharing paling banyak pada gugur (fall), sedangkan paling rendah pada musim semi")



elif plot_option == "Analisis RFM dalam rangka peningkatan revenue":
    st.subheader("Analisis RFM dalam rangka peningkatan revenue")

    rfm_df = day.groupby(by="day", as_index=False).agg({
        "date": "max",         # Mendapatkan tanggal terakhir transaksi untuk setiap "day"
        "instant": "nunique",  # Menghitung jumlah transaksi unik (frekuensi)
        "total_user": "sum"    # Menjumlahkan total pendapatan untuk setiap "day"
    })


    rfm_df.columns = ["day", "max_order_timestamp", "frequency", "monetary"]
    #max_order_timestamp: Tanggal terakhir transaksi.
    #frequency: Frekuensi transaksi (jumlah pesanan).
    #monetary: Total pendapatan.

    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date #Tanggal terakhir transaksi.
    #recent_date: Mengambil tanggal terbaru dari semua transaksi.
    recent_date = day["date"].dt.date.max()

    #recency: Dihitung sebagai selisih hari antara recent_date (hari terakhir transaksi dalam dataset) dan max_order_timestamp (tanggal transaksi terakhir). Ini menggambarkan berapa lama sejak transaksi terakhir.
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)

    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)#Kolom max_order_timestamp dihapus setelah informasi recency dihitung karena sudah tidak diperlukan lagi.

    rfm_df = rfm_df

    # visualisasi
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 8))
    colors = sns.color_palette("coolwarm", 7)

    # Recency
    sns.lineplot(y="recency", x="day", data=rfm_df.sort_values(by="recency", ascending=True),
                marker="o", linewidth=2.5, color=colors[3], ax=ax[0])
    ax[0].set_title("Recency (days)", fontsize=18)
    ax[0].set_xlabel("Day", fontsize=14)
    ax[0].set_ylabel("Recency", fontsize=14)
    ax[0].tick_params(axis='x', labelsize=12)

    # Frequency
    sns.scatterplot(y="frequency", x="day", data=rfm_df.sort_values(by="frequency", ascending=False),
                    s=200, color=colors[2], ax=ax[1])
    ax[1].set_title("Frequency", fontsize=18)
    ax[1].set_xlabel("Day", fontsize=14)
    ax[1].set_ylabel("Frequency", fontsize=14)
    ax[1].tick_params(axis='x', labelsize=12)

    # Monetary
    sns.barplot(x="monetary", y="day", data=rfm_df.sort_values(by="monetary", ascending=False),
                palette="coolwarm", ax=ax[2])
    ax[2].set_title("Monetary", fontsize=18)
    ax[2].set_xlabel("Monetary", fontsize=14)
    ax[2].set_ylabel("Day", fontsize=14)
    ax[2].tick_params(axis='y', labelsize=12)

    # Adjust layout
    plt.tight_layout()
    
    # Display the plot in Streamlit
    st.pyplot(fig)
    
    st.markdown("Dari hasil analisis RFM tersebut, berikut rekomendasi untuk  promosi peningkatan revenue dari tahun ke tahun yang dihasilkan dari analysis RFM :")
    st.markdown("- Hari Jumat memenuhi kriteria monetary, strateginya melakukan kampanye loyalitas dan promosi khusus untuk memaksimalkan frekuensi serta nilai pembelian pelanggan. Optimalkan potensi pelanggan yang sudah melakukan transaksi baru-baru ini.")
    st.markdown("- Hari Sabtu dgn pendapatan tinggi, strateginya tingkatkan volume penjualan dengan strategi cross-selling dan bundling.")
    st.markdown("- Hari Selasa untuk retensi pelanggan baru, fokuskan strategi retensi seperti pemberian insentif atau pesan pengingat kepada pelanggan aktif.")
    