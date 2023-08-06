import pprint
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def takeTimeWithSolution():
    risultati_dict = {}
    risultati_list = []
    for i in range(1,26):
        for j in range(0,5):
            if (i ==19 and j ==2 ) or (i ==20 and j ==0 ) or (i ==23 and j ==1 ) or (i ==23 and j ==3 ) or (i ==25 and j ==2 ):
                continue
            lines = open("./results_MA_2/miconic-s{}-{}.txt".format(i, j), "r").readlines()
            size = len(lines)
            seconds = 0
            if "seconds" in lines[size-1]:
                temp = lines[size-1].split()
            seconds = float(temp[0])
            key = "miconic-s{}-{}".format(i, j)
            risultati_dict.update({key:seconds})
            risultati_list.append(seconds)
    return risultati_dict

def takeTime():
    risultati_dict = {}
    risultati_list = []
    for i in range(1,21):
        for j in range(0,5): # qua ci sono sia le sol mancanti che gli error, anche se non serve file .sol non si riesce a risolvere con tale modellazione
            if (i ==18 and j ==1 )or(i ==16 and j ==2 )or(i ==19 and j ==2 ) or (i ==20 and j ==0 ) or (i ==23 and j ==1 ) or (i ==23 and j ==3 ) or (i ==25 and j ==2 ) or (i ==17 and j ==3)or (i ==19 and j ==1) or(i ==19 and j ==3)or (i ==20 and j ==1)or (i ==20 and j ==4):
                continue
            lines = open("./results_MA_1/miconic-s{}-{}.txt".format(i, j), "r").readlines()
            size = len(lines)
            seconds = 0
            if "seconds" in lines[size-1]:
                temp = lines[size-1].split()
            seconds = float(temp[0])
            key = "miconic-s{}-{}".format(i, j)
            risultati_dict.update({key:seconds})
            risultati_list.append(seconds)
    return risultati_dict

def takeNode():
    risultati_dict = {}
    listaNodi = countNode("NodiCopia")
    for i in range(1,26):
        for j in range(0,5): # qua ci sono sia le sol mancanti che gli error, anche se non serve file .sol non si riesce a risolvere con tale modellazione
            if (i ==18 and j ==1 )or(i ==16 and j ==2 )or(i ==19 and j ==2 ) or (i ==20 and j ==0 ) or (i ==23 and j ==1 ) or (i ==23 and j ==3 ) or (i ==25 and j ==2 ) or (i ==17 and j ==3)or (i ==19 and j ==1) or(i ==19 and j ==3)or (i ==20 and j ==1)or (i ==20 and j ==4):
                continue
            key = "miconic-s{}-{}".format(i, j)
            nodo = 0
            risultati_dict.update({key:nodo})
    lista = getKey(risultati_dict)
    for i in range(0,len(lista)):
        risultati_dict.update({lista[i]:listaNodi[i]})
    return risultati_dict

def takeNodeWithSolution():
    risultati_dict = {}
    listaNodi = countNode("NodiSol.txt")
    for i in range(1,26):
        for j in range(0,5): # qua ci sono sia le sol mancanti che gli error, anche se non serve file .sol non si riesce a risolvere con tale modellazione
            if (i ==19 and j ==2 ) or (i ==20 and j ==0 ) or (i ==23 and j ==1 ) or (i ==23 and j ==3 ) or (i ==25 and j ==2 ):
                continue
            key = "miconic-s{}-{}".format(i, j)
            nodo = 0
            risultati_dict.update({key:nodo})
    lista = getKey(risultati_dict)
    for i in range(0,len(lista)):
        risultati_dict.update({lista[i]:listaNodi[i]})
    return risultati_dict

def shiftedGeometricMean(valori,shift):
    tempo = 1
    size = len(valori)
    for i in valori:
        tempo = tempo * (i + shift)
    tempo = pow(tempo,1/size)
    tempo = tempo - shift
    return tempo

def getKey(dizionario):
  return list(dizionario.keys())

def getValue(dizionario,index):
  return dizionario[list(dizionario.keys())[index]]

def countNode(stringa):
    nodo = 0
    listaNodi = []
    lines = open(stringa,"r").readlines()
    for i in lines:
        for j in range(0,len(i)):
            if i[j] ==":":
                nodo = int(i[j+1:-1])
                nodo = nodo + 1 #il nodo radice vale 0 ma esiste
                listaNodi.append(nodo)
    return listaNodi
                
def count_occurences(dictionary, upperbound):
  counter = 0
  for key in dictionary:
    if dictionary[key] <= upperbound:
        counter = counter + (1/91) # 150 istanze
  return counter

def perc_resolver(data):
  perc = {}
  for value in sorted(data.values()):
    perc[value] = count_occurences(data, value)
  return perc

def max_key(dictionary, max):
  keys = sorted(dictionary.keys())
  i = 0
  while(i < len(keys)):
    if keys[i] > max: break
    i = i + 1
  if i >= len(keys): return keys[i-1]
  return keys[i]

def convertNameToNumber(lista):
    temp = []
    for value in lista:
        for i in range(0,len(value)):
            if value[i] == "s":
                numero = value[i+1:]
                temp.append(numero)
    med = []
    final =[]
    for x in temp:
        string_list = list(x)
        string_list[len(x)-2] = "."
        newX = "".join(string_list)
        med.append(newX)
    for stringa in med:
        numero = float(stringa)
        final.append(numero)
    return final



if __name__ == "__main__":
    
    



    # ALL TEMPI
    # dizionarioSol = takeTimeWithSolution()
    # keylistSol = getKey(dizionarioSol)
    # xAxisSol = []
    # yAxisSol = []
    # listaSol = convertNameToNumber(keylistSol)
    # for i in range(0,len(keylistSol)):
    #     xAxisSol.append(listaSol[i])
    #     yAxisSol.append(dizionarioSol[keylistSol[i]])

    # dizionarioNotSol = takeTime()
    # keylistNotSol = getKey(dizionarioNotSol)
    # xAxisNotSol =[]
    # yAxisNotSol = []
    # listaNotSol = convertNameToNumber(keylistNotSol)
    # for i in range(0,len(keylistNotSol)):
    #     xAxisNotSol.append(listaNotSol[i])
    #     yAxisNotSol.append(dizionarioNotSol[keylistNotSol[i]])

    # plt.xlabel("Numero istanza")
    # plt.ylabel("Tempo in secondi")
    # plt.xticks(xAxisSol)
    # plt.plot(xAxisSol,yAxisSol,'o',color="red")
    # plt.plot(xAxisNotSol,yAxisNotSol,'o',color="blue")
    # plt.show()



    # ALL NODI
    dizionarioSol = takeNodeWithSolution()
    keylistSol = getKey(dizionarioSol)
    xAxisSol = []
    yAxisSol = []
    listaSol = convertNameToNumber(keylistSol)
    for i in range(0,len(keylistSol)):
        xAxisSol.append(listaSol[i])
        yAxisSol.append(dizionarioSol[keylistSol[i]])

    dizionarioNotSol = takeNode()
    keylistNotSol = getKey(dizionarioNotSol)
    xAxisNotSol =[]
    yAxisNotSol = []
    listaNotSol = convertNameToNumber(keylistNotSol)
    for i in range(0,len(keylistNotSol)):
        xAxisNotSol.append(listaNotSol[i])
        yAxisNotSol.append(dizionarioNotSol[keylistNotSol[i]])

    plt.xlabel("Numero istanza")
    plt.ylabel("Nodi")
    plt.xticks(xAxisSol)
    plt.plot(xAxisSol,yAxisSol,'o',color="red")
    plt.plot(xAxisNotSol,yAxisNotSol,'o',color="blue")
    plt.show()