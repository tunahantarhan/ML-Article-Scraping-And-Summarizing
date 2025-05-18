from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv
import time
import os
import gc

baslangic_sayfa = 1
maks_sayfa = 40 # 15 x maks_sayfa = maks_yazi

yazarlar = [
    {"adi": "Altan Öymen", "url_kodu": "altan-oymen"},
    {"adi": "Mine Esen", "url_kodu": "mine-esen"},
    {"adi": "Mustafa Balbay", "url_kodu": "mustafa-balbay"},
    {"adi": "Barış Terkoğlu", "url_kodu": "baris-terkoglu"},
    {"adi": "Orhan Bursalı", "url_kodu": "orhan-bursali"},
    {"adi": "Müjdat Gezen", "url_kodu": "mujdat-gezen"},
    {"adi": "Emre Kongar", "url_kodu": "emre-kongar"},
    {"adi": "Murat Ağırel", "url_kodu": "murat-agirel"},
]

os.makedirs("veriler", exist_ok=True)

def yeni_driver_baslat():
    options = Options()
    #options.add_argument("--headless")
    service = Service("/Users/tunahantarhan/chromedriver/chromedriver")
    return webdriver.Chrome(service=service, options=options)

driver = yeni_driver_baslat()

for yazar in yazarlar:
    yazar_adi = yazar["adi"]
    yazar_url_kodu = yazar["url_kodu"]

    dosya_adi = f"veriler/{yazar_url_kodu}.csv"

    if os.path.exists(dosya_adi):
        print(f"👍 {yazar_adi} yazıları zaten mevcut.")
        continue

    print(f"⏳ {yazar_adi} için veri çekiliyor:")

    with open(dosya_adi, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Yazar", "Başlık", "Tarih", "Metin", "URL"])

        yazi_sayaci = 0

        for sayfa in range(baslangic_sayfa, maks_sayfa + 1):
            if sayfa == 1:
                url = f"https://www.cumhuriyet.com.tr/yazarlar/{yazar_url_kodu}"
            else:
                url = f"https://www.cumhuriyet.com.tr/yazarlar/{yazar_url_kodu}/{sayfa}"

            print(f"📃 Sayfa {sayfa} kontrol ediliyor: {url}")

            try:
                driver.get(url)
                time.sleep(2)

                liste = driver.find_elements(By.CSS_SELECTOR, "ul.yazilar li a")
                yazi_linkleri = set([a.get_attribute("href") for a in liste if a.get_attribute("href")])

                print(f"🔗 {len(yazi_linkleri)} yazı bulundu.")

                for yazi_url in yazi_linkleri:
                    try:
                        driver.get(yazi_url)
                        time.sleep(1.5)

                        baslik = driver.find_element(By.CSS_SELECTOR, "h1.baslik").text.strip().replace("...", "")

                        try:
                            tarih = driver.find_element(By.CLASS_NAME, "yayin-tarihi").text.strip()
                        except Exception as e:
                            print(f"❌ Tarih hatası: ({yazi_url}): {e}")
                            continue

                        metin_paragraflar = driver.find_elements(By.CSS_SELECTOR, "div.haberMetni p")
                        metin = " ".join([p.text.strip() for p in metin_paragraflar if p.text.strip()])
                        metin = metin.replace("\n", " ").replace("\r", " ").strip()


                        writer.writerow([yazar_adi, baslik, tarih, metin, yazi_url])
                        yazi_sayaci += 1
                        print(f"✅ {yazi_sayaci} | {tarih} - {baslik}")

                        if yazi_sayaci % 100 == 0:
                            print("-*- Tarayıcı Yenileniyor -*-")
                            driver.quit()
                            gc.collect()
                            time.sleep(3)
                            driver = yeni_driver_baslat()

                    except Exception as e:
                        print(f"❌ Yazı içeriği alınamadı: {e}")
                        continue

            except Exception as e:
                print(f"❌ Sayfa yüklenemedi veya mevcut değil ({url}): {e}")
                continue

driver.quit()
gc.collect()

print("--*  TÜM VERİLER BAŞARIYLA ÇEKİLDİ.  *--")
