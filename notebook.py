#!/usr/bin/env python
# coding: utf-8

# # Proyek Analisis Data: Nama dataset
# - Nama: Muhammad Riszky Wibowo
# - Email: bowolime@gmail.com
# - Id Dicoding:riszky18

# ## Menentukan Pertanyaan Bisnis

# - 5 Kota dengan penjualan terbanyak?
# - Produk apa yang paling banyak peminatnya di kota Sao Paulo?
# - 

# ## Menyaipkan semua library yang dibuthkan

# In[43]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# ## Data Wrangling

# ### Gathering Data

# In[44]:


customer_df = pd.read_csv("customers_dataset.csv")


# In[45]:


data_order_df = pd.read_csv("orders_dataset.csv")


# In[46]:


order_item_df = pd.read_csv("order_items_dataset.csv")


# In[47]:


product_df = pd.read_csv("products_dataset.csv")


# In[48]:


rating_product = pd.read_csv("order_reviews_dataset.csv")


# In[49]:


data_customer_df = pd.merge(
    left=customer_df,
    right=data_order_df,
    how="inner",
    left_on="customer_id",
    right_on="customer_id"
)


# In[50]:


data_product_customer = pd.merge(
    left=data_customer_df,
    right=order_item_df,
    how="inner",
    left_on="order_id",
    right_on="order_id"
)


# In[51]:


all_data = pd.merge(
    left=data_product_customer,
    right=product_df,
    how="inner",
    left_on="product_id",
    right_on="product_id"
)


# ### Assessing Data

# 

# In[52]:


all_data.isnull().sum()


# In[ ]:


#melakukan pengecekan terhadap duplikasi data
print("Jumlah duplikasi: ",all_data.duplicated().sum())


# In[53]:


#membersihkan data
all_data.drop_duplicates(inplace=True)


# In[54]:


#melakukan pengecekan terhadap duplikasi data
print("Jumlah duplikasi: ",all_data.duplicated().sum())


# In[56]:


all_data.info()


# In[57]:


all_data.describe(include="all")


# In[58]:


print(all_data.isna().sum())


# ### Cleaning Data

# In[59]:


#menghilangakan data missing value
all_data.fillna(value="NaN", inplace=True)


# In[61]:


#mengubah tyoe data dari object menjadi date time
datetime_columns = ["order_purchase_timestamp", "order_approved_at","order_delivered_carrier_date","order_delivered_customer_date","order_estimated_delivery_date"]
 
for column in datetime_columns:
  all_data[column] = pd.to_datetime(all_data[column])


# In[62]:


#Melakukan pengecekan missing value pada data
print(all_data.isna().sum())


# 

# In[63]:


#Menghilangkan missing value menggunakan metode fillna
all_data.fillna(value="/n", inplace=True)


# In[64]:


#mengecek kemungkinan masih adanya missing value
print(all_data.isna().sum())


# ## Exploratory Data Analysis (EDA)

# ### Explore ...

# In[65]:


#Memembuat table order id dan sales
all_data.groupby(by="product_category_name").agg({
    "order_id": "nunique",
    "price": "mean"
})


# In[66]:


print(all_data['product_category_name'].unique())


# In[67]:


all_data.groupby(by=["customer_city", "product_category_name"]).agg({
    "price": "sum"
})


# In[68]:


all_data.groupby(by="product_category_name").agg({
    "order_id": "nunique",
    "price": "sum"
})


# In[69]:


city_sales = all_data.groupby('customer_city')['price'].sum()

top_cities = city_sales.nlargest(5)
top_cities.head()

print(top_cities)


# In[70]:


# Membuat codingan untuk menampilkan 5 kota yang memiliki sales terbanyak
selected_cities = ['sao paulo', 'rio de janeiro', 'belo horizonte', 'brasilia', 'curitiba']
filtered_data = all_data[all_data['customer_city'].isin(selected_cities)]
total_prices = filtered_data.groupby('customer_city')['price'].sum().reset_index()

# Menampilkan hasil
print(total_prices)


# In[71]:


top_products = filtered_data.groupby('product_category_name').size().reset_index(name='total_sold')

# Mengurutkan berdasarkan total terjual secara descending
top_products = top_products.sort_values(by='total_sold', ascending=False)

# Mengambil top 5 produk
top5_products = top_products.head(5)

# Menampilkan hasil
print(top5_products)


# In[72]:


sao_paulo_data = filtered_data[filtered_data['customer_city'] == 'sao paulo']

# Hitung total penjualan untuk setiap kategori produk di São Paulo
category_sales = sao_paulo_data.groupby('product_category_name')['price'].sum()

# Pilih 5 kategori teratas
top_categories = category_sales.nlargest(5)

# Tampilkan hasilnya
print("Top 5 Kategori Produk yang Terjual di São Paulo:")
print(top_categories)


# In[ ]:





# ## Visualization & Explanatory Analysis

# ### Pertanyaan 1: 5 kota yang memiliki penjualan terbaik di mana saja

# In[73]:


plt.figure(figsize=(10, 6))
top_cities.plot(kind='bar', color='red')
plt.title('Top 5 Cities by Sales')
plt.xlabel('City')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.show()


# ### Pertanyaan 2: apa saja product yang paling banyak terjual di kota yang memiliki penjualan terbanyak

# In[74]:


sao_paulo_data = filtered_data[filtered_data['customer_city'] == 'sao paulo']

# Hitung total penjualan untuk setiap kategori produk di Sao Paulo
category_sales = sao_paulo_data.groupby('product_category_name')['price'].sum()

# Pilih 5 kategori teratas
top_categories = category_sales.nlargest(5)


# In[75]:




# Menampilkan hasil dari 5 kategori produk teratas di Sao Paulo
print("Top 5 Kategori Produk yang Terjual di Sao Paulo:")
print(top_categories)

# Tampilkan grafik bar horizontal
plt.barh(y=top_categories.index, width=top_categories.values)
plt.xlabel("Total Harga")
plt.title("Top 5 Kategori Produk Terjual di Sao Paulo")
plt.show()


# In[76]:


bottom_products = sao_paulo_data.sort_values(by='price').head(5)


# In[ ]:





# ## Conclusion

# In[ ]:





# - Conclution pertanyaan 1 : 5 kota dengan penjualan terbaik kota "Sao Paulo", "Rio De Jeneiro", "Belo Horizonte", "Brasilia", dan "Curitiba"
# - conclution pertanyaan 2 : Produk dengan 5 Penjualan terbaik di kota Sau Paulo adalah : "Beleza Saude", "Cama Mesa Banho", "Relogios_presentes", "Informatica_acessorios", "esporte_ezer"

# STREAMLIT 
# 

# In[77]:


st.title('Muhammad Riszky Wibowo')
col1, col2= st.columns(2)
 
with col1:
    st.header("5 Kategori Sales Terbanyak di Kota Sao Paulo")
    st.bar_chart(top_categories)
 
with col2:
    st.header("5 Kota dengan Sales Terbanyak")
    st.bar_chart(top_cities)


# In[ ]:




