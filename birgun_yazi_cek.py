from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv
import time
import os
import gc

baslangic_sayfa = 1
maks_sayfa = 50  # 20 x maks_sayfa = maks_yazi

yazarlar = [
    {"adi": "Aziz Çelik", "url_kodu": "aziz-celik-257"},
    {"adi": "Selçuk Candansayar", "url_kodu": "selcuk-candansayar-219"},
    {"adi": "Faruk Bildirici", "url_kodu": "medya-ombudsmani-faruk-bildirici-372"},
    {"adi": "Metin Özuğurlu", "url_kodu": "metin-ozugurlu-135"},
    {"adi": "Yakup Kepenek", "url_kodu": "yakup-kepenek-348"},
    {"adi": "Gözde Bedeloğlu", "url_kodu": "gozde-bedeloglu-223"},
    {"adi": "Selin Nakipoğlu", "url_kodu": "selin-nakipoglu-363"},
    {"adi": "Zeynep Altıok Akatlı", "url_kodu": "zeynep-altiok-akatli-366"},
    {"adi": "Fikri Sağlar", "url_kodu": "fikri-saglar-232"},
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

    dosya_adi = f"veriler/{yazar_url_kodu[:-4]}.csv"

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
                url = f"https://www.birgun.net/profil/{yazar_url_kodu}"
            else:
                url = f"https://www.birgun.net/profil/{yazar_url_kodu}?p={sayfa}"

            print(f"📃 Sayfa {sayfa} kontrol ediliyor: {url}")

            try:
                driver.get(url)
                time.sleep(2)

                link_elements = driver.find_elements(By.CSS_SELECTOR, "h2.card-title a")
                yazi_linkleri = set([a.get_attribute("href") for a in link_elements if a.get_attribute("href")])

                print(f"🔗 {len(yazi_linkleri)} yazı bulundu.")

                for yazi_url in yazi_linkleri:
                    try:
                        driver.get(yazi_url)
                        time.sleep(1.5)

                        baslik = driver.find_element(By.CSS_SELECTOR, "div.page-header h1").text.strip()

                        try:
                            tarih = driver.find_element(By.CSS_SELECTOR, "li.nav-item.no-line").text.strip()
                        except:
                            tarih = ""

                        try:
                            yazar_adi_yazidan = driver.find_element(By.CSS_SELECTOR, "h4.m-0 a").text.strip()
                        except:
                            yazar_adi_yazidan = yazar_adi

                        paragraflar = driver.find_elements(By.CSS_SELECTOR, "div.resize p")
                        metin = " ".join([p.text.strip() for p in paragraflar if p.text.strip()])
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
                print(f"❌ Sayfa yüklenemedi veya mevcut değil ({url}): {e}")
                continue

driver.quit()
gc.collect()
print("--* TÜM BİRGÜN VERİLERİ BAŞARIYLA ÇEKİLDİ. *--")
