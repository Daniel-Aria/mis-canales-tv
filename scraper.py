import requests
import re

# ============================================================
# AQUÍ HE AÑADIDO TU NUEVO CANAL DE EL SALVADOR
# ============================================================
canales_a_buscar = {
    "CBC News Canada": "https://famelack.com/tv/ca/0TNzmvJYBpUTj4",
    "TVO Canal 23 SV": "https://tvocanal23.com/tvo-en-vivo/"
}
# ============================================================

def get_m3u8(url):
    # Usamos un User-Agent de navegador para que la web nos deje entrar
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # Buscamos el enlace del streaming (.m3u8)
        links = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', response.text)
        if links:
            return links[0]
    except:
        pass
    return None

# Proceso de escritura de la lista
with open("lista.m3u", "w") as f:
    f.write("#EXTM3U\n")

for nombre, url in canales_a_buscar.items():
    link = get_m3u8(url)
    if link:
        with open("lista.m3u", "a") as f:
            f.write(f"#EXTINF:-1, {nombre}\n")
            f.write(f"{link}\n")
        print(f"✅ Canal añadido: {nombre}")
    else:
        print(f"❌ No se encontró señal para: {nombre}")
