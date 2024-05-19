#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on Sun Sep  3 17:59:43 2023

# @author: JuanManuelHuertasArango

#
import time
import pandas as pd
import torch

from matplotlib import pyplot as plt
import random

import os


os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'

#os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Variable global de buffer
global_buffer = 0
buffer = []
delete = []
cajas_pp = []
figs = []
espemax = []
max_rear = 0

empates = 0

# resp_global_max=[]

# resp_global_ce=[]

# Clase Caja Rotada


class CajaRot:
    def __init__(self, id_p, x, y, z):
        self.id_p = id_p
        self.x = x
        self.y = y
        self.z = z

# Clase tipo de caja


class CajaTipo:

    def __init__(self, id_p, x, y, z, dx, dy, dz):
        self.volumen = x*y*z
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.x = x
        self.y = y
        self.z = z
        self.id_p = id_p
        self.list_caja = self.lista_caja_rot(id_p, x, y, z, dx, dy, dz)

    # Funcion rotar caja
    def lista_caja_rot(self, id_p, x, y, z, dx, dy, dz):
        lista_resp = []
        add_box_x = None
        add_box_x1 = None
        add_box_y = None
        add_box_y1 = None
        add_box_z = None
        add_box_z1 = None

        # Se obtienen las diferentes cajas
        if (dx == 1):
            add_box_x = CajaRot(id_p, z, y, x)
            lista_resp.append(add_box_x)
        elif(dx == 2):
            add_box_x = CajaRot(id_p, y, z, x)
            lista_resp.append(add_box_x)
        elif(dx == 3):
            add_box_x = CajaRot(id_p, z, y, x)
            lista_resp.append(add_box_x)
            add_box_x1 = CajaRot(id_p, y, z, x)
            lista_resp.append(add_box_x1)

        if(dy == 1):
            add_box_y = CajaRot(id_p, x, z, y)
            lista_resp.append(add_box_y)
        elif(dy == 2):
            add_box_y = CajaRot(id_p, z, x, y)
            lista_resp.append(add_box_y)
        elif(dy == 3):
            add_box_y = CajaRot(id_p, x, z, y)
            lista_resp.append(add_box_y)
            add_box_y1 = CajaRot(id_p, z, x, y)
            lista_resp.append(add_box_y1)

        if(dz == 1):
            add_box_z = CajaRot(id_p, x, y, z)
            lista_resp.append(add_box_z)
        elif(dz == 2):
            add_box_z = CajaRot(id_p, y, x, z)
            lista_resp.append(add_box_z)
        elif(dz == 3):
            add_box_z = CajaRot(id_p, x, y, z)
            lista_resp.append(add_box_z)
            add_box_z1 = CajaRot(id_p, y, x, z)
            lista_resp.append(add_box_z1)

        return (lista_resp)


##########
# Class ESP MAX
class EspMax:
    def __init__(self, x1, y1, z1, x2, y2, z2):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.dx = abs(x1-x2)
        self.dy = abs(y1-y2)
        self.dz = abs(z1-z2)
        # self.esquina=0

# Class Caja Empacada


class CajaEmpacada():
    def __init__(self, id_p, x1, y1, z1, x2, y2, z2):
        self.id_p = id_p
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2

# Class Contenedor


class Contenedor():

    def __init__(self, id_p, x_cont, y_cont, z_cont):
        self.id_p = id_p
        self.CajasEmpacadas = []
        self.utilizacion = 0
        self.EspMax_p = [EspMax(0, 0, 0, x_cont, y_cont, z_cont)]
        self.vol_cont = x_cont*y_cont*z_cont
        self.cajasEmpMov = []
        # guardar los valores de las dimensiones del contenedor
        self.x_cont_glob = x_cont
        self.y_cont_glob = y_cont
        self.z_cont_glob = z_cont

    def obtener_EspMax_p(self):
        return self.EspMax_p

    def obtener_CajEmp(self):
        return self.CajasEmpacadas

    def obtener_cajEmpMov(self):
        return self.cajasEmpMov

    def get_volem(self):
        volem = 0
        for i in self.EspMax_p:
            volem = i.dx*i.dy*i.dz+volem

        n = len(self.EspMax_p)

        if n == 0:
            resp = 0
        else:
            resp = volem/n

        return (resp)

    def crearEspacios(self, CE: CajaEmpacada):
        resp = []
        for ii in range(len(self.EspMax_p)-1, -1, -1):
            i = self.EspMax_p[ii]
            seUsa = False

            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (CE.y1-i.y1 > 0):
                resp.append(EspMax(i.x1, i.y1, i.z1, i.x2, CE.y1, i.z2))
                if(i.x1 > i.x2 or i.y1 > CE.y1):
                    print("entro 1")
                    print("i.x1 "+str(i.x1))
                    print("i.x2 "+str(i.x2))
                    print("i.y1 "+str(i.y1))
                    print("CE.y1 "+str(CE.y1))
                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (CE.x1-i.x1 > 0):
                resp.append(EspMax(i.x1, i.y1, i.z1, CE.x1, i.y2, i.z2))
                if(i.x1 == CE.x1):
                    print("entro 2")
                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (i.y2-CE.y2 > 0):
                resp.append(EspMax(i.x1, CE.y2, i.z1, i.x2, i.y2, i.z2))
                if(i.x1 > i.x2 or CE.y2 > i.y2):
                    print("entro 3")

                    print("i.x1 "+str(i.x1))
                    print("i.x2 "+str(i.x2))
                    print("CE.y1 "+str(CE.y2))
                    print("i.y2 "+str(i.y2))
                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (i.x2-CE.x2 > 0):
                resp.append(EspMax(CE.x2, i.y1, i.z1, i.x2, i.y2, i.z2))
                if(i.x2 == CE.x2):
                    print("entro 2")
                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (CE.z1-i.z1 > 0):
                resp.append(EspMax(CE.x1, CE.y1, i.z1, CE.x2, CE.y2, CE.z1))
                if(CE.x1 > CE.x2 or CE.y1 > CE.y2):
                    print("entro 5")
                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (i.z2-CE.z2 > 0):
                resp.append(EspMax(CE.x1, CE.y1, CE.z2, CE.x2, CE.y2, i.z2))
            #    if(CE.x1>CE.x2 or CE.y1>CE.y2):
               # print("entro 6")
               # print("CE.z2: "+str(CE.z2))
               # print("i.z2: "+str(i.z2))

                seUsa = True

            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (i.z2-CE.z2 == 0):
                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (CE.z1-i.z1 == 0):
                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (i.x2-CE.x2 == 0):
                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (i.y2-CE.y2 == 0):
                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (CE.x1-i.x1 == 0):
                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (CE.y1-i.y1 == 0):
                seUsa = True

            print()

            if (seUsa):
                self.EspMax_p.pop(ii)
               # print (ii)
                # print(resp)
                # print(self.EspMax_p)

        for j in resp:
            self.EspMax_p.append(j)

        return(self.EspMax_p)

    def delete_em_cont(self):
        for ii in range(len(self.EspMax_p)-1, -1, -1):
            i = self.EspMax_p[ii]
           # print(ii)
            for jj in range(len(self.EspMax_p)-1, ii, -1):
                #    print(jj)
                # Caso de j contenido en
                j = self.EspMax_p[jj]
                if(i != j):
                    if((i.x1 <= j.x1) and (j.x2 <= i.x2) and (i.y1 <= j.y1) and (j.y2 <= i.y2) and (i.z1 <= j.z1) and (j.z2 <= i.z2)):
                        self.EspMax_p.pop(jj)
        # self.EspMax_p=nuevos_esp

    def juntarEspacios(self):

        bool_p = False
        for ii in range(len(self.EspMax_p)-1, -1, -1):
            i = self.EspMax_p[ii]
            for jj in range(len(self.EspMax_p)-1, ii, -1):
                # Caso de se solapa en Z
                j = self.EspMax_p[jj]
                salio = False
                if (i.z1 == j.z1) and (i.z2 == j.z2):
                    # Caso igual en X
                    if (i.x1 == j.x1) and (i.x2 == j.x2):
                        if not((i.y1 > j.y2) or (j.y1 > i.y2)):

                            min_y = min(i.y1, j.y1)
                            max_y = max(i.y2, j.y2)

                            nuevo_em = EspMax(
                                i.x1, min_y, i.z1, i.x2, max_y, i.z2)

                           # nuevo_em=EspMax(i.x1,i.y1,i.z1,i.x2,j.y2,i.z2)
                            self.EspMax_p.pop(jj)
                            self.EspMax_p[ii] = nuevo_em
                            i = nuevo_em
                            salio = True
                            bool_p = True

                    # Caso igual en Y
                    if (i.y1 == j.y1) and (i.y2 == j.y2):
                        if not((i.x1 > j.x2) or (j.x1 > i.x2)):
                            min_x = min(i.x1, j.x1)
                            max_x = max(i.x2, j.x2)

                            nuevo_em = EspMax(
                                min_x, i.y1, i.z1, max_x, j.y2, i.z2)

                            # nuevo_em=EspMax(i.x1,i.y1,i.z1,j.x2,j.y2,i.z2)
                            if salio == False:
                                self.EspMax_p.pop(jj)
                            self.EspMax_p[ii] = nuevo_em
                            i = nuevo_em
                            bool_p = True

        return(self.EspMax_p, bool_p)

    # Expandir
    def expandirEm(self):
        bool_p = False
        for ii in range(len(self.EspMax_p)-1, -1, -1):
            i = self.EspMax_p[ii]
            for jj in range(len(self.EspMax_p)-1, -1, -1):
                j = self.EspMax_p[jj]
                if(i != j):
                    # Igual en Z
                    if (i.z1 == j.z1) and (i.z2 == j.z2):
                        # Contencion en X
                        if(i.x1 <= j.x1) and (j.x2 <= i.x2):
                            # Solapamiento en Y
                            if not((i.y1 > j.y2) or (j.y1 > i.y2)):
                                # expandir EM
                                min_y = min(i.y1, j.y1, i.y2, j.y2)
                                max_y = max(i.y2, j.y2, i.y1, j.y1)

                                exp_em = EspMax(
                                    j.x1, min_y, j.z1, j.x2, max_y, j.z2)
                                self.EspMax_p[jj] = exp_em
                                bool_p = True

                              #  print("min y: "+str(min_y))
                               # print("max y: "+ str(max_y))

                                # No eliminar espacio maximal

                        # Contencion en Y
                        if(i.y1 <= j.y1) and (j.y2 <= i.y2):
                            # Solapamiento en X
                            if not((i.x1 > j.x2) or (j.x1 > i.x2)):
                                # expandir EM
                                min_x = min(i.x1, j.x1, i.x2, j.x2)
                                max_x = max(i.x2, j.x2, i.x1, j.x1)
                                exp_em = EspMax(
                                    min_x, j.y1, j.z1, max_x, j.y2, j.z2)
                                self.EspMax_p[jj] = exp_em
                                bool_p = True

                              #  print("min x: "+str(min_x))
                              #  print("max x: "+ str(max_x))

        return(bool_p)

    # Juntar los metodos
    def todoEM(self):
        seguir = True
        a = []
        contador = 1
      #  esp_max_ini=self.EspMax_p

        while(seguir):

            seguir = False
            a, bool_junt = self.juntarEspacios()

            esp_max_ini = []
            for i in self.EspMax_p:
                esp_max_ini.append(i)

            bool_exp = self.expandirEm()

            for i in range(0, len(esp_max_ini)):
                if esp_max_ini[i] != self.EspMax_p[i]:
                    bool_exp = False

           # if not(esp_max_ini!=self.EspMax_p):
            #    bool_exp=False

            if(bool_junt == True or bool_exp == True):
                seguir = True

            # if(seguir==False):
             #   print("no entro a seguir"+ str(seguir))

            self.delete_em_cont()

            contador = contador+1

       # print('contador: '+str(contador))

    # Funcion para empacar las cajas
    def empacar_s(self, CR: CajaRot, EM: EspMax, esq):

        # Esquina 0 en el origen del espacio maximal
        # Esquina 1 - 0 en X y max en y
        # Esquina 2 - max en x y max en y
        # Esquina 3 - 0 en Y max en X

        x1_ini = 0
        y1_ini = 0
        z1_ini = 0

        x2_fin = 0
        y2_fin = 0
        z2_fin = 0

        if esq == 0:
            x1_ini = EM.x1
            y1_ini = EM.y1

        elif esq == 1:
            x1_ini = EM.x1
            y1_ini = EM.y2-CR.y

        elif esq == 2:
            x1_ini = EM.x2-CR.x
            y1_ini = EM.y2-CR.y

        elif esq == 3:
            x1_ini = EM.x2-CR.x
            y1_ini = EM.y1

        # En Z la altura siempre va a ser la minima del Espacio Maximal
        z1_ini = EM.z1

        x2_fin = x1_ini+CR.x
        y2_fin = y1_ini+CR.y
        z2_fin = z1_ini+CR.z
        # print(z2_fin_n)
       # print(type(z1_ini+CR.z))

        id_c_emp = CR.id_p

        cajaEmpac = CajaEmpacada(
            id_c_emp, x1_ini, y1_ini, z1_ini, x2_fin, y2_fin, z2_fin)
        self.CajasEmpacadas.append(cajaEmpac)

        # Se tiene que remover las que estan encima antes de ponerla
        if len(self.cajasEmpMov) > 0:
            for i in self.cajasEmpMov:
                # Esta una sobre la otra
                if(i.z2 == z1_ini):
                    # Solapamiento en Y
                    if not((i.y1 > y2_fin) or (y1_ini > i.y2)):
                        # Solapamiento en X
                        if not((i.x1 > x2_fin) or (x1_ini > i.x2)):
                            self.cajasEmpMov.remove(i)

        self.cajasEmpMov.append(cajaEmpac)

        self.utilizacion += (CR.x*CR.y*CR.z)/self.vol_cont

        return (cajaEmpac)

    # Metodo Constructivo - donde se toma la decision de empacar las cajas

    def constructivo_s(self, cajas):

        # Para cada orientacion de la caja se evalua el best fit.. inicialmente la menor diferencia en X
        contador_cajas = 0
        # Diccionario de best fit
        best_fit = {}
        for i in cajas:
            contador_espmax = 0
            for j in self.EspMax_p:
                if (i.z+j.z1 <= j.z2):
                    for k in range(0, 4):
                        # distancia en X
                        best_fit[contador_cajas, contador_espmax, k] = j.x2-i.x
                contador_espmax = contador_espmax+1
            contador_cajas = contador_cajas+1

        # Se organizan las cajas, de menor a mayor - en este caso se escogen los menores.
        sorted_items = sorted(best_fit.items(), key=lambda x: x[1])

        # Print the sorted items
        # for key, value in sorted_items:
        #   print(f'{key}: {value}')

        # Obtener la lista de tuplas clave-valor y acceder al primer elemento
       # print(type(sorted_items))
        primer_elemento = sorted_items[0]

        # El primer elemento es una tupla (clave, valor)
        clave, valor = primer_elemento

        # Empacar Caja
        caja_param = cajas[clave[0]]
        esp_max_param = self.EspMax_p[clave[1]]
        esquina_param = clave[2]

        cajaEmp1 = self.empacar_s(caja_param, esp_max_param, esquina_param)
        # Empacar la caja y crear los nuevos espacios maximales
        self.crearEspacios(cajaEmp1)
        # Unir los espacios maximales
        self.todoEM()

        self.utilizacion = self.utilizacion + \
            (caja_param.x*caja_param.y*caja_param.z)/self.vol_cont

        # definir el espacio maximal donde se va a empacar la caja
        # crear las diferentes rotaciones de las cajas

        # El parametro cajas tiene la lista de las rotaciones de las cajas

    def best_pos_s(self, cajas):
        # Para cada orientacion de la caja se evalua el best fit.. inicialmente la menor diferencia en X
        contador_cajas = 0
        # Diccionario de best fit
        best_fit = {}
        for i in cajas:
            contador_espmax = 0
            for j in self.EspMax_p:
                # añadir las restricciones en X,Y,Z
                if (j.dz >= i.z):
                    # if (i.z+j.z1<=j.z2):
                    if(j.dx >= i.x) and (j.dy >= i.y):
                        for k in range(0, 4):
                            # distancia en X
                            best_fit[contador_cajas,
                                     contador_espmax, k] = j.x2-i.x
                contador_espmax = contador_espmax+1
            contador_cajas = contador_cajas+1

        # Se organizan las cajas, de menor a mayor - en este caso se escogen los menores.
        sorted_items = sorted(best_fit.items(), key=lambda x: x[1])

        # Print the sorted items
        # for key, value in sorted_items:
        #   print(f'{key}: {value}')

        # Obtener la lista de tuplas clave-valor y acceder al primer elemento
       # print(type(sorted_items))
        primer_element = sorted_items[0]

        # El primer elemento es una tupla (clave, valor)

        return(primer_element)

# Metodo constructivo con buffer
    def constructivo_buf(self, cajas):

        # El primer elemento es una tupla (clave, valor)
        clave, valor = self.best_pos_s(cajas)

        # Empacar Caja
        caja_param = cajas[clave[0]]
        esp_max_param = self.EspMax_p[clave[1]]
        esquina_param = clave[2]

        # empaco en buffer
        # si esta vacio entonces la guardo.. aún no la empaco
        if (len(buffer) < global_buffer):
            buffer.append(cajas)
        else:

            # definir si usar la caja del buffer o la de la banda
            # encontrar la caja con el minimo volumen del buffer

            lista_temp = []
            for i in buffer:
                lista_temp.append((i[0].x)*(i[0].y)*(i[0].z))
            min_vol = max(lista_temp)  # Encuentra el mínimo valor
            # Encuentra el indice de la caja
            minimo_vol_i = lista_temp.index(min_vol)

            # si el valor del volumen de la caja que entra es menor o igual al menor volumen del buffer entonces entra
            vol_caj_actual = cajas[0].x*cajas[0].y*cajas[0].z

            if(vol_caj_actual > min_vol):
                cajaEmp1 = self.empacar_s(
                    caja_param, esp_max_param, esquina_param)
                # Empacar la caja y crear los nuevos espacios maximales
                self.crearEspacios(cajaEmp1)

                # Unir los espacios maximales
                self.todoEM()

            else:
                caja_min_buf = buffer[minimo_vol_i]
                clave, valor = self.best_pos_s(caja_min_buf)

                # Empacar Caja
                caja_param = caja_min_buf[clave[0]]
                esp_max_param = self.EspMax_p[clave[1]]
                esquina_param = clave[2]

                cajaEmp1 = self.empacar_s(
                    caja_param, esp_max_param, esquina_param)
                # Empacar la caja y crear los nuevos espacios maximales
                self.crearEspacios(cajaEmp1)
                # Unir los espacios maximales
                self.todoEM()

                # Eliminar el elemento del buffer
                del buffer[minimo_vol_i]
                buffer.append(cajas)


# Metodo constructivo con buffer y elegir las cajas aleatorias;
    """
    Cajas: es una lista de cajas rotadas
    """

    def constructivo_buf_rand(self, cajas):

        # El primer elemento es una tupla (clave, valor)
        clave, valor = self.best_pos_s(cajas)

        # Empacar Caja
        caja_param = cajas[clave[0]]
        esp_max_param = self.EspMax_p[clave[1]]
        esquina_param = clave[2]

        # empaco en buffer
        # si esta vacio entonces la guardo.. aún no la empaco
        if (len(buffer) < global_buffer):
            buffer.append(cajas)
        else:

            # LLAMAR LA FUNCION
            cajas_p = [cajas, buffer]

            best_uti, best_em, best_sol = contenedorRandom(self, cajas_p)

            # le devuelve una CajaEmpacada
            # Se escoge la primera como criterio aleatorio
            empacar = best_sol[0]

            # Es de las que entra
            if(cajas[0].id_p == empacar.id_p):

                cajaEmp1 = self.empacar_s(
                    caja_param, esp_max_param, esquina_param)
                # Empacar la caja y crear los nuevos espacios maximales
                self.crearEspacios(cajaEmp1)
                # Unir los espacios maximales
                self.todoEM()
            else:
                for i in buffer:
                    if i.id_p == empacar.id_p:

                        caja_min_buf = i
                        clave, valor = self.best_pos_s(caja_min_buf)

                        # Empacar Caja
                        caja_param = caja_min_buf[clave[0]]
                        esp_max_param = self.EspMax_p[clave[1]]
                        esquina_param = clave[2]

                        cajaEmp1 = self.empacar_s(
                            caja_param, esp_max_param, esquina_param)
                        # Empacar la caja y crear los nuevos espacios maximales
                        self.crearEspacios(cajaEmp1)
                        # Unir los espacios maximales
                        self.todoEM()

                        # Eliminar el elemento del buffer
                        buffer.remove(i)
                        buffer.append(cajas)

                        break

            # tengo que saber si esta en el buffer

    # tengo que definir una funcion apra usa

    # Volver a la lista de poder moverse

    # Recibe una lista de CajaEmpacada
    def volver_av(self, lista_volv):
        for i in lista_volv:
            self.cajasEmpMov.append(i)

    # elimino la caja de las listas y devuelvo para que se guarde en el buffer
    # Se actualizan los espacios maximales---- como al quitarlo entonces tengo que vovlerlos a crear
    def eliminarbox(self, id_p_box):

        vol = 0

        for i in self.cajasEmpMov:

            if(i.id_p == id_p_box):

                vol = abs(i.x2-i.x1)*abs(i.y2-i.y1)*abs(i.z2-i.z1)
                eliminada = i
                self.cajasEmpMov.remove(i)
                self.CajasEmpacadas.remove(i)

                break

        self.utilizacion -= vol/self.vol_cont
        return(eliminada)

# Metodo constructivo con buffer y rearrangement Random--- REVISAR

#####

# ME FALTA LA PARTE DE REAARRANGED SE ME DAÑA :( )
    def constructivo_buf_rearrangement_rand(self, cajas, contador_cajas, max_cajas):

        # empaco en buffer
        # si esta vacio entonces la guardo.. aún no la empaco
        if (len(buffer) < global_buffer) and (max_cajas-contador_cajas > global_buffer):
            buffer.append(cajas)
          #  print("entro_aca")
        else:

            # Le paso todas las cajas

            cajas_p = []

            uti_antes = 0
            if len(cajas) > 0:
                # for i in range(0,len(cajas)):
                cajas_p.append(cajas)
            # print(len(cajas_p))

            if len(buffer) > 0:
                for i in range(0, len(buffer)):
                    cajas_p.append(buffer[i])

            if (len(self.cajasEmpMov) > 0) and (max_rear > 0):

                aux_empMov = []
                cont_rear = 0
                emp = []

                for i in self.cajasEmpMov:
                    emp.append(i)

                while (cont_rear < max_rear):

                    if len(emp) > 0:
                        rand = random.randint(0, len(emp)-1)
                        # guardo la lista de las que saco
                        aux_empMov.append(emp[rand])
                        # saco de la lista la que ya decidí sacar
                        emp.pop(rand)
                       # print("entro")
                        cont_rear += 1
                    else:
                        # cont_rear=1000000000000000
                        cont_rear = float("inf")

                # En este for se saca la caja de las que estan ya empacadas, porque se va a volver a empacar
             #   gu=len(cajas_p)
              #  cle=len(self.CajasEmpacadas)
                eliminadas = []
                uti_antes = self.utilizacion

                for i in range(0, len(aux_empMov)):
                    cajaEmp = aux_empMov[i]
                    caja_p21 = CajaTipo(cajaEmp.id_p, abs(
                        cajaEmp.x2-cajaEmp.x1), abs(cajaEmp.y2-cajaEmp.y1), abs(cajaEmp.z2-cajaEmp.z1), 0, 0, 3)
                    l3_in = caja_p21.list_caja
                    cajas_p.append(l3_in)
                 #   print("cajas_emp antes: "+str(len(self.CajasEmpacadas)))
                    eliminadas.append(self.eliminarbox(cajaEmp.id_p))
                  #  print("cajas_emp despues: "+str(len(self.CajasEmpacadas)))

            self.EspMax_p = [
                EspMax(0, 0, 0, self.x_cont_glob, self.y_cont_glob, self.z_cont_glob)]
         #   print("EM INI: "+str(len(self.EspMax_p)))
          #  print("primero "+str(self.EspMax_p[0].x1)+", "+str(self.EspMax_p[0].x2)+", "+str(self.EspMax_p[0].y1)+", "+str(self.EspMax_p[0].y2)+", "+str(self.EspMax_p[0].z1)+", "+str(self.EspMax_p[0].z2)+", ")

            resp_global_ce = []
            # contadorrr=0
            for i in self.CajasEmpacadas:
                # contadorrr+=1
                #print("contador"+ str(contadorrr))
                self.crearEspacios(i)
                self.todoEM()
                resp_global_ce.append(i)
                #    print("caja "+str(i.id_p)+" "+str(i.x1)+", "+str(i.x2)+", "+str(i.y1)+", "+str(i.y2)+", "+str(i.z1)+", "+str(i.z2)+", ")

            #print("EM fin: "+str(len(self.EspMax_p)))
            contener0 = 0
            resp_global_max = []
            resp_global_max_es = []
            for i in range(0, len(self.EspMax_p)):
                resp_global_max.append(i)
                resp_global_max_es.append(self.EspMax_p[i])
                contener0 += 1
              #  print(str(i)+" "+str(self.EspMax_p[i].x1)+", "+str(self.EspMax_p[i].x2)+", "+str(self.EspMax_p[i].y1)+", "+str(self.EspMax_p[i].y2)+", "+str(self.EspMax_p[i].z1)+", "+str(self.EspMax_p[i].z2)+", ")

            #print("entrooo: a"+str(contener0))

          #  print("Esp_max: "+str(len(self.EspMax_p)))
           # print("Cajas a empacar: "+str(len(cajas_p)))
            #print("Espacios maximales: "+str(len(self.EspMax_p)))

           # print("cajas a empacar "+str(len(cajas_p)))
            best_uti, best_em, best_sol, best_cajas, esp_best, esquinas = contenedorRandom(self, cajas_p)

          #  print("best_uti:"+ str(best_uti))
           # print(len(best_cajas))
           # print("uti_antes: "+str(uti_antes))

            # si la utilizacion mejora es porque es una mejor solucion
            # Antes de empacar tengo que ver si hay delete o no
            if(uti_antes > best_uti):
                # print("entro acaaa siu señore")
                for i in eliminadas:
                    # cajaEmp1=self.empacar_s(best_cajas[j],esp_best[j],esquinas[j])
                    # Empacar la caja y crear los nuevos espacios maximales
                    self.CajasEmpacadas.append(i)
                    z1_ini = i.z1
                    y1_ini = i.y1
                    y2_fin = i.y2
                    x1_ini = i.x1
                    x2_fin = i.x2

                    # Se tiene que remover las que estan encima antes de ponerla
                    if len(self.cajasEmpMov) > 0:
                        for r in self.cajasEmpMov:
                            # Esta una sobre la otra
                            if(r.z2 == z1_ini):
                                # Solapamiento en Y
                                if not((r.y1 > y2_fin) or (y1_ini > r.y2)):
                                    # Solapamiento en X
                                    if not((r.x1 > x2_fin) or (x1_ini > r.x2)):
                                        self.cajasEmpMov.remove(r)

                    self.cajasEmpMov.append(i)

                    self.utilizacion += (abs(i.x2-i.x1)*abs(i.y2-i.y1)
                                         * abs(i.z2-i.z1))/self.vol_cont

                    self.crearEspacios(i)
                    # Unir los espacios maximales
                    self.todoEM()

            elif (best_uti <= 1):

                for j in range(0, len(best_cajas)):
                    #    print("entro acaaaaa")
                    empacar = best_cajas[j]
                    cajaEmp1 = self.empacar_s(
                        best_cajas[j], esp_best[j], esquinas[j])
                    # Empacar la caja y crear los nuevos espacios maximales
                  #  contaa=0
                 #   print("antes")
                  #  for i in self.EspMax_p:
                #     contaa+=1
                    #    print("Esp "+str(contaa))
                    #   print("z1 "+str(i.z1))
                    #  print("z2 "+str(i.z2))

                    self.crearEspacios(cajaEmp1)

                #    print("despues")
                 #   for i in self.EspMax_p:
                  #      contaa+=1
                #     print("Esp "+str(contaa))
                    #    print("z1 "+str(i.z1))
                    #   print("z2 "+str(i.z2))

                    # Unir los espacios maximales
                    self.todoEM()

                    for i in buffer:
                        if i[0].id_p == empacar.id_p:
                            # Eliminar el elemento del buffer
                            buffer.remove(i)
                           # buffer.append(cajas)

        return(self.CajasEmpacadas, self.EspMax_p)

        # meter_en_buf=best_cajas[len(best_cajas)-1]
        # caja_meter_buf=CajaTipo(meter_en_buf.id_p, meter_en_buf.x, meter_en_buf.y, meter_en_buf.z, 0, 0, 3)
        # lbuf=caja_meter_buf.list_caja
        # buffer.append(lbuf)

    """
                        
                        if(buff==False):
                            if(len(self.cajasEmpMov)>0):
                                
                                for j in self.cajasEmpMov:
                                    
                                    if(j.id_p == empacar.id_p):
                                    #####Sacar la caja
                                        id_p_del=j.id_p
                                        meter_en_buf=self.eliminarbox(id_p_del)
                                        
                                        #con la caja que saque la vuelvo a meter al buffer
                                        caja_meter_buf=CajaTipo(id_p_del, meter_en_buf.x2-meter_en_buf.x1, meter_en_buf.y2-meter_en_buf.y1, meter_en_buf.z2-meter_en_buf.z1, 0, 0, 3)
                                        lbuf=caja_meter_buf.list_caja
                                        buffer.append(lbuf)
                                        
                                    
                                #ingreso la del buffer
                                caja_min_buf=empacar
                                clave, valor = self.best_pos_s(caja_min_buf)
                                
                                ##Empacar Caja
                                caja_param=caja_min_buf[clave[0]]
                                esp_max_param=self.EspMax_p[clave[1]]
                                esquina_param=clave[2]
                                
                                cajaEmp1=self.empacar_s(caja_param,esp_max_param,esquina_param)
                     
                        
                                #Empacar la caja y crear los nuevos espacios maximales 
                                self.crearEspacios(cajaEmp1)
                                #Unir los espacios maximales
                                self.todoEM()
                                
                                #elimino la caja del buffer
                                
                                for i in buffer:
                                    if(i.id_p==empacar.id_p):
                                        buffer.remove(i)
                                        break
                                """


# Metodo constructivo con buffer y rearrangement
    def constructivo_buf_rearrangement(self, cajas):

        # El primer elemento es una tupla (clave, valor)
        clave, valor = self.best_pos_s(cajas)

        # Empacar Caja
        caja_param = cajas[clave[0]]
        esp_max_param = self.EspMax_p[clave[1]]
        esquina_param = clave[2]

        # empaco en buffer
        # si esta vacio entonces la guardo.. aún no la empaco
        if (len(buffer) < global_buffer):
            buffer.append(cajas)
        else:
            # definir si usar la caja del buffer o la de la banda
            # encontrar la caja con el minimo volumen del buffer
            lista_temp = []
            for i in buffer:
                lista_temp.append((i[0].x)*(i[0].y)*(i[0].z))
            min_vol = min(lista_temp)  # Encuentra el mínimo valor
            # Encuentra el indice de la caja
            minimo_vol_i = lista_temp.index(min_vol)

            # si el valor del volumen de la caja que entra es menor o igual al menor volumen del buffer entonces entra
            vol_caj_actual = cajas[0].x*cajas[0].y*cajas[0].z
            if(vol_caj_actual > min_vol):
                cajaEmp1 = self.empacar_s(
                    caja_param, esp_max_param, esquina_param)
                # Empacar la caja y crear los nuevos espacios maximales
                self.crearEspacios(cajaEmp1)
                # Unir los espacios maximales
                self.todoEM()
            else:
                caja_min_buf = buffer[minimo_vol_i]
                clave, valor = self.best_pos_s(caja_min_buf)

                # Empacar Caja
                caja_param = caja_min_buf[clave[0]]
                esp_max_param = self.EspMax_p[clave[1]]
                esquina_param = clave[2]

                cajaEmp1 = self.empacar_s(
                    caja_param, esp_max_param, esquina_param)
                # Empacar la caja y crear los nuevos espacios maximales
                self.crearEspacios(cajaEmp1)
                # Unir los espacios maximales
                self.todoEM()

                # Eliminar el elemento del buffer
                del buffer[minimo_vol_i]
                buffer.append(cajas)

        # rearrange

        if(len(self.cajasEmpMov) > 0):
            # revisar entre el min de los que se pueden mover y el buffer
            lista_temp_buf = []
            for i in buffer:
                lista_temp_buf.append((i[0].x)*(i[0].y)*(i[0].z))
            min_vol_buf = min(lista_temp_buf)  # Encuentra el mínimo valor
            minimo_vol_i_buf = lista_temp_buf.index(
                min_vol_buf)  # Encuentra el indice de la caja

            lista_temp_rea = []
           # print(len(self.cajasEmpMov))
            for i in self.cajasEmpMov:
                lista_temp_rea.append((i.x2-i.x1)*(i.y2-i.y1)*(i.z2-i.z1))
            min_vol_rea = min(lista_temp_rea)  # Encuentra el mínimo valor
            minimo_vol_i_rea = lista_temp_rea.index(
                min_vol_rea)  # Encuentra el indice de la caja

            # si el volumenr del bufeer es mayor al de rea.. entonces ingreso buf y saco rea
            if(min_vol_buf > min_vol_rea):
              #  print("entro")
                # Sacar la caja
                id_p_del = self.cajasEmpMov[minimo_vol_i_rea].id_p
                meter_en_buf = self.eliminarbox(id_p_del)

                # ingreso el del buffer
                caja_min_buf = buffer[minimo_vol_i_buf]
                clave, valor = self.best_pos_s(caja_min_buf)

                # Empacar Caja
                caja_param = caja_min_buf[clave[0]]
                esp_max_param = self.EspMax_p[clave[1]]
                esquina_param = clave[2]

                cajaEmp1 = self.empacar_s(
                    caja_param, esp_max_param, esquina_param)

                # Empacar la caja y crear los nuevos espacios maximales
                self.crearEspacios(cajaEmp1)
                # Unir los espacios maximales
                self.todoEM()

                # elimino la caja del buffer
                del buffer[minimo_vol_i_buf]

                # con la caja que saque la vuelvo a meter al buffer
                caja_meter_buf = CajaTipo(id_p_del, meter_en_buf.x2-meter_en_buf.x1,
                                          meter_en_buf.y2-meter_en_buf.y1, meter_en_buf.z2-meter_en_buf.z1, 3, 3, 3)
                lbuf = caja_meter_buf.list_caja
                buffer.append(lbuf)


# Clase contenedor Resumido
class ContenedorSum():

    def __init__(self, cont: Contenedor):
        self.EspMax_p = []
        for i in cont.EspMax_p:
            self.EspMax_p.append(EspMax(i.x1, i.y1, i.z1, i.x2, i.y2, i.z2))

        self.utilizacion = cont.utilizacion

        self.CajasEmpacadas = []
        for j in cont.CajasEmpacadas:
            self.CajasEmpacadas.append(CajaEmpacada(
                j.id_p, j.x1, j.y1, j.z1, j.x2, j.y2, j.z2))

        self.volem = cont.get_volem()
        self.vol_cont = cont.vol_cont

        self.cajasEmpMov = []
        for j in cont.cajasEmpMov:
            self.cajasEmpMov.append(CajaEmpacada(
                j.id_p, j.x1, j.y1, j.z1, j.x2, j.y2, j.z2))


# Funciones copiarlas


    def get_volem(self):
        volem = 0
        for i in self.EspMax_p:
            volem = i.dx*i.dy*i.dz+volem

        n = len(self.EspMax_p)

        if n == 0:
            resp = 0
        else:
            resp = volem/n

        return (resp)

    def empacar_s(self, CR: CajaRot, EM: EspMax, esq):

        # Esquina 0 en el origen del espacio maximal
        # Esquina 1 - 0 en X y max en y
        # Esquina 2 - max en x y max en y
        # Esquina 3 - 0 en Y max en X

        x1_ini = 0
        y1_ini = 0
        z1_ini = 0

        x2_fin = 0
        y2_fin = 0
        z2_fin = 0

        if esq == 0:
            x1_ini = EM.x1
            y1_ini = EM.y1

            x2_fin = x1_ini+CR.x
            y2_fin = y1_ini+CR.y

        elif esq == 1:
            x1_ini = EM.x1
            x2_fin = x1_ini+CR.x

            y1_ini = EM.y2-CR.y
            y2_fin = y1_ini+CR.y

        elif esq == 2:
            x1_ini = EM.x2-CR.x
            x2_fin = x1_ini+CR.x

            y1_ini = EM.y2-CR.y
            y2_fin = y1_ini+CR.y

        elif esq == 3:
            x1_ini = EM.x2-CR.x
            x2_fin = x1_ini+CR.x

            y1_ini = EM.y1
            y2_fin = y1_ini+CR.y

        # En Z la altura siempre va a ser la minima del Espacio Maximal
        z1_ini = EM.z1
        z2_fin = z1_ini+CR.z
       # print("empacando")
        # print(z2_fin_n)
       # print(type(z1_ini+CR.z))

        id_c_emp = CR.id_p

        cajaEmpac = CajaEmpacada(
            id_c_emp, x1_ini, y1_ini, z1_ini, x2_fin, y2_fin, z2_fin)

        # agrego a la lista de cajas empacadas
        self.CajasEmpacadas.append(cajaEmpac)

        # Se tiene que remover las que estan encima antes de ponerla
        if len(self.cajasEmpMov) > 0:
            for i in self.cajasEmpMov:
                # Esta una sobre la otra
                if(i.z2 == z1_ini):
                    # Solapamiento en Y
                    if not((i.y1 > y2_fin) or (y1_ini > i.y2)):
                        # Solapamiento en X
                        if not((i.x1 > x2_fin) or (x1_ini > i.x2)):
                            self.cajasEmpMov.remove(i)

        self.cajasEmpMov.append(cajaEmpac)

        return (cajaEmpac)

    def crearEspacios(self, CE: CajaEmpacada):
        resp = []
        for ii in range(len(self.EspMax_p)-1, -1, -1):
            i = self.EspMax_p[ii]
            seUsa = False
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (CE.y1-i.y1 > 0):
                resp.append(EspMax(i.x1, i.y1, i.z1, i.x2, CE.y1, i.z2))
                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (CE.x1-i.x1 > 0):
                resp.append(EspMax(i.x1, i.y1, i.z1, CE.x1, i.y2, i.z2))

                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (i.y2-CE.y2 > 0):
                resp.append(EspMax(i.x1, CE.y2, i.z1, i.x2, i.y2, i.z2))

                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (i.x2-CE.x2 > 0):
                resp.append(EspMax(CE.x2, i.y1, i.z1, i.x2, i.y2, i.z2))

                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (CE.z1-i.z1 > 0):
                resp.append(EspMax(CE.x1, CE.y1, i.z1, CE.x2, CE.y2, CE.z1))

                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (i.z2-CE.z2 > 0):
                resp.append(EspMax(CE.x1, CE.y1, CE.z2, CE.x2, CE.y2, i.z2))

                seUsa = True

            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (i.z2-CE.z2 == 0):
                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (CE.z1-i.z1 == 0):
                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (i.x2-CE.x2 == 0):
                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (i.y2-CE.y2 == 0):
                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (CE.x1-i.x1 == 0):
                seUsa = True
            if not(i.x1 >= CE.x2 or CE.x1 >= i.x2 or i.y1 >= CE.y2 or CE.y1 >= i.y2 or i.z1 >= CE.z2 or CE.z1 >= i.z2) and (CE.y1-i.y1 == 0):
                seUsa = True

            if (seUsa):
                self.EspMax_p.pop(ii)
                # print (ii)
                # print(resp)
                # print(self.EspMax_p)

        for j in resp:
            self.EspMax_p.append(j)

        return(self.EspMax_p)

     # Funciones EM

    def delete_em_cont(self):
        for ii in range(len(self.EspMax_p)-1, -1, -1):
            i = self.EspMax_p[ii]
            for jj in range(len(self.EspMax_p)-1, ii, -1):
                # Caso de j contenido en
                j = self.EspMax_p[jj]
                if(i != j):
                    if((i.x1 <= j.x1) and (j.x2 <= i.x2) and (i.y1 <= j.y1) and (j.y2 <= i.y2) and (i.z1 <= j.z1) and (j.z2 <= i.z2)):
                        self.EspMax_p.pop(jj)
        # self.EspMax_p=nuevos_esp

    def juntarEspacios(self):

        bool_p = False
        for ii in range(len(self.EspMax_p)-1, -1, -1):
            i = self.EspMax_p[ii]
            for jj in range(len(self.EspMax_p)-1, ii, -1):
                # Caso de se solapa en Z
                j = self.EspMax_p[jj]
                salio = False
                if (i.z1 == j.z1) and (i.z2 == j.z2):
                    # Caso igual en X
                    if (i.x1 == j.x1) and (i.x2 == j.x2):
                        if not((i.y1 > j.y2) or (j.y1 > i.y2)):
                            y1 = min(i.y1, j.y1)
                            y2 = max(i.y2, j.y2)
                            nuevo_em = EspMax(i.x1, y1, i.z1, i.x2, y2, i.z2)
                            self.EspMax_p.pop(jj)
                            self.EspMax_p[ii] = nuevo_em
                            i = nuevo_em
                            salio = True
                            bool_p = True

                    # Caso igual en Y
                    if (i.y1 == j.y1) and (i.y2 == j.y2):
                        if not((i.x1 > j.x2) or (j.x1 > i.x2)):
                            x1 = min(i.x1, j.x1)
                            x2 = max(i.x2, j.x2)
                            nuevo_em = EspMax(x1, i.y1, i.z1, x2, j.y2, i.z2)
                            if salio == False:
                                self.EspMax_p.pop(jj)
                            self.EspMax_p[ii] = nuevo_em
                            i = nuevo_em
                            bool_p = True

        return(self.EspMax_p, bool_p)

    # Expandir
    def expandirEm(self):
        bool_p = False
        for ii in range(len(self.EspMax_p)-1, -1, -1):
            i = self.EspMax_p[ii]
            for jj in range(len(self.EspMax_p)-1, -1, -1):
                j = self.EspMax_p[jj]
                if(i != j):
                    # Igual en Z
                    if (i.z1 == j.z1) and (i.z2 == j.z2):
                        # Contencion en X
                        if(i.x1 <= j.x1) and (j.x2 <= i.x2):
                            # Solapamiento en Y
                            if not((i.y1 > j.y2) or (j.y1 > i.y2)):
                                # expandir EM
                                min_y = min(i.y1, j.y1, i.y2, j.y2)
                                max_y = max(i.y2, j.y2, i.y1, j.y1)

                                exp_em = EspMax(
                                    j.x1, min_y, j.z1, j.x2, max_y, j.z2)
                                self.EspMax_p[jj] = exp_em
                                bool_p = True

                                # No eliminar espacio maximal

                        # Contencion en Y
                        if(i.y1 <= j.y1) and (j.y2 <= i.y2):
                            # Solapamiento en X
                            if not((i.x1 > j.x2) or (j.x1 > i.x2)):
                                # expandir EM
                                min_x = min(i.x1, j.x1, i.x2, j.x2)
                                max_x = max(i.x2, j.x2, i.x1, j.x1)
                                exp_em = EspMax(
                                    min_x, j.y1, j.z1, max_x, j.y2, j.z2)
                                self.EspMax_p[jj] = exp_em
                                bool_p = True

        return(bool_p)

    # Juntar los metodos
    def todoEM(self):
        seguir = True
        a = []
        contador = 1
      #  esp_max_ini=self.EspMax_p

        while(seguir):

            seguir = False

            esp_max_ini = []
            for i in self.EspMax_p:
                esp_max_ini.append(i)

            a, bool_junt = self.juntarEspacios()

            esp_max_ini = []
            for i in self.EspMax_p:
                esp_max_ini.append(i)

            bool_exp = self.expandirEm()

            for i in range(0, len(esp_max_ini)):
                if esp_max_ini[i] != self.EspMax_p[i]:
                    bool_exp = False

           # if not(esp_max_ini!=self.EspMax_p):
            #    bool_exp=False

            if(bool_junt == True or bool_exp == True):
                seguir = True

            # if(seguir==False):
             #   print("no entro a seguir"+ str(seguir))

            self.delete_em_cont()

       # print('contador: '+str(contador))


# FUNCION PARA ORDENAR 3 NUMEROS PARA TENER EL BEST FIT.

    def sort_3(self, a, b, c):
        if a <= b <= c:
            return a, b, c
        elif a <= c <= b:
            return a, c, b
        elif b <= a <= c:
            return b, a, c
        elif b <= c <= a:
            return b, c, a
        elif c <= a <= b:
            return c, a, b
        else:
            return (c, b, a)

    def cont_aleatorio(self, cajas_pe):

        # escoger aleatoriamente la pos de la caja
      #  print("largo caa" + str(len(cajas_p)))
       # Luego de escogerlo, escogo el espacio maximal random
       # cajasempMov
        cajas_p = []
        cajas_per = []
        for i in cajas_pe:
            cajas_p.append(i)
            cajas_per.append(i)
        
        caja_param_l = []
        esp_max_param_l = []
        esquina_param_l = []

        if len(cajas_p) > 0:
         #   print("Entro acaaa en donde las cajas son mayores a 0 ")
            # escogo el espacio maximal mas pequeño
            cajas_a_uti = False

            while cajas_a_uti == False:

                cabe = False
                aux_esp_max = []
                # Se guardan los espacios maximales si actualizar es true
                for i in self.EspMax_p:
                    aux_esp_max.append(i)

                while cabe == False:
                    vol_ini = 100000000000000000

                    # escogo el espacio maximal mas peqqueno-- con esto la uti es de 0.57
                    # escogamos el espacio maximal más grande -- con esto la uti es de
                    # vol_ini=0
                    esp_peq = None
                    # print(len(aux_esp_max))
                    for i in aux_esp_max:
                        vol_is = abs(i.x1-i.x2)*abs(i.y1-i.y2)*abs(i.z1-i.z2)
                      #  print(vol_is)
                        if(vol_is < vol_ini):
                            vol_ini = vol_is
                            esp_peq = i

                            # print(vol_i)
                    # tengo el más pequeno voy a ver si hay alguna caja que entre en el:
                    cajas_fit = []
                    if esp_peq != None:
                        for i in cajas_p:
                            # escogo la mejor posicion con respecto al eje x
                            cajas_buenas = []
                            for j in i:
                                random_box = j
                                # verifico que la caja entra en el espacio maximal
                                if (random_box.z+esp_peq.z1 <= esp_peq.z2) and (random_box.x+esp_peq.x1 <= esp_peq.x2) and (random_box.y+esp_peq.y1 <= esp_peq.y2) and self.utilizacion < 1:
                                    cajas_buenas.append(random_box)
                                    cabe = True

                        # escoger la mejor posicion con respecto al eje x
                        # tabla_fit=[]
                        if len(cajas_buenas) > 0:
                            # eje_x_dist=100000000000
                            # eje_y_dist=100000000000
                            # eje_z_dist=100000000000
                            mejor_caja = None

                            dicc = {}

                            for j in cajas_buenas:
                                resp = self.sort_3(abs(j.x+esp_peq.x1-esp_peq.x2), abs(
                                    j.y+esp_peq.y1-esp_peq.y2), abs(j.z+esp_peq.z1-esp_peq.z2))
                                dicc[j] = resp

                            tripletas_ordenadas = sorted(
                                dicc.items(), key=lambda item: item[1])

                            # Ahora tienes la lista de tripletas ordenadas de menor a mayor
                            # for objeto, tripleta in tripletas_ordenadas:
                            #   print("Objeto:", objeto.x)
                            #  print("Tripleta ordenada:", tripleta)

                          #   objetos_organizados = sorted(objetos, key=lambda obj: (obj.valor1, obj.valor2, obj.valor3))

                          #  print(tripletas_ordenadas)
                           # print(dicc)
                            iterador_claves = iter(tripletas_ordenadas)
                            primera_clave = next(iterador_claves)
                            # valor_primera_clave = dicc[primera_clave]

                            cajas_fit.append(primera_clave[0])

                    # si no entra en ninguno entonces tengo que eliminar el espacio maximal
                    if cabe == False and len(aux_esp_max) > 1:
                        # print(esp_peq.id)
                        # print(esp_peq.x1)
                        #print("antes "+ str(len(aux_esp_max)))
                        aux_esp_max.remove(esp_peq)
                        #print("despues "+ str(len(aux_esp_max)))
                    elif cabe == False and len(aux_esp_max) == 1:
                        aux_esp_max.remove(esp_peq)

                    else:
                        cabe = True
                        # aux_esp_max.remove(esp_peq)

                # tengo el espacio maximal mas pequeno y la lista de cajas que caben en ese espacio maximal
                    # Selecciono la caja que tenga un mejor fit con respecto al eje x
                if len(cajas_fit) > 0:
                  #  eje_x_dist=100000000000
                    # eje_y_dist=100000000000
                    # eje_z_dist=100000000000

                    mejor_caja = None

                    dicc = {}

                    for j in cajas_fit:
                        resp = self.sort_3(abs(j.x+esp_peq.x1-esp_peq.x2), abs(
                            j.y+esp_peq.y1-esp_peq.y2), abs(j.z+esp_peq.z1-esp_peq.z2))
                        dicc[j] = resp
                 #   print("antes")
                  #  print (dicc)
                    tripletas_ordenadas = sorted(dicc.items(), key=lambda item: item[1])

                    # Ahora tienes la lista de tripletas ordenadas de menor a mayor
                 #   for objeto, tripleta in tripletas_ordenadas:
                  #      print("Objeto:", objeto.x)
                    #     print("Tripleta ordenada:", tripleta)

                #   objetos_organizados = sorted(objetos, key=lambda obj: (obj.valor1, obj.valor2, obj.valor3))

                  #  print("TRIPLETAS ORDENADAS 0:"+str(tripletas_ordenadas))
                #    print("TRIPLETAS ORDENADAS 1:"+str(dicc))

                    iterador_claves = iter(tripletas_ordenadas)
                    primera_clave = next(iterador_claves)
                  #  print("primer clave"+str(primera_clave))
                  #  valor_primera_clave = dicc[primera_clave]

                    mejor_caja = primera_clave[0]
                    # empacar la mejor caja

                    # definir aleatoriamente la esquina
                    # k=random.randint(0,3)
                    # k=1
                    # Definir en que esquina se va a empacar, la empaco en la esquina que sea mas cerca a la pared

                    # calculo distancia cartesiana a la esquina de la caja

                    dist_0 = ((esp_peq.x1-0)**2+(esp_peq.y1-0)**2)**(1/2)
                    dist_1 = ((esp_peq.x1-0)**2+(esp_peq.y2-10)**2)**(1/2)
                    dist_2 = ((esp_peq.x2-10)**2+(esp_peq.y2-10)**2)**(1/2)
                    dist_3 = ((esp_peq.x2-10)**2+(esp_peq.y1-0)**2)**(1/2)

                    minim = min(dist_0, dist_1, dist_2, dist_3)

                    if minim == dist_0:
                        k = 0
                    elif minim == dist_1:
                        k = 1
                    elif minim == dist_2:
                        k = 2
                    else:
                        k = 3
                    # Empacar Caja
                    caja_param = mejor_caja
                    esp_max_param = esp_peq
                    esquina_param = k

                    caja_param_l.append(mejor_caja)
                    esp_max_param_l.append(esp_max_param)
                    esquina_param_l.append(k)

                    cajaEmp1 = self.empacar_s(
                        caja_param, esp_max_param, esquina_param)
                    # Empacar la caja y crear los nuevos espacios maximales
                    self.crearEspacios(cajaEmp1)
                    # Unir los espacios maximales
                    self.todoEM()

                    # esp_max_param_l.append(self.EspMax_p)

                    self.utilizacion = self.utilizacion + \
                        ((caja_param.x*caja_param.y*caja_param.z)/self.vol_cont)

                    # elimino la caja a guardar
                    for i in cajas_p:
                        if(i[0].id_p == mejor_caja.id_p):
                            cajas_p.remove(i)
                            break
            #    print(len(cajas_p))
             #   print(len(aux_esp_max))
                if((len(cajas_p) == 0) or (len(aux_esp_max) == 0)):
                    cajas_a_uti = True

            # print("entro aca "+str(len(cajas_p)))

            # tengo que pasarle los espacios Maximales sin esas cajas para que las vuelva a acomodar

             # Se escoge el espacio maximal random
                # empaco aleatoriamente

            """
            caja_param_l=[]
            esp_max_param_l=[]
            esquina_param_l=[]
          
            box_to_pack_i=random.randint(0,len(cajas_val)-1)
            pack=cajas_val[box_to_pack_i]
            
            #definir aleatoriamente la esquina
            k=random.randint(0,3)
            
            ##Empacar Caja
            caja_param=pack
            esp_max_param=esp_max_rand
            esquina_param=k
            
            caja_param_l.append(pack)
            esp_max_param_l.append(esp_max_rand)
            esquina_param_l.append(k)
            
            
            cajaEmp1=self.empacar_s(caja_param,esp_max_param,esquina_param)
            #Empacar la caja y crear los nuevos espacios maximales 
            self.crearEspacios(cajaEmp1)
            #Unir los espacios maximales
            self.todoEM()
            
            #esp_max_param_l.append(self.EspMax_p)
            
            self.utilizacion=self.utilizacion+((caja_param.x*caja_param.y*caja_param.z)/self.vol_cont)
            
            
            
               
            """
            # print("evlauar")
            # print(len(caja_param_l))
            # print(len(esp_max_param_l))
            # print(len(esquina_param_l))

        return(caja_param_l, esp_max_param_l, esquina_param_l)

        # print(sol)

    # se escoge primero el espacio maximal donde caben las cajas

    def cont_aleatorio_2(self, cajas_p):

        # Se recorre uno a uno los espacios maximales.

        for i in self.EspMax_p:

            # Escoger la pos de la caja aleatoriamente

            print('hola')

        # escoger aleatoriamente la pos de la caja
        for i in cajas_p:
            # Para cada caja escojo la posicion random
            random_box_index = random.randint(0, len(i)-1)
            random_box = i[random_box_index]

            # Luego de escogerlo, escogo el espacio maximal random

            entro = True

            while entro:

                random_esp_max = random.randint(0, len(self.EspMax_p)-1)
                esp_max_rand = self.EspMax_p[random_esp_max]
                # print(esp_max_rand.z2)
             #   print("esp max z1: "+str(esp_max_rand.z1))
             #   print("esp max z2: "+str(esp_max_rand.z2))
             #   print("z box: "+ str(random_box.z))

              #  print("esp max x1: "+str(esp_max_rand.x1))
                # print("esp max x2: "+str(esp_max_rand.x2))
                #print("x box :"+ str(random_box.x))

                # print("esp max y1: "+str(esp_max_rand.y1))
                # print("esp max y2: "+str(esp_max_rand.y2))
                # print("y box: "+ str(random_box.y))

                if (random_box.z+esp_max_rand.z1 <= esp_max_rand.z2) and (random_box.x+esp_max_rand.x1 <= esp_max_rand.x2) and (random_box.y+esp_max_rand.y1 <= esp_max_rand.y2):

                    # definir aleatoriamente la esquina
                    k = random.randint(0, len(self.EspMax_p)-1)

                    # Empacar Caja
                    caja_param = random_box
                    esp_max_param = esp_max_rand
                    esquina_param = k

                    cajaEmp1 = self.empacar_s(
                        caja_param, esp_max_param, esquina_param)
                    # Empacar la caja y crear los nuevos espacios maximales
                    self.crearEspacios(cajaEmp1)
                    # Unir los espacios maximales
                    self.todoEM()

                    self.utilizacion = self.utilizacion + \
                        ((caja_param.x*caja_param.y*caja_param.z)/self.vol_cont)

                    entro = False
                    # print(entro)


def contenedorRandom(cont: Contenedor, cajas_p):

    best_sol = None
    best_em = 0
    best_uti = 0
    max_iter = 20
    iter_c = 0

    sol_iter = None
    uti_iter = 0
    em_iter = 0
    iter_t = 0
    box_packed = 0

    best_cajas = []
    esp_best = []
    esquinas = []

    # TENGO QUE GUARDAR LA SOLUCION QUE ME META LAS CAJAS,  SI NO LA TENGO ENTONCES EVALUO CUAL ES LA QUE NO ESTA ENTRANDO

    cajas_emp = len(cajas_p)

    este_p = cajas_p
    #print('cajas a emp '+str(len(este_p)))
    # print(este_p)

    while iter_c < max_iter:
        # print("mejor uti "+str(best_uti))
        inst = ContenedorSum(cont)
        box_bef = len(inst.CajasEmpacadas)

        caja_iter, esp_iter, esquina_iter = inst.cont_aleatorio(este_p)

        box_aft = len(inst.CajasEmpacadas)

        # PendingDeprecationWarning()print("se empaco"+str(box_aft))

        se_empacaron = box_aft-box_bef
        #print("se empacaron "+ str(se_empacaron))

        iter_t += 1

        uti_iter = inst.utilizacion
        em_iter = inst.get_volem()
        sol_iter = inst.CajasEmpacadas

        if (cajas_emp-se_empacaron <= global_buffer):  # and (box_aft>box_bef)
            # print("entro")
            if(uti_iter > best_uti):  # --and box_packed<=box_aft :

                best_sol = sol_iter
                best_em = em_iter
                best_uti = uti_iter
             #   box_packed=box_aft
                iter_c = 0

                best_cajas = caja_iter
                esp_best = esp_iter
                esquinas = esquina_iter

            elif best_uti == uti_iter and best_em < em_iter:  # and box_packed<=box_aft:

                best_sol = sol_iter
                best_em = em_iter
                best_uti = uti_iter
              #  box_packed=box_aft
                iter_c = 0

                best_cajas = caja_iter
                esp_best = esp_iter
                esquinas = esquina_iter

         #   elif box_packed<box_aft:

          #      best_sol=sol_iter
            #     best_em=em_iter
            #    best_uti=uti_iter
             #   box_packed=box_aft
             #   iter_c=0

              #  best_cajas=caja_iter
              #  esp_best=esp_iter
              #  esquinas=esquina_iter

            else:
                iter_c += 1
        else:
            iter_c += 1

    return best_uti, best_em, best_sol, best_cajas, esp_best, esquinas


# Prueba con el buff rearrangement rand

"""
caja_1=CajaTipo(1,1,1,1 

l1=caja_1.list_caja


caja_2=CajaTipo(2, 2, 2, 2, 0, 0, 3)

l2=caja_2.list_caja


caja_3=CajaTipo(3,3,3,3,0,0,3)

l3=caja_3.list_caja


caja_4=CajaTipo(4,4,4,4,0,0,3)

l4=caja_4.list_caja

caja_5=CajaTipo(5,5,5,5,0,0,3)

l5=caja_5.list_caja


caja_6=CajaTipo(6,2,1,2,0,0,3)

l6=caja_6.list_caja

"""

#empaco=CajaEmpacada(1, 0, 0, 0, 1, 1, 1)


# a.crearEspacios(empaco)

# a.todoEM()
#empaco=CajaEmpacada(2, 1, 1, 0, 2, 2, 1)


# a.crearEspacios(empaco)
# a.todoEM()

# nuevo_esp_max=EspMax(0,0,0,1,1,1)
# a.EspMax_p.append(nuevo_esp_max)

# a.todoEM()
# resp=a.EspMax_p


# a.constructivo_buf_rearrangement_rand(l1)
# a.constructivo_buf_rearrangement_rand(l3)
# a.constructivo_buf_rearrangement_rand(l3)
# a.constructivo_buf_rearrangement_rand(l4)
# a.constructivo_buf_rearrangement_rand(l6)
# a.constructivo_buf_rearrangement_rand(l4)

# a.constructivo_buf_rearrangement(l1)

# a.constructivo_buf_rand(l1)


def gen_random_hex_color():
    hex_digits = '0123456789ABCDEF'

    return '#' + ''.join(
        random.choice(hex_digits)
        for _ in range(6)
    )

from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from matplotlib.patches import Rectangle

def plotear3D(elem, largo, ancho, alto, multicolor=True, ejes_iguales=False, numero=1, save_path=None):

    fig = plt.figure(num=numero)
    ax = fig.add_subplot(111, projection='3d')
    poly3d = []
    for i in range(0, len(elem)):
        if isinstance(elem[i], CajaEmpacada):
            e = elem[i]
            x = [e.x1, e.x2, e.x2, e.x1, e.x1, e.x2, e.x2, e.x1]
            y = [e.y1, e.y1, e.y2, e.y2, e.y1, e.y1, e.y2, e.y2]
            z = [e.z1, e.z1, e.z1, e.z1, e.z2, e.z2, e.z2, e.z2]
            alfa = 0.6
            edge = 'k'

        elif isinstance(elem[i], EspMax):
            e = elem[i]
            x = [e.x1, e.x2, e.x2, e.x1, e.x1, e.x2, e.x2, e.x1]
            y = [e.y1, e.y1, e.y2, e.y2, e.y1, e.y1, e.y2, e.y2]
            z = [e.z1, e.z1, e.z1, e.z1, e.z2, e.z2, e.z2, e.z2]
            alfa = 0
            edge = 'r'

        vertices = [[0, 1, 2, 3], [0, 1, 5, 4], [0, 3, 7, 4],
                    [2, 3, 7, 6], [1, 2, 6, 5], [4, 5, 6, 7]]

        tupleList = list(zip(x, y, z))
        # print(tupleList)

        poly3d = [[tupleList[vertices[ix][iy]] for iy in range(
            len(vertices[0]))] for ix in range(len(vertices))]
        if multicolor == True:
            color = gen_random_hex_color()
            color = '#8CB9A8'
        else:
            color = '#69b422'
        ax.add_collection3d(Poly3DCollection(poly3d, edgecolors=edge,
                            facecolors=color, linewidths=1, alpha=alfa))  # zorder=100-i))
        # print(poly3d)
    # ax.scatter(x,y,z)
    # '#69b422'

    if ejes_iguales == False:
        ax.set_xlim(0, largo)
        ax.set_ylim(0, ancho)
        ax.set_zlim(0, alto)
    else:
        ax.set_xlim(0, max(largo, alto, ancho))
        ax.set_ylim(0, max(largo, alto, ancho))
        ax.set_zlim(0, max(largo, alto, ancho))
        # ax.axis('equal')

    # Turn off grid
    ax.grid(False)
    # ax.yaxis.grid(False)
    # Turn off x, y, and z ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    # Hide x, y, and z tick labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

    os.chdir("C:/Users/juan.huertas/OneDrive - LLA/Documentos/Maestria/Tesis/GIF")

    #plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    plt.savefig("figura_"+str(save_path)+".png")
    figs.append("figura_"+str(save_path)+".png")
    # print(save_path)
    # plt.close(fig)
    # print(save_path)
    # plt.close(fig)

    plt.show()


# Ruta al archivo .pt
#ruta_archivo = "C:/Users/juan.huertas/OneDrive - LLA/Documentos/Maestria/Tesis/cut_1.pt"
#ruta_archivo = "C:/Users/juan.huertas/OneDrive - LLA/Documentos/Maestria/Tesis/rs.pt"
ruta_archivo = "C:/Users/juan.huertas/OneDrive - LLA/Documentos/Maestria/Tesis/cut_2.pt"

# Cargar el modelo desde el archivo .pt
cajas = torch.load(ruta_archivo)

#len(cajas[1])
vol_total = 0
conta = 0
for i in cajas[1]:
    vol_total += i[0]*i[1]*i[2]
    conta += 1

#print("vol: "+ str(vol_total))

#print("conta: "+ str(conta))

# Funcion de empacar cajas


def packing_buf_rear(cajas1):

    resp_cajas_1 = []
    a = Contenedor(1, 10, 10, 10)
    contador_cajas = 0
    for i in range(0, len(cajas1)):
    #for i in range(0,4):
        caja_x = cajas1[i][0]
        caja_y = cajas1[i][1]
        caja_z = cajas1[i][2]
        # print("iteracion:"+str(i))
        # print(len(cajas1))
        #print("y: "+str(caja_y))
        #print("z: "+str(caja_z))

        caja_param = CajaTipo(i, caja_x, caja_y, caja_z, 0, 0, 3)
       # print(len(caja_param.list_caja))
        lcaja = caja_param.list_caja

        respuesta = a.constructivo_buf_rearrangement_rand(lcaja, contador_cajas, len(cajas1))

        # se grafica para luego ver la secuencia
        resp = a.obtener_CajEmp()
        plotear3D(resp, 10, 10, 10, save_path=i)

      #  espemax=a.EspMax_p

        contador_cajas += 1
        empacadas_p = len(a.CajasEmpacadas)
        buf_act_p = len(buffer)
        total_cajas = empacadas_p+buf_act_p

        if(total_cajas < contador_cajas):
            # print("total_cajas"+str(total_cajas))
            # print(contador_cajas)
            break
        else:
            resp_cajas_1.append(respuesta)

    # Cajas empacads
    len_emp = len(a.CajasEmpacadas)

    # Cajas en Buffer
    len_buf = len(buffer)

    # Utilizacion
    uti = a.utilizacion

    # total cajas
    len_tot = len(cajas1)

#    espemax=a.EspMax_p

    return(len_tot, len_emp, len_buf, uti, a)


# Guardar tabla de simu


# Crear un DataFrame con 5 columnas vacías
res_data = pd.DataFrame(columns=['Instance', 'Total boxes', 'Total Packed Boxes',
                        'Boxes in Buffer', 'Buffer', 'Rearrangement', 'Utilization', 'Tiempo secs'])


# Iterar para agregar 4 filas


#os.chdir("/Users/JuanManuelHuertasArango/Desktop/Tesis/GIF")

# Registra el tiempo de inicio
inicio = time.time()

# Aquí va tu código que quieres medir

# Registra el tiempo de finalización

for i in range(1708, 1709):

    cajas_empacadas = pd.DataFrame(
        columns=['id_p', 'x1', 'y1', 'z1', 'x2', 'y2', 'z2'])
    cajas1 = cajas[i]

    inicio_1 = time.time()
    len_tot, len_emp, len_buf, uti, container = packing_buf_rear(cajas1)
    fin_1 = time.time()

    cajas_se_empacaron = container.CajasEmpacadas
    espemax = container.EspMax_p

    for j in cajas_se_empacaron:

        fila_empacadas = {
            'id_p': j.id_p,
            'x1': j.x1,
            'y1': j.y1,
            'z1': j.z1,
            'x2': j.x2,
            'y2': j.y2,
            'z2': j.z2
        }
        cajas_empacadas = cajas_empacadas.append(
            fila_empacadas, ignore_index=True)

 #   os.chdir("C:/Users/juan.huertas/OneDrive - LLA/Documentos/Maestria/Tesis/Solutions")
   # cajas_empacadas.to_excel('cut_2_bf/no_max_buf_'+str(global_buffer)+'_rea_'+str(
    #    max_rear)+'_/sol_i_'+str(i)+'_buf_'+str(global_buffer)+'_rea_'+str(max_rear)+'.xlsx')
    # Crear una nueva fila con valores ficticios
    nueva_fila = {
        'Instance': i+1,
        'Total boxes': len_tot,
        'Total Packed Boxes': len_emp,
        'Boxes in Buffer': len_buf,
        'Buffer': global_buffer,
        'Rearrangement': max_rear,
        'Utilization': uti,
        'Tiempo secs': fin_1-inicio_1
    }

    # Agregar la fila al DataFrame
    res_data = res_data.append(nueva_fila, ignore_index=True)

# Imprimir el DataFrame resultante
# print(res_data)


fin = time.time()

# Calcula el tiempo transcurrido
tiempo_transcurrido = fin - inicio


#plotear3D(espemax, 10, 10, 10)


#print("Tiempo Transcurrido "+str(tiempo_transcurrido) + " secs")


os.chdir("C:/Users/juan.huertas/OneDrive - LLA/Documentos/Maestria/Tesis/Solution_Resumen/Cut_2_bf")

#res_data.to_excel('no_max_1_summary_boxes_buf_'+str(global_buffer) +
 #                 '_rea_'+str(max_rear)+'.xlsx')
#UTI CON ROTACION 0,68 cut 2
import cv2

os.chdir("C:/Users/juan.huertas/OneDrive - LLA/Documentos/Maestria/Tesis/GIF")
images_dir = "C:/Users/juan.huertas/OneDrive - LLA/Documentos/Maestria/Tesis/GIF"

# Get list of image filenames

image_files = os.listdir(images_dir)
image_file=figs
print(image_files)
# Video settings
fps = 0.5  # Adjust the frames per second as needed
video_width = 640
video_height = 480

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (video_width, video_height))

# Iterate through the images and add them to the video
for i in range(0,len(image_file)):
    
    image_file='figura_'+str(i)+'.png'
    image_path = os.path.join(images_dir, image_file)
    
    # Attempt to read the image
    frame = cv2.imread(image_path)
    
    # Check if the image was read successfully
    if frame is None:
        print(f"Error: Unable to read image file '{image_path}'. Skipping...")
        continue
    
    # Resize frame to match video dimensions
    frame = cv2.resize(frame, (video_width, video_height))
    
    # Add frame to the video
    out.write(frame)

# Release the VideoWriter object
out.release()



"""

#probar con primera instancia 
resp_cajas_1=[]
cajas1=cajas[1]
for i in range(0,len(cajas1)):
    
    caja_x=cajas1[i][0]
    caja_y=cajas1[i][1]
    caja_z=cajas1[i][2]
    
    caja_param=CajaTipo(i,caja_x,caja_y,caja_z,0,0,3)
    lcaja=caja_param.list_caja
    resp_cajas_1.append(a.constructivo_buf_rearrangement_rand(lcaja))

print("total len cajas: "+str(len(cajas1)))


#best_uti,best_em,best_sol,best_cajas,esp_best,esquinas=contenedorRandom(b, l6)

r=contenedorRandom



r12=a.obtener_cajEmpMov()

rbuf=buffer

resp=a.obtener_CajEmp()
#resp=best_sol()

uti=a.utilizacion


"""
"""
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import random
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

def gen_random_hex_color():
    hex_digits = '0123456789ABCDEF'

    return '#' + ''.join(
        random.choice(hex_digits)
        for _ in range(6)
    )



def plotear3D(elem,largo,ancho,alto,multicolor=True,ejes_iguales=False,numero=1,save_path=None):
    
        fig = plt.figure(num=numero)
        ax = fig.add_subplot(111, projection='3d')
        poly3d=[]
        for i in range(0,len(elem)):
            if isinstance(elem[i],CajaEmpacada):
                e=elem[i]
                x = [e.x1, e.x2, e.x2, e.x1, e.x1, e.x2, e.x2, e.x1]
                y = [e.y1, e.y1, e.y2, e.y2, e.y1, e.y1, e.y2, e.y2]
                z = [e.z1, e.z1, e.z1, e.z1, e.z2, e.z2, e.z2, e.z2] 
                alfa=0.6
                edge='k'
                
                
            elif isinstance(elem[i],EspMax):
                e=elem[i]
                x = [e.x1, e.x2, e.x2, e.x1, e.x1, e.x2, e.x2, e.x1]
                y = [e.y1, e.y1, e.y2, e.y2, e.y1, e.y1, e.y2, e.y2]
                z = [e.z1, e.z1, e.z1, e.z1, e.z2, e.z2, e.z2, e.z2]
                alfa=0
                edge='r'
    
            vertices = [[0,1,2,3], [0,1,5,4], [0,3,7,4], [2,3,7,6], [1,2,6,5], [4,5,6,7]]
    
            tupleList = list(zip(x, y, z))
            # print(tupleList)
    
            poly3d =  [[tupleList[vertices[ix][iy]] for iy in range(len(vertices[0]))] for ix in range(len(vertices))]
            if multicolor==True:
                color=gen_random_hex_color()
                color='#8CB9A8'
            else:
                color='#69b422'
            ax.add_collection3d(Poly3DCollection(poly3d, edgecolors=edge, facecolors=color, linewidths=1, alpha=alfa))#zorder=100-i))
            # print(poly3d)
        # ax.scatter(x,y,z)
        #'#69b422'
    
        if ejes_iguales==False:
            ax.set_xlim(0,largo)
            ax.set_ylim(0,ancho)
            ax.set_zlim(0,alto)
        else:
            ax.set_xlim(0,max(largo,alto,ancho))
            ax.set_ylim(0,max(largo,alto,ancho))
            ax.set_zlim(0,max(largo,alto,ancho))
            # ax.axis('equal')
        
        #Turn off grid
        ax.grid(False)
        #ax.yaxis.grid(False)
        # Turn off x, y, and z ticks
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        
        # Hide x, y, and z tick labels
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])

       
        if save_path:
            #plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
            plt.savefig("figura_"+str(save_path)+".png")
            # plt.close(fig)
            print(save_path)
        #plt.close(fig) 
       
        plt.show()
        
    

###Plotear 3D-2 plotea 


def plotear3D_2(elem,dos,largo,ancho,alto,multicolor=True,ejes_iguales=False,numero=1):
    
        fig = plt.figure(num=numero)
        ax = fig.add_subplot(111, projection='3d')
        poly3d=[]
        for i in range(0,len(elem)):
            if isinstance(elem[i],CajaEmpacada):
                e=elem[i]
                x = [e.x1, e.x2, e.x2, e.x1, e.x1, e.x2, e.x2, e.x1]
                y = [e.y1, e.y1, e.y2, e.y2, e.y1, e.y1, e.y2, e.y2]
                z = [e.z1, e.z1, e.z1, e.z1, e.z2, e.z2, e.z2, e.z2] 
                alfa=0.6
                edge='k'
                
                
            elif isinstance(elem[i],EspMax):
                e=elem[i]
                x = [e.x1, e.x2, e.x2, e.x1, e.x1, e.x2, e.x2, e.x1]
                y = [e.y1, e.y1, e.y2, e.y2, e.y1, e.y1, e.y2, e.y2]
                z = [e.z1, e.z1, e.z1, e.z1, e.z2, e.z2, e.z2, e.z2]
                alfa=0
                edge='r'
    
            vertices = [[0,1,2,3], [0,1,5,4], [0,3,7,4], [2,3,7,6], [1,2,6,5], [4,5,6,7]]
    
            tupleList = list(zip(x, y, z))
            # print(tupleList)
    
            poly3d =  [[tupleList[vertices[ix][iy]] for iy in range(len(vertices[0]))] for ix in range(len(vertices))]
            if multicolor==True:
                color=gen_random_hex_color()
            else:
                color='#69b422'
            ax.add_collection3d(Poly3DCollection(poly3d, edgecolors=edge, facecolors=color, linewidths=1, alpha=alfa))#zorder=100-i))
            # print(poly3d)
        # ax.scatter(x,y,z)
        #'#69b422'
        for i in range(0,len(dos)):
            if isinstance(dos[i],CajaEmpacada):
                e=dos[i]
                x = [e.x1, e.x2, e.x2, e.x1, e.x1, e.x2, e.x2, e.x1]
                y = [e.y1, e.y1, e.y2, e.y2, e.y1, e.y1, e.y2, e.y2]
                z = [e.z1, e.z1, e.z1, e.z1, e.z2, e.z2, e.z2, e.z2] 
                alfa=0.6
                edge='k'
                
                
            elif isinstance(dos[i],EspMax):
                e=dos[i]
                x = [e.x1, e.x2, e.x2, e.x1, e.x1, e.x2, e.x2, e.x1]
                y = [e.y1, e.y1, e.y2, e.y2, e.y1, e.y1, e.y2, e.y2]
                z = [e.z1, e.z1, e.z1, e.z1, e.z2, e.z2, e.z2, e.z2]
                alfa=0
                edge='r'
    
            vertices = [[0,1,2,3], [0,1,5,4], [0,3,7,4], [2,3,7,6], [1,2,6,5], [4,5,6,7]]
    
            tupleList = list(zip(x, y, z))
            # print(tupleList)
    
            poly3d =  [[tupleList[vertices[ix][iy]] for iy in range(len(vertices[0]))] for ix in range(len(vertices))]
            if multicolor==True:
                color=gen_random_hex_color()
                #print(color)
                color='#8CB9A8'
                
            else:
                color='#69b422'
            ax.add_collection3d(Poly3DCollection(poly3d, edgecolors=edge, facecolors=color, linewidths=1, alpha=alfa))#zorder=100-i))
            # print(poly3d)
        # ax.scatter(x,y,z)
        #'#69b422'

    
    
    
        if ejes_iguales==False:
            ax.set_xlim(0,largo)
            ax.set_ylim(0,ancho)
            ax.set_zlim(0,alto)
        else:
            ax.set_xlim(0,max(largo,alto,ancho))
            ax.set_ylim(0,max(largo,alto,ancho))
            ax.set_zlim(0,max(largo,alto,ancho))
            # ax.axis('equal')
        
        #Turn off grid
        ax.grid(False)
        #ax.yaxis.grid(False)
        # Turn off x, y, and z ticks
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        
        # Hide x, y, and z tick labels
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])

       
        
        plt.show()



"""

# Empacar la primera instancia
# plotear3D(resp,10,10,10)

# resp_max=a.EspMax_p

# art=[resp_max[0]]
# art1=[resp_max[1]]
# art2=[resp_max[2]]

# plotear3D(art,10,10,10)
# plotear3D(art1,10,10,10)
# plotear3D(art2,10,10,10)

# plotear3D_2(art,resp,10,10,10)
# plotear3D_2(art1,resp,10,10,10)
# plotear3D_2(art2,resp,10,10,10)


"""
#Pruebas del contenedor Random 

import torch

# Ruta al archivo .pt
ruta_archivo = "C:/Users/juan.huertas/OneDrive - LLA/Documentos/Maestria/Tesis/cut_2.pt"

# Cargar el modelo desde el archivo .pt
cajas = torch.load(ruta_archivo)


#probar con primera instancia 
cajas1=cajas[0]




a=Contenedor(1, 10, 10, 10)

cajas_to_pack=[]
cajas_to_pack_sample=[]





for i in range(0,len(cajas1)):
    caja=CajaTipo(1,cajas1[i][0],cajas1[i][1],cajas1[i][2],0,0,3)
    lcajas=caja.list_caja
    cajas_to_pack.append(lcajas)    
    if (i<=10):
        cajas_to_pack_sample.append(lcajas)

#cajas_to_pack_sample

uti_test,em_test,sol_test=contenedorRandom(a,cajas_to_pack_sample)








##Tests para crea las diferentes cajas 

caja_1=CajaTipo(1,1,1,1,3,3,3)

l1=caja_1.list_caja

caja_2=CajaTipo(2, 2, 2, 2, 3, 3, 3)

l2=caja_2.list_caja


caja_3=CajaTipo(3,3,3,3,3,3,3)

l3=caja_3.list_caja


caja_4=CajaTipo(4,4,4,4,3,3,3)

l4=caja_4.list_caja

caja_5=CajaTipo(5,5,5,5,3,3,3)

l5=caja_5.list_caja


caja_6=CajaTipo(6,6,6,6,3,3,3)

l6=caja_6.list_caja



#for i in l1:
    
 #   print("x: "+str(i.x))
  #  print("y: "+str(i.y))
  #  print("z: "+str(i.z))
   # print(" ")
    
    
##Tests para crear los espacios maximales
import os
os.chdir('C:/Users/juan.huertas/OneDrive - LLA/Documentos/Maestria/Tesis')
archivo='datos dummies tesis.txt'
#datos_leidos_cont,datos_leidos_cajas=leer_datos(archivo)



## Test de contenedor aleatorio 

#a=Contenedor(1, int(datos_leidos_cont[0][0]), int(datos_leidos_cont[0][1]), int(datos_leidos_cont[0][2]))

"""

"""
a=Contenedor(1,3,3,3)
caja_1=CajaTipo(1,1,1,1,3,3,3)

l1=caja_1.list_caja


caja_2=CajaTipo(2,2,2,2,3,3,3)

l2=caja_2.list_caja


caja_3=CajaTipo(3,1,1,1,3,3,3)

l3=caja_3.list_caja



caja_4=CajaTipo(4,2,1,2,3,3,3)

l4=caja_4.list_caja



caja_5=CajaTipo(5,1,1,3,3,3,3)

l5=caja_5.list_caja


caja_5=CajaTipo(6,1,1,1,3,3,3)

l5=caja_5.list_caja


cajas_rand=[]
cajas_rand.append(l1)
cajas_rand.append(l2)
cajas_rand.append(l3)
cajas_rand.append(l4)

"""
# uti_test,em_test,sol_test=contenedorRandom(a,cajas_rand)


# Test de constructivos basicos, buf y buf_add rearr

"""
#a.constructivo_buf_rearrangement_rand(l1,1,8)
#a.constructivo_buf_rearrangement_rand(l2,2,8)
#a.constructivo_buf_rearrangement_rand(l3,3,8)
#a.constructivo_buf_rearrangement_rand(l4,4,8)
#a.constructivo_buf_rearrangement_rand(l5,5,8)
#a.constructivo_buf_rearrangement_rand(l2,6,8)
#a.constructivo_buf_rearrangement_rand(l1,7,8)
#a.constructivo_buf_rearrangement_rand(l2,8,8)

print("uti: afuera "+ str(a.utilizacion))
#a.constructivo_buf_rearrangement_rand(l4,4,2)
  #  def constructivo_buf_rearrangement_rand(self,cajas,contador_cajas,max_cajas):

r12=a.obtener_cajEmpMov()

rbuf=buffer

resp=a.obtener_CajEmp()

resp_esp=a.obtener_EspMax_p()

#plotear3D(resp_esp,3,3,3)

path='C:/Users/juan.huertas/OneDrive - LLA/Documentos/Maestria/Tesis/GIF'
os.chdir(path)



#plotear3D(resp,3,3,3,save_path=path)

a.constructivo_buf_rearrangement_rand(l1,1,8)
resp=a.obtener_CajEmp()
plotear3D(resp,3,3,3,save_path=1)

a.constructivo_buf_rearrangement_rand(l2,2,8)
resp=a.obtener_CajEmp()
plotear3D(resp,3,3,3,save_path=2)


a.constructivo_buf_rearrangement_rand(l3,3,8)
resp=a.obtener_CajEmp()
plotear3D(resp,3,3,3,save_path=3)

a.constructivo_buf_rearrangement_rand(l4,4,8)
resp=a.obtener_CajEmp()
plotear3D(resp,3,3,3,save_path=4)

a.constructivo_buf_rearrangement_rand(l5,5,8)
resp=a.obtener_CajEmp()
plotear3D(resp,3,3,3,save_path=5)

"""


# REVISAR CREAR ESPACIOS
