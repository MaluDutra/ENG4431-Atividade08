from bs4 import BeautifulSoup
import requests

def extrair_informacao():
  try:
    url = 'https://tecnoblog.net/responde/os-filmes-animados-do-studio-ghibli-em-ordem-de-lancamento/'
    headers = {
      "User-Agent": "Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion"
    }
    response = requests.get(url,headers=headers)
    
    if response.status_code !=200:
      return False
      
    sopa = BeautifulSoup(response.text, "html.parser")
    lista = sopa.find_all('td')
    #print(lista)
    info = 'Filmes do Studio Ghibli em ordem de lançamento °。°。°。°。°。°。\n'
    for i in range(2,len(lista),2):
      info += "\n◦ %s (%s)" %(lista[i].text, lista[i+1].text)
  
    return info
    
  except:
    return None


def extrair_horario():
  try:
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(service=service,options=options)
    browser.get("https://time.is/pt_br/Japan")
    sleep(2)

    info = "Horário atual no Japão: "
    element = browser.find_element(by=By.ID, value='clock')
    print(element.text)
    browser.quit

    hora = str(element.text)
    print(hora)
    info+=hora

    return info
  except:
    return None
