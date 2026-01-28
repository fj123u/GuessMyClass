
import sys, os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_score_options_path():
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    full_path = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), "score", "options.txt")
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    return full_path

import mysql.connector
import random
from shape_creator import *

def connect():
    
    cnx = mysql.connector.connect(
            host="frchassot.fr",
            port=2000,
            user="gmc",
            password="9eyIha9VC_V96bmO",
            database='gmc')
    
    return cnx
    

def create_table(cnx):
    
    cur = cnx.cursor()
    cur.execute('CREATE TABLE accounts (account_name VARCHAR(20) PRIMARY KEY NOT NULL, password TEXT(5) NOT NULL, best_of_5 CHAR, best_of_10 CHAR, best_of_20 CHAR);')
    cur.fetchone()
    
def reset_table(cnx):
    
    cur = cnx.cursor()
    cur.execute('DELETE FROM accounts')
    cur.fetchone()
    

def generate_password(password_lenght=5):
    caracts = "azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN?!12345678990"
    
    password = ""
    for i in range(password_lenght):
        rand = random.randint(0,len(caracts)-1)
        password += caracts[rand]
    return password
    
    
def add_account(cnx, name):
    
    password = ""
        
    cur = cnx.cursor()
    cur.execute(f'SELECT password FROM accounts;')
    passwords = cur.fetchall()
    
    if passwords is None:
        password = generate_password()
    else:
        password = generate_password()
        while password in passwords:
            password = generate_password()
    
    try:
        cur.execute(f"INSERT INTO accounts VALUES ('{name}','{password}','{0}','{0}','{0}');")
        cnx.commit()
        retoursql = cur.fetchone()
    except:
        print("table gmc already have this account_name, please change it")
    
    return password


def get_account_password(cnx, name):
    
    cur = cnx.cursor()
    cur.execute(f'SELECT password FROM accounts WHERE account_name ="{name}";')
    password = cur.fetchone()
    if password:
        return password[0]
    else:
        return "None"



def get_score(cnx, password, nb=5):
    
    cur = cnx.cursor()
    cur.execute(f'SELECT best_of_{nb} FROM accounts WHERE password="{password}";')
    score = cur.fetchone()
    
    return score

def set_score(cnx, password, nb, score):

    cur = cnx.cursor()
    cur.execute(f'UPDATE accounts SET best_of_{nb}={str(score)} WHERE password="{password}";')
    cur.fetchone()


def get_leaderboards(cnx, out_5=True,out_10=True,out_20=True):
        
    if out_5:
        cur = cnx.cursor()
        cur.execute(f"SELECT * FROM accounts ORDER BY best_of_5 DESC LIMIT 20;")
        row = cur.fetchone()
        a1 = []
        c = 1
        height = 20 +100 +10
        while row != None:
            if c<=21:
                b = Shape(None,str(c) + " : " + str(row[0]) + " / Best Score : " + str(row[2]), current_w/3 -15 -10, 40, (15, height +50 +5), 0, (224, 180, 229), False, (resource_path('font/Mighty Souly.ttf'), 35))
            a1.append(b)
            row = cur.fetchone()
            height += 40 + 4
            c += 1
            
    if out_10:
        cur = cnx.cursor()
        cur.execute(f"SELECT * FROM accounts ORDER BY best_of_10 DESC LIMIT 20;")
        row = cur.fetchone()
        a2 = []
        c = 1
        height = 20 +100 +10
        while row != None:
            if c<=21:
                b = Shape(None,str(c) + " : " + str(row[0]) + " / Best Score : " + str(row[3]), current_w/3 -15 -10, 40, (15 +current_w/3 -15 +15, height +50 +5), 0, (224, 180, 229), False, (resource_path('font/Mighty Souly.ttf'), 35))
            a2.append(b)
            row = cur.fetchone()
            height += 40 + 4
            c += 1
            
    if out_20:
        cur = cnx.cursor()
        cur.execute(f"SELECT * FROM accounts ORDER BY best_of_20 DESC LIMIT 20;")
        row = cur.fetchone()
        a3 = []
        c = 1
        height = 20 +100 +10
        while row != None:
            if c<=21:
                b = Shape(None,str(c) + " : " + str(row[0]) + " / Best Score : " + str(row[4]), current_w/3 -15 -10, 40, (15 +current_w/3 -15 +15 +current_w/3 -15 +15, height +50 +5), 0, (224, 180, 229), False, (resource_path('font/Mighty Souly.ttf'), 35))
            a3.append(b)
            row = cur.fetchone()
            height += 40 + 4
            c += 1
            
    return a1, a2, a3
            
def check_pseudo(cnx, pseudo):

    cur = cnx.cursor()
    cur.execute(f'SELECT password FROM accounts WHERE account_name="{pseudo}";')
    result = cur.fetchone()

    if result != None:
        return True
    return False