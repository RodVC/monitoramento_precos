import os
import smtplib # Biblioteca que permite o envio de emails via smtp
from email.message import EmailMessage
import imghdr # permite identificar qual é o tipo de extensão da imagem
import time

class Emailer:
    def __init__(self,email_remetente,senha_email_remetente):
        #Configuração de Login
        self.email_remetente = email_remetente
        self.senha_email = senha_email_remetente
        

    def definir_conteudo_email(self,assunto,lista_destinatarios,conteudo_email):
        #Criando o Email
        self.msg = EmailMessage()
        self.msg['Subject'] = assunto
        self.msg['From'] = self.email_remetente
        self.msg['To'] = ', '.join(lista_destinatarios) #acrescenta um ', ' entre cada contato da lista

        self.msg.set_content(conteudo_email)

    def anexar_imagens(self,lista_imagens):
        #CONFIGURAR O ANEXO DE IMAGENS
        os.chdir('Arquivos')
        imagens = lista_imagens

        for imagem in imagens: 

            with open(imagem, 'rb') as arquivo: # 'rb' quer dizer read binary. Imagens devem ser lidas em binário
                dados = arquivo.read() # para ler o conteúdo do arquivo
                extensao_imagem = imghdr.what(arquivo.name) # indentifica qual é a extensão da imagem
                nome_arquivo = arquivo.name
            self.msg.add_attachment(dados,maintype='image',subtype=extensao_imagem,filename=nome_arquivo)

        os.chdir('..')

    def anexar_arquivos_variados(self,lista_arquivos):
        #  COMO ENVIAR DEMAIS TIPOS DE ARQUIVOS
        os.chdir('Arquivos')
        arquivos = lista_arquivos

        for arquivo in arquivos:
        
            with open(arquivo,'rb') as arquivo:
                dados = arquivo.read()
                nome_arquivo = arquivo.name
            self.msg.add_attachment(dados,maintype = 'application',subtype='octet-stream',filename=nome_arquivo) 
            # 'application'  é um termo genérico pra maioria dos tipos de arquivos
            # 'octet-stream' é um tipo genérico pra informar extensão dos arquivos
        os.chdir('..')

    def enviar_email_gmail(self,intervalo):
    # Fazer o envio usando SSL que é um protocolo de Email mais seguro
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp: #essa configuração depende do tipo de serviço que está sendo utilizado 
            smtp.login(self.email_remetente,self.senha_email)
            smtp.send_message(self.msg)
            time.sleep(intervalo)
