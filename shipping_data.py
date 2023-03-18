from selenium import webdriver, By
import json
import requests
import datetime
import pandas as pd

def getEvents():
    url = "https://api.frete.v2.alfatracking.com.br/v1/event"
    payload = json.dumps({
    "clientCode": client_code,
    "date": datetime.today().strftime('%Y-%m-%d')
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {access_token}'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    return response['data']

data=pd.DataFrame(columns=["Orders","BarCodes","Events"])
dfResult=pd.DataFrame(columns=["code","nomeDestinatario","numPedido","cpf","endereço","Numero","complemento","bairro","Cidade","estado","cep"])
link="https://rastreio.alfatracking.com.br/#/"
driver=webdriver.Chrome()
client_code = "your_client_code"
access_token = "your_access_token"

for i in getEvents():
    url2 = "https://api.frete.v2.alfatracking.com.br/v1/tracking"
    payload2 = json.dumps({
      "clientCode": client_code,
      "typeSearch": "2",
      "value": str(i['orderNumber'])
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Basic {access_token}'
    }
    response2 = requests.request("POST", url2, headers=headers, data=payload2)
    strigAuxiliar={}
    for k in response2.json():
        strigAuxiliar.push(k['dateInsertion'],k['status'])
    data.loc[len(data)] = [i['orderNumber'],i['barCode'],f"{strigAuxiliar}"]
    newlink = link + i['barCode']
    driver.get(newlink)
    driver.implicitly_wait(4)
    button = driver.find_element(By.XPATH,"/html/body/div/div/div/div[2]/div/div/button[2]")
    driver.implicitly_wait(2)
    driver.execute_script("arguments[0].click();", button)
    nomeDestinatario = driver.find_element(By.XPATH,'/html/body/div/div/div/div[4]/div/div/div[1]/div[1]/div/div/input').get_attribute('value')
    numPedido = driver.find_element(By.XPATH,'/html/body/div/div/div/div[1]/div/div[3]/div/div/input').get_attribute('value')
    cpf = str(driver.find_element(By.XPATH,'/html/body/div/div/div/div[4]/div/div/div[1]/div[2]/div/div/input').get_attribute('value'))
    endereco = driver.find_element(By.XPATH,'/html/body/div/div/div/div[4]/div/div/div[1]/div[4]/div/div/textarea').get_attribute('innerHTML')
    numero = driver.find_element(By.XPATH,'/html/body/div/div/div/div[4]/div/div/div[2]/div[1]/div/div/input').get_attribute('value')
    complemento = driver.find_element(By.XPATH,'/html/body/div/div/div/div[4]/div/div/div[2]/div[2]/div/div/input').get_attribute('value')
    bairro = driver.find_element(By.XPATH,'/html/body/div/div/div/div[4]/div/div/div[3]/div[1]/div/div/input').get_attribute('value')
    cidade = driver.find_element(By.XPATH,'/html/body/div/div/div/div[4]/div/div/div[3]/div[2]/div/div/input').get_attribute('value')
    estado = driver.find_element(By.XPATH,'/html/body/div/div/div/div[4]/div/div/div[3]/div[3]/div/div/input').get_attribute('value')
    cep = driver.find_element(By.XPATH,'/html/body/div/div/div/div[4]/div/div/div[3]/div[4]/div/div/input').get_attribute('value')
    cpf = cpf.rjust(11, '0')[:11]
    dfResult.loc[i]=[i['barCode'],nomeDestinatario,numPedido,str(cpf),endereco,numero,complemento,bairro,cidade,estado,str(cep)]
    driver.implicitly_wait(2)
driver.close()

dfResult.to_excel("ShippingData.xlsx")
