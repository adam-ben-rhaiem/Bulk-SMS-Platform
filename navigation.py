from selenium import webdriver
import random
import time
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import tkinter as tk




fenetre=tk.Tk()

fenetre.geometry('400x400')

message_a_envoyer=''
numero_debut=''
numero_fin=''
filtre_par_domaine=[]
filtre_par_proffession=[]
contacts=[]
f=0

def deteruire_fenetre():
  fenetre.destroy()

def enlever_filtre(filtre,filtrex,x):
  global filtre_par_proffession,filtre_par_domaine
  filtre.pack_forget()
  filtrex.pack_forget()
  try:
    filtre_par_domaine.remove(x)
  except:
    filtre_par_proffession.remove(x)
  


def filtrer_domaine(x):
  global boite_filtre,filtre_par_domaine
  filtre=tk.Button(boite_filtre,text=x)
  filtre.pack(side='left')
  filtrex=tk.Button(boite_filtre,text='x',command=lambda:enlever_filtre(filtre,filtrex,x),bg='red')
  filtrex.pack(side='left')
  filtre_par_domaine.append(x)

def filtrer_proffession(x):
  global boite_filtre,filtre_par_proffession
  filtre=tk.Button(boite_filtre,text=x)
  filtre.pack(side='left')
  filtrex=tk.Button(boite_filtre,text='x',command=lambda:enlever_filtre(filtre,filtrex,x),bg='red')
  filtrex.pack(side='left')
  filtre_par_proffession.append(x)

def filtrer_numero():
  global boite_filtre,f

  button=tk.Button(boite_filtre,text='x',command=lambda:enlever_filtre_num(label1,zone_numero_de_debut,label2,zone_numero_de_fin,button),bg='red')
  button.pack(side='right')

  label1=tk.Label(boite_filtre,text='De ce numéro')
  label1.pack()
  
  zone_numero_de_debut=tk.Entry(boite_filtre,textvariable=numero1)
  zone_numero_de_debut.pack()

  label2=tk.Label(boite_filtre,text='jusqua ce numéro')
  label2.pack()

  zone_numero_de_fin=tk.Entry(boite_filtre,textvariable=numero2)
  zone_numero_de_fin.pack()

  f=1
def enlever_filtre_num(label1,zone_numero_de_debut,label2,zone_numero_de_fin,button):
  global f
  label1.destroy()
  label2.destroy()
  zone_numero_de_debut.destroy()
  zone_numero_de_fin.destroy()
  button.destroy()
  f=0


  

def Envoyer():
  global message_a_envoyer,numero_debut,numero_fin,contacts,fenetre
  message_a_envoyer=message_saisie.get()

  if f==1:
    numero_debut=numero1.get()
    numero_fin=numero2.get()
    if (numero_debut!='') and (numero_fin!=''):
      if int(numero_debut)>int(numero_fin):
        fenetre_error1()
      else:  
        fenetre.destroy()# fermer la fenètre
        for num in range(int(numero_debut),int(numero_fin)+1):
          contacts.append(str(num))
      
        # creer une variable pour le declencher le driver
        driver= webdriver.Chrome()
        driver.get("https://messages.google.com/web/conversations")

        wait = WebDriverWait(driver, 30)
        for contact in contacts:
          # creer un nouvelle converstation
          conversation = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fab-label")))
          conversation.click()

          # insérer le numéro de contact
          search_contact = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".input")))
          search_contact.send_keys(contact)
            
          # choisir le contact
          send_to_number = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".selector-container")))
          send_to_number.click()
            
          # ecrire le message
          zone_de_message = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.input")))
          zone_de_message.send_keys(message_a_envoyer)

          # envoyer le message
          click_on_next = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".floating-button")))
          click_on_next.click()

          time.sleep(random.uniform(0.1,1))  
    else:
      fenetre_error2()    
  else:
    fenetre.destroy()# fermer la fenètre
    cnx=sqlite3.connect('Num_DB.db')
    cur= cnx.cursor() # c'est pour executer des requète sql et récuperer des résultats

    commande=f"Select Numero FROM base_de_test "
    if len(filtre_par_domaine)!=0:
      commande+=f"WHERE "
      for i in range(len(filtre_par_domaine)-1):
        commande=commande+f" Domaine = '{filtre_par_domaine[i]}'"+f" OR"
      commande=commande+f" Domaine = '{filtre_par_domaine[-1]}'"
    if len(filtre_par_proffession)!=0:
      if len(filtre_par_domaine)!=0:
        commande=commande+f" OR"
      else:
        commande+=f"WHERE "  
      for i in range(len(filtre_par_proffession)-1):
        commande=commande+f" Proffession = '{filtre_par_proffession[i]}'"+f" OR"
      commande=commande+f" Proffession = '{filtre_par_proffession[-1]}'"

    res= cur.execute(commande) # extraire les contacts de la base de données

    contacts=res.fetchall() # mettre les contacts dans une liste
    cnx.close()
    if len(contacts)==0 :
      fenetre=tk.Tk()
      label=tk.Label(fenetre,text='Aucun numero est trouvé')
      label.pack()
      button_exit=tk.Button(fenetre,text='Fermer',command=deteruire_fenetre)
      button_exit.pack()
      fenetre.mainloop()
    else:
      # creer une variable pour le declencher le driver
      driver= webdriver.Chrome()
      driver.get("https://messages.google.com/web/conversations")

      wait = WebDriverWait(driver, 30)
      for contact in contacts:
        # creer un nouvelle converstation
        conversation = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fab-label")))
        conversation.click()

        # insérer le numéro de contact
        search_contact = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".input")))
        search_contact.send_keys(contact[0])
          
        # choisir le contact
        send_to_number = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".selector-container")))
        send_to_number.click()
          
        # ecrire le message
        zone_de_message = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.input")))
        zone_de_message.send_keys(message_a_envoyer)

        # envoyer le message
        click_on_next = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".floating-button")))
        click_on_next.click()

        time.sleep(random.uniform(0.1,1))


def fenetre_error1():
  window_error=tk.Tk()
  error_label=tk.Label(window_error,text='le premier numero doit etre inferieur ou égale au deuxieme')
  error_label.pack()
  window_error.mainloop
def fenetre_error2():
  window_error=tk.Tk()
  error_label=tk.Label(window_error,text='un ou les 2 champs sont vides')
  error_label.pack()
  window_error.mainloop

mon_menu=tk.Menu(fenetre)

# la sous-onglet
option_envoi=tk.Menu(mon_menu,tearoff=0)

# sous sous-onglet
tire_par=tk.Menu(option_envoi,tearoff=0)


# sous sous sous-onglets
profession=tk.Menu(tire_par,tearoff=0)
profession.add_command(label='Médcins',command=lambda:filtrer_proffession('Médcin'))
profession.add_command(label='Pharmacien',command=lambda:filtrer_proffession('Pharmacien'))
profession.add_command(label='Developeur',command=lambda:filtrer_proffession('Developeur'))


domaine=tk.Menu(tire_par,tearoff=0)
domaine.add_command(label='Medical',command=lambda:filtrer_domaine('Medical'))
domaine.add_command(label='Télécommunication',command=lambda:filtrer_domaine('Télécommunication'))
domaine.add_command(label='Finaciaire',command=lambda:filtrer_domaine('Finaciaire'))

numero=tk.Menu(tire_par,tearoff=0)
numero.add_command(label='Intervale')
numero.add_command(label='Pharmacien')
numero.add_command(label='Developeur')

mon_menu.add_cascade(label='Option d envoi',menu=option_envoi) # la principale onglet
option_envoi.add_cascade(label='tiré par',menu=tire_par)
tire_par.add_cascade(label='Proffession',menu=profession)
tire_par.add_cascade(label='Domaine d activité',menu=domaine)
tire_par.add_command(label='Numero de téléphone',command=filtrer_numero)








fenetre.config(menu=mon_menu) # afficher le menu


message_saisie=tk.StringVar()
numero1=tk.StringVar()
numero2=tk.StringVar()

boite_filtre=tk.Frame(fenetre,bg='yellow')
boite_filtre.pack()

label=tk.Label(fenetre,text='Saisir votre message à envoyer')
label.pack()

zone_de_saisir=tk.Entry(fenetre,textvariable=message_saisie)
zone_de_saisir.pack()

button_envoie=tk.Button(fenetre,text='envoyer',command=Envoyer)
button_envoie.pack()


fenetre.mainloop()
 














 