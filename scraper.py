import requests
import re

# ============================================================
# TU LISTA DE CANALES ACTUALIZADA
# ============================================================

canales_a_buscar = {
    "TVO": "https://tvocanal23.com/tvo-en-vivo/"
}
# ============================================================

def get_m3u8(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Referer': 'https://famelack.com/'
    }

    # 🔥 NUEVO: si la URL YA es un .m3u8, devolverla directo
    if url.endswith(".m3u8") or ".m3u8?" in url:
        return url

    try:
        response = requests.get(url, headers=headers, timeout=15)

        # Intento 1: Buscar .m3u8 directo dentro del HTML
        links = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', response.text)
        if links:
            return links[0]

        # Intento 2: Buscar dentro del iframe (para canales de Famelack)
        iframe_match = re.search(r'iframe.*?src=["\'](.*?)["\']', response.text)
        if iframe_match:
            iframe_url = iframe_match.group(1)
            if iframe_url.startswith('//'):
                iframe_url = 'https:' + iframe_url

            res_iframe = requests.get(iframe_url, headers=headers, timeout=10)
            links_hidden = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', res_iframe.text)
            if links_hidden:
                return links_hidden[0]

    except Exception as e:
        print(f"Error en {url}: {e}")

    return None


# Crear el archivo de lista
with open("lista.m3u", "w") as f:
    f.write("#EXTM3U\n")

print("--- Actualizando tu lista ---")
for nombre, url in canales_a_buscar.items():
    print(f"Procesando {nombre}...", end=" ")
    resultado = get_m3u8(url)
    if resultado:
        with open("lista.m3u", "a") as f:
            f.write(f"#EXTINF:-1,{nombre}\n")
            f.write(f"{resultado}\n")
        print("✅")
    else:
        print("❌")

print("--- ¡Listo! ---")
