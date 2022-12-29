import requests
from bs4 import BeautifulSoup
import time
import pywhatkit
import mysql.connector


# ask questions about telephone number and skills that the user lacks
# send a msg saying that the bot will send the msg soon.
print('digite uma habilidade que você não é familiarizado')
habilidade_faltante = input('>')
print('digite um número para o qual as ofertas serão enviadas')
numero_whats = input('digite no formato: +000.00.0000000. >')
print("em breve o robô enviará a mensagem via whatsap..")



connector = mysql.connector.connect(user='sql10585660',
                                    password='8x7X382pdd',
                                    host='sql10.freesqldatabase.com',
                                    database='Users')

def encontre_empregos():
    # use get method of request library. it requests information from website. we use .txt to request only text
    texto_html = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text



    # create a beautiful Instance. 'html_text' is the object we want to scrap
    # 'lxml' is the parse 'mode'
    soup = BeautifulSoup(texto_html, 'lxml')

    # now we select via 'find()' soup method in html the element we want to
    # look apart which is 'li' tag, "clearfix job-bx wht-shd-bx" element.
    empregos = soup.find_all('li', class_="clearfix job-bx wht-shd-bx")

    # for loop to interate through every job and execute the commands below
    for emprego in empregos:
        published_date = emprego.find('span', class_='sim-posted').span.text

        # check if published date has 'few' word in it.
        if 'few' in published_date:

            # search for 'h3' tag inside job object. 
            # we use .text for getting only text elements. excluding html symbols.
            # then we use replace method to exclude the white spaces when printings.
            nome_empresa = emprego.find('h3', class_= 'joblist-comp-name').text.replace(' ', '')

            # seach for skill requeriments inside each job.
            # its insite 'span' class with the name 'class="srp-skills"'
            habilidades = emprego.find('span', class_="srp-skills").text.replace(' ', '')

            # seach for link in each job post
            mais_infos = emprego.header.h2.a['href']

            # cretae condition to write the options
            # it will include only the skills im familiar 

            if habilidade_faltante not in habilidades:

                # send the job to whatsapp number chosen
                pywhatkit.sendwhatmsg_instantly(numero_whats ,f'Nome da Empresa:{nome_empresa} Habilidades:{habilidades} Mais_infos:{mais_infos}', 10, True, 3)
                time.sleep(10)

                
                cursor = connector.cursor()
                qry = 'INSERT INTO users (id, nome_empresa, habilidades, mais_infos) VALUES (%s, %s, %s)'
                val = (nome_empresa, habilidades, mais_infos)
                cursor.execute(qry, val)
                connector.commit()

                with open(f'posts/posts.txt', 'a') as f:
                    f.write(f'company name: {nome_empresa.strip()}\n')
                    f.write(f'skills: {habilidades.strip()}\n')
                    f.write(f'more info: {mais_infos}\n')
                    time.sleep(5)
                    f.write("\n")
            
    connector.close()


# create a condition to make the function runs
if __name__ == '__main__':
    while True:
        encontre_empregos()
        time_wait = 10
        print(f'waiting {time_wait} minutos')
        time.sleep(time_wait * 60)
