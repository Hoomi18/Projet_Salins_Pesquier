#! /usr/bin/python3.9
from datetime import datetime
from time import sleep#faire des pauses
import mysql.connector #connexion avec la bdd
import pathlib#pour avoir le chemin du script
from email.mime.multipart import MIMEMultipart#pour envoyer un mail
from email.mime.text import MIMEText#pour envoyer un mail
import smtplib#pour envoyer un mail
import time#date et heure

path=pathlib.Path("send_mail_error.py").parent.absolute()#récupère le chemin du fichier
path=str(path)#converti le chemin en string
print(path)

f=open(path+"/message.txt", mode="w") # ouvre le fichier message.txt en mode écriture ("C:\Users\Corentin\message.txt")
f.write("") # affiche le numéro de la balise
f.close() # ferme le fichier

# paramètre de connexion avec la bdd
db = mysql.connector.connect(
    host="192.168.0.120",
    user="py_con",
    password="pesquierPY",
    database="monitoring_pesquiers"
)

id_max="SELECT MAX(sensor_id) FROM `sensorsValues`"#requete pour récupérer le nombre de capteur
cursor = db.cursor()  # configure un curseur sur la bdd
cursor.execute(id_max)  # execute ma requete
nb_capteur = cursor.fetchall()  # récupère la valeur maximum ou minimum atteignable
cursor.close() # ferme le curseur


i = 1 # numéro d'ID dans la table
print (nb_capteur[0][0])
nb_capteur = int(nb_capteur[0][0]) # nombre de capteur

while i <= nb_capteur:

    request = "SELECT `value` FROM `sensorsValues` WHERE `sensor_id`=" + str(i) + " ORDER BY id DESC LIMIT 1" # requete pour observer la valeur du capteur dans la table
    comp = "SELECT `control` FROM `alerts` WHERE `sensor_id`=" + str(i) # requete pour observer le nombre que je dois comparer dans la table 
    sign = "SELECT `sign` FROM `alerts` WHERE `sensor_id`=" + str(i) # requete pour observer dans la table le signe de comparaison

    cursor = db.cursor()  # configure un curseur sur la bdd
    cursor.execute(comp)  # execute ma requete
    control = cursor.fetchall()  # récupère la valeur maximum ou minimum atteignable
    cursor.close() # ferme le curseur

    cursor = db.cursor()  # configure un curseur sur la bdd
    cursor.execute(sign)  # execute ma requete
    signe = cursor.fetchall()  # récupère le signe de comparaison
    cursor.close() # ferme le curseur

    cursor = db.cursor()  # configure un curseur sur la bdd
    cursor.execute(request)  # execute ma requete
    resultats = cursor.fetchall()  # récupère la valeur reçu du capteur
    cursor.close() # ferme le curseur
    print(resultats)
    print(signe)
    print(control)
    print("j'ai fait les cursors")
    
    if(signe==[] or resultats==[] or control==[]): # si une des valeurs est vide:
        print("pas de valeur")
        i=i+1
    else:
        condition = str(resultats[0][0])+str(signe[0][0])+"="+str(control[0][0]) # condition de comparaison
        y = 1
        while y < int(len(signe)): # si j'ai plus d'un signe dans la table alors j'ajoute une nouvelle condition
            condition2 = str(resultats[0][0])+str(signe[y][0])+"="+str(control[y][0]) 
            condition=condition+" and "+condition2 # ajout de ma deuxième condition
            y = y+1 # ferme la boucle
            
        print("condition="+str(condition)) # affiche la condition
        verif = eval(condition) # évalue la condition (rend True ou False)
        print(verif) # affiche le résultat de la condition

        if verif == True: # si verif me ressort True alors ma valeur est dans les bonnes bornes
            print("pas de mail envoyé")

        elif verif == False: # si verif me ressort False alors ma valeur est en dehors des bonnes bornes je dois donc envoyer un mail d'alerte
            balise_id="SELECT `balise_id` FROM `sensorsValues` WHERE `sensor_id`=" + str(i) + " ORDER BY id DESC LIMIT 1" # trouve le numéro de la balise
            cursor = db.cursor()  # configure un curseur sur la bdd
            cursor.execute(balise_id)  # execute ma requete
            balise_id = cursor.fetchall()  # récupère la valeur reçu par ma requête
            cursor.close() # ferme le curseur

            f=open(path+"/message.txt", "a") # ouvre le fichier message.txt en mode écriture ("C:\Users\Corentin\message.txt")
            mess="balise_id="+str(balise_id[0][0])+","+"sensor_id="+str(i)+","+str(condition)
            mess=str(mess)
            print("message : "+mess)
            f.write(mess) # affiche le numéro de la balise
            f.write('\n') # saute une ligne
            f.close() # ferme le fichier
            print("envoie mail")

        else:
            print("erreur")
        i = i+1
        print("fin de boucle")

db.close()

sleep(1)

f=open(path+"/message.txt", "r") # ouvre le fichier message.txt en mode écriture ("C:\Users\Corentin\message.txt")
body_mess=str(f.readlines()) # lit le fichier
print(body_mess)

msg = MIMEMultipart()
msg ['From'] = "envoie.test18@gmail.com"
msg ['To'] = "recoit.test18@gmail.com"
password = "vcdzemogzvalpljz"
msg['Subject'] = str(datetime.now())
body = body_mess
msg.attach(MIMEText(body, 'html'))
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(msg['From'], password)
server.sendmail(msg['From'], msg['To'], msg.as_string())
server.quit()
f.close()
