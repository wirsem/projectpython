import datetime
import pandas as pd
import matplotlib.pyplot as plt
dataset = pd.read_csv('https://storage.googleapis.com/dqlab-dataset/retail_raw_reduced.csv')
dataset['order_month'] = dataset['order_date'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").strftime('%Y-%m'))
dataset['gmv'] = dataset['item_price']*dataset['quantity']

#mengambil informasi top 5 brands berdasarkan quantity

top_brands = (dataset[dataset['order_month']=='2019-12'].groupby('brand')['quantity'].sum().reset_index().sort_values(by='quantity', ascending=False).head(5))

#membuat dataframe baru, filter hanya di bulan Desember 2019 dan hanya top 5 brands
dataset_top5brand_dec = dataset[(dataset['order_month']=='2019-12') & (dataset['brand'].isin(top_brands['brand'].to_list()))]

dataset_top5brand_dec.groupby(['order_date', 'brand'])['quantity'].sum().unstack().plot(marker='.', cmap ='plasma')
plt.title('Daily Sold Quantity Dec 2019 - Breakdown by Brands',loc='center', pad= 30, fontsize=15, color='blue')
plt.xlabel('Order Date',fontsize=12)
plt.ylabel('Quantity',fontsize=12)
plt.grid(color='darkgray', linestyle=':', linewidth=0.5)
plt.ylim(ymin=0)
plt.legend(loc='upper center', bbox_to_anchor=(1.1,1), shadow=True, ncol=1)
plt.annotate('Terjadi lonjakan',
            xy=(7,310),
            xytext=(8,300),
            weight='bold',
            color='red',
            arrowprops=dict(arrowstyle='->', 
                            connectionstyle='arc3',
                            color='red'))
plt.gcf().set_size_inches(10,5)
plt.tight_layout()
plt.show()

# Cari tahu jumlah product untuk masing-masing brand yang laku selama bulan Desember 2019. 
# Gunakan barchart untuk visualisasinya, urutkan dengan yang kiri adalah brand dengan product lebih banyak.

plt.clf()
dataset_top5brand_dec.groupby('brand')['product_id'].nunique().sort_values(ascending=False).plot(kind='bar', color='green')
plt.title('Number of Sold Products per Brand, December 2019', loc='center', pad=30, fontsize=15, color='blue')
plt.xlabel('Brand', fontsize=15)
plt.ylabel('Number of Products', fontsize=15)
plt.ylim(ymin=0)
plt.xticks(rotation=0)
plt.show()

#Gunakan stacked chart, untuk breakdown barchart yang di Case 3, antara product yang terjual >= 100 dan < 100 di bulan Desember 2019. Apakah ada pola yang menarik?
# Case 3: Cari tahu jumlah product untuk masing-masing brand yang laku selama bulan Desember 2019. Gunakan barchart untuk visualisasinya, urutkan dengan yang kiri adalah brand dengan product lebih banyak.

#membuat dataframe baru, untuk agregat jumlah quantity terjual per product
dataset_top5brand_dec_per_product = dataset_top5brand_dec.groupby(['brand','product_id'])['quantity'].sum().reset_index()

#beri kolom baru untuk menandai product yang terjual >= 100 dan <100
dataset_top5brand_dec_per_product['quantity_group']= dataset_top5brand_dec_per_product['quantity'].apply(lambda x: '>=100' if x>=100 else '<100')
dataset_top5brand_dec_per_product.sort_values('quantity', ascending=False,inplace=True)

#membuat referensi pengurutan brand berdasarkan banyaknya semua product
s_sort = dataset_top5brand_dec_per_product.groupby('brand')['product_id'].nunique().sort_values(ascending=False)

#plot stacked barchart
dataset_top5brand_dec_per_product.groupby(['brand','quantity_group'])['product_id'].nunique().reindex(index = s_sort.index, level='brand').unstack().plot(kind='bar', stacked=True)
plt.title('Number of Sold Products per Brand, December 2019', loc='center', pad=30, fontsize=15, color='blue')
plt.xlabel('Brand', fontsize=15)
plt.ylabel('Number of Products', fontsize=15)
plt.ylim(ymin=0)
plt.xticks(rotation=0)
plt.show()

#Gunakan histogram untuk melihat distribusi harga product-product yang ada di top 5 brand tersebut (untuk tiap product_id, ambil median harganya). 
# Bagaimana persebaran harga product-nya? Cenderung banyak yang murah atau yang mahal?

plt.figure(figsize=(10,5))
plt.hist(dataset_top5brand_dec.groupby('product_id')['item_price'].median(), bins=10, stacked= False,range=(1,2000000), color='green')
plt.title('Distribution of Price Median per Product\nTop 5 Brands in Dec 2019',fontsize=15, color='blue')
plt.xlabel('Price Median', fontsize=12)
plt.ylabel('Number of Products', fontsize=12)
plt.xlim(xmin=0, xmax=2000000)
plt.tight_layout()
plt.show()

# Untuk setiap product_id, cek scatterplot antara quantity dan GMV, apakah ada korelasi? 

data_per_product_top5brand_dec = dataset_top5brand_dec.groupby('product_id').agg({'quantity':'sum', 'gmv':'sum', 'item_price':'median'}).reset_index()

plt.figure(figsize=(10,8))
plt.scatter(data_per_product_top5brand_dec['quantity'], data_per_product_top5brand_dec['gmv'], marker='+' ,color='red')
plt.title('Correlation of Quantity and GMV per Product\nTop 5 Brands in December 2019', fontsize=15, color='blue')
plt.xlabel('Quantity', fontsize=12)
plt.ylabel('GMV (in Millions)', fontsize=12)
plt.xlim(xmin=0, xmax=300)
plt.ylim(ymin=0, ymax=200000000)
labels, locations = plt.yticks()
plt.yticks(labels,(labels/1000000).astype(int))
plt.show()
# Bagaimana dengan median harga vs quantity? Apakah product yang murah cenderung dibeli lebih banyak?
plt.figure(figsize=(10,8))
plt.scatter(data_per_product_top5brand_dec['item_price'], data_per_product_top5brand_dec['quantity'], marker='o' ,color='green')
plt.title('Correlation of Price and Quantity per Product\nTop 5 Brands in December 2019', fontsize=15, color='blue')
plt.xlabel('Price Median', fontsize=12)
plt.ylabel('Quantity', fontsize=12)
plt.xlim(xmin=0, xmax=2000000)
plt.ylim(ymin=0, ymax=250)
plt.show()