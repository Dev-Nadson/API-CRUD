import os
from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

DataBase = create_engine("sqlite:///PsyApp.bd")
Session = sessionmaker(bind=DataBase)
session = Session()

base = declarative_base()

class Paciente(base):
    __tablename__ = "pacientes"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    civil_status = Column("status_civil", String)
    profession = Column("profissao", String)
    birthday = Column("data_de_nascimento", String)
    gender = Column("genero", String)
    cpf = Column("cpf", String)
    rg = Column("rg", String)
    adress = Column("endereço", String)
    contact = Column("contato", String)
    status = Column("status", Boolean)

    def __init__(self, name, age, civil_status, profession, birthday, gender, cpf, rg, adress, contact, status = True):
        self.name = name
        self.age = age
        self.civil_status = civil_status
        self.profession = profession
        self.birthday = birthday
        self.gender = gender
        self.cpf = cpf
        self.rg = rg
        self.adress = adress
        self.contact = contact
        self.status = status

class Sessao(base):
    __tablename__ = "sessoes"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    paciente_id = Column("owner", ForeignKey("pacientes.id"))
    date = Column("data", String)
    hour = Column("hora", String)
    duration = Column("duracao", String)
    queixa_principal = Column("queixa_principal", String)
    historico_familiar = Column("historico_familiar", String)
    historico_pessoal = Column("historico_pessoal", String)
    aspectos = Column("aspectos", String)
    obs = Column("observacoes", String)

    def __init__(self, paciente_id, date, hour, duration, queixa_principal, historico_familiar, historico_pessoal, aspectos, obs):
        self.paciente_id = paciente_id
        self.date = date
        self.hour = hour
        self.duration = duration
        self.queixa_principal = queixa_principal
        self.historico_familiar = historico_familiar
        self.historico_pessoal = historico_pessoal
        self.aspectos = aspectos
        self.obs = obs

base.metadata.create_all(bind=DataBase)

def create():
    #Dados do Paciente
    name = input("Insira o nome do paciente: ")
    age = (input("Insira a idade do Paciente: "))
    civil_status = input("Estado cívil do paciente: ")
    profession = input("Insira a profissão do paciente: ")
    birthday = input("Insira a data de nascimento do paciente: ")
    gender = input("Insira o gênero do paciente: ")
    cpf = (input("Insira o CPF do paciente (Apenas Números): "))
    rg = (input("Insira o RG do paciente (Apenas Números): "))
    adress = input("Insira o endereço do paciente: ")
    contact = (input("Insira o telefone para contato do paciente (Apenas Números): "))
    paciente = Paciente(name, age, civil_status, profession, birthday, gender, cpf, rg, adress, contact)
    session.add(paciente)
    session.commit()

    #Dados da sessão
    # date = input("Insira a data do atendimento: ")
    # hour = input("Insira o horário da sessão: ")
    # duration = input("Queixa principal: ")
    # queixa_principal = input("Queixa principal: ")
    # historico_familiar = input("Histórico Familiar: ")
    # historico_pessoal = input("Histórico Pessoal: ")
    # aspectos = input("Aspectos emocionais e comportamentais: ")
    # obs = input("Observações: ")
    # sessao = Sessao(date, hour, duration, queixa_principal, historico_familiar, historico_pessoal, aspectos, obs)
    # session.add(sessao)
    # session.commit()

        
def read():
    # name = input("Insira o nome do paciente: ")
    pass
  

def update():
    # name = input("Insira o nome do paciente: ")
    # queixa_principal = input("\nDigite o conteúdo da Alteração: \n")
    pass

def remove():
    # name = input("Insira o nome do paciente: ")
    pass

def invalid():
    print("Opção inválida.")


Menu = {
    1: create,
    2: read,
    3: update,
    4: remove
}

os.system('cls')

while True:
    print("\n----- Gerenciamento de Pacientes -----")
    print("\n1.Criar novo paciente  " \
        "\n2.Ler o prontuário " \
        "\n3.Atualizar o prontuário " \
        "\n4.Excluir algum paciente" \
        "\n5.Sair \n")

    option = int(input("Selecione a opção desejada: "))
    if option == 5:
        break
    Menu.get(option, invalid)()