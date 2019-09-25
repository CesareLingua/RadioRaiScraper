from lxml import html
import requests
import os, sys
import request
import time

page = requests.get('https://www.raiplayradio.it/programmi/hollywoodparty-ilcinemaallaradio/archivio/puntate/')
tree = html.fromstring(page.content)
urls = tree.xpath('//ul[@class="listaStagioniPuntate"]//li/a/@href')
downloaded_files = 0
start_time = time.time()

for u in urls:
    print("Scrico da: "+u)
    there_is_next = True
    num_pg = 1
    while there_is_next:
        print(" * Pagina "+str(num_pg))
        page = requests.get("https://www.raiplayradio.it"+u+'/'+str(num_pg))
        tree = html.fromstring(page.content)
        film_urls = tree.xpath('//div[@class="row listaAudio "]/@data-mediapolis')
        titles = tree.xpath('//div[@class="columns large-expand medium-expand small-12"]//h3//a/text()')
        for i in range(len(titles)):
          titles[i] = titles[i].strip().replace("/", "")
        if len(film_urls) != len(titles):
            print("titoli e urls non hanno lo stesso numero!!")
            exit()
        for i in range(len(film_urls)):
            print("     + "+titles[i])
            if not os.path.isfile('./'+titles[i]+'.mp3'):
                file = requests.get(film_urls[i], allow_redirects=True)
                open('./'+titles[i]+'.mp3', 'wb').write(file.content)
                downloaded_files += 1
        if film_urls:
            num_pg += 1
        else:
            there_is_next = False


print("Tempo totale: .............. " + str(round(time.time() - start_time, 2)) + " sec")
print("File scaricati: ............ " + str(downloaded_files))
