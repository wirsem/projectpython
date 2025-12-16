import pandas as pd
import datetime
import matplotlib.pyplot as plt

dataset = pd.read_csv('https://storage.googleapis.com/dqlab-dataset/retail_raw_reduced.csv')
dataset['order_month'] = dataset['order_date'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").strftime('%Y-%m'))
dataset['gmv'] = dataset['item_price']*dataset['quantity']
# Buat variabel untuk 5 propinsi dengan GMV tertinggi
top_provinces = (dataset.groupby('province')['gmv']
                        .sum()
                        .reset_index()
                        .sort_values(by='gmv',ascending=False)
                        .head(5))

# Buat satu kolom lagi di dataset dengan nama province_top
dataset['province_top'] = dataset['province'].apply(lambda x: x if(x in top_provinces['province'].to_list())else 'other')

# ===== FIGURE & SUBPLOTS =====
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(14, 28))

# ===== GRAFIK 1: SEMUA PROVINSI =====
dataset.groupby(['order_month', 'province'])['gmv'].sum().unstack().plot(marker='.', cmap='plasma', ax=ax1)

ax1.set_title(
    'Monthly GMV Year 2019 - Breakdown by Province',
    loc='center',
    pad=30,
    fontsize=20,
    color='blue'
)

ax1.set_xlabel('Order Month', fontsize=15)
ax1.set_ylabel('Total Amount (in Billions)', fontsize=15)
ax1.grid(color='darkgray', linestyle=':', linewidth=0.5)
ax1.set_ylim(bottom=0)

labels = ax1.get_yticks()
ax1.set_yticks(labels)
ax1.set_yticklabels((labels / 1000000000).astype(int))

ax1.legend(
    loc='center left', # Titik jangkar legend adalah sisi kirinya
    bbox_to_anchor=(1, 0.5), # Posisikan titik jangkar di x=1 (paling kanan) dan y=0.5 (tengah)
    shadow=True,
    ncol=1, # Ubah menjadi 1 kolom agar lebih mudah dibaca di samping
    title='Province',
    fontsize=9,
    title_fontsize=11
)
# ===== GRAFIK 2: TOP 5 + OTHER =====
# Plot multi-line chartnya
dataset.groupby(['order_month','province_top'])['gmv'].sum().unstack().plot(marker='.', cmap='plasma',ax=ax2)
ax2.set_title('Monthly GMV Year 2019 - Breakdown by Top Province', loc='center', pad=30, fontsize=20, color='blue')
ax2.set_xlabel('Order Month', fontsize=15)
ax2.set_ylabel('Total Amount (in Billions)', fontsize=15)
ax2.grid(color='darkgray', linestyle=':', linewidth=0.5)
ax2.set_ylim(bottom=0)

labels = ax2.get_yticks()
ax2.set_yticks(labels)
ax2.set_yticklabels((labels/1000000000).astype(int))

ax2.legend(
    loc='center left', # Titik jangkar legend adalah sisi kirinya
    bbox_to_anchor=(1, 0.5), # Posisikan titik jangkar di x=1 (paling kanan) dan y=0.5 (tengah)
    shadow=True,
    ncol=1)
# Anotasi pertama
ax2.annotate('GMV other meningkat pesat', 
			xy=(5,900000000),
			xytext=(3, 1700000000),
			weight='bold',
			color='red',
			arrowprops=dict(arrowstyle='fancy',
                    connectionstyle='arc3',
					color='red'))
# Anotasi kedua
ax2.annotate('DKI Jakarta mendominasi',
			xy=(3,3300000000),
			xytext=(0,3700000000),
            weight='bold',
			color='red',
			arrowprops=dict(arrowstyle='->',
						    connectionstyle='angle',
						    color='red'))

# ===== PIE CHART =====
dataset_dki_q4 = dataset[(dataset['province']=='DKI Jakarta') & (dataset['order_month'] >= '2019-10')]
gmv_per_city_dki_q4 = dataset_dki_q4.groupby('city')['gmv'].sum().reset_index()

ax3.pie(gmv_per_city_dki_q4['gmv'],
	   labels = gmv_per_city_dki_q4['city'], autopct='%1.1f%%',startangle=90)
ax3.set_title('GMV Contribution Per City - DKI Jakarta in Q4 2019',
		pad = 30,
		fontsize = 15,
		color =  'blue')

# ===== BAR CHART =====
dataset_dki_q4.groupby('city')['gmv'].sum().sort_values(ascending=False).plot(kind='bar', color='green', ax=ax4)
ax4.set_title(
    'GMV Per City - DKI Jakarta in Q4 2019',
    loc='center',
    pad=30,
    fontsize=15,
    color='blue'
)
ax4.set_xlabel('City', fontsize=15)
ax4.set_ylabel('Total Amount (in Billions)', fontsize=15)
ax4.set_ylim(bottom=0)

labels = ax4.get_yticks()
ax4.set_yticks(labels)
ax4.set_yticklabels((labels / 1e9).astype(int))

ax4.tick_params(axis='x', rotation=0)
ax4.grid(axis='y', linestyle=':', alpha=0.7)

# ===== Multi-Bar Chart =====
dataset_dki_q4.groupby(['city', 'order_month'])['gmv'].sum().unstack().plot(kind='bar',ax=ax5)

ax5.set_title(
    'GMV Per City, Breakdown by Month\nDKI Jakarta in Q4 2019',
    loc='center',
    pad=30,
    fontsize=15,
    color='blue'
)

ax5.set_xlabel('City', fontsize=12)
ax5.set_ylabel('Total Amount (in Billions)', fontsize=12)
ax5.set_ylim(bottom=0)

labels = ax5.get_yticks()
ax5.set_yticks(labels)
ax5.set_yticklabels((labels / 1e9).astype(int))

ax5.legend(
    bbox_to_anchor=(1, 1),
    shadow=True,
    title='Month'
)

ax5.tick_params(axis='x', rotation=45)
ax5.grid(axis='y', linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()

