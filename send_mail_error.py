#! /usr/bin/python3.9
from datetime import datetime
import time #date et heure
from time import sleep #faire des pauses
import mysql.connector #connexion avec la bdd
import pathlib #pour avoir le chemin du script
from email.mime.multipart import MIMEMultipart #pour envoyer un mail
from email.mime.text import MIMEText #pour envoyer un mail
import smtplib #pour envoyer un mail
import re #pour les adapter mon message

path=pathlib.Path("send_mail_error.py").parent.absolute()#récupère le chemin du programme
path=str(path)#converti le chemin en string
#print(path) #débugage pour voir le chemin

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

id_max="SELECT MAX(sensor_id) FROM `listSensors`"#requete pour récupérer le nombre de capteur
cursor = db.cursor()  # configure un curseur sur la bdd
cursor.execute(id_max)  # execute ma requete
nb_capteur = cursor.fetchall()  # récupère la valeur maximum ou minimum atteignable
cursor.close() # ferme le curseur


#print (nb_capteur[0][0])#débugage
nb_capteur = int(nb_capteur[0][0]) # nombre de capteur
id = 1 # numéro d'ID dans la table

while id <= nb_capteur:

    request_sensor = "SELECT `value` FROM `sensorsValues` WHERE `sensor_id`=" + str(id) + " ORDER BY id DESC LIMIT 1" # requete pour observer la valeur du capteur dans la table
    valeur_comparant = "SELECT `control` FROM `alerts` WHERE `sensor_id`=" + str(id) # requete pour observer le nombre que je dois comparer dans la table 
    sup_or_inf = "SELECT `sign` FROM `alerts` WHERE `sensor_id`=" + str(id) # requete pour observer dans la table le signe de comparaison

    cursor = db.cursor()  # configure un curseur sur la bdd
    cursor.execute(valeur_comparant)  # execute ma requete
    control = cursor.fetchall()  # récupère la valeur maximum ou minimum atteignable
    cursor.close() # ferme le curseur

    cursor = db.cursor()  # configure un curseur sur la bdd
    cursor.execute(sup_or_inf)  # execute ma requete
    signe = cursor.fetchall()  # récupère le signe de comparaison
    cursor.close() # ferme le curseur

    cursor = db.cursor()  # configure un curseur sur la bdd
    cursor.execute(request_sensor)  # execute ma requete
    resultats = cursor.fetchall()  # récupère la valeur reçu du capteur
    cursor.close() # ferme le curseur
    #print(resultats)#débugage
    #print(signe)#débugage
    #print(control)#débugage
    #print("j'ai fait les cursors")#débugage pour voir si tout va bien
    
    if(signe==[] or resultats==[] or control==[]): # si une des valeurs est vide:
        print("pas de valeur")#en cas d'aucune valeur reçu
        id+=1
    else:
        condition = str(resultats[0][0])+str(signe[0][0])+"="+str(control[0][0]) # condition de comparaison
        nb_signe = 1
        while nb_signe < int(len(signe)): # si j'ai plus d'un signe dans la table alors j'ajoute une nouvelle condition
            condition2 = str(resultats[0][0])+str(signe[nb_signe][0])+"="+str(control[nb_signe][0]) 
            condition=condition+" and "+condition2 # ajout de ma deuxième condition
            nb_signe +=1 # ferme la boucle
            
        #print("condition="+str(condition)) # débugage affiche la condition
        verif = eval(condition) # évalue la condition (rend True ou False)
        print(verif) # débugage affiche le résultat de la condition


        #si pas d'alerte:
        if verif == True: # si verif me ressort True alors ma valeur est dans les bonnes bornes
            print("pas de mail envoyé")

        #en cas d'alerte:
        elif verif == False: # si verif me ressort False alors ma valeur est en dehors des bonnes bornes je dois donc envoyer un mail d'alerte

            req_balise_id = "SELECT `balise_id` FROM `sensorsValues` WHERE `sensor_id`=" + str(id) + " ORDER BY id DESC LIMIT 1" # requete pour observer la valeur du capteur dans la table
            cursor = db.cursor()  # configure un curseur sur la bdd
            cursor.execute(req_balise_id)  # execute ma requete
            num_balise = cursor.fetchall()  # récupère la valeur reçu du capteur
            cursor.close() # ferme le curseur
            num_balise=str(num_balise[0][0]) # converti la valeur en string
            #print("num balise="+num_balise) # débugage affiche la valeur de la balise

            req_name_balise="SELECT `name` FROM `listBalise` WHERE `balise_id`=" + num_balise # trouve le numéro de la balise

            cursor = db.cursor()  # configure un curseur sur la bdd
            cursor.execute(req_name_balise)  # execute ma requete
            name = cursor.fetchall()  # récupère la valeur reçu par ma requête
            cursor.close() # ferme le curseur
            #print("name balise="+str(name[0][0])) #débug affiche le nom de la balise")

            req_name_sensor="SELECT `name` FROM `listSensors` WHERE `sensor_id`=" + str(id) # trouve le numéro de la balise
            print(req_name_sensor)
            cursor = db.cursor()  # configure un curseur sur la bdd
            cursor.execute(req_name_sensor)  # execute ma requete
            name = cursor.fetchall()  # récupère la valeur reçu par ma requête
            cursor.close() # ferme le curseur

            #print("name sensor="+str(name)) # débugage affiche le nom de la balise
            request_symbol="SELECT `symbol` FROM `listSensors` WHERE `sensor_id`=" + str(id)#requete pour récupérer le nombre de capteur
            cursor = db.cursor()  # configure un curseur sur la bdd
            cursor.execute(request_symbol)  # execute ma requete
            symbol = cursor.fetchall()  # récupère la valeur maximum ou minimum atteignable
            cursor.close() # ferme le curseur
            #print("symbol="+str(symbol[0][0]))#débug affiche le symbole

            request_unite="SELECT `unit` FROM `listSensors` WHERE `sensor_id`=" + str(id)#requete pour récupérer le nombre de capteur
            cursor = db.cursor()  # configure un curseur sur la bdd
            cursor.execute(request_unite)  # execute ma requete
            unite = cursor.fetchall()  # récupère la valeur maximum ou minimum atteignable
            cursor.close() # ferme le curseur
            #print("unité="+str(unite[0][0]))#débug affiche le symbole
            
            f=open(path+"/message.txt", "a") # ouvre le fichier message.txt en mode écriture ("C:\Users\Corentin\message.txt")
            mess="<li>"+str(name[0][0])+", il y a un problème de "+str(name[0][0])+" car la valeur reçu est de "+str(resultats[0][0])+str(symbol[0][0])+" alors qu'elle devrait être comprise entre "+str(control[0][0])+" et "+str(control[1][0])+" "+str(unite[0][0])+'<br>' # crée le message à envoyer
            mess=str(mess)
            #print("message : "+mess)#débugage affiche le message
            f.write(mess) # affiche le numéro de la balise
            f.close() # ferme le fichier
            print("envoie mail")

        else:
            print("erreur")
        id+=1
        print("fin de boucle")

##########################################################################################################################################
id_max="SELECT MAX(balise_id) FROM `listBalise`"#requete pour récupérer le nombre de capteur
cursor = db.cursor()  # configure un curseur sur la bdd
cursor.execute(id_max)  # execute ma requete
nb_balise = cursor.fetchall()  # récupère la valeur maximum ou minimum atteignable
cursor.close() # ferme le curseur

id_balise=694201 #numéro de la balise à surveiller

id_max="SELECT `battery_level` FROM `listBalise` WHERE `balise_id=`str("#requete pour récupérer le nombre de capteur
cursor = db.cursor()  # configure un curseur sur la bdd
cursor.execute(id_max)  # execute ma requete
nb_capteur = cursor.fetchall()  # récupère la valeur maximum ou minimum atteignable
cursor.close() # ferme le curseur
##########################################################################################################################################

db.close()#ferme la bdd

sleep(1)#attend 1 seconde

f=open(path+"/message.txt", "r") # ouvre le fichier message.txt en mode écriture ("C:\Users\Corentin\message.txt")
body_mess=str(f.readlines()) # lit le fichier
body_mess=re.sub("\[|\'|\]|\"", "",body_mess) # supprime les retours à la ligne
#print(body_mess)#débug affiche le message

msg = MIMEMultipart()#crée un message
msg ['From'] = "envoie.test18@gmail.com"#adresse de l'expéditeur
msg ['To'] = "recoit.test18@gmail.com"#adresse du destinataire
password = "vcdzemogzvalpljz"#mot de passe d'application l'expéditeur
msg['Subject'] = str(datetime.now()) # sujet du message (date et heure)
body = "<p>Une erreur est survenue sur la balise:"+body_mess+"</p>"#corps du message
msg.attach(MIMEText(body, 'html'))#ajoute le corps du message avec le type d'encoage (html)
server = smtplib.SMTP("smtp.gmail.com", 587)#configure le serveur de messagerie (smtp pour gmail)
server.starttls()#active le TLS
server.login(msg['From'], password)#connecte l'expéditeur à son compte
server.sendmail(msg['From'], msg['To'], msg.as_string())#envoie le message
server.quit()#ferme la connexion
f.close()#ferme le fichier