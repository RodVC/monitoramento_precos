#pip install selenium==3.141.0
#pip install schedule
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as condicao_esperada
from datetime import datetime
import os
import sys # para pausar a execução do programa
import time # para retornar a data e hora
import schedule #programar execuão em tempo
from CLASSE_EMAIL import Emailer

class projeto_acompanhar_preco:

    def __init__(self):
        chrome_options = Options()
        chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
        caminho_chromedriver = os.environ.get('CHROMEDRIVER_PATH')  
        # chrome_options.add_argument('--lang=pr-BR')
        # chrome_options.add_argument('--disable-notifications')

        # Configurações para rodar no heroku
        chrome_options.add_argument('--headless') # faz o chrome rodar sem abrir o navegador
        chrome_options.add_argument('--disable-dev-shm-usage') #config que permite que o chrome seja rodado em MVs com menor potência
        chrome_options.add_argument('--no-sandbox') # necessário quando o servidor é linux

        self.driver = webdriver.Chrome(executable_path=caminho_chromedriver,options=chrome_options)
        self.wait = WebDriverWait(self.driver,10,1,[NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException])
        self.link_pagina = 'https://cursoautomacao.netlify.app/dinamico'
        
    
    def iniciar(self):
        self.navegar_ate_a_pagina()
        self.verificar_mudancas()
        self.schedule(2)
   
    def schedule(self,minutos):
        schedule.every(minutos).minutes.do(self.verificar_mudancas)
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    def navegar_ate_a_pagina(self):
        self.driver.get(self.link_pagina)

    def verificar_mudancas(self):    
        # self.driver.get(self.driver.current_url) # refresh
        self.preco = self.wait.until(condicao_esperada.visibility_of_element_located((By.XPATH,'//li[@id="BasicPlan"]')))
        self.data_e_hora_em_texto = datetime.now().strftime('%d/%m/%Y às %H:%M')
        if self.preco.text != 'R$ 9.99 / ano':
            print(f'{self.data_e_hora_em_texto} - O preco foi alterado para {self.preco.text}.')
            self.enviar_email()
            self.driver.quit()
            # sys.exit()
        elif self.preco.text == 'R$ 9.99 / ano':
             print(f'{self.data_e_hora_em_texto} - O preço continua o mesmo')

    def enviar_email(self):
        remetente = os.environ.get('EMAIL_REMETENTE')
        senha = os.environ.get('SENHA_EMAIL')
        contatos = ['rdrigo_test@hotmail.com']
        assunto = 'ALTERAÇÃO DE PREÇO DETECTADA'
        conteudo = 'Prezado(a),' + '\n' + '\n' + f'O preço foi alterado para{self.preco.text} hoje, {self.data_e_hora_em_texto}.' +'\n'+'\n' + 'Atenciosamente,' + '\n' + 'Rodrigo Coelho' +'\n' + 'Tel.:(81) 9.9669-7126' 
        # imagens = ['imagem_1.jpg','imagem_2.jpg']
        # arquivos = ['csv_exemplo.csv','exemplo_word.docx','ExemploPlanilha.xlsx','json_exemplo.json','PDF_Exemplo.pdf','txt_exemplo.txt']

        mail = Emailer(email_remetente=remetente,senha_email_remetente=senha)
        mail.definir_conteudo_email(assunto=assunto,lista_destinatarios=contatos,conteudo_email=conteudo)
        # mail.anexar_imagens(lista_imagens=imagens)
        # mail.anexar_arquivos_variados(lista_arquivos=arquivos)
        mail.enviar_email_gmail(intervalo=1)


start = projeto_acompanhar_preco()
start.iniciar()
    

