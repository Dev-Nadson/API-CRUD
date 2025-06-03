import os
from CRUD import *

def Option_INT(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Por favor, insira um número válido.")

def create_menu():
    while True:
        print("\n----- Criação de Pacientes -----")
        print("1. Criar paciente")
        print("2. Sair\n")

        option = Option_INT("Selecione uma opção: ")
        match option:
            case 1:
                create_patient()
            case _:
                break

def main():
    main_menu = {
        1: create_menu,
        2: read_patients,
        3: update_patient,
        4: remove_patient
    }
    while True:
        os.system('cls')
        print("----- Gerenciamento de Pacientes -----\n")
        print("1. Criar novo paciente")
        print("2. Ler o prontuário")
        print("3. Atualizar o prontuário")
        print("4. Excluir algum paciente")
        print("5. Sair\n")

        option = Option_INT("Selecione uma opção ")
        if option == 5:
            break
        main_menu.get(option, invalid_option)()

main()