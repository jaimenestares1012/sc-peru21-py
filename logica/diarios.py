from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from functions import urlnoticia, hashear, contiene_p_o_m, generaJson
from utils.testS3 import insertS3
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
            self.driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', desired_capabilities=options.to_capabilities())
            self.wait = WebDriverWait(self.driver, 10)
        except:
            pass
        print(" 1 - Inicio abrir webdriver y navegador ")
        

    def logica(self):
        start = time.time()
        self.driver.get(self.url)
        # https://larepublica.pe/politica
        coleccion = self.url.split('/')[3]
        print("coleccion", coleccion)
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
        for noticia in noticias:
            try:
                url = noticia.find_element(By.XPATH,  './div/figure/a').get_attribute('href')
                url_img = noticia.find_element(By.XPATH,  './div/figure/a/picture/img').get_attribute('src')
                fecha_publicada = noticia.find_element(By.XPATH,  './div/div/div/p').text
                fecha_publicada_obj = ''
                if(contiene_p_o_m(fecha_publicada)):
                    fecha_publicada_obj = datetime.now().date().strftime("%Y-%m-%d")
                    fecha_publicada_obj= datetime.strptime(fecha_publicada_obj, "%Y-%m-%d").date()
                    pass
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

        
  
        
        for noticia in arrayNoticias:
            try:
                url_noticia = noticia['url']
                url_img = noticia['url_img']
                self.driver.get(url_noticia)
                time.sleep(5)
                scroll_distance = 500
                self.driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
                time.sleep(5)
                html = self.driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                contenedor = soup.find(id="contenedor")
                titulo = soup.find(class_="sht__title")
                datos = soup.find(class_="story-contents__author")
                datetime_str = datos.find('time')['datetime']
                fecha_datetime = datetime.fromisoformat(datetime_str)
                timestamp = fecha_datetime.timestamp() * 1000
                parrafos = contenedor.find_all('p')

                for parrafo in parrafos:
                    # Extraer el contenido del párrafo eliminando las etiquetas HTML
                    texto_limpio = ''.join(parrafo.findAll(text=True))
                    # Agregar el párrafo limpio a la lista parrafos_limpios
                    
                    urlParrafo = urlnoticia(url_noticia, texto_limpio.strip())
                    id_parrafo = hashear(urlParrafo)



                    json_limpio = {
                        'id':  id_parrafo,
                        'source_place': '2dfa9ecb0179a4e4',
                        'sample_lang': 'es',
                        'sample_app': 'web',
                        'source_snetwork_id': 'nws',
                        'sample_created_at': timestamp,
                        'sample_text': texto_limpio.strip(),
                        'sample_link': urlParrafo,
                        'author_id': 'md5pordefinir',
                        'author_fullname': 'Diario Perú21',
                        'author_photo': 'Fotobds3',
                        'author_screen_name': 'peru21.pe',
                        'sample_post_author_id': 'md5pordefinir',
                        'sample_post_author': 'Diario Perú21', 
                        'sample_post_author_photo': 'Fotobds3',
                        'sample_post_id': hashear(url_noticia), 
                        'sample_post_text': titulo.text.strip().replace('\\"', '"').replace("\\'", "'") ,
                        # + subtitulo.text.strip().replace('\\"', '"').replace("\\'", "'"), 
                        'sample_post_created_at': timestamp,
                        'sample_post_image': url_img,
                        'sample_post_link': url_noticia
                    }
                    generaJson(json_limpio, id_parrafo,fecha_scrapeo )
                    insertS3(fecha_scrapeo,id_parrafo)
                    print(json_limpio)
                time.sleep(10)
            except Exception as e:
                print("Error:", str(e))
                time.sleep(10)
                pass
        self.driver.quit()

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

    