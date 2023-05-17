import requests as r
from bs4 import BeautifulSoup as bs
from datetime import date
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO

def split_string(string, panjang):
    kata = string.split()
    baris = []
    baris_saat_ini = ""
    
    for word in kata:
        if len(baris_saat_ini) + len(word) <= panjang:
            baris_saat_ini += word + " "
        else:
            baris.append(baris_saat_ini.strip())
            baris_saat_ini = word + " "
    
    if baris_saat_ini:
        baris.append(baris_saat_ini.strip())
    
    return baris

date_today = date.today().strftime('%d %B').split(' ')

html = r.get(f"https://www.animecharactersdatabase.com/birthdays.php?theday={date_today[0]}&themonth={date_today[1]}", headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}).text
soup = bs(html, 'html.parser')

characters = soup.find_all('li', {'style':lambda x: x and 'width' in x and not 'height' in x})
for character in characters:
    name = character.find_all('div')[-1].text
    url = character.find('a')['href']
    html2 = r.get('https://www.animecharactersdatabase.com/' + url, headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }).text
    soup2 = bs(html2, 'html.parser')
    img_url = soup2.find('img', class_ = 'thumb200')['src']
    anime_name = soup2.find('a', href = lambda x: x and 'source.php' in x).text

    img = BytesIO()
    img.write(r.get(img_url).content)

    background = Image.open(img).resize((800,800))

    border = Image.open('border.png')
    border = border.resize((800, 500), Image.LANCZOS)
    border_draw = ImageDraw.Draw(border)
    font = ImageFont.truetype('coolvetica.otf', 40)

    _, _, wB, _ = border_draw.textbbox((0, 0), name, font = font)
    border_draw.text(((border.width - wB) / 2, border.height - border.height * 0.5), name, font = font)

    for i, text in enumerate(split_string(anime_name, 35)):
        _, _, wB2, _ = border_draw.textbbox((0, 0), text, font = font)
        border_draw.text(((border.width - wB2) / 2, (border.height - border.height * 0.5) + 40 + 35 * i), text, font = font)

    result = background = Image.alpha_composite(
        Image.new("RGBA", background.size),
        background.convert('RGBA')
    )

    result.paste(
        border,
        (0, background.height - border.height),
        border
    )

    result.save(f'result/{date_today[0]}_{date_today[1]}_{anime_name}_{name}.png')
    print(f"result/{date_today[0]}_{date_today[1]}_{anime_name}_{name}.png saved!")