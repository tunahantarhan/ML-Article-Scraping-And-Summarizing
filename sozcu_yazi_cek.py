from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv
import time
import os
import gc

baslangic_yili = 2023 # ocak {baslangic_yili}
bitis_yili = 2024 # aralık {bitis_yili}

yazarlar = [
    {"adi": "Uğur Dündar", "url_kodu": "ugur-dundar-a27"},
    {"adi": "Rahmi Turan", "url_kodu": "rahmi-turan-a28"},
    {"adi": "Sultan Uçar", "url_kodu": "sultan-ucar-a41"},
    {"adi": "Emin Çölaşan", "url_kodu": "emin-colasan-a26"},
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

    dosya_adi = f"veriler/{yazar_url_kodu[:-4]}.csv"
    
    if os.path.exists(dosya_adi):
        print(f"👍 {yazar_adi} yazıları zaten mevcut.")
        continue

    print(f"⏳ {yazar_adi} için veri çekiliyor:")

    with open(dosya_adi, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Yazar", "Başlık", "Tarih", "Metin", "URL"])

        yazi_sayaci = 0  

        for yil in range(baslangic_yili, bitis_yili + 1):
            for ay in range(1, 13):
                url = f"https://www.sozcu.com.tr/{yazar_url_kodu}?SelectedMonth={ay}&SelectedYear={yil}"
                print(f"📅 {yil}-{ay} kontrol ediliyor...")

                try:
                    driver.get(url)
                    time.sleep(2)
                    linkler = driver.find_elements(By.CLASS_NAME, "list-group-item")

                    yazi_linkleri = set()
                    for link in linkler:
                        href = link.get_attribute("href")
                        if href and ("-p" in href or "-wp" in href):
                            yazi_linkleri.add(href)

                    print(f"🔗 {len(yazi_linkleri)} yazı bulundu.")

                    for yazi_url in yazi_linkleri:
                        try:
                            driver.get(yazi_url)
                            time.sleep(1.5)

                            baslik = driver.find_element(By.CLASS_NAME, "author-content-title").text.strip()

                            try:
                                tarih = driver.find_element(By.CSS_SELECTOR, "time").text.replace("Yayınlanma: ", "").strip()
                            except Exception as e:
                                print(f"❌ Tarih hatası: ({yazi_url}): {e}")
                                continue

                            metin = driver.find_element(By.CLASS_NAME, "article-body").text.strip()
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
                            print(f"❌ İçerik hatası: {e}")
                            continue

                except Exception as e:
                    print(f"❌ Ay sayfası yüklenemedi ({url}): {e}")
                    continue

driver.quit()
gc.collect()

print("--*  TÜM VERİLER BAŞARIYLA ÇEKİLDİ.  *--")