# Парсим госуслуги ЖКХ
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


def gos():
    xxx="C:\\3-14\\Gos\\"
    flag_10_100=True # флаг для проверки кол. домов - 1 при кол домов в поиске более 10
    # открываем файл для записи, чтения и создаем его если его не существует, по хорошему туда сразу нужно записать 1 если файла ранее небуло, или
    # добавить обработку ошибки если в файле нет начало прохода улиц
    with open(xxx+"итог.txt", "a") as itog:

    #инициализация Хрома
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        driver=webdriver.Chrome(executable_path=xxx+"chromedriver.exe",options=chrome_options )
        Action=ActionChains(driver)
        driver.get("https://dom.gosuslugi.ru/#!/houses")
        driver.implicitly_wait(100)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

        winsound.Beep(1200, 100)

        input_a=driver.find_element(By.XPATH, '/html/body/div[1]/div[8]/div/div[2]/houses-search-form/div[2]/div/ef-bp-form/div/form/div[2]/div/div/div/div[1]/div/div/div[1]/ef-pa-form-4/div/form/div/div/div/div[1]/div[1]/div/div/a')
        driver.execute_script("arguments[0].scrollIntoView(true);", input_a)
        
        # выбираем область (ввод Ульяновская область) и переходим в область город - там просто прощелкиваенм вариант до последнего города - Ульяновска
        #highlight(input_a, 3, "red", 5)
        Action.move_to_element(input_a)
        Action.perform()
        Action.click()
        Action.perform()
        input_a.send_keys("Ульяновская область")
        input_a.send_keys(Keys.ENTER)
            # поиск окошка выбора города
        input_a=driver.find_element(By.XPATH, '/html/body/div[1]/div[8]/div/div[2]/houses-search-form/div[2]/div/ef-bp-form/div/form/div[2]/div/div/div/div[1]/div/div/div[1]/ef-pa-form-4/div/form/div/div/div/div[1]/div[3]/div/div/a')
        driver.execute_script("arguments[0].scrollIntoView(true);", input_a)
        Action.move_to_element(input_a)
        Action.perform()
        Action.click()
        Action.perform()
        Action.send_keys(Keys.DOWN)
        Action.send_keys(Keys.NULL) 
        Action.perform()
        time.sleep(1)
        Action.send_keys(Keys.DOWN)
        Action.send_keys(Keys.NULL) 
        Action.perform()
        time.sleep(1)
        Action.send_keys(Keys.DOWN)
        Action.send_keys(Keys.NULL) 
        Action.perform()
        time.sleep(1)
        Action.send_keys(Keys.ENTER)
        Action.perform()

        end_line = open(xxx+"итог.txt", 'r').readlines()
        try:
            end_nume=int(end_line[-1])
        except:
            end_nume=0 #ну вдруг мы только создали файл и он пустой или там лажа какято. проверять лень - поставил полузаглушку
        end_find=end_nume+1 #т.к. в файле отмечена позиция которая прошла и все в норме то нам нужен след адрес

        ulica=open(xxx+"улицы.txt", "r")
        add = ulica.readlines()

        ulica_pol=open(xxx+"улицы_полный.txt", "r")
        add_pol = ulica_pol.readlines()
        
        pyperclip.copy(str(add[end_find]))
        winsound.Beep(1200, 100)
        winsound.Beep(1500, 100)
        
        #находим окно ввода, открываем
        sub_input=driver.find_element(By.XPATH,'/html/body/div[1]/div[8]/div/div[2]/houses-search-form/div[2]/div/ef-bp-form/div/form/div[2]/div/div/div/div[1]/div/div/div[1]/ef-pa-form-4/div/form/div/div/div/div[2]/div[2]/div/div')
        Action.move_to_element(sub_input)
        Action.perform()
        Action.click(sub_input)
        Action.perform()
        time.sleep(2)
       
       #вводим адрес для поиска
        odin='//*[@id="s2id_autogen16_search"]'
        sub_input=driver.find_element(By.XPATH, odin)
        sub_input.send_keys(str(add[end_find]))
        pyperclip.copy(str(add[end_find]))
        pyperclip.paste()
        time.sleep(2)
        
        #открываем под список под поиска 
        sub_numer='//*[@id="select2-results-16"]'
        sub_numer_f=driver.find_element(By.XPATH, sub_numer) 
        sub=sub_numer_f.text.split('\n')
        
        # находим индекс нашей строки с адресом в предлагаемым сайтом списке подстановок адреса
        sub_index=(sub.index(add_pol[end_find].rstrip('\n')))
        sub_i=sub_index
        while sub_i>0:
            Action.send_keys(Keys.DOWN)
            Action.send_keys(Keys.NULL) 
            Action.perform()
            time.sleep(1)
            sub_i=sub_i-1
        Action.send_keys(Keys.ENTER)
        Action.perform()
        
        # находим кнопку "найти", щелкаем по ней 
        p="/html/body/div[1]/div[8]/div/div[2]/houses-search-form/div[2]/div/ef-bp-form/div/form/div[3]/div/div[2]/button"
        ctoto=driver.find_element(By.XPATH, p)
        Action.move_to_element(ctoto)
        Action.click(ctoto)
        Action.perform()
        
        # запускаем цыклю обработки
        try:
            while True:
                winsound.Beep(1200, 100)
                time.sleep(10)
            #определение сколько домов на улице - используем для перебора
                numer="/html/body/div[1]/div[8]/div/houses-search-result/div/div[1]/h4/b"
                numer_f=driver.find_element(By.XPATH, numer)
                try:
                    ii=int(numer_f.text)
                except:
                    ii=0
                print(ii)
                
                # если кол. домов больше 10 то сдвигаем выбор до 100 - делаем выбор 1 раз
                if (ii>10) and flag_10_100:
                    skoko=driver.find_element(By.XPATH, "/html/body/div[1]/div[8]/div/houses-search-result/div/div[4]/div/div[2]/div/div/div/div")
                    driver.execute_script("arguments[0].scrollIntoView(true);", skoko)
                    #highlight(skoko, 3, "red", 5)
                    Action.move_to_element(skoko)
                    Action.perform()
                    Action.click()
                    Action.perform()
                    # доходим до выбора кол. страниц =100
                    for q in range(6):
                        time.sleep(1)
                        Action.send_keys(Keys.DOWN)
                        Action.send_keys(Keys.NULL) 
                        Action.perform()

                    time.sleep(1)
                    Action.send_keys(Keys.ENTER)
                    Action.perform()
                    flag_10_100=False
                
                # создаем файл с улицей
                add_f=open(xxx+str(add_pol[end_find].rstrip('\n'))+".txt", "w")
                
                for j in range(1, int(ii//100)+1): # целочисленно делим кол. страниц на 100. Если 50 то даст 1 - цыкл перескочит дальше
                    # если 150 то даст 1 +1 -> пройдет 1 цыкл и перескочит далее
                    for i in range(1, 101): # если зашли в этот цыкл то кол. домов более//равно 100 и все норм 
            #Проходим по ссылкам на дома внутри основной страницы
                        
                        blok_1="/html/body/div[1]/div[8]/div/houses-search-result/div/div[1]/div["+str(i)+"]/div[1]/span/div/span"
                        blok_2=driver.find_element(By.XPATH, blok_1)
                        blok_add=blok_2.text
                        
                        blok_1="/html/body/div[1]/div[8]/div/houses-search-result/div/div[1]/div["+str(i)+"]/div[2]/div/div/div[2]/table"
                        blok_2=driver.find_element(By.XPATH, blok_1)
                        blok_qq=blok_2.text
                        
                        blok_1="/html/body/div[1]/div[8]/div/houses-search-result/div/div[1]/div["+str(i)+"]/div[2]/div/div/div[3]/table"
                        blok_2=driver.find_element(By.XPATH, blok_1)
                        blok_ww=blok_2.text
                        
                        c="/html/body/div[1]/div[8]/div/houses-search-result/div/div[1]/div["+str(i)+"]/div[3]/a[1]"
                        output=driver.find_element(By.XPATH, c)
                        Action.move_to_element(output)
                        Action.perform()
                        Action.click()
                        Action.perform()
                        time.sleep(2)
                        driver.switch_to.window(driver.window_handles[1])
                        add_f.write(str(driver.current_url)+'\n'+"|"+blok_add+'\n'+blok_qq+blok_ww+"|"+'\n')
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                    if j<int(ii//100): # делаем переходы на новую страницу до предпоследнего прохода. в последнем - переход, в слечае необходимости  
                        # прогоняем в цыкле добивания остков домов
                        next="/html/body/div[1]/div[8]/div/houses-search-result/div/div[4]/div/div[1]/div/ul[3]/li[2]/a/span[1]"
                        next_f=driver.find_element(By.XPATH, next)
                        Action.move_to_element(next_f)
                        Action.perform()
                        Action.click()
                        Action.perform()
                        time.sleep(10)
                        winsound.Beep(900, 100)
                        time.sleep(1)
                        winsound.Beep(900, 100)
                        time.sleep(1)
                        winsound.Beep(900, 100)
                # прошли цыкл кратный 100, осталась//не осталось пройти остаток домов (остаток от целочисленного деления ii на 100)
                flag_do_100=True
                for i in range(1, int((ii/100-int(ii/100))*100)+1): # определяем остаток домов, если 0 то показывает от 1 до 1 и проскакиваем дальше
                # переходим на след страницу - ! раз!!!!
                    if flag_do_100 and ii>100:
                        next="/html/body/div[1]/div[8]/div/houses-search-result/div/div[4]/div/div[1]/div/ul[3]/li[2]/a/span[1]"
                        next_f=driver.find_element(By.XPATH, next)
                        Action.move_to_element(next_f)
                        Action.perform()
                        Action.click()
                        Action.perform()
                        time.sleep(10)
                        winsound.Beep(900, 100)
                        time.sleep(1)
                        winsound.Beep(900, 100)
                        time.sleep(1)
                        winsound.Beep(900, 100)
                        flag_do_100=False
                #Проходим по ссылкам на дома внутри основной страницы
                    blok_1="/html/body/div[1]/div[8]/div/houses-search-result/div/div[1]/div["+str(i)+"]/div[1]/span/div/span"
                    blok_2=driver.find_element(By.XPATH, blok_1)
                    blok_add=blok_2.text
                    blok_1="/html/body/div[1]/div[8]/div/houses-search-result/div/div[1]/div["+str(i)+"]/div[2]/div/div/div[2]/table"
                    blok_2=driver.find_element(By.XPATH, blok_1)
                    blok_qq=blok_2.text
                    blok_1="/html/body/div[1]/div[8]/div/houses-search-result/div/div[1]/div["+str(i)+"]/div[2]/div/div/div[3]/table"
                    blok_2=driver.find_element(By.XPATH, blok_1)
                    blok_ww=blok_2.text
                    c="/html/body/div[1]/div[8]/div/houses-search-result/div/div[1]/div["+str(i)+"]/div[3]/a[1]"
                    output=driver.find_element(By.XPATH, c)
                    Action.move_to_element(output)
                    Action.perform()
                    Action.click()
                    Action.perform()
                    time.sleep(2)
                    driver.switch_to.window(driver.window_handles[1])
                    add_f.write(str(driver.current_url)+'\n'+"|"+blok_add+'\n'+blok_qq+blok_ww+"|"+'\n')
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                # закрываем файл с улицей
                add_f.close()
                itog.write('\n'+str(end_find))
                end_find=end_find+1
                pyperclip.copy(str(add[end_find]))

                winsound.Beep(1500, 100)
                time.sleep(1)
                winsound.Beep(1500, 100)

                # вводим адрес для поиска
                odin='/html/body/div[1]/div[8]/div/div[2]/houses-search-form/div[2]/div/ef-bp-form/div/form/div[2]/div/div/div/div[1]/div/div/div[1]/ef-pa-form-4/div/form/div/div/div/div[2]/div[2]/div/div'
                sub_input=driver.find_element(By.XPATH,odin)
                Action.move_to_element(sub_input)
                Action.perform()
                Action.click(sub_input)
                Action.perform()
                time.sleep(2)
                
                #открываем под список под поиска 
                odin='//*[@id="s2id_autogen16_search"]'
                sub_input=driver.find_element(By.XPATH,odin)
                sub_input.send_keys(str(add[end_find]))
                pyperclip.paste()
                time.sleep(2)
                
                # находим ундекс нашей строки с адресом в предлагаемым сайтом списке подстановок адреса
                sub_numer='//*[@id="select2-results-16"]'
                sub_numer_f=driver.find_element(By.XPATH, sub_numer) 
                sub=sub_numer_f.text.split('\n')
                sub_index=(sub.index(add_pol[end_find].rstrip('\n')))
                sub_i=sub_index
                while sub_i>0:
                    Action.send_keys(Keys.DOWN)
                    Action.send_keys(Keys.NULL) 
                    Action.perform()
                    time.sleep(1)
                    sub_i=sub_i-1
                Action.send_keys(Keys.ENTER)
                Action.perform()

                # находим кнопку "найти", щелкаем по ней 
                p="/html/body/div[1]/div[8]/div/div[2]/houses-search-form/div[2]/div/ef-bp-form/div/form/div[3]/div/div[2]/button"
                ctoto=driver.find_element(By.XPATH, p)
                Action.move_to_element(ctoto)
                Action.click(ctoto)
                Action.perform()

                # возвращаемся к еачалу цыкла обработки
        finally: # произошел уирдык - в лучшем случае завис сайта ГосУслуг и мы возвращаем номер обрабатываемой улицы 
            # (проблемка - мы можем вернуть как вылетевший адрес который обрабатывали так и адрес который мы еще не начали обрабатывать.
            # в первом случае будем повторно обрабаывать ранее обрабатываемый адрес.... - нужно полумать !!!!!!!!!!!!!!!!!!!!!!!!)
            winsound.Beep(1500, 300)
            time.sleep(1)
            winsound.Beep(1500, 300)
            time.sleep(1)
            winsound.Beep(1500, 300)
            return(end_find)

flag1=True
r1=0
ito=open("C:\\3-14\\Gos\\неработат.txt", "a")
ito.write("____________запись нового блока___________"+'\n')
while flag1:
    r2=gos()
    ito.write("____________ОШИБКА В АДРЕСЕ___________"+'\n')
    ito.write("-----"+str(r2)+'\n')
    if r1==r2:
        ito.write("Повторная ошибка в адресе!!!!!")
        ito.write("----"+str(r2)+'\n')
        exit()
    r1=r2
    if int(r1)>992: exit()