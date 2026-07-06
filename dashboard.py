import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")
sns.set_theme(style='darkgrid')

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

day_df = load_data()

st.sidebar.title("🚲 Menu Navigasi")

# Filter Rentang Waktu
st.sidebar.markdown("### Filter Rentang Waktu")
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

date_range = st.sidebar.date_input(
    label='Pilih Rentang Tanggal',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = date_range[0]
    end_date = date_range[0]

# Filter Musim
st.sidebar.markdown("### Filter Musim")
season_options = ['Spring', 'Summer', 'Fall', 'Winter']
selected_season = st.sidebar.selectbox(
    'Pilih Musim untuk Grafik Cuaca:',
    options=season_options,
    index=2 
)

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                 (day_df["dteday"] <= str(end_date))]

# Main Dashboard
st.title("Bike Sharing Data Dashboard (2012)")
st.markdown("Dashboard interaktif ini dibangun berdasarkan hasil analisis proyek pada Jupyter Notebook.")
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = main_df['cnt'].sum()
    st.metric("Total Penyewaan (Sesuai Filter Tanggal)", value=f"{total_rentals:,}")
with col2:
    total_registered = main_df['registered'].sum()
    st.metric("Total Pengguna Terdaftar", value=f"{total_registered:,}")
with col3:
    total_casual = main_df['casual'].sum()
    st.metric("Total Pengguna Kasual", value=f"{total_casual:,}")

st.markdown("---")

# Visualisasi 1: Pengaruh Cuaca Berdasarkan Musim Terpilih
st.subheader(f"Pengaruh Kondisi Cuaca terhadap Penyewaan di Musim {selected_season}")
st.markdown(f"Grafik ini menampilkan rata-rata penyewaan sepeda berdasarkan cuaca pada musim **{selected_season}** (Default: Fall, sesuai pertanyaan bisnis 1).")

# Memfilter data berdasarkan musim yang dipilih di sidebar
seasonal_data = main_df[main_df['season'] == selected_season]
weather_impact = seasonal_data.groupby('weathersit')['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 5))

if not weather_impact.empty:
    sns.barplot(
        x='weathersit', 
        y='cnt', 
        hue='weathersit',  
        data=weather_impact, 
        palette="Blues_d", 
        ax=ax,
        legend=False       
    )
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)
else:
    # Jika pengguna memilih tanggal Januari (Winter) tapi memaksa melihat musim Fall, berikan informasi yang rapi
    st.info(f"Tidak ada data Musim {selected_season} pada rentang tanggal yang Anda pilih di kalender. Silakan sesuaikan tanggal kalender Anda atau ubah filter musim di sidebar.")

# Visualisasi 2: Tren Pengguna Casual VS Registered
st.markdown("---")
st.subheader("Tren Pengguna Casual VS Registered")
st.markdown("Grafik ini menjawab pertanyaan bisnis 2 mengenai perbandingan perilaku pengguna pada hari kerja vs hari libur.")

user_type_day = main_df.groupby('workingday_label')[['casual', 'registered']].mean().reset_index()
user_type_melted = pd.melt(user_type_day, id_vars=['workingday_label'], value_vars=['casual', 'registered'])

fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='workingday_label', 
    y='value', 
    hue='variable', 
    data=user_type_melted, 
    palette=["#FF9999", "#72BCD4"], 
    ax=ax2
)
ax2.set_xlabel("Tipe Hari")
ax2.set_ylabel("Rata-rata Penyewaan")
ax2.legend(title='Tipe Pengguna')
st.pyplot(fig2)

# Footer
st.caption("Proyek Akhir Dicoding - Analisis Data dengan Python")