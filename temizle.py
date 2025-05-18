import os
import csv
import re #regex
import html

girdi_klasoru = "veriler"
cikti_klasoru = "veriler_temiz"
os.makedirs(cikti_klasoru, exist_ok=True)

semboller = [
    "★", "●", "♦", "▪", "■", "☑", "✍", "✅", "❌", "📅", "🔗", "🔥", "📰",
    "👉", "👇", "📌", "📍", "🔍", "📢", "📣", "🚨", "💥", "❗", "‼",
    "–", "—", "…", "...", "*"
]

stopwords = set()
with open("turkce-stop-words.txt", "r", encoding="utf-8") as f:
    for line in f:
        kelime = line.strip().lower()
        if kelime:
            stopwords.add(kelime)

def temizle_metin(metin):
    for sembol in semboller:
        metin = metin.replace(sembol, " ")
        
    metin = html.unescape(metin)
    metin = re.sub(r"[\u200b\xa0]", " ", metin)
    metin = re.sub(r"\s+", " ", metin)
    metin = metin.replace("“", "").replace("”", "").replace("‘", "").replace("’", "")
    metin = metin.replace("..", ".").replace(" ,", ",")
    metin = metin.replace("\n", " ").replace("\r", " ")
    metin = metin.lower()
    metin = re.sub(r"[^\w\s]", " ", metin)
    kelimeler = metin.split()
    kelimeler = [k for k in kelimeler if k not in stopwords]
    return " ".join(kelimeler)

for dosya in os.listdir(girdi_klasoru):
    if not dosya.endswith(".csv"):
        continue

    girdi_yolu = os.path.join(girdi_klasoru, dosya)
    cikti_yolu = os.path.join(cikti_klasoru, dosya)

    print(f"⏳ Temizleniyor: {dosya}")

    with open(girdi_yolu, "r", encoding="utf-8-sig") as infile, \
         open(cikti_yolu, "w", newline="", encoding="utf-8-sig") as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        next(reader)
        writer.writerow(["Başlık", "Metin"])

        for satir in reader:
            if len(satir) < 5:
                continue

            baslik = temizle_metin(satir[1])
            metin = temizle_metin(satir[3])

            if baslik and metin:
                writer.writerow([baslik, metin])

    print(f"✅ Kaydedildi: {cikti_yolu}")

print("\nTüm veriler temizlendi.")