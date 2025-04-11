import os
import yt_dlp
import requests

CONVERTER_API_URL = "https://converter-api-uqhz.onrender.com/convert"

def search_and_download(search_query, download_path):
    refined_query = f"{search_query} official audio"

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch5',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            infos = ydl.extract_info(refined_query, download=False)['entries']
            if not infos:
                print(f"Nenhum vídeo encontrado para: {search_query}")
                return

            def is_official(info):
                channel = info.get('channel', '').lower()
                return (
                    'topic' in channel or
                    'vevo' in channel or
                    'official' in channel
                )

            sorted_infos = sorted(infos, key=lambda x: not is_official(x))
            chosen = sorted_infos[0]

            # Baixar .webm temporário
            temp_webm_path = os.path.join(download_path, "temp.webm")
            ydl.download([chosen['webpage_url']])
            for file in os.listdir(download_path):
                if file.endswith(".webm"):
                    os.rename(os.path.join(download_path, file), temp_webm_path)

            # Enviar para API e receber MP3
            with open(temp_webm_path, "rb") as f:
                files = {'file': (f"{search_query}.webm", f)}
                try:
                    response = requests.post(CONVERTER_API_URL, files=files, timeout=30)
                except requests.exceptions.Timeout:
                    print(f"Timeout ao converter {search_query}")
                    return

            if response.status_code == 200:
                output_path = os.path.join(download_path, f"{search_query}.mp3")
                with open(output_path, "wb") as out:
                    out.write(response.content)
            else:
                print(f"Erro na conversão: {response.text}")

            os.remove(temp_webm_path)

    except Exception as e:
        print(f"Erro ao baixar {search_query}: {e}")
