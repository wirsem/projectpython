#Library yang perlu diimport adalah: (1) pandas, (2) numpy, (3) io, dan (4) pandas_profiling. Untuk dua libray yang pertama importlah sebagai aliasnya.
import pandas as pd
import numpy as np
import io
from ydata_profiling import ProfileReport
retail_raw = pd.read_csv('https://storage.googleapis.com/dqlab-dataset/retail_raw_reduced_data_quality.csv')

# Cetak tipe data di setiap kolom retail_raw
print(retail_raw.dtypes)

# Kolom city
length_city = len (retail_raw['city'])
print('\nLength kolom city:', length_city)

# Tugas Praktek: Kolom product_id
length_product_id = len(retail_raw['product_id'])
print('\nLength kolom product_id:', length_product_id)

# Count kolom city
count_city = retail_raw['city'].count()
print('\nCount kolom count_city:', count_city)

# Tugas praktek: count kolom product_id
count_product_id = retail_raw['product_id'].count()
print('\nCount kolom product_id:', count_product_id)

# Missing value pada kolom city
number_of_missing_values_city = length_city - count_city
ratio_of_missing_values_city = number_of_missing_values_city/length_city
pct_of_missing_values_city = '{0:.1f}%'.format(ratio_of_missing_values_city * 100)
print('\nPersentase missing value kolom city:', pct_of_missing_values_city)

# Tugas praktek: Missing value pada kolom product_id
number_of_missing_values_product_id = length_product_id - count_product_id
ratio_of_missing_values_product_id = number_of_missing_values_product_id/length_product_id
pct_of_missing_values_product_id = '{0:.1f}%'.format(ratio_of_missing_values_product_id * 100)
print('\nPersentase missing value kolom product_id:', pct_of_missing_values_product_id)

# Deskriptif statistics kolom quantity
print('\nKolom quantity')
print('Minimum value: ', retail_raw['quantity'].min())
print('Maximum value: ', retail_raw['quantity'].max())
print('Mean value: ', retail_raw['quantity'].mean())
print('Mode value: ', retail_raw['quantity'].mode())
print('Median value: ', retail_raw['quantity'].median())
print('Standard Deviation value: ', retail_raw['quantity'].std())

# Tugas praktek: Deskriptif statistics kolom item_price
print('')
print('Kolom item_price')
print('Minimum value: ', retail_raw['item_price'].min())
print('Maximum value: ', retail_raw['item_price'].max())
print('Mean value: ', retail_raw['item_price'].mean())
print('Median value: ', retail_raw['item_price'].median())
print('Standard Deviation value: ', retail_raw['item_price'].std())

# Quantile statistics kolom quantity
print('\nKolom quantity:')
print(retail_raw['quantity'].quantile([0.25, 0.5, 0.75]))

# Tugas praktek: Quantile statistics kolom item_price
print('')
print('Kolom item_price:')
print(retail_raw['item_price'].quantile([0.25, 0.5, 0.75]))

print('\nKorelasi quantity dengan item_price')
print(retail_raw[['quantity', 'item_price']].corr())

#Profiling dengan ProfileReport
# profile = ProfileReport(retail_raw)
# profile.to_file("profiling_report.html")

# Check kolom yang memiliki missing data
print('Check kolom yang memiliki missing data:')
print(retail_raw.isnull().any())

# Filling the missing value (imputasi)
print('\nFilling the missing value (imputasi):')
print(retail_raw['quantity'].fillna(retail_raw.quantity.mean()))

# Drop missing value
print('\nDrop missing value:')
print(retail_raw['quantity'].dropna())

# Q1, Q3, dan IQR
Q1 = retail_raw['quantity'].quantile(0.25)
Q3 = retail_raw['quantity'].quantile(0.75)
IQR = Q3 - Q1

# Check ukuran (baris dan kolom) sebelum data yang outliers dibuang
print('Shape awal: ', retail_raw.shape)

# Removing outliers
retail_raw = retail_raw[~((retail_raw['quantity'] < (Q1 - 1.5 * IQR)) | (retail_raw['quantity'] > (Q3 + 1.5 * IQR)))]

# Check ukuran (baris dan kolom) setelah data yang outliers dibuang
print('Shape akhir: ', retail_raw.shape)