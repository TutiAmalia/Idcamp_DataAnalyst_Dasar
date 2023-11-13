import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-commerce Insights")

# Set the title and subheader of your Streamlit app
st.title(
    "E-commerce Insights"
)
# Load data
product_count_english_df = pd.read_csv('../product_count_english_df.csv')
review_product_count = pd.read_csv('../review_product_count.csv')
customers_df = pd.read_csv('../customers_df.csv')
total_revenue_df = pd.read_csv('../total_revenue_df.csv')
order_payment_df = pd.read_csv('../order_payment_df.csv')
orders_df = pd.read_csv('../orders_df.csv')

# Define color palette
colors = ['#068DA9', '#D3D3D3', '#D3D3D3', '#D3D3D3', '#D3D3D3']

# 1. Kategori Produk Terlaris dan Kurang Laris
st.subheader('Kategori Produk Terlaris dan Kurang Laris')

product_count_df = product_count_english_df.groupby(by='product_category_name_english')['product_id'].count().reset_index()
product_count_df = product_count_df.rename(columns={'product_category_name_english': 'Kategori', 'product_id': 'Jumlah Produk'})

# Membuat plot dengan Plotly Express
fig = px.bar(product_count_df.sort_values(by='Jumlah Produk', ascending=False).head(5),
             x='Jumlah Produk', y='Kategori', orientation='h',
             color='Kategori',
             color_discrete_sequence=colors,  # Gunakan color_discrete_sequence
             width=800, height=400)

fig.update_layout(xaxis_tickangle=0, yaxis_categoryorder='total ascending')
fig.update_traces(showlegend=False)

fig2 = px.bar(product_count_df.sort_values(by='Jumlah Produk', ascending=True).head(5),
              x='Jumlah Produk', y='Kategori', orientation='h',
              color='Kategori',
              color_discrete_sequence=colors,  # Gunakan color_discrete_sequence
              width=800, height=400)

fig2.update_layout(xaxis_tickangle=0, yaxis_categoryorder='total ascending')
fig2.update_traces(showlegend=False)

# Membuat dua tab
tabs = st.tabs(['Terlaris', 'Kurang Laris'])
tabs[0].plotly_chart(fig)
tabs[1].plotly_chart(fig2)

# 2. Produk Tertinggi dan Terendah berdasarkan Review
st.subheader('Produk Tertinggi dan Terendah berdasarkan Review')

# Membuat plotly
fig3 = px.bar(review_product_count.sort_values(by='mean_review_score', ascending=False).head(5),
              x='mean_review_score', y='product_category_name_english',
              labels={'product_category_name_english': 'Kategori', 'mean_review_score': 'Skor Review'},
              orientation='h',
              color='product_category_name_english',
              color_discrete_sequence=colors,  # Gunakan color_discrete_sequence
              width=800, height=400)
fig3.update_layout(xaxis_tickangle=0, yaxis_categoryorder='total ascending')
fig3.update_traces(showlegend=False)

fig4 = px.bar(review_product_count.sort_values (by='mean_review_score', ascending=True).head(5),
              x='mean_review_score', y='product_category_name_english',
              labels={'product_category_name_english': 'Kategori', 'mean_review_score': 'Skor Review'},
              orientation='h',
              color='product_category_name_english',
              color_discrete_sequence=colors,  # Gunakan color_discrete_sequence
              width=800, height=400)
fig4.update_layout(xaxis_tickangle=0, yaxis_categoryorder='total ascending')
fig4.update_traces(showlegend=False)

# Membuat dua tab
tabs = st.tabs(['Review Tertinggi', 'Review Terendah'])
tabs[0].plotly_chart(fig3)
tabs[1].plotly_chart(fig4)

# 3. Jumlah Kostumer Berdasarkan State
st.subheader('Jumlah Kostumer Berdasarkan State')

customer_state_count = customers_df.groupby(by='customer_state').customer_id.nunique().sort_values(ascending=False).reset_index()

# Mencari state dengan jumlah pelanggan terbanyak
most_common_state = customer_state_count.loc[0, 'customer_state']

# Membuat warna untuk setiap state
colors = {state: "#068DA9" if state == most_common_state else "#D3D3D3" for state in customer_state_count['customer_state']}

fig5 = px.bar(customer_state_count, x='customer_state', y='customer_id',
              labels={'customer_state': 'State', 'customer_id': 'Jumlah Kostumer'},
              orientation='v',
              color='customer_state',
              color_discrete_map=colors,  # Gunakan color_discrete_map
              width=800, height=400)
fig5.update_layout(xaxis_tickangle=0, yaxis_categoryorder='total ascending')
fig5.update_traces(showlegend=False)
st.plotly_chart(fig5)

# 4. Status Pemesanan
st.subheader('Status Pemesanan')
order_status_count = total_revenue_df.groupby(by='order_status').order_id.nunique().sort_values(ascending=False).reset_index()

# Mencari state dengan jumlah pelanggan terbanyak
most_common_status = order_status_count.loc[0, 'order_status']

# Membuat warna untuk setiap state
colors = {status: "#068DA9" if status == most_common_status else "#D3D3D3" for status in order_status_count['order_status']}

fig6 = px.bar(order_status_count, x='order_status', y='order_id',
              labels={'order_status': 'Order Status', 'order_id': 'Jumlah Pesanan'},
              orientation='v',
              color='order_status',
              color_discrete_map=colors,  # Gunakan color_discrete_map
              width=800, height=400)
fig6.update_layout(xaxis_tickangle=0, yaxis_categoryorder='total ascending')
fig6.update_traces(showlegend=False)
st.plotly_chart(fig6)


# 5. Distribusi Jenis Pembayaran berdasarkan rata-rata pembayaran dan berdasarkan jumlah pesanan

# Rata-rata pembayaran
mean_payment_value = order_payment_df.groupby(by='payment_type').payment_value.mean().reset_index()
mean_payment_value = mean_payment_value[mean_payment_value['payment_type'] != 'Not Defined'].sort_values(by='payment_value', ascending=False)
most_common_mean_payment = mean_payment_value.loc[mean_payment_value['payment_value'].idxmax(), 'payment_type']

# Membuat warna untuk setiap state
colors = {payment: "#068DA9" if payment == most_common_mean_payment else "#D3D3D3" for payment in mean_payment_value['payment_type']}

# Jumlah pesanan
order_payment_count = order_payment_df.groupby(by='payment_type').order_id.nunique().reset_index()
order_payment_count = order_payment_count[order_payment_count['payment_type'] != 'Not Defined'].sort_values(by='order_id', ascending=False)
most_common_order_payment = order_payment_count.loc[0, 'payment_type']

col1, col2 = st.columns([2,1])
with col1:
    st.markdown("<h4 style='text-align:center;'>Jenis Pembayaran berdasarkan Rata-rata Jumlah Pembayaran</h4>", unsafe_allow_html=True)
    fig7 = px.bar(mean_payment_value, x='payment_type', y='payment_value',
                labels={'payment_type': 'Jenis Pembayaran', 'payment_value': 'Rata-rata Pembayaran'},
                orientation='v',
                color='payment_type',
                color_discrete_map=colors,  # Gunakan color_discrete_map
                width=400, height=400)

    fig7.update_layout(xaxis_tickangle=0, yaxis_categoryorder='total ascending')
    fig7.update_traces(showlegend=False)
    st.plotly_chart(fig7)


# Create a list of colors
with col2:
    colors1 = ['#068DA9', '#D3D3D3', '#66b3ff', '#ff9999']
    st.markdown("<h4 style='text-align:center;'>Jenis Pembayaran berdasarkan Jumlah Pesanan</h4>", unsafe_allow_html=True)

    # Create a pie chart using Plotly Express
    fig8 = px.pie(order_payment_count, values='order_id', names='payment_type', color_discrete_sequence=colors1, 
                labels={'order_id': 'Percentage'},
                width=400, height=400)

    # Display the pie chart using Streamlit
    st.plotly_chart(fig8)


# 6. Tren pertumbuhan penjualan
# Membuat DataFrame yang berisi data tanggal dan jumlah order
orders_date = orders_df.groupby(by='month').order_id.nunique().reset_index()
# Menghapus komponen waktu (00:00:00) dari kolom 'month'
orders_date['month'] = pd.to_datetime(orders_date['month']).dt.date

# Mengonversi kolom 'order_purchase_timestamp' menjadi datetime
orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])

# Membuat DataFrame untuk bulan November 2017
get_nov_value = orders_df.loc[:, ['order_purchase_timestamp', 'order_id']]
get_nov_value['month'] = get_nov_value['order_purchase_timestamp'].dt.strftime('%m-%Y')
get_nov_value['day'] = get_nov_value['order_purchase_timestamp'].dt.strftime('%d')
nov_2017_data = get_nov_value[get_nov_value['month'] == '11-2017']

# Menghitung jumlah order per tanggal di bulan November 2017
daily_order_count = nov_2017_data.groupby(['day', 'month']).order_id.nunique().reset_index()
daily_order_count.columns = ['Tanggal', 'Bulan', 'Jumlah Pemesanan']

# Membagi layar menjadi 2 kolom
col3, col4 = st.columns([3, 1])

# Kolom 1: Grafik Tren Pertumbuhan Penjualan
with col3:
    st.markdown("<h5 style='text-align:center;'>Tren Pertumbuhan Penjualan</h5>", unsafe_allow_html=True)
    # Membuat plot dengan Plotly Express
    fig9 = px.line(orders_date.sort_values(by='month', ascending=False), x='month', y='order_id',
                   labels={'month': 'Tanggal', 'order_id': 'Total order'},
                   width=500, height=300)

    # Mengatur tampilan grafik
    fig9.update_xaxes(title_text='Tanggal', tickangle=45, tickformat="%d-%m-%Y")
    fig9.update_yaxes(title_text='Total Order')
    fig9.update_traces(line=dict(width=2))  # Mengatur ketebalan garis

    # Menampilkan plot menggunakan Streamlit
    # st.markdown(css1, unsafe_allow_html=True)
    st.plotly_chart(fig9)

# Kolom 2: Tabel Jumlah Pemesanan per Tanggal di Bulan November 2017
with col4:
    # Menggunakan CSS untuk mengatur ukuran tabel
    css = """
        <style>
        table {
            font-size: 12px;  /* Atur ukuran font */
            width: 250px;     /* Atur lebar tabel */
        }
        </style>
    """
    st.markdown("<h5 style='text-align:center;'>Jumlah Pemesanan per Tanggal di Bulan November 2017</h5>", unsafe_allow_html=True)
    st.markdown(css, unsafe_allow_html=True)
    st.table(daily_order_count.sort_values(by='Jumlah Pemesanan', ascending=False).head(5))

# 7. Persebaran Pembelian Berdasarkan Pembagian Waktu dan Hari
st.subheader('Persebaran Pembelian Berdasarkan Pembagian Waktu dan Hari')

# Definisi urutan kategori untuk hari dan waktu
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
time_order = ['Dawn', 'Morning', 'Afternoon', 'Night']

# Pembagian hari
delivery_day_df = orders_df.groupby(by='order_day').order_id.nunique().sort_values(ascending=False).reset_index()
delivery_day_df.rename(columns={'order_id': 'total_orders'}, inplace=True)

# Menggunakan pd.Categorical untuk mengatur urutan kategori
delivery_day_df['order_day'] = pd.Categorical(delivery_day_df['order_day'], categories=day_order, ordered=True)
delivery_day_df = delivery_day_df.sort_values('order_day')

most_common_day = delivery_day_df.loc[delivery_day_df['total_orders'].idxmax(), 'order_day']
# Membuat warna untuk setiap state
colors = {day: "#068DA9" if day == most_common_day else "#D3D3D3" for day in delivery_day_df['order_day']}

# Membuat plot dengan Plotly Express
fig10 = px.bar(delivery_day_df,
             x='order_day', y='total_orders', orientation='v',
             labels={'total_orders': 'Jumlah Order', 'order_day': 'Hari'},
             color='order_day',  
             color_discrete_map=colors,
             width=800, height=400)

fig10.update_layout(xaxis_tickangle=0)
fig10.update_traces(showlegend=False)


# Pembagian waktu
delivery_time_df = orders_df.groupby(by='order_datetime').order_id.nunique().reset_index()
delivery_time_df.rename(columns={'order_id': 'total_orders'}, inplace=True)

# Menggunakan pd.Categorical untuk mengatur urutan kategori
delivery_time_df['order_datetime'] = pd.Categorical(delivery_time_df['order_datetime'], categories=time_order, ordered=True)
delivery_time_df = delivery_time_df.sort_values('order_datetime')

most_common_datetime = delivery_time_df.loc[delivery_time_df['total_orders'].idxmax(), 'order_datetime']

# Membuat warna untuk setiap state
colors = {time: "#068DA9" if time == most_common_datetime else "#D3D3D3" for time in delivery_time_df['order_datetime']}

# Membuat plot dengan Plotly Express
fig11 = px.bar(delivery_time_df,
             x='order_datetime', y='total_orders', orientation='v',
             labels={'total_orders': 'Jumlah Order', 'order_datetime': 'Waktu'},
             color='order_datetime',
             color_discrete_map= colors, # Gunakan color_discrete_sequence
             width=800, height=400)

fig11.update_layout(xaxis_tickangle=0)
fig11.update_traces(showlegend=False)

# Membuat dua tab
tabs = st.tabs(['Hari', 'Waktu'])
tabs[0].plotly_chart(fig10)
tabs[1].plotly_chart(fig11)



