from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

search = input('Digite a chave de busca: ')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://www.google.com/maps/place/S%C3%A3o+Paulo,+SP")

dados_titles = []

def remove_dup(lista):
    lista = set(lista)
    return lista

driver.find_element(By.ID, 'searchboxinput').send_keys(' Lojas de materiais para construção na cidade de são paulo no bairro ' + search + Keys.RETURN)

sleep(10)

scroll = driver.find_elements(By.CSS_SELECTOR, '.Nv2PK')

try:
    scroll.execute_script("window.scrollTo(0,document.body.scrollHeight)")
except:
    pass

sleep(20)

links = driver.find_elements(By.CSS_SELECTOR, '.Nv2PK')

for link in links:
    sleep(2)
    text = link.find_element(By.CSS_SELECTOR, '.hfpxzc')
    text_link = text.get_attribute('href')
    dados_titles.append(text_link)

lista = remove_dup(dados_titles)

sleep(5)

dados = []

for dado in lista:
    driver.get(dado)
    sleep(3)

    for attribute in driver.find_elements(By.CSS_SELECTOR, '.WNBkOb'):
        text = driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[1]').text
        try:
            address = driver.find_element(By.XPATH, '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]/div[3]/button/div[1]/div[2]/div[1]').text
        except:
            address = None
        try:
            website = driver.find_element(By.PARTIAL_LINK_TEXT, '.com').text
        except:
            website = None
        try:
            phone = driver.find_element(By.XPATH, "//div[contains(text(), '(11)')]").text
        except:
            phone = None
            
        dados_final = {
            'name': text,
            'address': address,
            'website': website,
            'phone': phone
            }   
        dados.append(dados_final)

driver.close()

df = pd.DataFrame(dados)
df.drop_duplicates(inplace=True)
newdf = df[df['address'].str.lower().str.contains(search, na=False)]
newdf.head()
newdf.to_csv('leads_googleMaps.csv', index=False)

print(newdf.head())
        
        