import pprint
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#taking time from results
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
    
    #ALL 
    # dizionarioCopiaNodiNotSol = takeNode()
    # keylistNotSolNodi = getKey(dizionarioCopiaNodiNotSol)
    # xAxisNotSol = []
    # col1 = "Nodi"
    # yAxisNotSol = []
    # col2 = "Istanze"
    # listaNotSolNodi = convertNameToNumber(keylistNotSolNodi)
    
    # dizionarioCopiaNodiSol = takeNodeWithSolution()
    # keylistSolNodi = getKey(dizionarioCopiaNodiSol)
    # xAxisSol = []
    # col1 = "Nodi"
    # yAxisSol = []
    # col2 = "Istanze"
    # listaSolNodi = convertNameToNumber(keylistSolNodi)
    
    
    # for i in range(0,len(keylistNotSolNodi)):
    #     xAxisNotSol.append(listaNotSolNodi[i])
    #     yAxisNotSol.append(dizionarioCopiaNodiNotSol[keylistNotSolNodi[i]])
  
    # for i in range(0,len(keylistSolNodi)):
    #     xAxisSol.append(listaSolNodi[i])
    #     yAxisSol.append(dizionarioCopiaNodiSol[keylistSolNodi[i]])


    # plt.xlabel("Numero istanza")
    # plt.ylabel("Nodi")
    # plt.xticks(xAxisSol)
    # plt.plot(xAxisSol,yAxisSol,'o')
    # plt.show()








    
    #versione senza soluzione(NODI)
    # dizionarioCopia = takeNode()
    # keylist = getKey(dizionarioCopia)
    # xAxis = []
    # col1 = "Nodi"
    # yAxis = []
    # col2 = "Istanze"
    # lista = convertNameToNumber(keylist)
    # for i in range(0,len(keylist)):
    #     xAxis.append(lista[i])
    #     yAxis.append(dizionarioCopia[keylist[i]])
    # plt.xlabel("Numero istanza")
    # plt.ylabel("Nodi")
    # plt.xticks(xAxis)
    # plt.plot(xAxis,yAxis,'o')
    # plt.show()


    #versione con soluzione(NODI)
    # dizionarioCopia = takeNodeWithSolution()
    # keylist = getKey(dizionarioCopia)
    # xAxis = []
    # col1 = "Nodi"
    # yAxis = []
    # col2 = "Istanze"
    # lista = convertNameToNumber(keylist)
    # for i in range(0,len(keylist)):
    #     xAxis.append(lista[i])
    #     yAxis.append(dizionarioCopia[keylist[i]])
    # plt.xlabel("Numero istanza")
    # plt.ylabel("Nodi")
    # plt.xticks(xAxis)
    # plt.plot(xAxis,yAxis,'o')
    # plt.show()


    #Versione senza soluzione
    # dizionarioCopia = takeTime()
    # keylist = getKey(dizionarioCopia)
    # xAxis = []
    # col1 = "Solution time"
    # yAxis = []
    # col2 = "Istanze"
    # lista = convertNameToNumber(keylist)
    # for i in range(0,len(keylist)):
    #     xAxis.append(lista[i])
    #     yAxis.append(dizionarioCopia[keylist[i]])
    # #df = pd.DataFrame({col1: xAxis, col2: yAxis})
    # #df.plot(x=col1, y=col2, title="Tempi risoluzione ", color="blue")
    # plt.xlabel("Numero istanza")
    # plt.ylabel("Tempo in secondi")
    # plt.xticks(xAxis)
    # plt.plot(xAxis,yAxis,'o',color="green")
    # plt.show()


    #Versione con soluzione
    # dizionarioSol = takeTimeWithSolution()
    # keylist = getKey(dizionarioSol)
    # xAxis = []
    # col1 = "Solution time"
    # yAxis = []
    # col2 = "Istanze"
    
    # lista = convertNameToNumber(keylist)
    # for i in range(0,len(keylist)):
    #     xAxis.append(lista[i])
    #     yAxis.append(dizionarioSol[keylist[i]])
    # #df = pd.DataFrame({col1: xAxis, col2: yAxis})
    # #df.plot(x=col1, y=col2, title="Tempi risoluzione ", color="blue")

    # plt.xlabel("Numero istanza")
    # plt.ylabel("Tempo in secondi")
    # plt.xticks(xAxis)
    # plt.plot(xAxis,yAxis,'o')
    # plt.show()

   
#    sol = "NodiSol.txt"
#    copia = "NodiCopia"

#    NodiCopia = countNode(copia)
#    NodiSol = countNode(sol)

#    mediaCopia = shiftedGeometricMean(NodiCopia,10) 
#    mediaSol =  shiftedGeometricMean(NodiSol,10)

#    print("MediaCopia",mediaCopia)
#    print("MediaSol",mediaSol)

    # dizionarioSol = takeTimeWithSolution()
    # dizionarioCopia = takeTime()

    # percentualeSol = perc_resolver(dizionarioSol)
    # percentualeCopia = perc_resolver(dizionarioCopia)
    
    
    # #Versione senza soluzione
    # xAxis = []
    # col1 = "Solution time"
    # yAxis = []
    # col2 = "% risolte"
    # for key in percentualeCopia:
    #     xAxis.append(key)
    #     yAxis.append(percentualeCopia[key])
    # df = pd.DataFrame({col1: xAxis, col2: yAxis})
    # df.plot(x=col1, y=col2, title="% istanze risolte", color="blue")
    # plt.xlabel("Tempo in sec (scala log)")
    # plt.xscale("log")
    # plt.ylabel("% istanze")
    # plt.axhline(y=1, color="grey", linestyle="--")
    # plt.show()


    #Versione con soluzione
    # xAxis = []
    # col1 = "Solution time"
    # yAxis = []
    # col2 = "% risolte"
    # for key in percentualeSol:
    #     xAxis.append(key)
    #     yAxis.append(percentualeSol[key])
    # df = pd.DataFrame({col1: xAxis, col2: yAxis})
    # df.plot(x=col1, y=col2, title="% istanze risolte", color="red")
    # plt.xlabel("Tempo in sec (scala log)")
    # plt.xscale("log")
    # plt.ylabel("% istanze")
    # plt.axhline(y=1, color="grey", linestyle="--")
    # plt.show()


    # xAxis = []
    # col1 = "Solution time"
    # sol = []
    # col2 = "% Con Soluzione in input"
    # copia = []
    # col3 = "% Senza soluzione in input"
    # planner = []
    
    # step = 0.001
    # for key in set(list(percentualeSol.keys())+list(percentualeCopia.keys())):
    #     xAxis.append(key)
    #     sol.append(percentualeSol[max_key(percentualeSol, key)])
    #     copia.append(percentualeCopia[max_key(percentualeCopia, key)])
        
    # df = pd.DataFrame({col1: xAxis, col2: sol, col3: copia})
    # ax = df.plot(x=col1, y=col2, color="red", label=col2, kind="scatter", s=1)
    # df.plot(x=col1, y=col3, color="blue", label=col3, kind="scatter", s=1, ax=ax)
    # plt.xlabel("Tempo in secondi (scala log)")
    # plt.xscale("log")
    # plt.ylabel("% istanze")
    # plt.title("Comparazione formulazione con soluzione in input e senza soluzione")
    # plt.axhline(y=1, color="grey", linestyle="--")
    # plt.show()