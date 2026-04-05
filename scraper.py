import requests
import re

# ============================================================
# TUS CANALES (He añadido una mejora para CBC)
# ============================================================
canales_a_buscar = {
    "CBC News Canada": "https://famelack.com/tv/ca/J0CqDMWbn8VHaM",
    "TVO Canal 23 SV": "https://tvocanal23.com/tvo-en-vivo/"
}
# ============================================================

def get_m3u8(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Referer': 'https://famelack.com/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        # Intento 1: Buscar .m3u8 directo (como el del canal 23)
        links = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', response.text)
        if links:
            return links[0]
        
        # Intento 2: Si es Famelack y no hay .m3u8, buscamos el "embed" (para CBC)
        embed_url = re.search(r'iframe.*?src=["\'](.*?)["\']', response.text)
        if embed_url:
            embed_res = requests.get(embed_url.group(1), headers=headers, timeout=10)
            links_embed = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', embed_res.text)
            if links_embed:
                return links_embed[0]
                
    except Exception as e:
        print(f"Error en {url}: {e}")
    return None

# Limpiamos y empezamos la lista
with open("lista.m3u", "w") as f:
    f.write("#EXTM3U\n")

print("--- Iniciando Rastreo ---")

for nombre, url in canales_a_buscar.items():
    print(f"Buscando: {nombre}...", end=" ")
    link = get_m3u8(url)
    if link:
        with open("lista.m3u", "a") as f:
            f.write(f"#EXTINF:-1, {nombre}\n")
            f.write(f"{link}\n")
        print("✅")
    else:
        print("❌")

print("--- Proceso Terminado ---")
