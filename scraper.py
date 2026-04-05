import requests
import re

# ============================================================
# LISTA DE CANALES
# ============================================================
canales_a_buscar = {
    "CBC News Network": "https://famelack.com/tv/ca/J0CqDMWbn8VHaM",
    "TVO Canal 23 SV": "https://tvocanal23.com/tvo-en-vivo/"
}
# ============================================================

def get_m3u8(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Referer': 'https://famelack.com/'
    }
    try:
        # 1. Intentamos leer la página principal
        response = requests.get(url, headers=headers, timeout=15)
        
        # 2. Buscamos el .m3u8 directamente
        links = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', response.text)
        if links:
            return links[0]
        
        # 3. Si no hay link (caso CBC), buscamos la URL del reproductor interno (iframe)
        iframe_match = re.search(r'iframe.*?src=["\'](.*?)["\']', response.text)
        if iframe_match:
            iframe_url = iframe_match.group(1)
            # Si la URL del iframe es relativa, la completamos
            if iframe_url.startswith('//'):
                iframe_url = 'https:' + iframe_url
            
            # Entramos al reproductor interno para buscar el link real
            res_iframe = requests.get(iframe_url, headers=headers, timeout=10)
            links_hidden = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', res_iframe.text)
            if links_hidden:
                return links_hidden[0]
                
    except Exception as e:
        print(f"Error procesando {url}: {e}")
    return None

# Crear el archivo m3u
with open("lista.m3u", "w") as f:
    f.write("#EXTM3U\n")

print("--- Actualizando canales ---")

for nombre, url in canales_a_buscar.items():
    print(f"Buscando {nombre}...", end=" ")
    link_encontrado = get_m3u8(url)
    
    if link_encontrado:
        with open("lista.m3u", "a") as f:
            f.write(f"#EXTINF:-1, {nombre}\n")
            f.write(f"{link_encontrado}\n")
        print("✅")
    else:
        print("❌ (No se encontró)")

print("--- Finalizado ---")
