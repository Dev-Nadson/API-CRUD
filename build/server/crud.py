from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///build/database/psyapp.db")
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
Base = declarative_base()


class Patient(Base):
    __tablename__ = "patients"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("nome", String, nullable=False)
    age = Column("idade", Integer, nullable=False)
    civil_status = Column("status_civil", String, nullable=False)
    profession = Column("profissao", String, nullable=False)
    birthday = Column("data_de_nascimento", String, nullable=False)
    gender = Column("genero" ,String, nullable=False)
    cpf = Column("cpf", String, nullable=False, unique=True)
    rg = Column("rg", String, nullable=False, unique=True)
    address = Column("endereco", String, nullable=False)
    contact = Column("contato" ,String, nullable=False)
    status = Column("status" ,Boolean, nullable=False)

    def __init__(self, name: str, age: int, civil_status: str, profession: str, birthday: str, gender: str, cpf: str, rg: str, address: str, contact: str, status: bool = True):
        self.name = name
        self.age = age
        self.civil_status = civil_status
        self.profession = profession
        self.birthday = birthday
        self.gender = gender
        self.cpf = cpf
        self.rg = rg
        self.address = address
        self.contact = contact
        self.status = status

class SessionRecord(Base):
    __tablename__ = "sessions"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    patient_id = Column("paciente_id", Integer, ForeignKey("patients.id"), nullable=False)
    date = Column("data", String, nullable=False)
    hour = Column("hora", String, nullable=False)
    duration = Column("duracao", String, nullable=False)
    main_complaint = Column("queixa_principal", String, nullable=False)
    family_history = Column("historico_familiar", String, nullable=False)
    personal_history = Column("historico_pessoal", String, nullable=False)
    aspects = Column("aspectos", String, nullable=False)
    observations = Column("observacoes", String, nullable=True)

    def __init__(self, patient_id: int, date: str, hour: str, duration: str, main_complaint: str, family_history: str, personal_history: str, aspects: str, observations: str):
        self.patient_id = patient_id
        self.date = date
        self.hour = hour
        self.duration = duration
        self.main_complaint = main_complaint
        self.family_history = family_history
        self.personal_history = personal_history
        self.aspects = aspects
        self.observations = observations

Base.metadata.create_all(bind=engine)

def create_patient():
    name = input("Insira o nome do paciente: ")
    age = (input("Insira a idade do Paciente: "))
    civil_status = input("Estado cívil do paciente: ")
    profession = input("Insira a profissão do paciente: ")
    birthday = input("Insira a data de nascimento do paciente: ")
    gender = input("Insira o gênero do paciente: ")
    cpf = (input("Insira o CPF do paciente (Apenas Números): "))
    rg = (input("Insira o RG do paciente (Apenas Números): "))
    address = input("Insira o endereço do paciente: ")
    contact = (input("Insira o telefone para contato do paciente (Apenas Números): "))

    # Verifica duplicação de CPF ou RG
    existing_cpf = session.query(Patient).filter_by(cpf=cpf).first()
    existing_rg = session.query(Patient).filter_by(rg=rg).first()
    if existing_cpf or existing_rg:
        return print("Já existe um paciente com esse CPF ou RG.")

    patient = Patient(name, age, civil_status, profession, birthday, gender, cpf, rg, address, contact)
    session.add(patient)
    session.commit()
    print(f"\nPaciente: {patient.name}, ID: {patient.id}.")
    print("\n----- Criação de Sessões -----")
    print("\n1.Criar primeira sessão\n2.Sair\n")
    option = int(input("Selecione a opção desejada: "))
    if option == 1:
        create_session(patient.id)

def create_session(patient_id):
    date = input("Insira a data do atendimento: ")
    hour = input("Insira o horário da sessão: ")
    duration =  input("Duração da sessão: ")
    main_complaint = input("Queixa principal: ")
    family_history = input("Histórico Familiar: ")
    personal_history = input("Histórico Pessoal: ")
    aspects =  input("Aspectos emocionais e comportamentais: ")
    observations = input("Observações: ")

    session_record = SessionRecord(patient_id, date, hour, duration, main_complaint, family_history, personal_history, aspects, observations)
    session.add(session_record)
    session.commit()

def read_patients():
    patients = session.query(Patient).all()
    for patient in patients:
        print(f"ID: {patient.id}, Nome: {patient.name}")
    try:
        selected_id = int(input("\nInsira o ID do paciente para detalhes: "))
    except ValueError:
        print("ID inválido.")
        return

    patient = session.query(Patient).filter_by(id=selected_id).first()

    print(f"\n--- Detalhes do: {patient.name}, ID: {patient.id} ---")
    print(f"Idade: {patient.age}")
    print(f"Status Cívil : {patient.civil_status}")
    print(f"Profissão: {patient.profession}")
    print(f"Data de nascimento: {patient.birthday}")
    print(f"Gênero: {patient.gender}")
    print(f"CPF: {patient.cpf}")
    print(f"RG: {patient.rg}")
    print(f"Endereço: {patient.address}")
    print(f"Contato: {patient.contact}")
    print(f"Status: {'Ativo' if patient.status else 'Inativo'}")

    sessions = session.query(SessionRecord).filter_by(patient_id=patient.id).all()
    if sessions:
        print("\n--- Sessões ---")
        for s in sessions:
            print(f"\n• Data: {s.date} | Hora: {s.hour} | Duração: {s.duration}")
            print(f"  Queixa principal: {s.main_complaint}")
            print(f"  Histórico Familiar: {s.family_history}")
            print(f"  History Pessoal: {s.personal_history}")
            print(f"  Aspectos: {s.aspects}")
            print(f"  Observações: {s.observations}")
    else:
        print("\nNenhuma sessão com esse paciente.")


def update_patient():
    print("\n----- Gerenciador de Sessões -----")
    patients = session.query(Patient).all()
    for patient in patients:
        print(f"ID: {patient.id}, Nome: {patient.name}")
    try:
        selected_id = int(input("\nInsira o ID do paciente para adicionar a sessão: "))
    except ValueError:
        print("ID inválido.")
        return
    patient = session.query(Patient).filter_by(id=selected_id).first()
    if not patient:
        print("Paciente não encontrado.")
        return
    print("\n1.Adicionar sessão\n2.Sair\n")
    try:
        option = int(input("Selecione a opção desejada: "))
    except ValueError:
        option = 2
    if option == 1:
        create_session(patient.id)


def remove_patient():
    patients = session.query(Patient).all()
    for patient in patients:
        print(f"ID: {patient.id}, Nome: {patient.name}")
    try:
        selected_id = int(input("\nInsira o ID do paciente removido: "))
    except ValueError:
        print("ID inválido.")
        return
    patient = session.query(Patient).filter_by(id=selected_id).first()
    if not patient:
        print("Paciente não encontrado.")
        return
    session.query(SessionRecord).filter_by(patient_id=patient.id).delete()
    session.delete(patient)
    session.commit()
    print(f"Paciente ID: {selected_id} e suas sessões foram removidas.")

def invalid_option():
    print("Opção inválida, tente novamente.")