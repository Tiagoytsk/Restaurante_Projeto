import re 
import json
import datetime
import getpass
import os
def save(filename, lista):#feito
    try:
        with open(filename, 'w') as f:#w-write a- appende r- read
            json.dump(lista, f, indent = 4)
    except:
        print("")
    else:
        print("")
def load(filename):#feito
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except:
        print("")
    else:
        print("")
    return data
def checkemail(email):
    formato= r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(formato, email)):
        return True
    else:
        return False
def conta(login):#feito
    if checkemail(login):
        log=0
        listautilizadores=load("users.json")
        for pessoa in listautilizadores:
            if pessoa['email']==login:
                log=1
                return pessoa ['email'], pessoa['tipo']
        if log==0:
            return login, 0
    else:
        input("Formato de email esta errado, tente outravez\nClique no enter para continuar...")
        return 0,4
def numpessoas(lotacao, restaurante):#feito
    count=0
    while count!=1:
        pessoas=int(input('Numero de pessoas:\n\nIndique o numero de pessoas(max12):'))
        total_pessoa=lotacao+pessoas
        if total_pessoa<=restaurante['ocupacaomaxima'] and pessoas<=12:
            criancas=int(input("Indique o numero de criancas:"))
            if criancas<=pessoas:    
                pessoastotal=pessoas-criancas
                count+=1
                return pessoastotal, criancas
            else:
                input("Tem criancas a mais para o numero de pessoas\nClique no enter para continuar...")
        else:
            input(f"Restaurante cheio so existem {restaurante['ocupacaomaxima']-lotacao} lugares.\nClique no enter para continuar...")
            break           
def fatura():#feito
    nome=input('Dados para da fatura:\n\nIndique o seu nome:')
    nif=input('Indique o seu NIF:')
    return nome, nif
def resumoreserva(restaurante, data, horario, totalpessoas, criancas, nome, nif):#feito
    precoadulto=restaurante['precoadulto']
    precocrianca=restaurante['precocrianca']               
    precototal=(precoadulto*totalpessoas)+(precocrianca*criancas)
    confirmar=input(f"Resumo da reserva:\n\nData:  {data}     Hora: {horario}\nAdultos:   {totalpessoas}      Criancas: {criancas} Total de pessoas: {totalpessoas+criancas}\n*\nDados de Faturacao:\nNome: {nome} com NIF: {nif} \nTotal a pagar:{precototal}\nConfirmar a reserva(s/n)?")
    return confirmar, precototal
def verificadata(data):#feito
    date_format = '%Y-%m-%d'
    try:
        input_date = datetime.datetime.strptime(data, date_format)
        today = datetime.datetime.now().date()
        if input_date.date() >= today + datetime.timedelta(days=1):
            return True
        else:
            input("Data deve ser marcada com pelo menos um dia de antecedencia!\nClique no enter para continuar...")
            return False
    except ValueError:
        input("Data incorreta!\nClique no enter para continuar...")
        return False
def verificafolgas(data, closedays):
    for dia in closedays:
        if dia['data']==data:
            input("Ja existe este dia de feicho.\nClique no enter para continuar...")
            return False
    return True
def marcarrefeicao(utilizador):#falta dias da semana
    count=0
    reservas=load("meals.json")
    restaurante=load("defenitions.json")
    while count!=1:
        data=input("Book Table\n\nIntroduza a data no formato aaaa-mm-dd:")
        if verificadata(data) and verificar_dia_semana(data)!="Segunda-feira" and verificafolgas(data):
            horario=input("Horario: 19:00h as 22:00h\n introduza a hora prevista para a sua chegada no formato hh:mm: ")
            if verificahoras(horario):
                count, lotacao=verificareserva(utilizador, restaurante, reservas, data)
                if count==0:
                    adultos, criancas=numpessoas(lotacao, restaurante)
                    totalpessoas=adultos+criancas
                    nome, nif=fatura()
                    confirmar, precototal=resumoreserva(restaurante, data, horario, adultos, criancas, nome, nif)
                    if confirmar=='s':
                        reservas+=[{'email':utilizador,'nome':nome,'nif':nif,'data':data,'horachegada':horario,'totalpessoas':totalpessoas,'adultos':adultos,'criancas':criancas,'precototal':precototal}]
                        save("meals.json", reservas)
                        count=1
                    else:
                        return 
        else:
            input("A data entroduzida nao esta certa ou corresponde a um dia que o restaurante estafechado\nClique no enter para continuar...")
def verificar_dia_semana(data):
    date_format = '%Y-%m-%d'
    try:
        date_object = datetime.datetime.strptime(data, date_format)
        dia_semana_numero = date_object.weekday()
        dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
        return dias_semana[dia_semana_numero]
    except ValueError:
        input("Data incorreta!\nClique no enter para continuar...")
        return None
def verificamail(utilizador, reserva):#feito
    if reserva['email']==utilizador:
        return True
    else:
        return False 
def verificareserva(utilizador, restaurante, reservas, data):#feito
    count=0
    lotacao=0
    reservastotais=0
    for reserva in reservas:
        if reserva['data']==data:
            lotacao+=reserva['totalpessoas']
            if verificamail(utilizador, reserva): 
                count=1
            else:
                reservastotais+=1
    if count==0:   
        if reservastotais <restaurante['mesas'] and  lotacao <restaurante['ocupacaomaxima']:
            input("Possivel efetuar reserva\nClique no enter para continuar...")
            return 0, lotacao
        else:
            input('Nao foi possivel efetuar a reserva:\n Ja nao existe espaco disponivel.\nClique no enter para continuar...')
            return 1   
    elif count==1:
        input('Nao foi possivel efetuar a reserva:\n Ja existe uma reserva nesta data.\nClique no enter para continuar...')
def verhistorico(utilizador):#feito
    reservas=load("meals.json")
    for pessoa in reservas:
        for item in pessoa:
            if item =='email':
                if utilizador==pessoa['email']:
                    input(f"Historico de reservas do cliente:\n\n****\n\nData:   {pessoa['data']}     Hora:   {pessoa['horachegada']}\n\nAdultos:       {pessoa['adultos']}     criancas: {pessoa['criancas']}      total de pessoas: {pessoa['totalpessoas']} \nNome: {pessoa['nome']} com o NIF: {pessoa['nif']}\n\nTotal a pagar: {pessoa['precototal']}\nClique no enter para continuar...")
    return
def menucliente(utilizador):#feio
    op=int(input('Cliente Menu:\n\n1 - Marcar Refeicao\n2 -Ver Historico\n3 - Sair\nIndique a opcao desejada:'))
    match op:
        case 1:
            marcarrefeicao(utilizador)
        case 2:
            verhistorico(utilizador)
        case 3:
            return 1
def defenicoes():
    defenicoes=load("defenitions.json")
    input(f"Defenicoes:\n\nPreco por adulto: {defenicoes['precoadulto']}\nPreco por crianca: {defenicoes['precocrianca']}\nOcupacao maxima: {defenicoes['ocupacaomaxima']}\nNumero de mesas: {defenicoes['mesas']}\nDia de folga: {defenicoes['diadefolga']}\nClique no enter para continuar...")
def verificahoras(hora):#Feito
    formatohoras = ("%H:%M")
    restaurante=load("defenitions.json")
    interval_start = datetime.datetime.strptime(restaurante['abertura'], formatohoras).time()
    interval_end = datetime.datetime.strptime(restaurante['fecho'], formatohoras).time()
    try:
        validahora= datetime.datetime.strptime(hora, formatohoras).time()
        return interval_start <= validahora <= interval_end
    except ValueError:
        return False
def extratoreservas():
    count=0
    totaladultos=0
    totalcriancas=0
    totalpessoas=0
    faturado=0
    reservas=load("meals.json")
    while count==0:
        dia=input("Qual o dia que deseja consultar as reservas:")
        if verificadata(dia):   
            for pessoa in reservas:
                for item in pessoa:
                    if item =='data':
                        if dia==pessoa['data']:
                            faturado+=pessoa['precototal']
                            totaladultos+=pessoa['adultos']
                            totalcriancas+=pessoa['criancas']
                            totalpessoas+=pessoa['totalpessoas']
                            input(f"Historico de reservas do dia {pessoa['data']}\n\n****\n\nData:   {pessoa['data']}     Hora:   {pessoa['horachegada']}\n\nAdultos:       {pessoa['adultos']}     criancas: {pessoa['criancas']}      total de pessoas: {pessoa['totalpessoas']} \nNome: {pessoa['nome']} com o NIF: {pessoa['nif']}\n\nTotal a pagar: {pessoa['precototal']}\nClique no enter para continuar...")
            count=1
            input(f"Estatisticas:\n\nTotal faturado: {faturado}\n\nTotal Adultos: {totaladultos}\n\nTotal Criancas: {totalcriancas}\n\nTotal Pessoas: {totalpessoas}\nPrecione uma tecla para continuar...")
            return
def verificasetem1reserva(data):
    reservas=load("meals.json")
    for reserva in reservas:
        if reserva['data']==data:
            input("Ja existem reservas neste dia por isso o restaurante nao pode ser fechado.\nClique no enter para continuar...")
            return False
    return True
def fechosdia():
    closedays=load("closedays.json")
    printultimas10closedays(closedays)
    novfecho=input("Insira o dia em que quer fechar o restaurante no formato YYYY-MM-DD.")
    if verificadata(novfecho) and verificafolgas(novfecho, closedays) and verificasetem1reserva(novfecho):
        closedays+=[{"data":novfecho}]
        save("closedays.json",closedays)
        input("Dia de fecho guardado com sucesso\nClique no enter para continuar...")
    else:
        input("Error\nClique no enter para continuar...")
        
    return   
def printultimas10closedays(data):
    listadedatas= sorted(data, key=lambda x: obter_data(x), reverse=True)

    for item in listadedatas[:10]:
        print(f"Data de fecho: {item['data']}")
    input('Clique no enter para continuar...')
def obter_data(closedays):
    return datetime.datetime.strptime(closedays['data'], '%Y-%m-%d')    
def addadm():
    email=input("Adicionar Novo Admin\n\nIntroduza o email do utilizador para tornalo admin:")
    users=load("users.json")
    novalistadeusers=[]
    for user in users:
        if user['email']==email and user['tipo']==1:
            print("Utilizador encontrado!\nIntroduza uma password")
            paswd=getpass.getpass('pass:****')
            novalistadeusers+=[{"nome": user['nome'],"email": user['email'],"paswd": paswd,"tipo": 2}]
        elif user['tipo']==1:
            novalistadeusers+=[{"nome": user['nome'],"email": user['email'],"tipo": 1}]
        elif user['tipo']==2:
            novalistadeusers+=[{"nome": user['nome'],"email": user['email'],"paswd": user['paswd'],"tipo": 2}]
        elif user['tipo']==3:
            novalistadeusers+=[{"nome": user['nome'],"email": user['email'],"paswd": user['paswd'],"tipo": 3}]
    save("users.json",novalistadeusers)
def removeadm(): 
    email=input("Remover Admin\n\nIntroduza o email do utilizador para removelo de admin:")
    users=load("users.json")
    novalistadeusers=[]
    for user in users:
        if user['email']==email and user['tipo']==2:
            novalistadeusers+=[{"nome": user['nome'],"email": user['email'],"tipo": 1}]
            input("Utilizador removido com sucesso\nClique no enter para continuar...")
        elif user['tipo']==1:
            novalistadeusers+=[{"nome": user['nome'],"email": user['email'],"tipo": 1}]
        elif user['tipo']==2:
            novalistadeusers+=[{"nome": user['nome'],"email": user['email'],"paswd": user['paswd'],"tipo": 2}]
        elif user['tipo']==3:
            novalistadeusers+=[{"nome": user['nome'],"email": user['email'],"paswd": user['paswd'],"tipo": 3}]
    save("users.json",novalistadeusers)
def addfuncionario():
    email=input("Adicionar Novo Admin\n\nIntroduza o email do utilizador para tornalo admin:")
    users=load("users.json")
    novalistadeusers=[]
    for user in users:
        if user['email']==email and user['tipo']==1:
            print("Utilizador encontrado!\nIntroduza uma password")
            paswd=getpass.getpass('pass')
            novalistadeusers+=[{"nome": user['nome'],"email": user['email'],"paswd": paswd,"tipo": 3}]
            input("Funcionario adicionado com sucesso.\nClique no enter para continuar...")
        elif user['tipo']==1:
            novalistadeusers+=[{"nome": user['nome'],"email": user['email'],"tipo": 1}]
        elif user['tipo']==2:
            novalistadeusers+=[{"nome": user['nome'],"email": user['email'],"paswd": user['paswd'],"tipo": 2}]
        elif user['tipo']==3:
            novalistadeusers+=[{"nome": user['nome'],"email": user['email'],"paswd": user['paswd'],"tipo": 3}]
    save("users.json",novalistadeusers)
def removefuncionario():
    email=input("Despedir funcionario:\n\nIntroduza o email do funcionario para o despedir:")
    users=load("users.json")
    novalistadeusers=[]
    for user in users:
        if user['email']==email and user['tipo']==3:
            novalistadeusers+=[{"nome": user['nome'],"email": user['email'],"tipo": 1}]
            input("O funcionario foi despedido.\nClique no enter para continuar...")
        elif user['tipo']==1:
            novalistadeusers+=[{"nome": user['nome'],"email": user['email'],"tipo": 1}]
        elif user['tipo']==2:
            novalistadeusers+=[{"nome": user['nome'],"email": user['email'],"paswd": user['paswd'],"tipo": 2}]
        elif user['tipo']==3:
            novalistadeusers+=[{"nome": user['nome'],"email": user['email'],"paswd": user['paswd'],"tipo": 3}]
    save("users.json",novalistadeusers)
def checkadm(utilizador):
    users=load("users.json")
    for user in users:
        if utilizador==user['email'] and user['tipo']==2:
            input("Ja nao es admin!\nClique no enter para continuar...")
            return True
    return False              
def menuadmin(utilizador):
    sair=0
    while sair==0:
        if checkadm(utilizador):
            op=int(input('Admin Menu:\n\n1 - Defenicoes\n2 - Fecho dia\n3 - Extrato de reservas do dia\n4 - Adicionar admin\n5 - Remover admin\n6 - Adicionar funcionario\n7 - Remover funcionario\n8 - Ver horas dos funcionarios\n9 - sair\nIndique a opcao desejada: '))
            match op:
                case 1:
                    defenicoes()
                case 2:
                    fechosdia()
                case 3:
                    extratoreservas()
                case 4:
                    addadm()
                case 5:
                    removeadm()
                case 6:
                    addfuncionario()
                case 7:
                    removefuncionario()
                case 8:
                    verhorasfuncionario()
                case 9:
                    sair=1
                    return 1
        else:
            return 1
def verhorasfuncionario():
    funcionario=input("Indique o nome do funcionario que deseja ver as horas: ")
    horarios=load("funcionarios.json")
    for item in horarios:
        if item['email']==funcionario:
            print(f"Data: {item['data']}    Hora de entrada: {item['horadeentrada']}    Hora de saida: {item['horadesaida']}")
    input("Quando quiser voltar para o menu clique no enter...")
def verificapaswd(utilizador, paswd):#feito
    listauser=load("users.json")
    for pessoa in listauser:
        if  pessoa['email'] == utilizador and pessoa['paswd']== paswd:
            return 1
    return 0
def criarutilizador():
    user=load("users.json")
    email=input("Criacao de utilizador:\n\nIntroduza o seu email:")
    nome=input("introduza o seu nome:")
    user+=[{'nome':nome,'email':email,'tipo':1}]
    save("users.json", user)
    return
def checkfuncionario(utilizador):    
    users=load("users.json")
    for user in users:
        if utilizador==user['email'] and user['tipo']==3:
            return True
    input("Foste despedido!\nClique no enter para continuar...")
    return False
def marcarentrada(utilizador):
    horarios=load("funcionarios.json")
    agora=datetime.datetime.now()
    entradadata=agora.strftime("%Y-%m-%d")
    entradahora=agora.strftime("%H:%M")
    count=0
    for item in horarios:
        if utilizador== item['email'] and entradadata==item['data']:
            input("Ja marcaste a hora de entrada.\nClique no enter para continuar...")
            return
        elif utilizador!= item['email']:
            pass
        elif utilizador== item['email'] and entradadata==item['data']:
            pass
    horarios+=[{"email": utilizador,"data": entradadata,"horadeentrada": entradahora}]
    input("Hora de entrada marcada.\nClique no enter para continuar...")
    save("funcionarios.json",horarios) 
    return   
def marcarsaida(utilizador):
    horarios=load("funcionarios.json")
    agora=datetime.datetime.now()
    saidadata=agora.strftime("%Y-%m-%d")
    saidahora=agora.strftime("%H:%M") 
    newhorarios=[]
    count=0
    res=input('Ja marcas-te hora de entrada Hoje?(s/n)')
    if res=='s':
        for item in horarios:            
            if saidadata == item['data'] and utilizador == item['email'] and item.get('horadesaida') != None:
                input("Ja marcas-te a saida!\nClique no enter para continuar...")
                return
            elif utilizador!=item['email']:
                newhorarios+=[{'email':utilizador,'data':item['data'],'horadeentrada': item['horadeentrada'],'horadesaida':item['horasdesaida']}]
            elif utilizador==item['email'] and item['data'] != saidadata:
                newhorarios+=[{'email':utilizador,'data':item['data'],'horadeentrada': item['horadeentrada'],'horadesaida':item['horadesaida']}]
            elif utilizador==item['email'] and saidadata==item['data'] and item.get('horadeentrada') is not None:
                    newhorarios+=[{'email':utilizador,'data':saidadata,'horadeentrada': item['horadeentrada'], 'horadesaida': saidahora}]
                    input('Saida Marcada com sucesso.\nClique no enter para continuar...')
                    count=1
        if count==1:
            save("funcionarios.json",newhorarios)
        else:
            input("Error.\n","*"*40,"\nFalta marcar a entrada.\nClique no enter para continuar...")
    else:
        input("Nao podes marcar a hora de entrada sem marcares Hora de saida\nClique no enter para continuar...")                     
def menufuncionario(utilizador):
    sair=0
    while sair==0:
        if checkfuncionario(utilizador):
            op=int(input('Menu Funcionarios:\n\n1 - Marcar entrada\n2 - Marcar saida\n3 - sair\nEscolha a opcao desejada:'))
            match op:
                case 1:
                    marcarentrada(utilizador)
                case 2:
                    marcarsaida(utilizador)
                case 3:
                    sair=1
                    return 1
sair=0
while sair!=1:
    login=input('Autentificacao\n\n\nIntroduza o seu email:')
    utilizador, role= conta(login)
    if role == 1:
        sair = menucliente(utilizador)
    elif role==2:
        while sair!=1:
            paswd= getpass.getpass('Pass:****')
            autentificado=verificapaswd(utilizador, paswd)
            if autentificado==1:
                sair=menuadmin(utilizador)
            else:
               input('Senha Errada tente outravez.\nClique no enter para continuar...')
    elif role==3:
        while sair!=1:
            paswd= getpass.getpass('Pass:****')
            autentificado=verificapaswd(utilizador, paswd)
            if autentificado==1:
                sair=menufuncionario(utilizador)
            else:
                input('Senha Errada tente outravez.\nClique no enter para continuar...')
    elif role==0:
        usercreate=input("Utilizador nao encontrado!\nDeseja criar uma nova conta?(s/n)")
        if usercreate=='s':
            criarutilizador()
