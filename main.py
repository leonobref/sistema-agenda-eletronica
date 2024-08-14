import re
from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta
from tkcalendar import Calendar, DateEntry
import sqlite3

def ehemail(String):
    retorno = False
    padrao = re.search(r'[A-Fa-z]\w+@[\w-]+\.[\w.-]+', String)
    if padrao:
        retorno = True
    return retorno

def ehTelefone(String):
    retorno = False
    padrao = re.search(r'\d\d\d\d\d\d\d\d\d\d\d', String)
    if padrao:
        retorno = True
    if (len(String) > 11):
        retorno = False
    return retorno

def ehSenha(String):
    retorno = False
    
    maiusculas = re.findall(r'[A-Z]', String)
    minusculas = re.findall(r'[a-z]', String)
    digitos = re.findall(r'\d', String)
    caracespec = re.findall(r'[$@%&#(*)]', String)


    if len(maiusculas) >= 1 and len(minusculas) >= 1 and len(digitos) >= 1  and len(caracespec) >= 1 and len(String) >= 8:
        retorno = True
    return retorno

class Db():
    def connect_bd(self):
        self.conn = sqlite3.connect("Atividades.db")
        self.cursor = self.conn.cursor()
        print("Banco de Dados conectado")
    def disconnect_bd(self):
        self.conn.close()
        print("Banco de Dados desconectado")
    def create_tables(self):
        self.connect_bd();
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS tarefas (
                cod INTEGER PRIMARY KEY,
                nome CHAR(40) NOT NULL,
                desc CHAR(200),
                ddlnhour CHAR(3),
                ddlndate CHAR(10),
                done CHAR(5)
            );
            CREATE TABLE IF NOT EXISTS reunioes (
                cod INTEGER PRIMARY KEY,
                nome CHAR(40) NOT NULL,
                desc CHAR(200),
                hour CHAR(3) NOT NULL,
                date CHAR(10) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS eventos (
                cod INTEGER PRIMARY KEY,
                nome CHAR(40) NOT NULL,
                desc CHAR(200),
                hourb CHAR(5) NOT NULL,
                dateb CHAR(10) NOT NULL,
                houre CHAR(3) NOT NULL,
                datee CHAR(10) NOT NULL
            );
        """)
        self.conn.commit(); print("Banco de Dados Criado")
        self.disconnect_bd()

class HomeFuncs(Db):
    def logout(self):
        self.home.destroy()
        Login()
    
    def showHome(self):
        self.l_title.configure(text = "HOME")
        self.homeframe.place(relx= 0.15, rely = 0.15, relwidth= 0.8, relheight= 0.8)
        self.atividades.place_forget()
        self.historico.place_forget()
    def showAtividades(self):
        self.l_title.configure(text = "ATIVIDADES")
        self.homeframe.place_forget()
        self.atividades.place(relx= 0.15, rely = 0.15, relwidth= 0.8, relheight= 0.8)
        self.historico.place_forget()

    def showHistorico(self):
        self.l_title.configure(text = "HISTÓRICO")
        self.homeframe.place_forget()
        self.atividades.place_forget()
        self.historico.place(relx= 0.15, rely = 0.15, relwidth= 0.8, relheight= 0.8)

    def showGeral(self):
        self.la_title.configure(text= "VISÃO GERAL")
        self.geral.place(relx= 0, rely= 0.25, relwidth=1, relheight=0.8)
        self.tarefas.place_forget()
        self.reunioes.place_forget()
        self.eventos.place_forget()

    def showTarefas(self):
        self.la_title.configure(text= "TAREFAS")
        self.geral.place_forget()
        self.tarefas.place(relx= 0, rely= 0.25, relwidth=1, relheight=0.8)
        self.reunioes.place_forget()
        self.eventos.place_forget()

    def showReunioes(self):
        self.la_title.configure(text= "REUNIÕES")
        self.geral.place_forget()
        self.tarefas.place_forget()
        self.reunioes.place(relx= 0, rely= 0.25, relwidth=1, relheight=0.8)
        self.eventos.place_forget()

    def showEventos(self):
        self.la_title.configure(text= "EVENTOS")
        self.geral.place_forget()
        self.tarefas.place_forget()
        self.reunioes.place_forget()
        self.eventos.place(relx= 0, rely= 0.25, relwidth=1, relheight=0.8)


    def variaveis1(self):
        self.nome = self.ent_nome.get()
        self.desc = self.ent_desc.get('1.0', END)
        self.desc = self.desc.strip("\n")
        self.ddlndate = self.calendario1.get_date()
        self.feito_ = self.feito.get()
        self.ddlnhour = self.cb_hours1.get() + self.cb_hours2.get() + ":" + self.cb_minutes1.get() + self.cb_minutes2.get()
        self.done = ''
        if self.feito_ == 1:
            self.done = "Sim"
        if self.feito_ == 0:
            self.done = "Não"

    def add_task(self):
        self.variaveis1()
        if(int(self.cb_hours1.get()) == 2 and int(self.cb_hours2.get()) > 3):
            self.l_wrong.place(relx = 0.7, rely= 0.2)
        else:
            self.l_wrong.place_forget()
            self.connect_bd()
            self.cursor.execute(""" INSERT INTO tarefas(nome, desc, ddlnhour, ddlndate, done)
                VALUES (?, ?, ?, ?, ?)""", (self.nome, self.desc, self.ddlnhour, self.ddlndate, self.done))
            self.conn.commit()
            self.disconnect_bd()
            self.select_task()
        self.task.destroy()

    def OnDoubleClick(self, event):
        self.Task()
        for n in self.list_tasks.selection():
            col1, col2, col3, col4, col5, col6 = self.list_tasks.item(n, 'values')
            self.codigo = col1
            self.ent_nome.insert(END, col2)
            self.ent_desc.insert(END, col3)
            self.cb_hours1.set(int(col4[0]))
            self.cb_hours2.set(int(col4[1]))
            self.cb_minutes1.set(int(col4[3]))
            self.cb_minutes2.set(int(col4[4]))
            self.calendario1.selection_set(col5)
            if col6 == "Sim":
                self.feito.set(1)
            else:
                self.feito.set(0)

    def update_task(self):
        self.variaveis1()
        if(int(self.cb_hours1.get()) == 2 and int(self.cb_hours2.get()) > 3):
            self.l_wrong.place(relx = 0.7, rely= 0.2)
        else:
            self.l_wrong.place_forget()
            self.connect_bd()
            self.cursor.execute(""" UPDATE tarefas SET nome = ?, desc = ?, ddlnhour = ?, ddlndate = ?, done = ?
                                WHERE cod = ?""", (self.nome, self.desc, self.ddlnhour, self.ddlndate, self.done, self.codigo))
            self.conn.commit()
            self.disconnect_bd()
            self.select_task()
            self.task.destroy()

    def delete_task(self):
        self.connect_bd()
        self.cursor.execute("""DELETE FROM tarefas WHERE cod = ? """, (self.codigo))
        self.conn.commit()
        self.disconnect_bd()
        self.select_task()
        self.task.destroy()

    def variaveis2(self):
        self.nome = self.ent_nome.get()
        self.desc = self.ent_desc.get('1.0', END)
        self.desc = self.desc.strip("\n")
        self.date = self.calendario1.get_date()
        self.hour = self.cb_hours1.get() + self.cb_hours2.get() + ":" + self.cb_minutes1.get() + self.cb_minutes2.get()

    def add_reunion(self):
        self.variaveis2()
        if(int(self.cb_hours1.get()) == 2 and int(self.cb_hours2.get()) > 3):
            self.l_wrong.place(relx = 0.7, rely= 0.2)
        else:
            self.l_wrong.place_forget()
            self.connect_bd()
            self.cursor.execute(""" INSERT INTO reunioes(nome, desc, hour, date)
                VALUES (?, ?, ?, ?)""", (self.nome, self.desc, self.hour, self.date))
            self.conn.commit()
            self.disconnect_bd()
            self.select_reunion()
            self.reunion.destroy()
    
    def OnDoubleClick2(self, event):
        self.Reunion()
        for n in self.list_reunions.selection():
            col1, col2, col3, col4, col5 = self.list_reunions.item(n, 'values')
            self.codigo = col1
            self.ent_nome.insert(END, col2)
            self.ent_desc.insert(END, col3)
            self.cb_hours1.set(int(col4[0]))
            self.cb_hours2.set(int(col4[1]))
            self.cb_minutes1.set(int(col4[3]))
            self.cb_minutes2.set(int(col4[4]))
            self.calendario1.selection_set(col5)

    def update_reunion(self):
        self.variaveis2()
        if(int(self.cb_hours1.get()) == 2 and int(self.cb_hours2.get()) > 3):
            self.l_wrong.place(relx = 0.7, rely= 0.2)
        else:
            self.l_wrong.place_forget()
            self.connect_bd()
            self.cursor.execute(""" UPDATE reunioes SET nome = ?, desc = ?, hour = ?, date = ?
                                WHERE cod = ?""", (self.nome, self.desc, self.hour, self.date, self.codigo))
            self.conn.commit()
            self.disconnect_bd()
            self.select_reunion()
            self.reunion.destroy()

    def delete_reunion(self):
        self.connect_bd()
        self.cursor.execute("""DELETE FROM reunioes WHERE cod = ? """, (self.codigo))
        self.conn.commit()
        self.disconnect_bd()
        self.select_reunion()
        self.reunion.destroy()

    def variaveis3(self):
        self.nome = self.ent_nome.get()
        self.desc = self.ent_desc.get('1.0', END)
        self.desc = self.desc.strip("\n")
        self.dateb = self.calendario1.get_date()
        self.hourb = self.cb_hours1.get() + self.cb_hours2.get() + ":" + self.cb_minutes1.get() + self.cb_minutes2.get()
        self.datee = self.calendario2.get_date()
        self.houre = self.cb_hours1_2.get() + self.cb_hours2_2.get() + ":" + self.cb_minutes1_2.get() + self.cb_minutes2_2.get()

    def add_event(self):
        self.variaveis3()
        anomesdia = self.dateb.split('/')
        ano = int(anomesdia[2])
        mes = int(anomesdia[1])
        dia = int(anomesdia[0])
        horaminuto = self.hourb.split(':')
        hora = int(horaminuto[0])
        minuto = int(horaminuto[1])

        tempo = datetime(year= ano, month= mes, day= dia, hour= hora, minute= minuto)

        anomesdia2 = self.datee.split('/')
        ano = int(anomesdia2[2])
        mes = int(anomesdia2[1])
        dia = int(anomesdia2[0])
        horaminuto2 = self.houre.split(':')
        hora = int(horaminuto2[0])
        minuto = int(horaminuto2[1])

        tempo2 = datetime(year= ano, month= mes, day= dia, hour= hora, minute= minuto)

        if(int(self.cb_hours1.get()) == 2 and int(self.cb_hours2.get()) > 3):
            self.l_wrong.place(relx = 0.325, rely= 0.2)
        elif (int(self.cb_hours1_2.get()) == 2 and int(self.cb_hours2_2.get()) > 3):
            self.l_wrong2.place(relx = 0.65, rely= 0.2)
        elif (tempo >= tempo2):
            self.l_wrong3.place(relx = 0.325, rely = 0.75)
        else:
            self.l_wrong.place_forget()
            self.l_wrong2.place_forget()
            self.l_wrong3.place_forget()

            self.connect_bd()
            self.cursor.execute(""" INSERT INTO eventos(nome, desc, hourb, dateb, houre, datee)
                VALUES (?, ?, ?, ?, ?, ?)""", (self.nome, self.desc, self.hourb, self.dateb, self.houre, self.datee))
            self.conn.commit()
            self.disconnect_bd()
            self.select_event()
            self.event.destroy()

    def OnDoubleClick3(self, event):
        self.Event()
        for n in self.list_events.selection():
            col1, col2, col3, col4, col5, col6, col7, col8 = self.list_events.item(n, 'values')
            self.codigo = col1
            self.ent_nome.insert(END, col2)
            self.ent_desc.insert(END, col3)
            self.cb_hours1.set(int(col4[0]))
            self.cb_hours2.set(int(col4[1]))
            self.cb_minutes1.set(int(col4[3]))
            self.cb_minutes2.set(int(col4[4]))
            self.calendario1.selection_set(col5)
            self.cb_hours1_2.set(int(col6[0]))
            self.cb_hours2_2.set(int(col6[1]))
            self.cb_minutes1_2.set(int(col6[3]))
            self.cb_minutes2_2.set(int(col6[4]))
            self.calendario2.selection_set(col7)

    def update_event(self):
        self.variaveis3()
        anomesdia = self.dateb.split('/')
        ano = int(anomesdia[2])
        mes = int(anomesdia[1])
        dia = int(anomesdia[0])
        horaminuto = self.hourb.split(':')
        hora = int(horaminuto[0])
        minuto = int(horaminuto[1])

        tempo = datetime(year= ano, month= mes, day= dia, hour= hora, minute= minuto)

        anomesdia2 = self.datee.split('/')
        ano = int(anomesdia2[2])
        mes = int(anomesdia2[1])
        dia = int(anomesdia2[0])
        horaminuto2 = self.houre.split(':')
        hora = int(horaminuto2[0])
        minuto = int(horaminuto2[1])

        tempo2 = datetime(year= ano, month= mes, day= dia, hour= hora, minute= minuto)

        if(int(self.cb_hours1.get()) == 2 and int(self.cb_hours2.get()) > 3):
            self.l_wrong.place(relx = 0.325, rely= 0.2)
        elif (int(self.cb_hours1_2.get()) == 2 and int(self.cb_hours2_2.get()) > 3):
            self.l_wrong2.place(relx = 0.65, rely= 0.2)
        elif (tempo >= tempo2):
            self.l_wrong3.place(relx = 0.325, rely = 0.75)
        else:
            self.l_wrong.place_forget()
            self.l_wrong2.place_forget()
            self.l_wrong3.place_forget()
            self.connect_bd()
            self.cursor.execute(""" UPDATE eventos SET nome = ?, desc = ?, hourb = ?, dateb = ?, houre = ?, datee = ?
                                WHERE cod = ?""", (self.nome, self.desc, self.hourb, self.dateb, self.houre, self.datee, self.codigo))
            self.conn.commit()
            self.disconnect_bd()
            self.select_event()
            self.event.destroy()

    def delete_event(self):
        self.connect_bd()
        self.cursor.execute("""DELETE FROM eventos WHERE cod = ? """, (self.codigo))
        self.conn.commit()
        self.disconnect_bd()
        self.select_event()
        self.event.destroy()
    
    def select_task(self):
        self.list_tasks.delete(*self.list_tasks.get_children())
        self.connect_bd()
        list = self.cursor.execute(""" SELECT cod, nome, desc, ddlnhour, ddlndate, done FROM tarefas; """)
        matriz = []
        for i in list:
            filial = []
            for j in range(6):
                filial.append(i[j])
            matriz.append(filial)
        agora = datetime.now()

        for i in range(len(matriz)):
            for j in range(len(matriz) - 1):
                data = matriz[j][4]
                anomesdia = data.split('/')
                ano = int(anomesdia[2])
                mes = int(anomesdia[1])
                dia = int(anomesdia[0])
                horario = matriz[j][3]
                horaminuto = horario.split(':')
                hora = int(horaminuto[0])
                minuto = int(horaminuto[1])

                tempo = datetime(year= ano, month= mes, day= dia, hour= hora, minute= minuto)

                data2 = matriz[j+1][4]
                anomesdia2 = data2.split('/')
                ano2 = int(anomesdia2[2])
                mes2 = int(anomesdia2[1])
                dia2 = int(anomesdia2[0])
                horario2 = matriz[j+1][3]
                horaminuto2 = horario2.split(':')
                hora2 = int(horaminuto2[0])
                minuto2 = int(horaminuto2[1])

                tempo2 = datetime(year= ano2, month= mes2, day= dia2, hour= hora2, minute= minuto2)

                temp = matriz[j]
                if(tempo > tempo2):
                    matriz[j] = matriz[j + 1]
                    matriz[j + 1] = temp

        for i in range(len(matriz)):
            data = matriz[i][4]
            anomesdia = data.split('/')
            ano = int(anomesdia[2])
            mes = int(anomesdia[1])
            dia = int(anomesdia[0])
            horario = matriz[i][3]
            horaminuto = horario.split(':')
            hora = int(horaminuto[0])
            minuto = int(horaminuto[1])

            tempo = datetime(year= ano, month= mes, day= dia, hour= hora, minute= minuto)
            if(tempo >= agora):
                self.list_tasks.insert("", END, values= matriz[i])
        
        
        self.disconnect_bd()
        self.select_activities()

    def select_reunion(self):
        self.list_reunions.delete(*self.list_reunions.get_children())
        self.connect_bd()
        list = self.cursor.execute(""" SELECT cod, nome, desc, hour, date FROM reunioes; """)
        matriz = []
        for i in list:
            filial = []
            for j in range(5):
                filial.append(i[j])
            matriz.append(filial)
        agora = datetime.now()

        for i in range(len(matriz)):
            for j in range(len(matriz) - 1):
                data = matriz[j][4]
                anomesdia = data.split('/')
                ano = int(anomesdia[2])
                mes = int(anomesdia[1])
                dia = int(anomesdia[0])
                horario = matriz[j][3]
                horaminuto = horario.split(':')
                hora = int(horaminuto[0])
                minuto = int(horaminuto[1])

                tempo = datetime(year= ano, month= mes, day= dia, hour= hora, minute= minuto)

                data2 = matriz[j+1][4]
                anomesdia2 = data2.split('/')
                ano2 = int(anomesdia2[2])
                mes2 = int(anomesdia2[1])
                dia2 = int(anomesdia2[0])
                horario2 = matriz[j+1][3]
                horaminuto2 = horario2.split(':')
                hora2 = int(horaminuto2[0])
                minuto2 = int(horaminuto2[1])

                tempo2 = datetime(year= ano2, month= mes2, day= dia2, hour= hora2, minute= minuto2)

                temp = matriz[j]
                if(tempo > tempo2):
                    matriz[j] = matriz[j + 1]
                    matriz[j + 1] = temp

        for i in range(len(matriz)):
            data = matriz[i][4]
            anomesdia = data.split('/')
            ano = int(anomesdia[2])
            mes = int(anomesdia[1])
            dia = int(anomesdia[0])
            horario = matriz[i][3]
            horaminuto = horario.split(':')
            hora = int(horaminuto[0])
            minuto = int(horaminuto[1])

            tempo = datetime(year= ano, month= mes, day= dia, hour= hora, minute= minuto)
            if(tempo >= agora):
                self.list_reunions.insert("", END, values= matriz[i])
                
        self.disconnect_bd()
        self.select_activities()

    def select_event(self):
        self.list_events.delete(*self.list_events.get_children())
        self.connect_bd()
        list = self.cursor.execute(""" SELECT cod, nome, desc, hourb, dateb, houre, datee FROM eventos; """)
        matriz = []
        for i in list:
            filial = []
            for j in range(7):
                filial.append(i[j])
            matriz.append(filial)

        agora = datetime.now()

        for i in range(len(matriz)):
            for j in range(len(matriz) - 1):
                data = matriz[j][4]
                anomesdia = data.split('/')
                ano = int(anomesdia[2])
                mes = int(anomesdia[1])
                dia = int(anomesdia[0])
                horario = matriz[j][3]
                horaminuto = horario.split(':')
                hora = int(horaminuto[0])
                minuto = int(horaminuto[1])

                tempo = datetime(year= ano, month= mes, day= dia, hour= hora, minute= minuto)

                data2 = matriz[j+1][4]
                anomesdia2 = data2.split('/')
                ano2 = int(anomesdia2[2])
                mes2 = int(anomesdia2[1])
                dia2 = int(anomesdia2[0])
                horario2 = matriz[j+1][3]
                horaminuto2 = horario2.split(':')
                hora2 = int(horaminuto2[0])
                minuto2 = int(horaminuto2[1])

                tempo2 = datetime(year= ano2, month= mes2, day= dia2, hour= hora2, minute= minuto2)

                temp = matriz[j]
                if(tempo > tempo2):
                    matriz[j] = matriz[j + 1]
                    matriz[j + 1] = temp

        for i in range(len(matriz)):
            data = matriz[i][4]
            anomesdia = data.split('/')
            ano = int(anomesdia[2])
            mes = int(anomesdia[1])
            dia = int(anomesdia[0])
            horario = matriz[i][3]
            horaminuto = horario.split(':')
            hora = int(horaminuto[0])
            minuto = int(horaminuto[1])

            tempo = datetime(year= ano, month= mes, day= dia, hour= hora, minute= minuto)

            data2 = matriz[i][6]
            anomesdia2 = data2.split('/')
            ano2 = int(anomesdia2[2])
            mes2 = int(anomesdia2[1])
            dia2 = int(anomesdia2[0])
            horario2 = matriz[i][5]
            horaminuto2 = horario2.split(':')
            hora2 = int(horaminuto2[0])
            minuto2 = int(horaminuto2[1])

            tempo2 = datetime(year= ano2, month= mes2, day= dia2, hour= hora2, minute= minuto2)

            if(tempo <= agora < tempo2):
                matriz[i].append("Em Andamento")
                self.list_events.insert("", END, values = matriz[i])
            elif(agora < tempo):
                matriz[i].append("Em Breve")
                self.list_events.insert("", END, values = matriz[i])
        
        self.disconnect_bd()
        self.select_activities()

    def select_activities(self):
        self.list_activities.delete(*self.list_activities.get_children())
        self.connect_bd()
        list = self.cursor.execute(""" SELECT cod, nome, desc, ddlnhour, ddlndate, done FROM tarefas; """)
        #list5 = self.cursor.execute(""" SELECT cod, nome, desc, hour, date FROM reunioes; """)
        #list6 = self.cursor.execute(""" SELECT cod, nome, desc, hourb, dateb, houre, datee FROM eventos; """)
        
        matriz = []
        for i in list:
            filial = []
            filial.append(i[1])
            filial.append(i[2])
            filial.append("Tarefa")
            filial.append(i[3])
            filial.append(i[4])
            matriz.append(filial)

        list = self.cursor.execute(""" SELECT cod, nome, desc, hour, date FROM reunioes; """)
        for i in list:
            filial = []
            filial.append(i[1])
            filial.append(i[2])
            filial.append("Reunião")
            filial.append(i[3])
            filial.append(i[4])
            matriz.append(filial)

        list = self.cursor.execute(""" SELECT cod, nome, desc, hourb, dateb, houre, datee FROM eventos; """)
        for i in list:
            filial = []
            filial.append(i[1])
            filial.append(i[2])
            filial.append("Evento")
            filial.append(i[3])
            filial.append(i[4])
            matriz.append(filial)

        for i in range(len(matriz)):
            for j in range(len(matriz) - 1):
                data = matriz[j][4]
                anomesdia = data.split('/')
                ano = int(anomesdia[2])
                mes = int(anomesdia[1])
                dia = int(anomesdia[0])
                horario = matriz[j][3]
                horaminuto = horario.split(':')
                hora = int(horaminuto[0])
                minuto = int(horaminuto[1])

                tempo = datetime(year= ano, month= mes, day= dia, hour= hora, minute= minuto)

                data2 = matriz[j+1][4]
                anomesdia2 = data2.split('/')
                ano2 = int(anomesdia2[2])
                mes2 = int(anomesdia2[1])
                dia2 = int(anomesdia2[0])
                horario2 = matriz[j+1][3]
                horaminuto2 = horario2.split(':')
                hora2 = int(horaminuto2[0])
                minuto2 = int(horaminuto2[1])

                tempo2 = datetime(year= ano2, month= mes2, day= dia2, hour= hora2, minute= minuto2)

                temp = matriz[j]
                if(tempo > tempo2):
                    matriz[j] = matriz[j + 1]
                    matriz[j + 1] = temp
        agora = datetime.now()
        for i in range(len(matriz)):
            data = matriz[i][4]
            anomesdia = data.split('/')
            ano = int(anomesdia[2])
            mes = int(anomesdia[1])
            dia = int(anomesdia[0])
            horario = matriz[i][3]
            horaminuto = horario.split(':')
            hora = int(horaminuto[0])
            minuto = int(horaminuto[1])

            tempo = datetime(year= ano, month= mes, day= dia, hour= hora, minute= minuto)
            if(tempo >= agora):
                self.list_activities.insert("", END, values= matriz[i])
        
        self.disconnect_bd()

    def select_history(self):
        agora = datetime.now()
        filtrotempo = self.filtro2.get()
        if(filtrotempo == "Últimas 24 Horas"):
            horariolimite = agora - timedelta(days = 1)
        elif(filtrotempo == "Últimos 7 dias"):
            horariolimite = agora - timedelta(days = 7)
        elif(filtrotempo == "Últimos 15 dias"):
            horariolimite = agora - timedelta(days = 15)
        elif(filtrotempo == "Últimos 30 dias"):
            horariolimite = agora - timedelta(days = 30)
        elif(filtrotempo == "Últimos 90 dias"):
            horariolimite = agora - timedelta(days = 90)
        elif(filtrotempo == "Últimos 180 dias"):
            horariolimite = agora - timedelta(days = 180)
        
        self.list_history.delete(*self.list_history.get_children())

        self.connect_bd()
        matriz = []
        if (self.filtro1.get() == "Todos") or (self.filtro1.get() == "Tarefas"):
            list = self.cursor.execute(""" SELECT cod, nome, desc, ddlnhour, ddlndate, done FROM tarefas; """)
            for i in list:
                filial = []
                filial.append(i[1])
                filial.append(i[2])
                filial.append("Tarefa")
                filial.append(i[3])
                filial.append(i[4])
                matriz.append(filial)

        if (self.filtro1.get() == "Todos") or (self.filtro1.get() == "Reuniões"):
            list = self.cursor.execute(""" SELECT cod, nome, desc, hour, date FROM reunioes; """)
            for i in list:
                filial = []
                filial.append(i[1])
                filial.append(i[2])
                filial.append("Reunião")
                filial.append(i[3])
                filial.append(i[4])
                matriz.append(filial)

        if (self.filtro1.get() == "Todos") or (self.filtro1.get() == "Eventos"):
            list = self.cursor.execute(""" SELECT cod, nome, desc, hourb, dateb, houre, datee FROM eventos; """)
            for i in list:
                filial = []
                filial.append(i[1])
                filial.append(i[2])
                filial.append("Evento")
                filial.append(i[3])
                filial.append(i[4])
                matriz.append(filial)
        
        for i in range(len(matriz)):
            for j in range(len(matriz) - 1):
                data = matriz[j][4]
                anomesdia = data.split('/')
                ano = int(anomesdia[2])
                mes = int(anomesdia[1])
                dia = int(anomesdia[0])
                horario = matriz[j][3]
                horaminuto = horario.split(':')
                hora = int(horaminuto[0])
                minuto = int(horaminuto[1])

                tempo = datetime(year= ano, month= mes, day= dia, hour= hora, minute= minuto)

                data2 = matriz[j+1][4]
                anomesdia2 = data2.split('/')
                ano2 = int(anomesdia2[2])
                mes2 = int(anomesdia2[1])
                dia2 = int(anomesdia2[0])
                horario2 = matriz[j+1][3]
                horaminuto2 = horario2.split(':')
                hora2 = int(horaminuto2[0])
                minuto2 = int(horaminuto2[1])

                tempo2 = datetime(year= ano2, month= mes2, day= dia2, hour= hora2, minute= minuto2)

                temp = matriz[j]
                if(tempo < tempo2):
                    matriz[j] = matriz[j + 1]
                    matriz[j + 1] = temp

        for i in range(len(matriz)):
            data = matriz[i][4]
            anomesdia = data.split('/')
            ano = int(anomesdia[2])
            mes = int(anomesdia[1])
            dia = int(anomesdia[0])
            horario = matriz[i][3]
            horaminuto = horario.split(':')
            hora = int(horaminuto[0])
            minuto = int(horaminuto[1])

            tempo = datetime(year= ano, month= mes, day= dia, hour= hora, minute= minuto)
            if(horariolimite <= tempo < agora):
                self.list_history.insert("", END, values= matriz[i])

class Home(HomeFuncs):
    def create_home(self):
        self.home = Tk()
        #Configurando Tela Inicial
        self.homeTela()
        self.homeWidgets()

        #Configurando Tela Atividades
        self.atividadesWidgets()

        #Configurando Tela Tarefas, Reunioes, Eventos
        self.tarefaswidgets()
        self.reunionswidgets()
        self.eventswidgets()

        #Configurando Tela Histórico
        self.historicoWidgets()

        #Criando Banco de Dados
        self.create_tables()

        #Atualizando Tabelas
        self.select_task()
        self.select_reunion()
        self.select_event()

        self.home.mainloop()
        

    def homeTela(self):
        self.home.title("Quer um cafézinho?")
        self.home.configure(background= '#11114e')
        self.home.geometry("1280x720")
    
    def homeWidgets(self):

        self.l_title = Label(self.home, text="HOME",fg= "white",bg ="#11114e", font= ('verdana', 12, "bold"))
        self.l_title.place(relx= 0.65, rely = 0.05, relwidth= 0.1, relheight= 0.02)

        self.icon = PhotoImage(file= "images/icon.png")
        self.bt_perfil = Button(self.home, image= self.icon, bg= "#11114e", bd= 0)
        self.bt_perfil.place(relx= 0.025, rely= 0.025)

        self.house = PhotoImage(file= "images/house.png")
        self.bt_home = Button(self.home, image= self.house, bg= "#11114e", bd= 0, command= self.showHome)
        self.bt_home.place(relx= 0.075, rely= 0.025)

        self.bt_contatos = Button(self.home, text= "CONTATOS",fg= "white", bg = "#7a7f80", bd =3, font= ('verdana', 12, 'bold'))
        self.bt_contatos.place(relx= 0.025, rely= 0.2, relwidth= 0.1, relheight= 0.05)

        self.bt_nuvem = Button(self.home, text= "NUVEM",fg= "white", bg = "#7a7f80", bd =3, font= ('verdana', 12, 'bold'))
        self.bt_nuvem.place(relx= 0.025, rely= 0.275, relwidth= 0.1, relheight= 0.05)

        self.bt_atividades = Button(self.home, text= "ATIVIDADES",fg= "white", bg = "#7a7f80", bd =3, font= ('verdana', 12, 'bold'), command= self.showAtividades)
        self.bt_atividades.place(relx= 0.025, rely= 0.35, relwidth= 0.1, relheight= 0.05)

        self.bt_calendario = Button(self.home, text= "CALENDÁRIO",fg= "white", bg = "#7a7f80", bd =3, font= ('verdana', 12, 'bold'))
        self.bt_calendario.place(relx= 0.025, rely= 0.425, relwidth= 0.1, relheight= 0.05)

        self.bt_historico = Button(self.home, text= "HISTÓRICO",fg= "white", bg = "#7a7f80", bd =3, font= ('verdana', 12, 'bold'), command= self.showHistorico)
        self.bt_historico.place(relx= 0.025, rely= 0.5, relwidth= 0.1, relheight= 0.05)

        self.bt_grupos = Button(self.home, text= "GRUPOS",fg= "white", bg = "#7a7f80", bd =3, font= ('verdana', 12, 'bold'))
        self.bt_grupos.place(relx= 0.025, rely= 0.575, relwidth= 0.1, relheight= 0.05)

        self.bt_lembretes = Button(self.home, text= "LEMBRETES",fg= "white", bg = "#7a7f80", bd =3, font= ('verdana', 12, 'bold'))
        self.bt_lembretes.place(relx= 0.025, rely= 0.65, relwidth= 0.1, relheight= 0.05)

        self.bt_logout = Button(self.home, text= "LOGOUT",fg= "white", bg= "#474a51", bd= 3, font= ('verdana', 12, 'bold'), command= self.logout)
        self.bt_logout.place(relx= 0.025, rely= 0.8, relwidth= 0.1, relheight= 0.05)

        self.bt_fechar = Button(self.home, text= "SAIR",fg= "white", bg= "#8b0000", bd= 3, font= ('verdana', 12, 'bold'), command= self.home.destroy)
        self.bt_fechar.place(relx= 0.025, rely= 0.875, relwidth= 0.1, relheight= 0.05)

        self.homeframe = Frame(self.home, bg= "#11114e")
        self.watch = PhotoImage(file= "images/watch.png")
        self.l_watch = Label(self.homeframe, image= self.watch, bg = "#11114e")
        self.l_watch.pack()

        self.homeframe.place(relx= 0.15, rely = 0.15, relwidth= 0.8, relheight= 0.8)
        
        self.atividades = Frame(self.home, bg= "grey")       
        self.historico = Frame(self.home, bg= "grey")
    
    def historicoWidgets(self):
        self.list_history = ttk.Treeview(self.historico, height= 3, columns=("col1", "col2", "col3", "col4", "col5"))
        self.list_history.heading("#0", text= "")
        self.list_history.heading("#1", text= "Nome")
        self.list_history.heading("#2", text= "Descrição")
        self.list_history.heading("#3", text= "Tipo")
        self.list_history.heading("#4", text= "Hora")
        self.list_history.heading("#5", text= "Data")
        
        self.list_history.column("#0", width = 1)
        self.list_history.column("#1", width= 100)
        self.list_history.column("#2", width= 300)
        self.list_history.column("#3", width= 50)
        self.list_history.column("#4", width= 50)
        self.list_history.column("#5", width= 50)

        self.list_history.place(relx= 0.01, rely= 0.2, relwidth=0.95, relheight=0.78)
        self.scrollbar5 = Scrollbar(self.historico, orient="vertical")
        self.list_history.configure(yscroll= self.scrollbar5.set)
        self.scrollbar5.place(relx=0.96, rely=0.2, relwidth=0.03, relheight=0.78)

        list1 = ["Todos", "Tarefas", "Reuniões", "Eventos"]
        list2 = ["Últimas 24 Horas", "Últimos 7 dias", "Últimos 15 dias", "Últimos 30 dias", "Últimos 90 dias", "Últimos 180 dias"]
        self.filtro1 = ttk.Combobox(self.historico, values= list1, font=('verdana', 12, "bold"))
        self.filtro2 = ttk.Combobox(self.historico, values= list2, font=('verdana', 12, "bold"))
        self.filtro1.set("Todos")
        self.filtro2.set("Últimos 7 dias")

        self.filtro1.place(relx=0.1, rely= 0.05, relwidth= 0.15, relheight = 0.1)
        self.filtro2.place(relx=0.3, rely= 0.05, relwidth= 0.15, relheight = 0.1)

        self.bt_search = Button(self.historico, text= "BUSCAR",fg= "white", bg = "#8b0000", bd =3, font= ('verdana', 12, 'bold'), command= self.select_history)
        self.bt_search.place(relx= 0.65, rely= 0.05, relwidth= 0.1, relheight= 0.1)


    def atividadesWidgets(self):

        self.bt_tarefas = Button(self.atividades, text= "TAREFAS",fg= "white", bg = "#8b0000", bd =3, font= ('verdana', 12, 'bold'), command= self.showTarefas)
        self.bt_tarefas.place(relx= 0.15, rely= 0.05, relwidth= 0.1, relheight= 0.1)

        self.bt_reunioes = Button(self.atividades, text= "REUNIÕES",fg= "white", bg = "#8b0000", bd =3, font= ('verdana', 12, 'bold'), command= self.showReunioes)
        self.bt_reunioes.place(relx= 0.35, rely= 0.05, relwidth= 0.1, relheight= 0.1)

        self.bt_eventos = Button(self.atividades, text= "EVENTOS",fg= "white", bg = "#8b0000", bd =3, font= ('verdana', 12, 'bold'), command= self.showEventos)
        self.bt_eventos.place(relx= 0.55, rely= 0.05, relwidth= 0.1, relheight= 0.1)

        self.bt_geral = Button(self.atividades, text= "GERAL",fg= "white", bg = "#8b0000", bd =3, font= ('verdana', 12, 'bold'), command= self.showGeral)
        self.bt_geral.place(relx= 0.75, rely= 0.05, relwidth= 0.1, relheight= 0.1)

        self.geral = Frame(self.atividades, bg= "grey")
        self.geral.place(relx= 0, rely= 0.25, relwidth=1, relheight=0.8)

        self.tarefas = Frame(self.atividades, bg= "grey")
        self.reunioes = Frame(self.atividades, bg= "grey")
        self.eventos = Frame(self.atividades, bg= "grey")

        self.la_title = Label(self.atividades, text="VISÃO GERAL",fg= "white",bg ="grey", font= ('verdana', 12))
        self.la_title.place(relx= 0.02, rely = 0.2, relwidth= 0.15, relheight= 0.05)

        self.list_activities = ttk.Treeview(self.geral, height= 3, columns=("col1", "col2", "col3", "col4", "col5"))
        self.list_activities.heading("#0", text= "")
        self.list_activities.heading("#1", text= "Nome")
        self.list_activities.heading("#2", text= "Descrição")
        self.list_activities.heading("#3", text= "Tipo")
        self.list_activities.heading("#4", text= "Hora")
        self.list_activities.heading("#5", text= "Data")
        
        self.list_activities.column("#0", width = 1)
        self.list_activities.column("#1", width= 100)
        self.list_activities.column("#2", width= 300)
        self.list_activities.column("#3", width= 50)
        self.list_activities.column("#4", width= 50)
        self.list_activities.column("#5", width= 50)

        self.list_activities.place(relx= 0.01, rely= 0.01, relwidth=0.95, relheight=0.90)
        self.scrollbar1 = Scrollbar(self.geral, orient="vertical")
        self.list_activities.configure(yscroll= self.scrollbar1.set)
        self.scrollbar1.place(relx=0.96, rely=0.01, relwidth=0.03, relheight=0.90)

    def Task(self):
        self.task = Toplevel()
        self.task.title("Tarefa")
        self.task.configure(background= 'grey')
        self.task.geometry("600x400")

        self.codigo = ""
        
        self.l_nome = Label(self.task,text= "Nome da tarefa", bg= 'grey', font=('verdana', '12', 'bold'))
        self.l_nome.place(relx=0.05, rely= 0.05)
        self.ent_nome = Entry(self.task, font= ('verdana', '10'))
        self.ent_nome.place(relx=0.05, rely= 0.125, relwidth= 0.35, relheight= 0.095)

        self.feito = IntVar()
        self.c_Feito = Checkbutton(self.task, text= "Feito?", bg= 'grey', font=('verdana', '12', 'bold'), variable= self.feito)
        self.c_Feito.place(relx=0.45, rely= 0.125)

        self.l_desc = Label(self.task,text= "Descrição", bg= 'grey', font=('verdana', '12', 'bold'))
        self.l_desc.place(relx=0.05, rely= 0.225)
        self.ent_desc = Text(self.task, font=('verdana', '10'))
        self.ent_desc.place(relx = 0.05, rely= 0.3, relwidth= 0.35, relheight= 0.45)

        self.l_calendario = Label(self.task,text= "Data", bg= 'grey', font=('verdana', '12', 'bold'))
        self.l_calendario.place(relx=0.45, rely= 0.225)
        self.calendario1 = Calendar(self.task, fg= "gray75", bg= "blue", font=('verdana', '9', 'bold'), locale= 'pt_br')
        self.calendario1.place(relx= 0.45, rely = 0.3)

        self.l_hour = Label(self.task,text= "Horário", bg= 'grey', font=('verdana', '12', 'bold'))
        self.l_hour.place(relx=0.7, rely= 0.05)
        list1 = [0, 1 , 2]
        list2 = [0, 1 , 2 , 3, 4 , 5, 6, 7 , 8 , 9]
        list3 = [0, 1, 2 , 3, 4, 5]
        self.cb_hours1 = ttk.Combobox(self.task, values= list1)
        self.cb_hours2 = ttk.Combobox(self.task, values= list2)
        self.cb_minutes1 = ttk.Combobox(self.task, values= list3)
        self.cb_minutes2 = ttk.Combobox(self.task, values= list2)
        self.cb_hours1.set(2)
        self.cb_hours2.set(3)
        self.cb_minutes1.set(5)
        self.cb_minutes2.set(9)

        self.cb_hours1.place(relx=0.7, rely= 0.125, relwidth=0.05)
        self.cb_hours2.place(relx=0.75, rely= 0.125, relwidth=0.05)
        self.l_doispontos = Label(self.task, text= ":", bg= 'grey', font= ('verdana','12', 'bold'))
        self.l_doispontos.place(relx=0.8, rely=0.125)
        self.cb_minutes1.place(relx=0.82, rely= 0.125, relwidth=0.05)
        self.cb_minutes2.place(relx=0.87, rely= 0.125, relwidth=0.05)

        self.l_wrong= Label(self.task, text= "Horário Inválido", bg= 'grey', fg= 'red',font= ('verdana','9', 'bold'))

        self.bt_add = Button(self.task, text= "Novo", bg= "#8b0000", fg= 'white', bd = 3, font=('verdana', 12, 'bold'), command= self.add_task)
        self.bt_add.place(relx= 0.05, rely= 0.85 , relwidth= 0.125, relheight= 0.1)

        self.bt_edit = Button(self.task, text= "Editar", bg= "#8b0000", fg= 'white', bd = 3, font=('verdana', 12, 'bold'), command= self.update_task)
        self.bt_edit.place(relx= 0.225, rely= 0.85 , relwidth= 0.125, relheight= 0.1)

        self.bt_exclude = Button(self.task, text= "Excluir", bg= "#8b0000", fg= 'white', bd = 3, font=('verdana', 12, 'bold'), command= self.delete_task)
        self.bt_exclude.place(relx= 0.4, rely= 0.85 , relwidth= 0.125, relheight= 0.1)

        self.bt_close = Button(self.task, text= "Fechar", bg= "#8b0000", fg= 'white', bd = 3, font=('verdana', 12, 'bold'), command= self.task.destroy)
        self.bt_close.place(relx= 0.85, rely= 0.85 , relwidth= 0.125, relheight= 0.1)

    def Reunion(self):
        self.reunion = Toplevel()
        self.reunion.title("Reunião")
        self.reunion.configure(background= 'grey')
        self.reunion.geometry("600x400")

        self.codigo = ""
        
        self.l_nome = Label(self.reunion,text= "Assunto", bg= 'grey', font=('verdana', '12', 'bold'))
        self.l_nome.place(relx=0.05, rely= 0.05)
        self.ent_nome = Entry(self.reunion, font= ('verdana', '10'))
        self.ent_nome.place(relx=0.05, rely= 0.125, relwidth= 0.35, relheight= 0.095)

        self.l_desc = Label(self.reunion,text= "Descrição", bg= 'grey', font=('verdana', '12', 'bold'))
        self.l_desc.place(relx=0.05, rely= 0.225)
        self.ent_desc = Text(self.reunion, font=('verdana', '10'))
        self.ent_desc.place(relx = 0.05, rely= 0.3, relwidth= 0.35, relheight= 0.45)

        self.l_calendario = Label(self.reunion,text= "Data", bg= 'grey', font=('verdana', '12', 'bold'))
        self.l_calendario.place(relx=0.45, rely= 0.225)
        self.calendario1 = Calendar(self.reunion, fg= "gray75", bg= "blue", font=('verdana', '9', 'bold'), locale= 'pt_br')
        self.calendario1.place(relx= 0.45, rely = 0.3)

        self.l_hour = Label(self.reunion,text= "Horário", bg= 'grey', font=('verdana', '12', 'bold'))
        self.l_hour.place(relx=0.7, rely= 0.05)
        list1 = [0, 1 , 2]
        list2 = [0, 1 , 2 , 3, 4 , 5, 6, 7 , 8 , 9]
        list3 = [0, 1, 2 , 3, 4, 5]
        self.cb_hours1 = ttk.Combobox(self.reunion, values= list1)
        self.cb_hours2 = ttk.Combobox(self.reunion, values= list2)
        self.cb_minutes1 = ttk.Combobox(self.reunion, values= list3)
        self.cb_minutes2 = ttk.Combobox(self.reunion, values= list2)
        self.cb_hours1.set(1)
        self.cb_hours2.set(2)
        self.cb_minutes1.set(0)
        self.cb_minutes2.set(0)

        self.cb_hours1.place(relx=0.7, rely= 0.125, relwidth=0.05)
        self.cb_hours2.place(relx=0.75, rely= 0.125, relwidth=0.05)
        self.l_doispontos = Label(self.reunion, text= ":", bg= 'grey', font= ('verdana','12', 'bold'))
        self.l_doispontos.place(relx=0.8, rely=0.125)
        self.cb_minutes1.place(relx=0.82, rely= 0.125, relwidth=0.05)
        self.cb_minutes2.place(relx=0.87, rely= 0.125, relwidth=0.05)

        self.l_wrong= Label(self.reunion, text= "Horário Inválido", bg= 'grey', fg= 'red',font= ('verdana','9', 'bold'))

        self.bt_add = Button(self.reunion, text= "Novo", bg= "#8b0000", fg= 'white', bd = 3, font=('verdana', 12, 'bold'), command = self.add_reunion)
        self.bt_add.place(relx= 0.05, rely= 0.85 , relwidth= 0.125, relheight= 0.1)

        self.bt_edit = Button(self.reunion, text= "Editar", bg= "#8b0000", fg= 'white', bd = 3, font=('verdana', 12, 'bold'), command = self.update_reunion)
        self.bt_edit.place(relx= 0.225, rely= 0.85 , relwidth= 0.125, relheight= 0.1)

        self.bt_exclude = Button(self.reunion, text= "Excluir", bg= "#8b0000", fg= 'white', bd = 3, font=('verdana', 12, 'bold'), command = self.delete_reunion)
        self.bt_exclude.place(relx= 0.4, rely= 0.85 , relwidth= 0.125, relheight= 0.1)

        self.bt_close = Button(self.reunion, text= "Fechar", bg= "#8b0000", fg= 'white', bd = 3, font=('verdana', 12, 'bold'), command= self.reunion.destroy)
        self.bt_close.place(relx= 0.85, rely= 0.85 , relwidth= 0.125, relheight= 0.1)

    def Event(self):
        self.event = Toplevel()
        self.event.title("Evento")
        self.event.configure(background= 'grey')
        self.event.geometry("1000x400")

        self.codigo = ""

        self.l_nome = Label(self.event,text= "Nome", bg= 'grey', font=('verdana', '12', 'bold'))
        self.l_nome.place(relx=0.05, rely= 0.05)
        self.ent_nome = Entry(self.event, font= ('verdana', '10'))
        self.ent_nome.place(relx=0.05, rely= 0.125, relwidth= 0.25, relheight= 0.095)

        self.l_desc = Label(self.event,text= "Descrição", bg= 'grey', font=('verdana', '12', 'bold'))
        self.l_desc.place(relx=0.05, rely= 0.225)
        self.ent_desc = Text(self.event, font=('verdana', '10'))
        self.ent_desc.place(relx = 0.05, rely= 0.3, relwidth= 0.25, relheight= 0.45)

        self.l_calendario = Label(self.event,text= "Data Começo", bg= 'grey', font=('verdana', '12', 'bold'))
        self.l_calendario.place(relx=0.325, rely= 0.225)
        self.calendario1 = Calendar(self.event, fg= "gray75", bg= "blue", font=('verdana', '9', 'bold'), locale= 'pt_br')
        self.calendario1.place(relx= 0.325, rely = 0.3)

        self.l_hour = Label(self.event,text= "Horário Começo", bg= 'grey', font=('verdana', '12', 'bold'))
        self.l_hour.place(relx=0.325, rely= 0.05)
        list1 = [0, 1 , 2]
        list2 = [0, 1 , 2 , 3, 4 , 5, 6, 7 , 8 , 9]
        list3 = [0, 1, 2 , 3, 4, 5]
        self.cb_hours1 = ttk.Combobox(self.event, values= list1)
        self.cb_hours2 = ttk.Combobox(self.event, values= list2)
        self.cb_minutes1 = ttk.Combobox(self.event, values= list3)
        self.cb_minutes2 = ttk.Combobox(self.event, values= list2)
        self.cb_hours1.set(1)
        self.cb_hours2.set(2)
        self.cb_minutes1.set(0)
        self.cb_minutes2.set(0)

        self.cb_hours1.place(relx=0.325, rely= 0.125, relwidth=0.03)
        self.cb_hours2.place(relx=0.355, rely= 0.125, relwidth=0.03)
        self.l_doispontos = Label(self.event, text= ":", bg= 'grey', font= ('verdana','12', 'bold'))
        self.l_doispontos.place(relx=0.3825, rely=0.125)
        self.cb_minutes1.place(relx=0.395, rely= 0.125, relwidth=0.03)
        self.cb_minutes2.place(relx=0.425, rely= 0.125, relwidth=0.03)

        self.l_calendario2 = Label(self.event,text= "Data Fim", bg= 'grey', font=('verdana', '12', 'bold'))
        self.l_calendario2.place(relx=0.65, rely= 0.225)
        self.calendario2 = Calendar(self.event, fg= "gray75", bg= "blue", font=('verdana', '9', 'bold'), locale= 'pt_br')
        self.calendario2.place(relx= 0.65, rely = 0.3)

        self.l_hour2 = Label(self.event,text= "Horário Fim", bg= 'grey', font=('verdana', '12', 'bold'))
        self.l_hour2.place(relx=0.65, rely= 0.05)

        self.cb_hours1_2 = ttk.Combobox(self.event, values= list1)
        self.cb_hours2_2 = ttk.Combobox(self.event, values= list2)
        self.cb_minutes1_2 = ttk.Combobox(self.event, values= list3)
        self.cb_minutes2_2 = ttk.Combobox(self.event, values= list2)
        self.cb_hours1_2.set(1)
        self.cb_hours2_2.set(2)
        self.cb_minutes1_2.set(0)
        self.cb_minutes2_2.set(0)

        self.cb_hours1_2.place(relx=0.65, rely= 0.125, relwidth=0.03)
        self.cb_hours2_2.place(relx=0.68, rely= 0.125, relwidth=0.03)
        self.l_doispontos = Label(self.event, text= ":", bg= 'grey', font= ('verdana','12', 'bold'))
        self.l_doispontos.place(relx=0.7075, rely=0.125)
        self.cb_minutes1_2.place(relx=0.72, rely= 0.125, relwidth=0.03)
        self.cb_minutes2_2.place(relx=0.75, rely= 0.125, relwidth=0.03)

        self.l_wrong= Label(self.event, text= "Horário Inválido", bg= 'grey', fg= 'red',font= ('verdana','9', 'bold'))
        self.l_wrong2= Label(self.event, text= "Horário Inválido", bg= 'grey', fg= 'red',font= ('verdana','9', 'bold'))
        self.l_wrong3= Label(self.event, text= "O fim não pode ser antes do começo ou no mesmo tempo", bg= 'grey', fg= 'red',font= ('verdana','9', 'bold'))

        self.bt_add = Button(self.event, text= "Novo", bg= "#8b0000", fg= 'white', bd = 3, font=('verdana', 12, 'bold'), command= self.add_event)
        self.bt_add.place(relx= 0.05, rely= 0.85 , relwidth= 0.125, relheight= 0.1)

        self.bt_edit = Button(self.event, text= "Editar", bg= "#8b0000", fg= 'white', bd = 3, font=('verdana', 12, 'bold'), command= self.update_event)
        self.bt_edit.place(relx= 0.225, rely= 0.85 , relwidth= 0.125, relheight= 0.1)

        self.bt_exclude = Button(self.event, text= "Excluir", bg= "#8b0000", fg= 'white', bd = 3, font=('verdana', 12, 'bold'), command= self.delete_event)
        self.bt_exclude.place(relx= 0.4, rely= 0.85 , relwidth= 0.125, relheight= 0.1)

        self.bt_close = Button(self.event, text= "Fechar", bg= "#8b0000", fg= 'white', bd = 3, font=('verdana', 12, 'bold'), command= self.event.destroy)
        self.bt_close.place(relx= 0.85, rely= 0.85 , relwidth= 0.125, relheight= 0.1)


    def tarefaswidgets(self):
        self.add = PhotoImage(file= "images/add.png")
        self.bt_addtask = Button(self.tarefas, image= self.add, bg = "#8b0000", bd = 3, command= self.Task)
        self.bt_addtask.place(relx= 0.070, rely = 0.1, relwidth= 0.05, relheight= 0.1)

        self.list_tasks = ttk.Treeview(self.tarefas, height = 3, columns=("col1", "col2", "col3", "col4","col5", "col6"))
        self.list_tasks.heading("#0", text= "")
        self.list_tasks.heading("#1", text= "Cod")
        self.list_tasks.heading("#2", text= "Nome")
        self.list_tasks.heading("#3", text= "Descrição")
        self.list_tasks.heading("#4", text= "Horário")
        self.list_tasks.heading("#5", text= "Prazo")
        self.list_tasks.heading("#6", text= "Feito")

        self.list_tasks.column("#0", width = 1)
        self.list_tasks.column("#1", width = 10)
        self.list_tasks.column("#2", width = 75)
        self.list_tasks.column("#3", width = 270)
        self.list_tasks.column("#4", width = 50)
        self.list_tasks.column("#5", width = 50)
        self.list_tasks.column("#6", width = 20)

        self.list_tasks.place(relx= 0.21, rely= 0.01, relwidth=0.75, relheight=0.90)
        self.scrollbar2 = Scrollbar(self.tarefas, orient="vertical")
        self.list_tasks.configure(yscroll= self.scrollbar2.set)
        self.scrollbar2.place(relx=0.96, rely=0.01, relwidth=0.03, relheight=0.90)

        self.list_tasks.bind("<Double-1>", self.OnDoubleClick)
        
    def reunionswidgets(self):
        self.bt_addreunion = Button(self.reunioes, image= self.add, bg = "#8b0000", bd = 3, command= self.Reunion)
        self.bt_addreunion.place(relx= 0.07, rely = 0.1, relwidth= 0.05, relheight= 0.1)
        self.list_reunions = ttk.Treeview(self.reunioes, height = 3, columns=("col1", "col2", "col3", "col4", "col5"))
        self.list_reunions.heading("#0", text= "")
        self.list_reunions.heading("#1", text= "Cod")
        self.list_reunions.heading("#2", text= "Assunto")
        self.list_reunions.heading("#3", text= "Descrição")
        self.list_reunions.heading("#4", text= "Hora")
        self.list_reunions.heading("#5", text= "Data")

        self.list_reunions.column("#0", width = 1)
        self.list_reunions.column("#1", width = 10)
        self.list_reunions.column("#2", width = 75)
        self.list_reunions.column("#3", width = 275)
        self.list_reunions.column("#4", width = 50)
        self.list_reunions.column("#5", width = 50)

        self.list_reunions.place(relx= 0.21, rely= 0.01, relwidth=0.75, relheight=0.90)
        self.scrollbar3 = Scrollbar(self.reunioes, orient="vertical")
        self.list_reunions.configure(yscroll= self.scrollbar3.set)
        self.scrollbar3.place(relx=0.96, rely=0.01, relwidth=0.03, relheight=0.90)

        self.list_reunions.bind("<Double-1>", self.OnDoubleClick2)

    def eventswidgets(self):
        self.bt_addevent = Button(self.eventos, image= self.add, bg = "#8b0000", bd = 3, command= self.Event)
        self.bt_addevent.place(relx= 0.07, rely = 0.1, relwidth= 0.05, relheight= 0.1)

        self.list_events = ttk.Treeview(self.eventos, height = 3, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8"))
        self.list_events.heading("#0", text= "")
        self.list_events.heading("#1", text= "Cod")
        self.list_events.heading("#2", text= "Nome")
        self.list_events.heading("#3", text= "Descrição")
        self.list_events.heading("#4", text= "Hora")
        self.list_events.heading("#5", text= "Começo")
        self.list_events.heading("#6", text= "Hora")
        self.list_events.heading("#7", text= "Fim")
        self.list_events.heading("#8", text= "Status")

        self.list_events.column("#0", width= 1)
        self.list_events.column("#1", width= 10)
        self.list_events.column("#2", width= 50)
        self.list_events.column("#3", width= 250)
        self.list_events.column("#4", width= 50)
        self.list_events.column("#5", width= 50)
        self.list_events.column("#6", width= 50)
        self.list_events.column("#7", width= 50)
        self.list_events.column("#8", width= 50)

        self.list_events.place(relx= 0.21, rely= 0.01, relwidth=0.75, relheight=0.90)
        self.scrollbar4 = Scrollbar(self.eventos, orient="vertical")
        self.list_events.configure(yscroll= self.scrollbar4.set)
        self.scrollbar4.place(relx=0.96, rely=0.01, relwidth=0.03, relheight=0.90)

        self.list_events.bind("<Double-1>", self.OnDoubleClick3)

class CadastroFuncs():
    def irparahome(self):
        self.cadastro.destroy()
        self.create_home()
    def voltarparalogin(self):
        self.cadastro.destroy()
        Login()
    def verificar(self):
        self.name = self.ent_name.get()
        self.user = self.ent_user.get()
        self.email = self.ent_email.get()
        self.number = self.ent_number.get()
        self.password = self.ent_password.get()
        self.password2 = self.ent_password2.get()

        verificador = True
        if (ehemail(self.email) == False):
            self.l_wrongemail.place(relx=0.1 ,rely= 0.5)
            verificador = False
        else:
            self.l_wrongemail.place_forget()
        if(ehTelefone(self.number) == False and len(self.number) != 0):
            self.l_wrongnumber.place(relx=0.6 ,rely= 0.2)
            verificador = False
        else:
            self.l_wrongnumber.place_forget()
        if(ehSenha(self.password) == False):
            self.l_wrongpassword.place(relx=0.6 ,rely= 0.35)
            verificador = False
        else:
            self.l_wrongpassword.place_forget()
        if(self.password != self.password2):
            self.l_wrongpassword2.place(relx=0.6 ,rely= 0.5)
            verificador = False
        else:
            self.l_wrongpassword2.place_forget()
        if(self.name == '' or self.email == '' or self.password == '' or self.password2 == '' or self.user == ''):
            self.l_wrongevrt.place(relx= 0.1, rely= 0.6)
            verificador = False
        else:
            self.l_wrongevrt.place_forget()
        if(verificador == True):
            self.l_wrongemail.place_forget()
            self.l_wrongnumber.place_forget()
            self.l_wrongpassword.place_forget()
            self.l_wrongpassword2.place_forget()
            self.l_wrongevrt.place_forget()
            self.irparahome()       
        
class Cadastro(CadastroFuncs):
    def create_cadastro(self):
        self.cadastro = Tk()
        self.cadastroTela()
        self.cadastroWidgets()
        self.cadastro.mainloop()

    def cadastroTela(self):
        self.cadastro.title("Cadastro")
        self.cadastro.configure(background= '#11114e')
        self.cadastro.geometry("700x500")
    
    def cadastroWidgets(self):
        self.l_name = Label(self.cadastro, text="Nome  *",fg= "white",bg ="#11114e", font= ('verdana', 11))
        self.l_name.place(relx= 0.1, rely = 0.1)

        self.ent_name = Entry(self.cadastro, font= ('verdana', 10))
        self.ent_name.place(relx= 0.1, rely= 0.15, relwidth= 0.4, relheight= 0.05)

        self.l_user = Label(self.cadastro, text="Usuário  *",fg= "white",bg ="#11114e", font= ('verdana', 11))
        self.l_user.place(relx= 0.1, rely = 0.25)

        self.ent_user = Entry(self.cadastro, font= ('verdana', 10))
        self.ent_user.place(relx= 0.1, rely= 0.3, relwidth= 0.4, relheight= 0.05)

        self.l_email = Label(self.cadastro, text="E-mail  *",fg= "white",bg ="#11114e", font= ('verdana', 11))
        self.l_email.place(relx= 0.1, rely = 0.4)

        self.ent_email = Entry(self.cadastro, font= ('verdana', 10))
        self.ent_email.place(relx= 0.1, rely= 0.45, relwidth= 0.4, relheight= 0.05)
        self.l_wrongemail = Label(self.cadastro, text="E-mail Inválido",fg= "red",bg ="#11114e", font= ('verdana', 11))
        #self.l_wrongemail.place(relx=0.1 ,rely= 0.5)

        self.l_number = Label(self.cadastro, text="Número Celular",fg= "white",bg ="#11114e", font= ('verdana', 11))
        self.l_number.place(relx= 0.6, rely = 0.1)

        self.ent_number = Entry(self.cadastro, font= ('verdana', 10))
        self.ent_number.place(relx= 0.6, rely= 0.15, relwidth= 0.3, relheight= 0.05)

        self.l_wrongnumber = Label(self.cadastro, text="Número Inválido",fg= "red",bg ="#11114e", font= ('verdana', 11))
        #self.l_wrongnumber.place(relx=0.6 ,rely= 0.2)

        self.l_password = Label(self.cadastro, text="Senha  *",fg= "white",bg ="#11114e", font= ('verdana', 11))
        self.l_password.place(relx= 0.6, rely = 0.25)

        self.ent_password = Entry(self.cadastro,show="*", font= ('verdana', 10))
        self.ent_password.place(relx= 0.6, rely= 0.3, relwidth= 0.3, relheight= 0.05)

        self.l_wrongpassword = Label(self.cadastro, text="Senha Inválida  *",fg= "red",bg ="#11114e", font= ('verdana', 11))
        #self.l_wrongpassword.place(relx=0.6 ,rely= 0.35)

        self.l_password2 = Label(self.cadastro, text="Verificar Senha",fg= "white",bg ="#11114e", font= ('verdana', 11))
        self.l_password2.place(relx= 0.6, rely = 0.4)

        self.ent_password2 = Entry(self.cadastro,show="*", font= ('verdana', 10))
        self.ent_password2.place(relx= 0.6, rely= 0.45, relwidth= 0.3, relheight= 0.05)

        self.l_wrongpassword2 = Label(self.cadastro, text="Senhas não são as mesmas",fg= "red",bg ="#11114e", font= ('verdana', 11))
        #self.l_wrongpassword2.place(relx=0.6 ,rely= 0.5)

        self.l_wrongevrt = Label(self.cadastro, text= "Preencha as entradas obrigatórias",fg= "red",bg ="#11114e", font= ('verdana', 11))
        #self.l_wrongevrt.place(relx= 0.1, rely= 0.6)

        self.bt_confirm = Button(self.cadastro, text= "CONFIRMAR",fg= "white", bg = "#474a51", bd =3, font= ('verdana', 12, 'bold'), command= self.verificar)
        self.bt_confirm.place(relx= 0.65, rely= 0.7, relwidth= 0.2, relheight= 0.075)

        self.bt_return = Button(self.cadastro, text= "VOLTAR",fg= "white", bg = "#474a51", bd =3, font= ('verdana', 12, 'bold'), command= self.voltarparalogin)
        self.bt_return.place(relx= 0.15, rely= 0.7, relwidth= 0.2, relheight= 0.075)

class RecuperarFuncs():
    def voltarlogin(self):
        self.recuperar.destroy()
        Login()

    def verificar2(self):
        self.email = self.ent_email.get()
        if(ehemail(self.email) == False):
            self.l_wrongemail.place(relx=0.1 ,rely= 0.225)
        else:
            self.l_wrongemail.place_forget()
            self.voltarlogin()

class RecuperarSenha(RecuperarFuncs):
    def create_recuperar(self):
        self.recuperar = Tk()
        self.recuperarTela()
        self.recuperarWidgets()
        self.recuperar.mainloop()

    def recuperarTela(self):
        self.recuperar.title("Recuperar Senha")
        self.recuperar.configure(background= '#11114e')
        self.recuperar.geometry("500x400")

    def recuperarWidgets(self):
        self.bt_confirm = Button(self.recuperar, text= "CONFIRMAR",fg= "white", bg = "#474a51", bd =3, font= ('verdana', 12, 'bold'), command= self.verificar2)
        self.bt_confirm.place(relx= 0.65, rely= 0.7, relwidth= 0.225, relheight= 0.075)

        self.bt_return = Button(self.recuperar, text= "VOLTAR",fg= "white", bg = "#474a51", bd =3, font= ('verdana', 12, 'bold'), command= self.voltarlogin)
        self.bt_return.place(relx= 0.15, rely= 0.7, relwidth= 0.225, relheight= 0.075)

        self.l_email = Label(self.recuperar, text="E-mail para recuperação",fg= "white",bg ="#11114e", font= ('verdana', 11))
        self.l_email.place(relx= 0.1, rely = 0.09)

        self.ent_email = Entry(self.recuperar, font= ('verdana', 10))
        self.ent_email.place(relx= 0.1, rely= 0.15, relwidth= 0.6, relheight= 0.075)
        self.l_wrongemail = Label(self.recuperar, text="E-mail Inválido",fg= "red",bg ="#11114e", font= ('verdana', 11))
        #self.l_wrongemail.place(relx=0.1 ,rely= 0.225)

class LoginFuncs():
    def verifica_login(self):
        self.user = self.ent_user.get()
        self.password = self.ent_password.get()
        if self.user == "admin" and self.password == "admin":
            self.login.destroy()
            self.create_home()

        else:
            print("ta errado")

    def cadastro(self):
        self.login.destroy()
        self.create_cadastro()
    
    def recuperar(self):
        self.login.destroy()
        self.create_recuperar()

class Login(LoginFuncs, Home, Cadastro, RecuperarSenha):
    def __init__(self):
        self.login = Tk()
        self.loginTela()
        self.loginWidgets()
        
        self.login.mainloop()

    def loginTela(self):
        self.login.title("Bem Vindo")
        self.login.configure(background= '#11114e')
        self.login.geometry("450x700")

    def loginWidgets(self):
        self.l_user = Label(self.login, text="Usuário",fg= "white",bg ="#11114e", font= ('verdana', 12))
        self.l_user.place(relx= 0.25, rely = 0.15, relwidth= 0.5, relheight= 0.02)

        self.l_password = Label(self.login, text="Senha",fg= "white", bg= "#11114e", font= ('verdana', 12))
        self.l_password.place(relx= 0.25, rely = 0.25, relwidth= 0.5, relheight= 0.02)

        self.ent_user = Entry(self.login, font= ('verdana', 12))
        self.ent_user.place(relx= 0.25, rely= 0.175, relwidth= 0.5, relheight= 0.05)

        self.ent_password = Entry(self.login, show="*", font= ('verdana', 12))
        self.ent_password.place(relx= 0.25, rely= 0.275, relwidth = 0.5, relheight= 0.05)

        self.bt_logar = Button(self.login, text= "LOGAR",fg= "white", bg = "#474a51", bd =3, font= ('verdana', 12, 'bold'), command= self.verifica_login)
        self.bt_logar.place(relx= 0.25, rely= 0.4, relwidth= 0.5, relheight= 0.075)

        self.bt_cadastrar = Button(self.login, text= "CADASTRAR-SE",fg= "white", bg= "#7a7f80", bd= 3, font= ('verdana', 12, 'bold'), command = self.cadastro)
        self.bt_cadastrar.place(relx= 0.25, rely= 0.7, relwidth= 0.5, relheight= 0.0625)

        self.bt_esquecersenha = Button(self.login, text= "ESQUECEU SUA SENHA?",fg= "white", bg = "#7a7f80", bd = 3, font= ('verdana', 12, 'bold'), command= self.recuperar)
        self.bt_esquecersenha.place(relx= 0.25, rely= 0.825, relwidth= 0.5, relheight= 0.0625)

Login()


