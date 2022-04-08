import mysql.connector

# paramètre de connexion avec la bdd
db = mysql.connector.connect(
    host="192.168.0.120",
    user="py_con",
    password="pesquierPY",
    database="monitoring_pesquiers"
)
i = 1 # nombre de départ
nb_capteur = 2 # nombre de capteur

while i <= nb_capteur:

    request = "SELECT `value` FROM `sensorsValues` WHERE `sensor_id`=" + str(i) + " ORDER BY id DESC LIMIT 1" # requete pour observer la valeur du capteur dans la table
    comp = "SELECT `comparateur` FROM `alerts` WHERE `sensor_id`=" + str(i) # requete pour observer le nombre que je dois comparer dans la table 
    sign = "SELECT `signe` FROM `alerts` WHERE `sensor_id`=" + str(i) # requete pour observer dans la table le signe de comparaison

    cursor = db.cursor()  # configure un curseur sur la bdd
    cursor.execute(comp)  # execute ma requete
    comparateur = cursor.fetchall()  # récupère la valeur maximum ou minimum atteignable
    cursor.close() # ferme le curseur

    cursor = db.cursor()  # configure un curseur sur la bdd
    cursor.execute(sign)  # execute ma requete
    signe = cursor.fetchall()  # récupère le signe de comparaison
    cursor.close() # ferme le curseur

    cursor = db.cursor()  # configure un curseur sur la bdd
    cursor.execute(request)  # execute ma requete
    resultats = cursor.fetchall()  # récupère la valeur reçu du capteur
    cursor.close() # ferme le curseur
    
    condition = str(resultats[0][0])+str(signe[0][0])+"="+str(comparateur[0][0]) # condition de comparaison
    y = 1
    while y < int(len(signe)): # si j'ai plus d'un signe dans la table alors j'ajoute une nouvelle condition
        condition2 = str(resultats[0][0])+str(signe[y][0])+"="+str(comparateur[y][0]) 
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
        f=open("message.txt", mode="a") # ouvre le fichier message.txt en mode écriture ("C:\Users\Corentin\message.txt")
        f.write("balise_id="+str(balise_id[0][0])+","+str(condition)) # affiche le numéro de la balise
        f.write('\n') # saute une ligne
        f.close() # ferme le fichier
    else:
        print("erreur")
    i = i+1

db.close()
