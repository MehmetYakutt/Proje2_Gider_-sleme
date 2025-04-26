import pandas as pd
import sqlite3
import logging
import sys # Hata durumunda çıkış yapmak için

# Loglama yapılandırması (önceki script'indeki gibi)
logging.basicConfig(
    filename='gider_islemleri.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Gider işleme script'i başlatıldı.")

CSV_DOSYASI = 'giderler.csv'
DB_DOSYASI = 'ilk_veritabanim.db' # Önceki veritabanı dosyasını kullanabiliriz
TABLO_ADI = 'gider_kayitlari'

try:
    # 1. CSV Dosyasını Oku
    logging.info(f"'{CSV_DOSYASI}' okunuyor...")
    df_giderler = pd.read_csv(CSV_DOSYASI)
    logging.info(f"{len(df_giderler)} adet gider kaydı başarıyla okundu.")
    # print(df_giderler.head()) # İlk birkaç satırı görmek istersen açabilirsin

    # 2. Temel Veri Kalitesi Kontrolü (Örnek: Miktar negatif olamaz)
    if (df_giderler['Miktar'] < 0).any():
        logging.error("CSV dosyasında negatif Miktar değeri bulundu! İşlem durduruluyor.")
        sys.exit("Hata: Negatif gider miktarı olamaz.") # Script'i durdur
    logging.info("Temel veri kalitesi kontrolü yapıldı (Negatif miktar yok).")

    # 3. Hesaplamalar (Örnek)
    toplam_gider = df_giderler['Miktar'].sum()
    logging.info(f"Toplam gider hesaplandı: {toplam_gider:.2f}")
    # print(f"Toplam Gider: {toplam_gider:.2f}")

    kategori_bazli_gider = df_giderler.groupby('Kategori')['Miktar'].sum()
    logging.info(f"Kategori bazlı giderler hesaplandı:\n{kategori_bazli_gider}")
    # print("\nKategori Bazlı Giderler:")
    # print(kategori_bazli_gider)

    # 4. Veritabanına Bağlan ve Yaz
    logging.info(f"'{DB_DOSYASI}' veritabanına bağlanılıyor...")
    conn = sqlite3.connect(DB_DOSYASI)
    logging.info("Veritabanı bağlantısı başarılı.")

    logging.info(f"Veriler '{TABLO_ADI}' tablosuna yazılıyor ('replace' modu)...")
    # if_exists='replace': Tablo varsa silip yeniden oluşturur.
    # if_exists='append': Tablo varsa sonuna ekler. Başlangıç için 'replace' daha kolay.
    df_giderler.to_sql(TABLO_ADI, conn, if_exists='replace', index=False)
    logging.info("Veriler veritabanına başarıyla yazıldı.")

    # 5. Bağlantıyı Kapat
    conn.close()
    logging.info("Veritabanı bağlantısı kapatıldı.")

except FileNotFoundError:
    logging.error(f"HATA: '{CSV_DOSYASI}' dosyası bulunamadı!")
    print(f"HATA: '{CSV_DOSYASI}' dosyası bulunamadı!")
except KeyError as e:
    logging.error(f"HATA: CSV dosyasında beklenen sütun adı bulunamadı: {e}")
    print(f"HATA: CSV dosyasında beklenen sütun adı bulunamadı: {e}")
except Exception as e:
    logging.error(f"Beklenmedik bir hata oluştu: {e}")
    print(f"Beklenmedik bir hata oluştu: {e}")

logging.info("Gider işleme script'i tamamlandı.")