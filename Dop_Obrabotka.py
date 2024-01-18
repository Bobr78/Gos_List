import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import folium
import branca
import vincent
import json
import folium.plugins as plugins
import os
import time
import winsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import msvcrt as m
import pyperclip
from selenium.webdriver.support.ui import Select
import csv


def highlight(element, effect_time, color, border): 
    """обводим выбранный элемент рамкой-чисто для отладки/контроля """ 
    driver = element._parent 
    def apply_style(s): 
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", 
                              element, s) 
    original_style = element.get_attribute('style') 
    apply_style("border: {0}px solid {1};".format(border, color)) 
    time.sleep(effect_time) 
    apply_style(original_style)



directory = "C:\\3-14\\Gos\\NP\\"
xxx="C:\\3-14\\Gos\\"
# список поисковых полей
F_Pole1=["Тип дома:", "Год постройки:", "Идентификационный код адреса:"]
F_Pole2=["Управляющая организация:"]
F_Pole3=["МОБИЛЬНЫЕ ТЕЛЕСИСТЕМЫ", "ВЫМПЕЛ-КОММУНИКАЦИИ", "РОСТЕЛЕКОМ", "ТЕЛЕКОМ.РУ"]
        
#инициализация Хрома
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver=webdriver.Chrome(executable_path=xxx+"chromedriver.exe",options=chrome_options )
Action=ActionChains(driver)
driver.implicitly_wait(20)
files = []
files += os.listdir(directory)

dictionary={}

for i in files:
    line = open(directory+i, 'r').readlines()
    for j in range(0,len(line)):
        if line[j].startswith("https:"):
            driver.get(line[j])
            dictionary["Страница"]=line[j].rstrip('\n')
    # для ОТЛАДКИ !!!!!!!!!!!!!
            #driver.get("https://dom.gosuslugi.ru/#!/house-view?guid=6ad5f79e-6c1f-4dae-b6f8-f1a14c0da9b3&typeCode=1")
            
            time.sleep(2)
            driver.execute_script("window.scrollBy(0,500)","")
            # название дома
            
            try:
                text1=driver.find_element(By.XPATH, "/html/body/div[1]/div[8]/div/div/div[1]/h1").text.rstrip('На карте')
                dictionary["Адрес"]=text1.strip()
            except:
                dictionary["Адрес"]="-"


            # предварительный сброс данных в ноль
            for poisk in F_Pole1:
                dictionary[poisk]="-"

            try:
                blok1=driver.find_element(By.XPATH, "/html/body/div[1]/div[8]/div/div/div[2]/div/div/div/div").text.split('\n')
                for m in range(0,len(blok1)):
                    little=blok1[m]
                    for poisk in F_Pole1:
                        q=little.find(poisk)
                        if q!=-1:
                            dictionary[poisk]=little[q+len(poisk):]
            except:
                for poisk in F_Pole1:
                    dictionary[poisk]="!"

            try:                    
                blok2=driver.find_element(By.XPATH, "/html/body/div[1]/div[8]/div/div/div[4]/div/div/div/div[2]/table/tbody/tr/td[2]/div[1]/a").text.split('\n')
                dictionary["УК"]=blok2[0].strip()
            except:
                dictionary["УК"]="-"
            
            try:
                # переход на новую страницу ОБЩАЯ ХАРАКТЕРИСТИКА ДОМА
                driver.find_element(By.LINK_TEXT, "Информация об управлении МКД").click()
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(2)
                driver.execute_script("window.scrollBy(0,500)","")
                time.sleep(2)
            except:
                with open(xxx+"отчет.txt", "a") as otchet:
                    otchet.write(dictionary["Страница"]+"|"+dictionary["Адрес"]+"|"+dictionary["Тип дома:"]+"|"+
                    dictionary["Год постройки:"]+"|"+dictionary["Идентификационный код адреса:"]+"|"+dictionary["УК"]+"|"
                    +"!"+"|"+"!"+"|"+"!"+"|"+"!"+"|"+"!"+"\n")
                continue    

            dictionary["Количество жилых помещений, ед.:"]="-"
            try:
                blok3=driver.find_element(By.XPATH, "/html/body/div[1]/div[8]/div/div[2]/div[2]/div/div[1]/ef-och-duo-mkd-ci/div[2]").text.split('\n')
                sub_index=(blok3.index("Количество жилых помещений, ед.:"))
                dictionary["Количество жилых помещений, ед.:"]=blok3[sub_index+1]
            except:
                dictionary["Количество жилых помещений, ед.:"]="!"

            #print(dictionary)
            #exit()
            

            # переход на новую страницу О ИСПОЛЬЗОВАНИИ ИМУЩЕСТВА
            
            try: 
                driver.find_element(By.LINK_TEXT, "Использование общего имущества").click() 
                #driver.switch_to.window(driver.window_handles[1])
                time.sleep(2)
                driver.execute_script("window.scrollBy(0,500)","")
                time.sleep(3)
            except: #нет ссылки на Использование общего имущества
                with open(xxx+"отчет.txt", "a") as otchet:
                    otchet.write(dictionary["Страница"]+"|"+dictionary["Адрес"]+"|"+dictionary["Тип дома:"]+"|"+
                    dictionary["Год постройки:"]+"|"+dictionary["Идентификационный код адреса:"]+"|"+dictionary["УК"]+"|"
                    +dictionary["Количество жилых помещений, ед.:"]+"|"+"!"+"|"+"!"+"|"+"!"+"|"+"!"+"\n") 
                continue

            try:    
                for poisk in F_Pole3:
                    dictionary[poisk]="-"      
                #blok4=driver.find_element(By.XPATH, "/html/body/div[1]/div[8]/div/div[2]/div[2]/div/div[5]/ef-och-duo-mkd-uce/div/div[1]").text.split('\n')
                blok4=driver.find_element(By.XPATH, "/html/body/div[1]/div[8]/div/div[2]/div[2]/div/div[5]/ef-och-duo-mkd-uce/div").text.split('\n')
                #highlight(blok4, 3, "red", 5)
                for m in range(0,len(blok4)):
                    little=blok4[m]
                    for poisk in F_Pole3:
                        q=little.find(poisk)
                        if q!=-1:
                            dictionary[poisk]="+"
            except:
                # предварительный сброс данных в ноль
                for poisk in F_Pole3:
                    dictionary[poisk]="!"
            
            #print(dictionary)
            with open(xxx+"отчет.txt", "a") as otchet:
                otchet.write(dictionary["Страница"]+"|"+dictionary["Адрес"]+"|"+dictionary["Тип дома:"]+"|"+dictionary["Год постройки:"]+"|"
                            +dictionary["Идентификационный код адреса:"]+"|"+dictionary["УК"]+"|"
                            +dictionary["Количество жилых помещений, ед.:"]+"|"+dictionary["МОБИЛЬНЫЕ ТЕЛЕСИСТЕМЫ"]+"|"+
                            dictionary["ВЫМПЕЛ-КОММУНИКАЦИИ"]+"|"+dictionary["РОСТЕЛЕКОМ"]+"|"+dictionary["ТЕЛЕКОМ.РУ"]+"\n")
                
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            #exit()

