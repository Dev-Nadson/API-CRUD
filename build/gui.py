from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Label

WIDTH = 862
HEIGHT = 519

ASSETS_PATH = Path(__file__).parent / "assets" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class PsicoDataApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#004F83")
        self.center_window(WIDTH, HEIGHT)
        self.root.resizable(False, False)
        self.canvas = Canvas(
            self.root,
            bg="#004F83",
            height=HEIGHT,
            width=WIDTH,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.email_entry = None
        self.password_entry = None
        self.message_label = None

        self.build_interface()

    def center_window(self, w, h):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - w) // 2
        y = (screen_height - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def build_interface(self):
        self.build_background()
        self.build_texts()
        self.build_entries()
        self.build_buttons()
        self.build_message_label()

    def build_background(self):
        self.canvas.create_rectangle(430, 0, 862, 519, fill="#E7F7F8", outline="")

    def build_texts(self):
        self.canvas.create_text(47, 134, anchor="nw", text="Bem vindo(a) ao PsicoData",
                                fill="#FCFCFC", font=("Roboto Bold", 20, "bold"))
        self.canvas.create_text(482, 74, anchor="nw", text="Entre no PsicoData",
                                fill="#004F83", font=("Roboto Bold", 20, "bold"))
        self.canvas.create_text(482, 127, anchor="nw", text="Email",
                                fill="#004F83", font=("Roboto Bold", 18, "bold"))
        self.canvas.create_text(482, 256, anchor="nw", text="Senha",
                                fill="#004F83", font=("Roboto Bold", 18, "bold"))

        mensagens = [
            "Mantenha o controle completo",
            "dos prontuários dos seus pacientes",
            "e garanta que as informações estejam",
            "sempre atualizadas para oferecer um",
            "diagnóstico mais preciso e um",
            "atendimento de qualidade!"
        ]
        for i, texto in enumerate(mensagens):
            self.canvas.create_text(47, 190 + i * 25, anchor="nw", text=texto,
                                    fill="#FCFCFC", font=("Roboto Regular", 16))

    def build_entries(self):
        # Email
        entry_img_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.canvas.create_image(650, 205.5, image=entry_img_1)
        self.email_entry = Entry(self.root, bd=0, bg="#D5EFF4", fg="#000716", highlightthickness=0, font=("Roboto", 12))
        self.email_entry.place(x=490, y=175, width=321, height=59)
        self.email_img = entry_img_1  # evita coleta de lixo

        # Senha
        entry_img_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        self.canvas.create_image(650, 334.5, image=entry_img_2)
        self.password_entry = Entry(self.root, bd=0, bg="#D5EFF4", fg="#000716", show="*", highlightthickness=0, font=("Roboto", 12))
        self.password_entry.place(x=490, y=304, width=321, height=59)
        self.password_img = entry_img_2

    def build_buttons(self):
        button_img = PhotoImage(file=relative_to_assets("button_1.png"))
        button = Button(
            image=button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.validate_login,
            relief="flat"
        )
        button.place(x=557, y=401, width=180, height=55)
        self.button_img = button_img

    def build_message_label(self):
        self.message_label = Label(self.root, text="", fg="red", bg="#E7F7F8", font=("Roboto", 12))
        self.message_label.place(x=490, y=370)

    def validate_login(self):
        email = self.email_entry.get().strip() 
        password = self.password_entry.get().strip()

        if not email or not password:
            self.show_message("Preencha todos os campos!")
        else:
            self.show_message("")
            print(f"Login bem-sucedido com o e-mail: {email}")
            # Aqui você pode adicionar verificação real de login ou mudar de tela

    def show_message(self, msg):
        self.message_label.config(text=msg)

if __name__ == "__main__":
    window = Tk()
    app = PsicoDataApp(window)
    window.mainloop()
