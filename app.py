import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import numpy as np
import pandas as pd
import plotly.express as px
from numerize.numerize import numerize
import time
from PIL import Image, ImageDraw
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Propits",page_icon="mirror",layout="wide")

theme_plotly = None # None or streamlit

# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
# Load data
data = pd.read_csv("supply_chain_data.csv")

# Lebar sidebar
sidebar_width = 200
st.sidebar.markdown(
    f'<style>img.width {{ width: {sidebar_width}px; }} img.width:hover {{ width: 100%; transition: 0.3s; cursor: pointer; }}</style>',
    unsafe_allow_html=True,
)

st.sidebar.image("images/propits.jpg", use_column_width=True, output_format="JPEG", width=None,)
#Options Menu
with st.sidebar:
    selected = option_menu('Main Menu', ["Dashboard", "Home", "Application", "About Us"], 
        icons=['bar-chart','house','laptop', 'info-circle'], menu_icon='intersect', default_index=0)
    key="page_selection"


# Menggunakan CSS untuk mengubah ukuran teks
st.sidebar.markdown(
    """
    <style>
    label[for="page_selection"] {
        font-size: 50px;  /* Ganti dengan ukuran teks yang Anda inginkan */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if selected == "Dashboard":
        
    # Tambahkan judul
    st.title('Dashboard Data Produk')
    st.header("Halaman Dashboard")
    st.write("Selamat datang di halaman Dashboard.")

    #compute top analytics
    total_profit = data['Revenue generated'].sum()
    total_orders = data['Number of products sold'].sum()
    total_cost = data['Costs'].sum()
    total_stock = data['Stock levels'].sum()

    profit_column, orders_column, cost_column, stock_column, = st.columns(4)
    with profit_column:
        st.info('Total Profit', icon="💰")
        st.metric(label="Total Profit (TZS)", value=f"{total_profit:,.0f}")
    with orders_column:
        st.info('Total Orders', icon="📦")
        st.metric(label="Total Orders", value=f"{total_orders:,.0f}")
    with cost_column:
        st.info('Total Cost', icon="💲")
        st.metric(label="Total Cost (TZS)", value=f"{total_cost:,.0f}")
    with stock_column:
        st.info('Total Stock', icon="📈")
        st.metric(label="Total Stock", value=f"{total_stock:,.0f}")
    st.markdown("""---""")

    col1, col2 = st.columns(2)  
    with col1:
        st.subheader('Grafik Harga Produk')
        fig = px.bar(data, x='Product type', y='Price', color='Product type', title='Harga Produk per Tipe Produk')
        fig.update_layout(width=450, height=450)
        st.plotly_chart(fig)    
    with col2:
        st.subheader('Grafik Penjualan Produk')
        fig2 = px.bar(data, x='Product type', y='Number of products sold', color='Product type', title='Jumlah Produk Terjual per Tipe Produk')
        fig2.update_layout(width=450, height=450)
        st.plotly_chart(fig2)

    # Grafik Pie Chart untuk Inventori
    with col1:
        st.subheader('Grafik Inventori')
        inventory_data = data[['Product type', 'Stock levels']].groupby('Product type').sum().reset_index()
        pie_chart_inventory = px.pie(
            inventory_data, 
            names='Product type', 
            values='Stock levels', 
            title='Inventori per Tipe Produk',
            color_discrete_sequence=['blue', 'green', 'red', 'purple'])
        pie_chart_inventory.update_layout(width=450, height=450)
        st.plotly_chart(pie_chart_inventory)
    # Grafik Pie Chart untuk Biaya
    with col2:
        st.subheader('Grafik Biaya')
        cost_data = data[['Product type', 'Costs']].groupby('Product type').sum().reset_index()
        pie_chart_costs = px.pie(cost_data, names='Product type', values='Costs', title='Biaya per Tipe Produk')
        pie_chart_costs.update_layout(width=450, height=450)
        st.plotly_chart(pie_chart_costs)
    
     # Grafik Line Chart untuk Tren Prediksi
    with col1:
        st.subheader('Grafik Tren Prediksi')
        prediction_data = data[['Product type', 'Revenue generated']].groupby('Product type').sum().reset_index()
        line_chart = px.line(
            prediction_data, 
            x='Product type', 
            y='Revenue generated', 
            title='Tren Pendapatan per Tipe Produk',)  
        line_chart.update_layout(width=450, height=400)
        st.plotly_chart(line_chart)
    with col2:
        st.subheader('Write Data')
        st.write(data)
    

if selected == "Home":
    st.header("Halaman Home")
    st.write("Selamat datang di Halaman Home.")
    page_title="PROPITS - Prediksi Rantai Pasokan Optimal untuk Produksi Tinggi Skincare",
    page_icon=":lipstick:",
    layout="wide",

    tab1,tab2,=st.tabs(['Informasi','Latar Belakang'])
    st.markdown(
    """
    <style>
    /* Mengatur ukuran teks pada tab */
    .streamlit-tabs li {
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True
    )
    
    with tab1:
        st.title("Selamat Datang di PROPITS")
        st.markdown("Prediksi Rantai Pasokan Optimal untuk Produksi Tinggi Skincare")
        st.header("Mengoptimalkan Rantai Pasokan Skincare dengan Teknologi AI")
        col1, col2 = st.columns(2)
        col1.image("images/care.jpg", width=500)
        # Tentang PROPITS
        col2.header("Tentang PROPITS")
        col2.write(
            "PROPITS adalah perusahaan yang berfokus pada penggunaan kecerdasan buatan (AI) untuk mengoptimalkan rantai pasokan produk skincare. Kami memahami bahwa estimasi volume produksi dan manufaktur yang tidak akurat dapat berdampak pada efektivitas perkiraan fluktuasi permintaan pelanggan dan identifikasi tren.")
        col2.write(
            "Kami berkomitmen untuk membantu perusahaan skincare dan kecantikan dalam mengurangi biaya produksi yang berlebihan dan meningkatkan profitabilitas.")

        # Layanan dan Solusi
        st.header("Layanan dan Solusi")
        st.write("Kami menawarkan layanan dan solusi berbasis AI yang meliputi:")
        st.markdown("- Prediksi volume produksi skincare.")
        st.markdown("- Analisis rantai pasokan yang lebih efisien.")
        st.markdown("- Estimasi kebutuhan pelanggan dan pasar secara efektif.")

    with tab2:
        st.title("Latar Belakang")
        st.write('Perusahaan yang bergerak di industri skincare dan kecantikan sering menghadapi kendala dalam melakukan estimasi volume produksi komoditas barang mereka yang tidak akurat. Hal ini menyebabkan perusahaan tidak dapat memaksimalkan profit yang dapat dicapai. Oleh karena itu, diperlukan sebuah solusi yang dapat membantu perusahaan dalam mengatasi masalah tersebut.')
        st.write('Salah satu solusi yang dapat digunakan adalah penggunaan algoritma clustering, seperti K-Means atau Hierarchical Clustering, dalam pengerjaan proyek akhir aplikasi ini. Algoritma clustering merupakan metode analisis data yang digunakan untuk mengelompokkan data ke dalam kelompok-kelompok atau cluster berdasarkan kesamaan karakteristik. Dalam konteks ini, algoritma clustering akan digunakan untuk mengelompokkan data produksi komoditas barang berdasarkan kesamaan volume produksi.')
        st.write('Pembuatan aplikasi ini bertujuan untuk memberikan informasi yang akurat dan visualisasi yang jelas terkait estimasi volume produksi komoditas barang. aplikasi ini akan memberikan gambaran yang lebih baik tentang volume produksi yang diharapkan, sehingga perusahaan dapat melakukan perencanaan dan pengambilan keputusan yang lebih baik.')
        st.write('aplikasi ini akan menampilkan data historis volume produksi komoditas barang, serta hasil dari pengelompokan menggunakan algoritma clustering. Dengan demikian, perusahaan dapat melihat pola atau tren dari data historis, serta mendapatkan insight tentang kelompok-kelompok produksi yang ada.')
        st.write('Selain itu, aplikasi ini juga akan dilengkapi dengan fitur-fitur lain yang berguna bagi perusahaan. Misalnya, aplikasi ini dapat memberikan rekomendasi terkait strategi produksi yang dapat dilakukan berdasarkan hasil analisis data. Aplikasi ini juga dapat memberikan informasi tentang estimasi permintaan pasar, sehingga perusahaan dapat mengatur volume produksi secara lebih efisien.')
        st.write('Diharapkan bahwa dengan adanya Aplikasi ini, perusahaan dapat mengatasi kendala dalam melakukan estimasi volume produksi komoditas barang yang tidak akurat. Dengan informasi yang lebih akurat dan visualisasi yang jelas, perusahaan dapat memaksimalkan profit yang dapat dicapai dan mengambil keputusan yang lebih baik dalam mengatur volume produksi.')
        st.divider()  
        
    # Footer
    st.markdown(
        '<div style="background-color: #345995; padding: 10px; color: white;">'
        '© 2023 PROPITS. Hak Cipta Dilindungi Undang-Undang.'
        '</div>',
        unsafe_allow_html=True,
)
if selected == "Application":
    # Memuat model produksi yang sudah disimpan
    model_production = joblib.load('/propits/model/model_production.pkl')

    # Memuat model transportation yang sudah disimpan
    model_transportation = joblib.load('/propits/model/model_transportation.pkl')

    # Judul aplikasi
    st.title('Aplikasi Prediksi Jumlah Produksi')

    #Options Menu
    with st.sidebar:
        selected = option_menu('Pilih Aplikasi', ["Prediksi Produksi Stok Level", "Prediksi Biaya Transportasi"], 
            icons=['bar-chart','bar-chart', ], menu_icon='laptop', default_index=0)
        key="page_selection"

    if selected == "Prediksi Produksi Stok Level":
    # Input fitur untuk prediksi produksi
        col1, col2 = st.columns(2)
        with col1:
            price = st.number_input('Price ($)')
            availability = st.number_input('Availability')
            number_of_products_sold = st.number_input('Number of Product Sold')
            revenue_generated = st.number_input('Revenue Generated')
            stock_levels = st.number_input('Stock Levels')
        with col2:
            lead_times = st.number_input('Lead Time')
            order_quantities = st.number_input('Order Quantities')
            shipping_times = st.number_input('Shipping Times')
            shipping_costs = st.number_input('Shipping Cost')
            manufacturing_costs = st.number_input('Manufacturing Cost')

        # Menambahkan validasi untuk memastikan tidak ada input yang kosong atau bernilai 0
        if st.button('Prediksi Produksi') and all([
            price != 0, availability != 0, number_of_products_sold != 0, revenue_generated != 0,
            stock_levels != 0, lead_times != 0, order_quantities != 0, shipping_times != 0, 
            shipping_costs != 0, manufacturing_costs != 0
        ]):
            input_data = [price, availability, number_of_products_sold, revenue_generated,
                        stock_levels, lead_times, order_quantities, shipping_times, shipping_costs, 
                        manufacturing_costs]
            production_prediction = model_production.predict([input_data])[0]
            st.write(f'Prediksi Produksi: {production_prediction}')
        else:
            st.warning("Harap isi semua input dengan nilai yang bukan nol.")

        st.subheader('Grafik Data')
        data = pd.read_csv('supply_chain_data.csv')
        st.line_chart(data[['Price', 'Availability', 'Number of products sold']])
        
    else:
        col1, col2 = st.columns(2)
        with col1:
            price = st.number_input('Price')
            availability = st.number_input('Availability')
            stock_levels = st.number_input('Stock Levels')
        with col2:
            lead_times = st.number_input('Lead Times')
            shipping_times = st.number_input('Shipping Time')
            shipping_costs = st.number_input('Shipping costs')

        # Validasi untuk memastikan tidak ada input yang kosong atau bernilai 0
        inputs_valid = price != 0 and availability != 0 and stock_levels != 0 and lead_times != 0 and shipping_times != 0 and shipping_costs != 0

        # Tombol prediksi biaya transportasi hanya aktif jika semua input valid
        if inputs_valid and st.button('Prediksi Biaya Transportasi'):
            input_data = [price, availability, stock_levels, lead_times, shipping_times, shipping_costs]
            transportation_prediction = model_transportation.predict([input_data])[0]
            st.write(f'Prediksi Biaya Transportasi: {transportation_prediction}')
        elif not inputs_valid:
            st.warning('Pastikan tidak ada input yang kosong atau bernilai 0.')
        
        st.subheader('Grafik Data')
        data = pd.read_csv('supply_chain_data.csv')
        st.line_chart(data[['Price', 'Availability', 'Number of products sold']])

if selected == "About Us":
    # Data anggota tim
    st.title('Creator')
    st.markdown('<hr>', unsafe_allow_html=True)
    def shape_image(image_path, background_color):
        image = Image.open(image_path)
        width, height = image.size
        background = Image.new('RGBA', image.size, background_color)
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, width, height), fill=255)
        background.putalpha(mask)
        background.paste(image, (0, 0), image)
        
        return background
    background_color = (255, 255, 255, 255)

    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image(shape_image('images/profile/siju.png', background_color), width=300)
            st.write('')
            st.write('')
            st.write('**Name      :**    Siti Nurjubaedah')
            st.write('**University:**    Sekolah Tinggi Teknologi Bandung')
            st.write('**Task      :**    Data Engineer')
            st.write('**Contact   :**   sitinurjubaedah23@gmail.com')      
        with col2:
            st.image(shape_image('images/profile/juann.png', background_color), width=300)
            st.write('')
            st.write('')
            st.write('**Name      :**  Juan Rhema Christopher Togatorop')
            st.write('**University:**  Universitas Indonesia ')
            st.write('**Task      :**  Technical Writer')
            st.write('**Contact   :**  juan.rhema@ui.ac.id')
        with col3:
            st.image(shape_image('images/profile/sarii.png', background_color), width=300)
            st.write('')
            st.write('')
            st.write('**Name      :**    Sari Indah Wulan')
            st.write('**University:**    Institut Pendidikan dan Bahasa Invada')
            st.write('**Task      :**    UI/UX Designer')
            st.write('**Contact   :**    sariindahh02@gmail.com')
        st.divider()
        col4, col5, col6, col7 = st.columns(4)
        with col4:
            st.image(shape_image('images/profile/jae.png', background_color), width=300)
        with col5:
            st.write('')
            st.write('')
            st.write('**Name      :**    Lanlan Jaelani')
            st.write('**University:**    Institut Pendidikan Indonesia Garut')
            st.write('**Task      :**    Frontend Engineer')
            st.write('**Contact   :**  lanjae1916@gmail.com')
        with col6:
            st.image(shape_image('images/profile/puput.png', background_color), width=300)
        with col7:
            st.write('')
            st.write('')
            st.write('**Name      :**    Puput Novianti')
            st.write('**University:**    Institut Pendidikan dan Bahasa Invada')
            st.write('**Task      :**    Frontend Engineer')
            st.write('**Contact   :**  noviyantip06@gmail.com')
        st.divider()
