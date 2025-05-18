import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

#8233 yazı, 5 gazete, 27 yazar

TEMIZ_KLASOR = "veriler_temiz"
CIKTI_KLASOR = "grafikler"
os.makedirs(CIKTI_KLASOR, exist_ok=True)

tum_kelimeler = []
yazar_metin_uzunluklari = {}

for dosya in os.listdir(TEMIZ_KLASOR):
    if not dosya.endswith(".csv"):
        continue

    dosya_yolu = os.path.join(TEMIZ_KLASOR, dosya)
    df = pd.read_csv(dosya_yolu)

    yazar_adi = dosya.replace(".csv", "").replace("_", " ").title()

    kelime_sayilari = []

    for _, satir in df.iterrows():
        metin = str(satir["Metin"])
        baslik = str(satir["Başlık"])
        kelimeler = metin.split() + baslik.split()
        tum_kelimeler.extend(kelimeler)
        kelime_sayilari.append(len(kelimeler))

    if kelime_sayilari:
        yazar_metin_uzunluklari[yazar_adi] = sum(kelime_sayilari) / len(kelime_sayilari)

kelime_sayaci = Counter(tum_kelimeler)
en_sik_10 = kelime_sayaci.most_common(10)
kelimeler, frekanslar = zip(*en_sik_10)

# top 10 kelime - bar chart
plt.figure(figsize=(10, 6))
plt.bar(kelimeler, frekanslar, color="skyblue")
plt.title("En Sık Geçen 10 Kelime (Sütun Grafiği)")
plt.ylabel("Frekans")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(CIKTI_KLASOR, "top_10_kelime_sutun.png"))
plt.close()

# top 10 kelime - pie chart
plt.figure(figsize=(8, 8))
plt.pie(frekanslar, labels=kelimeler, autopct="%1.1f%%", startangle=140)
plt.title("En Sık Geçen 10 Kelime (Pasta Grafiği)")
plt.tight_layout()
plt.savefig(os.path.join(CIKTI_KLASOR, "top_10_kelime_pasta.png"))
plt.close()

# yazar başına yazı uzunluğu
if yazar_metin_uzunluklari:
    plt.figure(figsize=(10, 6))
    plt.bar(yazar_metin_uzunluklari.keys(), yazar_metin_uzunluklari.values(), color="coral")
    plt.ylabel("Ortalama Kelime Sayısı")
    plt.title("Yazar Başına Ortalama Metin Uzunluğu")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(CIKTI_KLASOR, "yazar_metin_uzunlugu.png"))
    plt.close()

# kelime bulutu
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(tum_kelimeler))
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout()
plt.savefig(os.path.join(CIKTI_KLASOR, "kelime_bulutu.png"))
plt.close()

print("Grafikler oluşturuldu. (/grafikler/...)")