import requests
import re

# ============================================================
# TU LISTA DE CANALES
# ============================================================
# ============================================================
# TUS CANALES SELECCIONADOS
# ============================================================
canales_a_buscar = {
    "TVO Canal 23 SV": "https://tvocanal23.com/tvo-en-vivo/",
    "ABC 7 New York": "https://famelack.com/tv/us/ABC-7-New-York",
    "ABC 7 Los Angeles": "https://famelack.com/tv/us/ABC-7-Los-Angeles-CA-KABC-TV",
    "ABC 7 Albuquerque": "https://famelack.com/tv/us/KOAT",
    "ABC 7 San Francisco": "https://famelack.com/tv/us/KGO-DT1"
}
# ============================================================
# ============================================================

def get_m3u8(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Referer': 'https://famelack.com/'
    }
    try:
        # 1. Leemos la página
        response = requests.get(url, headers=headers, timeout=15)
        
        # 2. Buscamos el .m3u8 directamente (como el del canal 23)
        links = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', response.text)
        if links:
            return links[0]
        
        # 3. Si no aparece (caso CBC), buscamos el "reproductor interno"
        iframe_match = re.search(r'iframe.*?src=["\'](.*?)["\']', response.text)
        if iframe_match:
            iframe_url = iframe_match.group(1)
            if iframe_url.startswith('//'):
                iframe_url = 'https:' + iframe_url
            
            # Entramos al reproductor para sacar el link real
            res_iframe = requests.get(iframe_url, headers=headers, timeout=10)
            links_hidden = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', res_iframe.text)
            if links_hidden:
                return links_hidden[0]
                
    except Exception as e:
        print(f"Error en {url}: {e}")
    return None

# Escribir la lista final
with open("lista.m3u", "w") as f:
    f.write("#EXTM3U\n")

print("--- Iniciando búsqueda ---")
for nombre, url in canales_a_buscar.items():
    print(f"Buscando {nombre}...", end=" ")
    resultado = get_m3u8(url)
    if resultado:
        with open("lista.m3u", "a") as f:
            f.write(f"#EXTINF:-1, {nombre}\n")
            f.write(f"{resultado}\n")
        print("✅")
    else:
        print("❌")
