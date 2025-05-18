from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv
import time
import os
import gc

baslangic_sayfa = 1
maks_sayfa = 125 # 8 x maks_sayfa = yazi_sayisi

yazarlar = [
    {"adi": "Ahmet Hakan", "url_kodu": "ahmet-hakan"},
    {"adi": "Sıtkı Şükürer", "url_kodu": "sitki-sukurer"},
    {"adi": "Fuat Bol", "url_kodu": "fuat-bol"},
    {"adi": "Hande Fırat", "url_kodu": "hande-firat"},
    {"adi": "Yalçın Bayer", "url_kodu": "yalcin-bayer"},
]

os.makedirs("veriler", exist_ok=True)

def yeni_driver_baslat():
    options = Options()
    options.add_argument("--headless")
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
            url = f"https://www.hurriyet.com.tr/yazarlar/{yazar_url_kodu}/?p={sayfa}"
            print(f"📃 Sayfa {sayfa} kontrol ediliyor: {url}")

            try:
                driver.get(url)
                time.sleep(2)

                divler = driver.find_elements(By.CSS_SELECTOR, "div.highlighted-box.mb20")
                yazi_linkleri = set()

                for div in divler:
                    relative_link = div.get_attribute("data-article-link")
                    if relative_link:
                        full_link = "https://www.hurriyet.com.tr" + relative_link
                    yazi_linkleri.add(full_link)    

                print(f"🔗 {len(yazi_linkleri)} yazı bulundu.")

                for yazi_url in yazi_linkleri:
                    try:
                        driver.get(yazi_url)
                        time.sleep(1.5)

                        baslik = driver.find_element(By.CLASS_NAME, "news-detail-title").text.strip()
                        tarih = driver.find_element(By.CSS_SELECTOR, "div.author-inf time").text.strip()
                        yazar_adi_yazidan = driver.find_element(By.CLASS_NAME, "author-detail-title").text.strip()

                        paragraflar = driver.find_elements(By.CSS_SELECTOR, "div.author-content.readingTime p")
                        metin = " ".join([p.text.strip() for p in paragraflar if p.text.strip() and p.text.strip() != "*"])
                        metin = metin.replace("\n", " ").replace("\r", " ").strip()


                        writer.writerow([yazar_adi_yazidan, baslik, tarih, metin, yazi_url])
                        yazi_sayaci += 1
                        print(f"✅ {yazi_sayaci} | {tarih} - {baslik}")

                        if yazi_sayaci % 100 == 0:
                            print("-*- Tarayıcı Yenileniyor -*-")
                            driver.quit()
                            gc.collect()
                            time.sleep(3)
                            driver = yeni_driver_baslat()

                    except Exception as e:
                        print(f"❌ Yazı alınamadı: {e}")
                        continue

            except Exception as e:
                print(f"❌ Sayfa yüklenemedi: {e}")
                continue

driver.quit()
gc.collect()
print("--* TÜM HÜRRİYET VERİLERİ BAŞARIYLA ÇEKİLDİ. *--")
