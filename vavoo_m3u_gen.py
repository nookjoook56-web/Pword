import asyncio
import aiohttp
import json

# Vavoo için gerekli başlıklar
HEADERS = {
    'User-Agent': 'VAVOO/2.6',
    'Accept': '*/*'
}

async def get_channels():
    """Vavoo'dan kanal listesini çeker."""
    url = "https://www2.vavoo.to/live2/index"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            return await response.json()

async def resolve_stream(session, channel_id):
    """Kanal ID'si için yayın linkini çözer."""
    url = f"https://www2.vavoo.to/live2/play?id={channel_id}"
    async with session.get(url, headers=HEADERS) as response:
        return await response.text()

async def main():
    print("Kanallar çekiliyor...")
    channels = await get_channels()
    
    m3u_content = "#EXTM3U\n"
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for channel in channels:
            # Kanal verisini işle (İsim, ID vb.)
            name = channel.get('name', 'Unknown')
            cid = channel.get('id', '')
            
            # Asenkron görevler oluştur
            tasks.append(resolve_stream(session, cid))
            
        # Tüm linkleri aynı anda çöz
        streams = await asyncio.gather(*tasks)
        
        # M3U içeriğini oluştur
        for i, channel in enumerate(channels):
            name = channel.get('name', 'Unknown')
            stream_url = streams[i]
            m3u_content += f"#EXTINF:-1,{name}\n{stream_url}\n"
            
    # Sonucu dosyaya yaz
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("playlist.m3u oluşturuldu!")

if __name__ == "__main__":
    asyncio.run(main())
