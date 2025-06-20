from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient
# Mengkomentari Pyrogram Client import di sini, karena tidak selalu diperlukan di file ini.
# from pyrogram import Client 

import sys # Diperlukan untuk sys.exit()
from urllib.parse import urlparse # Diperlukan untuk memparsing URL MongoDB

import config # Mengimpor modul konfigurasi (misalnya config.py)

from ..logging import LOGGER # Mengimpor logger bot

# Variabel ini tidak lagi di-hardcode di sini.
# Bot akan mengambil MONGO_DB_URI dari file config.py.
# TEMP_MONGODB = "mongodb+srv://Fakeya:KontolXD#123@fakeya.6hfphaj.mongodb.net/?retryWrites=true&w=majority&appName=FakeYa"

# Inisialisasi variabel klien MongoDB dan database sebagai None
# Ini akan diisi jika koneksi berhasil
_mongo_async_ = None
_mongo_sync_ = None
mongodb = None
pymongodb = None

# PERBAIKAN UTAMA: Memeriksa apakah MONGO_DB_URI sudah diatur di config.py
if config.MONGO_DB_URI is None:
    LOGGER(__name__).error(
        "Kesalahan Konfigurasi: Tidak ada MONGO_DB_URI yang ditemukan di config.py. "
        "Bot tidak dapat memulai tanpa URL database yang valid."
    )
    LOGGER(__name__).error(
        "Pastikan Anda telah mengisi variabel MONGO_DB_URI di file config.py Anda "
        "dengan string koneksi MongoDB Atlas Anda."
    )
    # Keluar dari bot karena tidak bisa berfungsi tanpa database
    sys.exit(1)
else:
    try:
        # Inisialisasi klien MongoDB menggunakan URI dari config.py
        _mongo_async_ = _mongo_client_(config.MONGO_DB_URI)
        _mongo_sync_ = MongoClient(config.MONGO_DB_URI)

        # Memparsing URI untuk mendapatkan nama database
        parsed_url = urlparse(config.MONGO_DB_URI)
        # Nama database seringkali berada di bagian 'path' dari URI (misal: /namadatabase)
        db_name = parsed_url.path.strip('/') 
        
        # Jika nama database tidak ditemukan di path URI, 
        # coba cek parameter appName atau gunakan default.
        if not db_name:
            # Contoh: jika URL berisi "appName=FakeYa", gunakan "FakeYa" sebagai nama database.
            if "appName=FakeYa" in config.MONGO_DB_URI:
                db_name = "FakeYa" 
            else:
                # Sebagai fallback terakhir, gunakan "Ryn" (sesuai logika lama bot Anda)
                # atau nama database default yang Anda buat di MongoDB Atlas.
                db_name = "Ryn" 
                LOGGER(__name__).warning(
                    f"Nama database tidak ditemukan di URI atau appName. "
                    f"Menggunakan nama database default: '{db_name}'. "
                    f"Pastikan ini cocok dengan nama database Anda di Atlas."
                )

        # Mengakses database menggunakan nama yang sudah ditentukan
        mongodb = _mongo_async_[db_name] # Untuk operasi asynchronous (Motor)
        pymongodb = _mongo_sync_[db_name] # Untuk operasi synchronous (PyMongo)

        LOGGER(__name__).info(f"Berhasil terhubung ke MongoDB Atlas. Nama Database: {db_name}")

    except Exception as e:
        LOGGER(__name__).error(f"Gagal terhubung ke MongoDB atau memparsing URI: {e}")
        LOGGER(__name__).error(
            "Periksa: 1. MONGO_DB_URI di config.py sudah benar. "
            "2. Pengaturan IP Access di MongoDB Atlas mengizinkan koneksi dari server Anda."
            "3. Username dan Password di URI sudah benar."
        )
        # Keluar jika gagal koneksi atau parsing
        sys.exit(1)

# Catatan: Bagian kode lama yang menggunakan temp_client untuk mendapatkan username bot
# dan menggunakannya sebagai nama database telah dihapus.
# Logika tersebut bermasalah karena username bot BUKAN nama database MongoDB.
# Bot sekarang mengandalkan config.MONGO_DB_URI untuk koneksi yang benar.
