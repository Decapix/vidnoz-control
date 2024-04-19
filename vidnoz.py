"""pour linux ou windows, dans tous les cas, seras firefox"""

import re
import shutil
import time
import platform
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import os
import json
import socket
import pygame

# python 3.12
# pip install selenium  playsound  pathlib

os_name = platform.system().lower()
BASE_DIR = Path(__file__).resolve().parent

pygame.init()
pygame.mixer.init()
sound = pygame.mixer.Sound(BASE_DIR / 'son.mp3')

# Lire le fichier JSON
with open('identifiant.json', 'r') as file:
    data = json.load(file)



def lister_fichiers(dossier):
    # Récupérer la liste des fichiers
    fichiers = [f for f in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, f))]
    return fichiers

def get_ip_address():
    try:
        # On crée un socket pour communiquer avec un serveur distant
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # On essaie de se connecter au serveur (ne s'établit pas réellement pour UDP)
        s.connect(("8.8.8.8", 80))  # Google DNS, ou un autre serveur fiable
        ip = s.getsockname()[0]  # On récupère l'adresse IP du socket
        s.close()  # On ferme le socket
        return ip
    except Exception as e:
        return "Erreur lors de la récupération de l'IP: " + str(e)


def driver_ip():
    if os_name == "linux":
        path_to_driver = BASE_DIR / 'geckodriver_linux'  # Chemin pour Linux
        service = FirefoxService(executable_path=path_to_driver)
        driver = webdriver.Firefox(service=service)
    elif os_name == "windows":
        path_to_driver = BASE_DIR / 'geckodriver_win.exe'  # Chemin pour Linux
        service = FirefoxService(executable_path=path_to_driver)
        driver = webdriver.Firefox(service=service)

    # change ip with proxy
    return driver


def go_firfox_upload(driver, email, password, video_src, tete_path):
        driver.get('https://www.vidnoz.com/face-swap.html')
        time.sleep(0.3)
        print("Lancement de firefox, on attend, ne touche a rien")
        try:
            # Ajustez le temps d'attente selon les besoins
            wait = WebDriverWait(driver, 10)  # Attendre jusqu'à 10 secondes
            button3 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[tabname="tab_video"]')))            # button3 = driver.find_element(By.XPATH, '//div[@class="tiktok-info"]/a[contains(@class, "download-btn")][1]')
            button3.click()
        except TimeoutException:
            print("Le bouton n'était pas cliquable après 10 secondes d'attente.")

        time.sleep(0.3)

        try:
            wait = WebDriverWait(driver, 10)

            # Utilisez JavaScript pour envoyer le chemin du fichier directement à l'input de fichier
            file_input_xpath = "//div[@class='video_step video_step1']//input[@type='file']"
            file_input = wait.until(EC.presence_of_element_located((By.XPATH, file_input_xpath)))
            driver.execute_script("arguments[0].style.display = 'block';", file_input)  # Assurez-vous que l'input est visible
            file_input.send_keys(video_src)

             # Attendez brièvement que la fenêtre de sélection de fichier apparaisse
            WebDriverWait(driver, 0.2)  # Vous pouvez ajuster le délai selon le comportement observé

            # Envoyer la touche Échap pour fermer la fenêtre de sélection de fichier
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        except TimeoutException as e:
            print("Le formulaire de video n'a pas été trouvé, on arrete")
            print(f"Erreur : {e}")
            # Simuler la pression de la touche "Entrée"
        
        time.sleep(0.3)
         
        try:
            wait = WebDriverWait(driver, 10)

            # Utilisez JavaScript pour envoyer le chemin du fichier directement à l'input de fichier
            file_input_xpath = "//div[@class='video_step video_step2']//input[@type='file']"
            file_input = wait.until(EC.presence_of_element_located((By.XPATH, file_input_xpath)))
            driver.execute_script("arguments[0].style.display = 'block';", file_input)  # Assurez-vous que l'input est visible
            file_input.send_keys(tete_path)

             # Attendez brièvement que la fenêtre de sélection de fichier apparaisse
            WebDriverWait(driver, 0.2)  # Vous pouvez ajuster le délai selon le comportement observé

            # Envoyer la touche Échap pour fermer la fenêtre de sélection de fichier
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        except TimeoutException as e:
            print("Le formulaire d'image n'a pas été trouvé, on arrete")
            print(f"Erreur : {e}")

        
        try:
            time.sleep(3.5)
            wait = WebDriverWait(driver, 10) 

            # Trouver le bouton de soumission
            button_submite_xpath_image = "//div[@class='v_step3_btn_submit']"
            button_submit = wait.until(EC.presence_of_element_located((By.XPATH, button_submite_xpath_image)))
                        
            # Attendre que le bouton soit vraiment cliquable
            wait.until(EC.element_to_be_clickable((By.XPATH, button_submite_xpath_image)))

            # Essayer de cliquer avec JavaScript si le bouton est obscurci
            driver.execute_script("arguments[0].click();", button_submit)
            print("bouton cliquer")
        except TimeoutException as e:
            print("Le bouton d'envoie n'a pas été trouvé, on arrete")
            print(f"Erreur : {e}")
            # Simuler la pression de la touche "Entrée"
        
        print("on attend le bouton de telechargement...")
        # connect
        while True:
            try:
                # Essayer de trouver l'élément "div id="v_controls_Download""
                download_button = driver.find_element(By.ID, "v_controls_Download")
                if download_button:
                    # Si l'élément est trouvé, cliquez dessus
                    download_button.click()
                    print("traitement finis")
                    break  # Sortir de la boucle après le clic
            except Exception as e:
                time.sleep(5)  # Attendre 5 secondes avant de réessayer
                print("pendant cette attente, tous en coeurs : Vive les fourmis !")

        


        try:
            wait = WebDriverWait(driver, 10)

            # Utilisez JavaScript pour envoyer le chemin du fichier directement à l'input de fichier
            login_xpath = "//div[@class='login-input-box error-tip-box']//input[@type='email']"
            login = wait.until(EC.presence_of_element_located((By.XPATH, login_xpath)))
            driver.execute_script("arguments[0].style.display = 'block';", login)  # Assurez-vous que l'input est visible
            login.send_keys(email)
             # Attendez brièvement que la fenêtre de sélection de fichier apparaisse
            WebDriverWait(driver, 0.2)  # Vous pouvez ajuster le délai selon le comportement observé
        except TimeoutException as e:
            print("Le formulaire d'email n'a pas été trouvé, saisit le toi meme, tu as 20 sc")
            print(f"Erreur : {e}")
            time.sleep(20)
        
        time.sleep(2)

        try:
            wait = WebDriverWait(driver, 10) 
            # Trouver le bouton de soumission
            button_submite_login_xpath_image = "//button[@class='pointer submit-btn login-submit bingClickBtn1']"
            button_submit_login = wait.until(EC.presence_of_element_located((By.XPATH, button_submite_login_xpath_image)))
                        
            # Attendre que le bouton soit vraiment cliquable
            wait.until(EC.element_to_be_clickable((By.XPATH, button_submite_login_xpath_image)))

            # Essayer de cliquer avec JavaScript si le bouton est obscurci
            driver.execute_script("arguments[0].click();", button_submit_login)
            print("bouton cliquer login email")
        except TimeoutException as e:
            print("Le bouton d'envoie n'a pas été trouvé, on arrete")
            print(f"Erreur : {e}")
            # Simuler la pression de la touche "Entrée"
        
        # page d'apres la connectiom
    
        try:
            wait = WebDriverWait(driver, 10)

            # Utilisez JavaScript pour envoyer le chemin du fichier directement à l'input de fichier
            login_password_xpath = "//input[@type='password']"
            login_password = wait.until(EC.presence_of_element_located((By.XPATH, login_password_xpath)))
            driver.execute_script("arguments[0].style.display = 'block';", file_input)  # Assurez-vous que l'input est visible
            login_password.send_keys(password)
             # Attendez brièvement que la fenêtre de sélection de fichier apparaisse
            WebDriverWait(driver, 0.2)  # Vous pouvez ajuster le délai selon le comportement observé
        except TimeoutException as e:
            print("Le formulaire de mot de passe n'a pas été trouvé, saisit le toi meme, tu as 20 sc")
            print(f"Erreur : {e}")
            time.sleep(20)

        # on attend 15 sc
        # print("met le code de verification \n ne clique pas sur le bouton")
        # time.sleep(12)
        """
        try:
            wait = WebDriverWait(driver, 10) 
            # Trouver le bouton de soumission
            button_submite_password_xpath_image = "//button[@class='pointer submit-btn login-account-btn bingClickBtn6']"
            button_submit_password = wait.until(EC.presence_of_element_located((By.XPATH, button_submite_password_xpath_image)))
                        
            # Attendre que le bouton soit vraiment cliquable
            wait.until(EC.element_to_be_clickable((By.XPATH, button_submite_password_xpath_image)))

            # Essayer de cliquer avec JavaScript si le bouton est obscurci
            driver.execute_script("arguments[0].click();", button_submit_password)
            print("bouton cliquer login email")
        except TimeoutException as e:
            print("Le bouton d'envoie n'a pas été trouvé, on arrete")
            print(f"Erreur : {e}")
            # Simuler la pression de la touche "Entrée"

        """
        # time.sleep(12)
        sound.play()
        print("Mets le code de vérification, ensuite clique sur login et telecharge la video, ne ferme pas la fenetre du navigauteur et ne deplace pas la video\n")

        input("Appuie sur n'importe quelle touche quand tu as finis...")
        
        """
        while True:
            try:
                
                wait = WebDriverWait(driver, 10) 
                # Trouver le bouton de soumission
                button_submite_password_xpath_image = "//button[@class='pointer submit-btn login-account-btn bingClickBtn6']"
                button_submit_password = wait.until(EC.presence_of_element_located((By.XPATH, button_submite_password_xpath_image)))
                            
                # Attendre que le bouton soit vraiment cliquable
                wait.until(EC.element_to_be_clickable((By.XPATH, button_submite_password_xpath_image)))

                # Essayer de cliquer avec JavaScript si le bouton est obscurci
                driver.execute_script("arguments[0].click();", button_submit_password)
                break
            except Exception as e:
                try:
                    wait = WebDriverWait(driver, 10) 
                    # Trouver le bouton de soumission
                    button_ok_xpath_image = "//div[@class='v_button_ok']"
                    button_ok = wait.until(EC.presence_of_element_located((By.XPATH, button_ok_xpath_image)))
                                
                    # Attendre que le bouton soit vraiment cliquable
                    wait.until(EC.element_to_be_clickable((By.XPATH, button_ok_xpath_image)))

                    # Essayer de cliquer avec JavaScript si le bouton est obscurci
                    driver.execute_script("arguments[0].click();", button_ok)
                    break
                except TimeoutException as e:
                    time.sleep(12)  # Attendre 12 secondes avant de réessayer
                    print("vielle brele, met le code de verification, tu as re-12 sc \n ne clique pas sur le bouton")
                time.sleep(12)  # Attendre 12 secondes avant de réessayer
                print("vielle brele, met le code de verification, tu as re-12 sc \n ne clique pas sur le bouton")
        
        """
        print("fin du programe firefox")
        driver.quit()




def change_file_location(target_folder, number):

    download_folder = data['download_folder']
    # Assurez-vous que le dossier cible existe
    Path(target_folder).mkdir(parents=True, exist_ok=True)

    # Trouver tous les fichiers .mp4 dans le dossier de téléchargement
    mp4_files = [f for f in Path(download_folder).glob('*.mp4')]

    # Trier les fichiers par date de modification, les plus récents en premier
    mp4_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    # Sélectionner les x derniers fichiers
    latest_files = mp4_files[:1]

    # Déplacer et renommer les fichiers
    for file in latest_files:
        new_filename = f"tiktok-{number}.mp4"
        new_filepath = Path(target_folder) / new_filename

        # Vérifier si le fichier existe déjà et modifier le nom si nécessaire
        while new_filepath.exists():
            number += 1  # Incrémenter le compteur si le fichier existe
            new_filename = f"tiktok-{number}.mp4"
            new_filepath = Path(target_folder) / new_filename

        # Déplacer et renommer le fichier
        shutil.move(str(file), str(new_filepath))
    


def check_update_ip(ip_address):
    sound.play()
    print("change ton address ip, tu as tous le temps que tu veux \n apres ne fait rien, le programme va detecter le changement d'ip")
    while True:
        if ip_address == get_ip_address() :
            time.sleep(7)
        else :
            print("Changement d'ip detecté")
            break

def get_number_in_file_name(file_name):
    # Utilisation d'une expression régulière pour trouver des chiffres après "back"
    match = re.search(r"back\s+(\d+)", file_name, re.IGNORECASE)
    if match:
        return match.group(1)  # Retourner le premier groupe de chiffres trouvé
    return None  # Retourner None si aucun chiffre n'est trouvé

    
def main():
    chemin_base_image = input("Veuillez saisir le chemin du fichier source (sa tete) :\n")
    chemin_destination_back = input("Veuillez saisir le chemin ou vous voulez que les video se telecharge (une fois deepfaker):\n")
    chemin = input("Veuillez saisir le chemin du dossier :\n")
    try:
        fichiers = lister_fichiers(chemin)
        if not fichiers:
            print("Aucun fichier trouvé dans le dossier.")
            return
        
        # Afficher les fichiers avec des numéros
        print("Saisissez les éléments que vous voulez :")
        for index, fichier in enumerate(fichiers, start=1):
            print(f"{fichier} ↦ {index}")
        
        # Lire les choix de l'utilisateur
        choix = input()
        numeros_choisis = set(map(int, choix.split()))
        
        # Sélectionner les fichiers correspondant aux numéros choisis
        fichiers_selectionnes = [fichiers[i - 1] for i in numeros_choisis if 1 <= i <= len(fichiers)]
        
        # Afficher les fichiers sélectionnés
        print("Voici les fichiers sélectionnés :")
        for fichier in fichiers_selectionnes:
            print(fichier)

        email = data['email']
        password = data['password']
    
        for index, vid in enumerate(fichiers_selectionnes):
            file_back_name = str(vid)
            number = int(get_number_in_file_name(file_back_name))
            ip_address = get_ip_address()
            driver = driver_ip()
            video_path = os.path.join(chemin, vid)
            go_firfox_upload(driver, email, password, video_path, chemin_base_image)
            change_file_location(chemin_destination_back, number)
            
            # Vérifiez si l'élément courant n'est pas le dernier
            if index != len(fichiers_selectionnes) - 1:
                check_update_ip(ip_address)



    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    main()

