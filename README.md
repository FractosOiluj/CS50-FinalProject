# Job Scraper
#### Video Demo: https://www.youtube.com/watch?v=gsWrHq4-A1Y
#### Description:

For this project i tried to solve a very big problem im facing right now, which is to find a job in the tech industry. One of the main problems i find is that there are to many job options, many of them requiring skills that i dont have. 

Another problem ive found is that there are diferent job requisites for sometimes the same job positons. so i think that if i create a database with job position and the skills it demands i could me more aware of the main abilities i need to improve.

first the user will input some skill that he dont have. and his phone number so the script can send him msg via whatsapp with the information we defined.

My project is a webscraper that scraps a especift web page that list many job positions. First the script is going to download all the html information. then it will parse it using 'lxml' mode with the BeautifulSoup method.

After that we are going to create a variable that will store every element that is inside especific tags that refers to the job postion, skills required and link for registration.

For each element inside the tags we defined, the script will filter only the jobs that were posted few days ago. 'cause we wanto to analyse only the most recent ones.
it the option matches with our requeriments, the script will go on creating 3 variables that will store respectivily : company_name, skills_required and link for registration.

After that we are going to define another IF statement to filter only the jobs that requires skills that we do have. excluding all skills that we dont. if all requisited are satisfied the script is going to send the whatsapp msg for the user, then it will save the information in a exeternal data base for future improviments and it also is going to create a file.txt with the information we defined earlier.


For this project i used the following tech:
1. dell notebook i5, 8gb ram.
2. windows 10;
3. python (latest version)
4. Requests library
5. BeautifulSoup library
6. pywhatkit library
7. time library
8. mysql-connector library.

For this job executing i followed the following steps:

1. Virtual enviroment activation;
2. pip install the dependencies above listed.
3. then we created a Mysql DATABASE in wwww.freesqldatabase.com, its a temporary database just for learning porpouse. its licence expires in 7 days.


the project body:

First we install the libraries >

import requests
from bs4 import BeautifulSoup
import time
import pywhatkit
import mysql.connector

then we ask for input from user > 

print('digite uma habilidade que você não é familiarizado')
habilidade_faltante = input('>')
print('digite um número para o qual as ofertas serão enviadas')
numero_whats = input('digite no formato: +000.00.0000000. >')
print("em breve o robô enviará a mensagem via whatsap..")

then we connect to our external DATABASE > 

connector = mysql.connector.connect(user='sql10585660',
                                    password='8x7X382pdd',
                                    host='sql10.freesqldatabase.com',
                                    database='Users')
                                    

now we use the 'get' method from requests to get all information from especift html page >

texto_html = requests.get('URL').text

we use '.text' at the end to filter the text only.

then we create a beautiful Instance. 'html_text' is the object we want to scrap, 'lxml' is the parse 'mode'.

soup = BeautifulSoup(texto_html, 'lxml')

now we select via 'find()' soup method in html the element we want to look apart which is 'li' tag, "clearfix job-bx wht-shd-bx" element.

empregos = soup.find_all('li', class_="clearfix job-bx wht-shd-bx")

for loop to interate through every job and execute the commands below
for emprego in empregos:
        published_date = emprego.find('span', class_='sim-posted').span.text

check if published date has 'few' word in it.
        if 'few' in published_date:
        
             search for 'h3' tag inside job object. 
             we use .text for getting only text elements. excluding html symbols.
             then we use replace method to exclude the white spaces when printings.
            nome_empresa = emprego.find('h3', class_= 'joblist-comp-name').text.replace(' ', '')

             seach for skill requeriments inside each job.
             its insite 'span' class with the name 'class="srp-skills"'
            habilidades = emprego.find('span', class_="srp-skills").text.replace(' ', '')

             seach for link in each job post
            mais_infos = emprego.header.h2.a['href']

             cretae condition to write the options
             it will include only the skills im familiar 
 
 
 if habilidade_faltante not in habilidades:

                 send the job to whatsapp number chosen
                pywhatkit.sendwhatmsg_instantly(numero_whats ,f'Nome da Empresa:{nome_empresa} Habilidades:{habilidades} Mais_infos:{mais_infos}', 10, True, 3)
                time.sleep(10)


                create a cursor and then insert our information in the external database as follows >
                cursor = connector.cursor()
                qry = 'INSERT INTO users (id, nome_empresa, habilidades, mais_infos) VALUES (%s, %s, %s)'
                val = (nome_empresa, habilidades, mais_infos)
                cursor.execute(qry, val)
                connector.commit()

            
                crete and save the infomration on a file.txt
              
                with open(f'posts/posts.txt', 'a') as f:
                    f.write(f'company name: {nome_empresa.strip()}\n')
                    f.write(f'skills: {habilidades.strip()}\n')
                    f.write(f'more info: {mais_infos}\n')
                    time.sleep(5)
                    f.write("\n")
            
    connector.close()


create a condition to make the function runs at especified time period

if __name__ == '__main__':
    while True:
        encontre_empregos()
        time_wait = 10
        print(f'waiting {time_wait} minutos')
        time.sleep(time_wait * 60)
 




