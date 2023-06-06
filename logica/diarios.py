from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re

from bd.mongo import insertarMongo
from utils.functions import urlnoticia, hashear, contiene_am_pm
from datetime import datetime

class Principal():
    def __init__(self, url, fecha_scraping):
        self.url = url
        self.fecha_scraping = fecha_scraping
        
        # Crear instancia de UserAgent
        ua = UserAgent()

        # Obtener un agente de usuario aleatorio
        user_agent = ua.random

        # Crear opciones del controlador
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={user_agent}')

        try:
            self.driver = webdriver.Remote(command_executor='http://192.168.54.215:4444/wd/hub', desired_capabilities=options.to_capabilities())
            self.wait = WebDriverWait(self.driver, 10)
        except:
            pass
        print(" 1 - Inicio abrir webdriver y navegador ")
        

    def logica(self):
        start = time.time()
        self.driver.get(self.url)
        # https://larepublica.pe/politica
        coleccion = self.url.split('/')[3]
        self.driver.maximize_window()
        # container = self.driver.find_element(By.CLASS_NAME , 'paginated-list--infinite')
        noticias = self.driver.find_elements(By.CLASS_NAME , 'story-item')
        print("noticias", noticias)
        # fecha_scraping = 

        # Convertir el string en un objeto datetime
        isend = False
        fecha_scrapeo = datetime.strptime(self.fecha_scraping, "%Y-%m-%d").date()
        arrayNoticias = []
        scroll_distance = 5000
        self.driver.execute_script(f"window.scrollBy(0, {scroll_distance});")


        end = time.time()
        dif = end - start

        print("DIFERENCIAAA----->", dif)

        for noticia in noticias:
            try:
                url = noticia.find_element(By.XPATH,  './div/figure/a').get_attribute('href')

                print("url", url)
                url_img = noticia.find_element(By.XPATH,  './div/figure/a/picture/img').get_attribute('src')
                print("url_img", url_img)
                fecha_publicada = noticia.find_element(By.XPATH,  './div/div/div/p').text
                print("fecha_publicada", fecha_publicada)
                fecha_publicada_obj = ''
                print("contiene_am_pm(fecha_publicada)", contiene_am_pm(fecha_publicada))
                if(contiene_am_pm(fecha_publicada)):
                    # fecha_publicada_obj= datetime.strptime(fecha_publicada, "%d/%m/%Y").date()
                    print("LA DATA ES DE HOY")
                else:
                    fecha_publicada_obj = datetime.strptime(fecha_publicada, "%d/%m/%Y").date()

                if fecha_publicada_obj == fecha_scrapeo:
                    data = {
                        "url": url,
                        'url_img': url_img
                    }
                    arrayNoticias.append(data)
                else:
                    print("Noticia fuera de fecha")  
            except Exception as e:
                print("Error:", str(e))
                time.sleep(10)
                self.driver.quit()
                pass

        
  
        

    #     for noticia in arrayNoticias:
    #         try:
    #             url_noticia = noticia['url']
    #             url_img = noticia['url_img']
    #             self.driver.get(url_noticia)
    #             time.sleep(5)
    #             scroll_distance = 500
    #             self.driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
    #             time.sleep(5)
    #             html = self.driver.page_source
    #             soup = BeautifulSoup(html, "html.parser")
    #             interna_content = soup.find(id="interna_content")
    #             datos = interna_content.find('div')
    #             datetime_str = datos.find('time')['datetime']
    #             contexto = datos.find('span')
    #             fecha_datetime = datetime.fromisoformat(datetime_str)
    #             timestamp = fecha_datetime.timestamp() * 1000
    #             titulo = interna_content.find('h1')
    #             subtitulo = interna_content.find('h2')

    #             MainContent_main__body__i6gEa = interna_content.find(class_="MainContent_main__body__i6gEa")    
    #             parrafos = MainContent_main__body__i6gEa.find_all('p')


    #             # Recorrer cada elemento de la lista parrafos
    #             for parrafo in parrafos:
    #                 # Extraer el contenido del párrafo eliminando las etiquetas HTML
    #                 texto_limpio = ''.join(parrafo.findAll(text=True))
    #                 # Agregar el párrafo limpio a la lista parrafos_limpios
    #                 print("<------------->")
    #                 urlParrafo = urlnoticia(url_noticia, texto_limpio.strip())
                    
    #                 json_limpio = {
    #                     'id':  hashear(urlParrafo),
    #                     'source_place': '2dfa9ecb0179a4e4',
    #                     'sample_lang': 'es',
    #                     'sample_app': 'web',
    #                     'source_snetwork_id': 'nws',
    #                     'sample_created_at': timestamp,
    #                     'sample_text': texto_limpio.strip(),
    #                     'sample_link': urlParrafo,
    #                     'author_id': 'md5pordefinir',
    #                     'author_fullname': 'Diario La República',
    #                     'author_photo': 'Fotobds3',
    #                     'author_screen_name': 'larepublica.pe',
    #                     'sample_post_author_id': 'md5pordefinir',
    #                     'sample_post_author': 'Diario La República', 
    #                     'sample_post_author_photo': 'Fotobds3',
    #                     'sample_post_id': hashear(url_noticia), 
    #                     'sample_post_text': titulo.text.strip().replace('\\"', '"').replace("\\'", "'") + subtitulo.text.strip().replace('\\"', '"').replace("\\'", "'"), 
    #                     'sample_post_created_at': timestamp,
    #                     'sample_post_image': url_img,
    #                     'sample_post_link': url_noticia
    #                 }

    #                 print(json_limpio)
    #                 insertarMongo(json_limpio, coleccion)
    #             time.sleep(10)
    #         except Exception as e:
    #             print("Error:", str(e))
    #             time.sleep(20)
    #             pass
    #     self.driver.quit()

    # def extraData(self, html):
    #     soup = BeautifulSoup(html, "html.parser")
    #     div = soup.find('div')
    #     print("div", div)
    #     h1 = div.find('h1')
    #     h2 = div.find('h2')
    #     # tbody = div.find('tbody')
    #     print("h1", h1)
    #     print("h2", h2)
    #     # titulo = self.driver.find_element(By.XPATH , '/html/body/div[1]/div/div[4]/div[2]/h1').text
    #     # print("titulo", titulo)
    #     return 0

    