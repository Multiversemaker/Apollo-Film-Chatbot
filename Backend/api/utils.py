from functools import wraps
import asyncio
from googletrans import Translator
from config import COUNTRY_NAMES

translator = Translator()

def async_route(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapped

def get_country_name(country, lang='id'):
    if ',' in str(country):
        countries = [c.strip() for c in country.split(',')]
        translated_countries = [
            COUNTRY_NAMES.get(c, {}).get(lang, c) 
            for c in countries
        ]
        return ', '.join(translated_countries)
    return COUNTRY_NAMES.get(country, {}).get(lang, country)

def extract_search_term(message):
    message = message.lower()
    keywords = [
        # Kata tanya
        "tahu", "tau", "apakah", "bagaimana", "siapa", "kapan", "dimana", "mengapa",
          # Kata kerja pencarian
        "film", "cari", "carikan", "mencari", "tolong", "bantu", "bantuin", "temukan",
        "tunjukkan", "tampilkan", "lihat", "cek", "check",
        
        # Kata sambung
        "tentang", "mengenai", "yang", "dengan", "dari", "ke", "di", "pada",
        
        # Kata perintah
        "tolong", "mohon", "bisa", "dapat", "minta", "butuh",
        
        # Kata ganti
        "saya", "aku", "gue", "gw", "kami", "kita",
        
        # Kata sifat
        "ingin", "mau", "pengen", "pengin",
        
        # Kata terkait film
        "movie", "cinema", "bioskop", "sinema", "video", "tontonan",
        
        # Kata keterangan
        "ada", "sudah", "belum", "pernah", "sedang", "akan",
        
        # Tanda baca dan karakter khusus
        ".", ",", "!", "?", ":", ";", "(", ")", "[", "]", "{", "}", "-", "_",
        
        # Stopwords umum
        "yang", "di", "ke", "dari", "pada", "dalam", "untuk", "dengan", "dan", "atau",
        "ini", "itu", "juga", "baik", "seperti", "harus", "setelah", "telah", "saat",
        
        # Kata sambung waktu
        "ketika", "sementara", "selama", "sebelum", "sesudah", "sejak", "sampai"
    ]
    
    keywords = list(set(keywords))
    
    for keyword in keywords:
        message = message.replace(keyword, '')
    
    message = ' '.join(message.split())
    message = message.strip()
    
    return message if message else "unknown"

async def translate_text(text):
    try:
        if not text or text == 'No description available':
            return 'Tidak ada deskripsi tersedia'
        
        translation = translator.translate(text, dest='id')
        return translation.text if hasattr(translation, 'text') else text
        
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return text
