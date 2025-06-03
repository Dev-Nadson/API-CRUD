from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuração do banco de dados SQLite
engine = create_engine("sqlite:///Backend/PsyApp.db")
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
Base = declarative_base()


class Patient(Base):
    __tablename__ = "patients"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    age = Column("idade", Integer, nullable=False)
    civil_status = Column("status_civil", String, nullable=False)
    profession = Column("profissao", String, nullable=False)
    birthday = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    rg = Column(String, nullable=False, unique=True)
    address = Column("address", String, nullable=False)
    contact = Column(String, nullable=False)
    status = Column(Boolean, nullable=False)

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

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    date = Column(String, nullable=False)
    hour = Column(String, nullable=False)
    duration = Column(String, nullable=False)
    main_complaint = Column(String, nullable=False)
    family_history = Column(String, nullable=False)
    personal_history = Column(String, nullable=False)
    aspects = Column(String, nullable=False)
    observations = Column(String, nullable=True)

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

    # Pergunta se quer criar sessão imediatamente
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
    #Nadson Revise amanha
    print("\n----- Read Patients -----")
    patients = session.query(Patient).all()
    if not patients:
        print("No patients found.")
        return

    for p in patients:
        print(f"ID: {p.id}, Name: {p.name}")

    try:
        selected_id = int(input("\nEnter patient ID for details: "))
    except ValueError:
        print("ID inválido.")
        return

    patient = session.query(Patient).filter_by(id=selected_id).first()
    if not patient:
        print("Patient not found.")
        return

    print(f"\n--- Details for '{patient.name}' (ID: {patient.id}) ---")
    print(f"Age: {patient.age}")
    print(f"Civil Status: {patient.civil_status}")
    print(f"Profession: {patient.profession}")
    print(f"Birthday: {patient.birthday}")
    print(f"Gender: {patient.gender}")
    print(f"CPF: {patient.cpf}")
    print(f"RG: {patient.rg}")
    print(f"Address: {patient.address}")
    print(f"Contact: {patient.contact}")
    print(f"Active Status: {'Active' if patient.status else 'Inactive'}")

    sessions = session.query(SessionRecord).filter_by(patient_id=patient.id).all()
    if sessions:
        print("\n--- Sessions ---")
        for s in sessions:
            print(f"\n• Date: {s.date} | Hour: {s.hour} | Duration: {s.duration}")
            print(f"  Main Complaint: {s.main_complaint}")
            print(f"  Family History: {s.family_history}")
            print(f"  Personal History: {s.personal_history}")
            print(f"  Aspects: {s.aspects}")
            print(f"  Observations: {s.observations}")
    else:
        print("\nNo sessions found for this patient.")


def update_patient():
    """
    Permite adicionar uma nova sessão a um paciente existente.
    """
    print("\n----- Update Patient -----")
    patients = session.query(Patient).all()
    if not patients:
        print("No patients found.")
        return

    for p in patients:
        print(f"ID: {p.id}, Name: {p.name}")

    try:
        selected_id = int(input("\nEnter patient ID to update: "))
    except ValueError:
        print("ID inválido.")
        return

    patient = session.query(Patient).filter_by(id=selected_id).first()
    if not patient:
        print("Patient not found.")
        return

    print("\n1. Add new session")
    print("2. Back to main menu\n")
    try:
        option = int(input("Select an option: "))
    except ValueError:
        option = 2

    if option == 1:
        create_session(patient.id)
    else:
        print("Returning to main menu.")


def remove_patient():
    """
    Remove um paciente (e suas sessões associadas) com base no ID informado.
    """
    print("\n----- Remove Patient -----")
    patients = session.query(Patient).all()
    if not patients:
        print("No patients found.")
        return

    for p in patients:
        print(f"ID: {p.id}, Name: {p.name}")

    try:
        selected_id = int(input("\nEnter patient ID to remove: "))
    except ValueError:
        print("ID inválido.")
        return

    patient = session.query(Patient).filter_by(id=selected_id).first()
    if not patient:
        print("Patient not found.")
        return

    # Remove sessões associadas primeiro (opcional, se houver cascade definido)
    session.query(SessionRecord).filter_by(patient_id=patient.id).delete()
    session.delete(patient)
    session.commit()
    print(f"Patient ID {selected_id} and associated sessions have been removed.")


def invalid_option():
    print("Invalid option. Please try again.")