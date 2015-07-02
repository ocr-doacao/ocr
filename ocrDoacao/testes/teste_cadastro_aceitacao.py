#!/usr/bin/python
# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Firefox()
##Colocar o ambiente de testes aqui
driver.get("https://ocr-rmmsilva.c9.io/ong/AACD/cadastro")

elem = driver.find_element_by_name("cnpj")
elem.send_keys("11111111111111")

coo = driver.find_element_by_name("coo").click()

error = driver.find_elements_by_class_name("validation_error")


assert error[0].text != ""


driver.close()