from lxml import html
import requests
import os, sys
import request
import time

generated_dir = 0
downloaded_files = 0

books_url = []
start_time = time.time()
#Ricava i link delle pagine di ogni libro
for i in range(1, 18):
    page = requests.get('https://www.raiplayradio.it/programmi/adaltavoce/archivio/audiolibri/tutte/'+str(i))
    tree = html.fromstring(page.content)
    books_url += tree.xpath('//div[@class="columns large-4 medium-6 small-6 bloccoPlaylist containerOption"]//@href')

#books_url = ["/playlist/2017/12/Favole-al-telefono-6f6a061d-65e4-415e-b73a-b52b1e4055d2.html"]
for b in books_url:
    page = requests.get('https://www.raiplayradio.it'+b)
    tree = html.fromstring(page.content)
    title = tree.xpath('//div[@class="column large-12 medium-12 small-12 playlistTitleContainer"]/h2//text()')
    if title:
      if not os.path.isdir(title[0]):
          os.mkdir("./"+title[0])
          generated_dir += 1
      links = tree.xpath('//li/@data-mediapolis')

      print("- Scarico: "+ title[0])
      i = 1
      for l in links:
          if l and not os.path.isfile('./'+title[0]+'/'+str(i)+'_'+title[0].lower()+'.mp3'):
              file = requests.get(l, allow_redirects=True)
              open('./'+title[0]+'/'+str(i)+'_'+title[0].lower()+'.mp3', 'wb').write(file.content)
              downloaded_files += 1
              print(" "+str(i))
          i += 1

print("Tempo totale: .............. " + str(round(time.time() - start_time, 2)) + " sec")
print("Cartelle create: ........... " + str(generated_dir))
print("File scaricati: ............ " + str(downloaded_files))
