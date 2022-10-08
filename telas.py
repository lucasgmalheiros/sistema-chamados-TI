# coding=utf-8
from pathlib import Path
from tkinter import *
from funcoes_sql import *
import tkinter.messagebox
from relatorios_xlsx import gera_relatorios_xlsx
# ________________________________________________Funcionalidades______________________________________________________#

cargos_tecnico = ['Técnico de informática', 'Estagiário de TI']
cargos_solicitante = ['Discente', 'Docente', 'Técnico administrativo', 'Coordenador de informática']
usuarios = cargos_solicitante + cargos_tecnico
servicos = ListaServicos()
prioridades = ['Baixa', 'Média', 'Alta']
relatorios = ['Quantidade de ordens por serviço',
              'Quantidade de chamados em aberto por serviço',
              'Tempo médio por funcionário',
              'Tempo médio por cargo do solicitante',
              'Tempo médio de atendimento por tipo de serviço']

def login_usuario(email, senha, janela):
    """Solicita a checagem dos dados do usuário para autorizar o acesso ao software"""
    execute = True

    check = CheckLogin(email, senha)
    cargo = check[0]

    if cargo == 'Usuário não cadastrado':
        tkinter.messagebox.showinfo('Usuário não encontrado', 'Login ou senha incorretos!')
        execute = False
    elif cargo == 'Docente' or cargo == 'Discente' or cargo == 'Técnico administrativo':
        TelaInicialSolicitante(email, janela)
    elif cargo in cargos_tecnico:
        TelaInicialTecnico(email, janela)
    elif cargo == 'Coordenador de informática':
        TelaInicialCoordenador(email, janela)

    return execute


def cadastro_usuario(email, senha, nome, cargo, janela):
    """Chama as funções que cadastram o usuário no servidor"""
    execute = True

    if cargo in cargos_tecnico and ('@' in email):
        InsertTecnico(email, senha, nome, cargo)
        tkinter.messagebox.showinfo('Concluído', 'Usuário cadastrado com sucesso!')
    elif cargo in cargos_solicitante and ('@' in email):
        InsertSolicitante(email, senha, nome, cargo)
        tkinter.messagebox.showinfo('Concluído', 'Usuário cadastrado com sucesso!')
    else:
        execute = False
        tkinter.messagebox.showinfo('Erro', 'Não foi possível cadastrar o usuário')
    TelaLogin(janela)

    return execute


def solicitar_servico(email, categoria, comentario, prioridade, local):
    """Envia informações da solicitação do usuários para inserção no servidor"""
    execute = True

    urgencia = 0
    if prioridade == 'Baixa':
        urgencia = 1
    elif prioridade == 'Média':
        urgencia = 2
    elif prioridade == 'Alta':
        urgencia = 3

    if InsertOrdem(email, categoria, comentario, urgencia, local):
        tkinter.messagebox.showinfo('Concluído', 'Solicitação enviada com sucesso!')
    else:
        tkinter.messagebox.showinfo('Erro', 'Solicitação de serviço não pôde ser enviada')
    return execute


def avaliar_servico(id_servico, feedback, nota):
    """Envia a avaliação do serviço para o servidor"""
    execute = True
    UpdateFeedbackSolicitante(id_servico, feedback, nota)
    tkinter.messagebox.showinfo('Concluído', 'Feedback enviado com sucesso!')
    return execute


def atualizar_ordem(descricao, prioridade, local, id_ordem):
    """Atualiza alguns dados da ordem de acordo com informações fornecidas pelos técnicos"""
    execute = True
    urgencia = 0
    if prioridade == 'Baixa':
        urgencia = 1
    elif prioridade == 'Média':
        urgencia = 2
    else:
        urgencia = 3
    UpdateOrdemTecnico(descricao, urgencia, local, id_ordem)
    tkinter.messagebox.showinfo('Concluído', 'Ordem atualizada com sucesso!')
    return execute


def atender_ordem(email_tecnico, id_ordem):
    """Atualiza o status da ordem quando ela for marcada como atendida pelo técnico responsável"""
    execute = True
    descricao = SelectDescricaoChamadoTecnico(id_ordem)
    status = descricao[6]
    if UpdateAtendeChamadoTecnico(id_ordem, status, email_tecnico):
        tkinter.messagebox.showinfo('Concluído', 'Ordem atualizada com sucesso!')
    else:
        tkinter.messagebox.showinfo('Erro', 'Não foi possível atualizar ordem')
    return execute


def exibe_relatorio(relatorio, campo):
    """Chama todas as funções que exibem relatórios gerenciais aos coordenadores de informática
    e formata a apresentação de informações na tela"""
    execute = True
    n_relatorio = 0
    # 1 - Quantidade total de ordens por serviço
    if relatorio == 'Quantidade de ordens por serviço':
        n_relatorio = 1
        r = Relatorio(n_relatorio)
        r.reverse()
        for s in r:
            servico = s[0]
            qtd = s[1]
            campo.insert('0.0', f'\n {25 * " "} {servico} {(50-len(servico)) * " "} {qtd} \n')
        campo.insert('0.0', f'\n {30 * " "} Serviço {33 * " "} Chamados \n\n')
    # 2 - Tempo médio por funcionário
    elif relatorio == 'Tempo médio por funcionário':
        n_relatorio = 2
        r = Relatorio(n_relatorio)
        r.reverse()
        for s in r:
            tecnico = s[0]
            tempo_medio = s[1]
            campo.insert('0.0', f'\n {30 * " "} {tecnico} {(35-len(tecnico)) * " "} {tempo_medio} minutos \n')
        campo.insert('0.0', f'\n {30 * " "} Técnico {30 * " "} Tempo médio \n\n')
    # 3 - Quantidade de chamados por serviço
    elif relatorio == 'Quantidade de chamados em aberto por serviço':
        n_relatorio = 3
        r = Relatorio(n_relatorio)
        r.reverse()
        for s in r:
            servico = s[0]
            qtd = s[1]
            campo.insert('0.0', f'\n {25 * " "} {servico} {(50-len(servico)) * " "} {qtd}\n')
        campo.insert('0.0', f'\n {30 * " "} Serviço {30 * " "} Chamados em aberto \n\n')
    # 4 - Tempo médio por cargo do solicitante
    elif relatorio == 'Tempo médio por cargo do solicitante':
        n_relatorio = 4
        r = Relatorio(n_relatorio)
        r.reverse()
        for s in r:
            cargo = s[0]
            tempo = s[1]
            campo.insert('0.0', f'\n {30 * " "} {cargo} {(35-len(cargo)) * " "} {tempo} minutos\n')
        campo.insert('0.0', f'\n {30 * " "} Cargo {30 * " "} Tempo médio \n\n')
    # 5 - Tempo médio de atendimento por tipo de serviço
    elif relatorio == 'Tempo médio de atendimento por tipo de serviço':
        n_relatorio = 5
        r = Relatorio(n_relatorio)
        for s in r:
            servico = s[0]
            tempo = s[1]
            campo.insert('0.0', f'\n {25 * " "} {servico} {(40-len(servico)) * " "} {tempo} minutos\n')
        campo.insert('0.0', f'\n {30 * " "} Serviço {30 * " "} Tempo médio \n\n')

    return execute

# _______________________________________________________Telas_________________________________________________________#

# ----------------------- Geral --------------------------#
def TelaLogin(janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\login")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.title('Login')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#346633")

    canvas = Canvas(
        window,
        bg="#346633",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        512.0,
        93.0,
        image=image_image_1
    )

    canvas.create_text(
        186.0,
        263.0,
        anchor="nw",
        text="SISTEMA DE SOLICITAÇÕES DE SERVIÇOS EM TI",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        512.0,
        530.7239990234375,
        image=entry_image_1
    )
    # Senha
    campo_senha = Entry(
        bd=0,
        bg="#0C380B",
        highlightthickness=0,
        fg='white'
    )
    campo_senha.place(
        x=255.0,
        y=504.0,
        width=514.0,
        height=51.447998046875
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        512.0,
        433.7239990234375,
        image=entry_image_2
    )
    # Login
    campo_email = Entry(
        bd=0,
        bg="#0C380B",
        highlightthickness=0,
        fg='white'
    )
    campo_email.place(
        x=255.0,
        y=407.0,
        width=514.0,
        height=51.447998046875
    )

    canvas.create_text(
        245.0,
        471.0,
        anchor="nw",
        text="Senha",
        fill="#FFFFFF",
        font=("OpenSansRoman Regular", 24 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    # Entrar
    botao_entrar = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: login_usuario(campo_email.get(), campo_senha.get(), window),
        relief="flat"
    )
    botao_entrar.place(
        x=463.0,
        y=591.0,
        width=98.0,
        height=50.0
    )

    canvas.create_text(
        245.0,
        374.0,
        anchor="nw",
        text="Usuário",
        fill="#FFFFFF",
        font=("OpenSansRoman Regular", 24 * -1)
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    # Cadastro
    botao_registrar = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaCadastro(window),
        relief="flat"
    )
    botao_registrar.place(
        x=438.0,
        y=702.0,
        width=147.0,
        height=50.0
    )
    window.resizable(False, False)
    window.mainloop()


def TelaCadastro(janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\cadastro")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.title('Cadastro')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#346633")

    canvas = Canvas(
        window,
        bg="#346633",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)

    cargo_clicado = StringVar()
    campo_cargo = OptionMenu(
        window, cargo_clicado, *usuarios
    )
    campo_cargo.config(bg="#0C380B", fg='white')
    campo_cargo.place(
        x=255.0,
        y=575.0,
        width=514.0,
        height=51.447998046875
    )

    canvas.create_text(
        245.0,
        538.0,
        anchor="nw",
        text="Cargo",
        fill="#FFFFFF",
        font=("OpenSansRoman Regular", 24 * -1)
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        512.0,
        511.7239990234375,
        image=entry_image_2
    )
    campo_senha = Entry(
        bd=0,
        bg="#0C380B",
        highlightthickness=0,
        fg='white'
    )
    campo_senha.place(
        x=255.0,
        y=485.0,
        width=514.0,
        height=51.447998046875
    )

    canvas.create_text(
        245.0,
        452.0,
        anchor="nw",
        text="Cadastre sua senha",
        fill="#FFFFFF",
        font=("OpenSansRoman Regular", 24 * -1)
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        512.0,
        421.7239990234375,
        image=entry_image_3
    )
    campo_email = Entry(
        bd=0,
        bg="#0C380B",
        highlightthickness=0,
        fg='white'
    )
    campo_email.place(
        x=255.0,
        y=395.0,
        width=514.0,
        height=51.447998046875
    )

    canvas.create_text(
        245.0,
        362.0,
        anchor="nw",
        text="Cadastre seu e-mail",
        fill="#FFFFFF",
        font=("OpenSansRoman Regular", 24 * -1)
    )

    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
        512.0,
        331.72400093078613,
        image=entry_image_4
    )
    campo_nome = Entry(
        bd=0,
        bg="#0C380B",
        highlightthickness=0,
        fg='white'
    )
    campo_nome.place(
        x=255.0,
        y=305.0,
        width=514.0,
        height=51.448001861572266
    )

    canvas.create_text(
        245.0,
        272.0,
        anchor="nw",
        text="Cadastre seu nome",
        fill="#FFFFFF",
        font=("OpenSansRoman Regular", 24 * -1)
    )

    canvas.create_text(
        438.0,
        202.0,
        anchor="nw",
        text="CADASTRO",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        512.0,
        93.0,
        image=image_image_1
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    botao_enviar = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: cadastro_usuario(campo_email.get(), campo_senha.get(),
                                         campo_nome.get(), cargo_clicado.get(), window),
        relief="flat"
    )
    botao_enviar.place(
        x=434.0,
        y=698.0,
        width=151.0,
        height=54.0
    )

    window.resizable(False, False)
    window.mainloop()


# ----------------------- Solicitante --------------------------#
def TelaInicialSolicitante(email, janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\inicial_solicitante")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.title('Solicitante')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#AFC6AF")

    canvas = Canvas(
        window,
        bg="#AFC6AF",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    botao_acompanhar = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaAcompanharServicoSolicitante(email, window),
        relief="flat"
    )
    botao_acompanhar.place(
        x=233.0,
        y=343.0,
        width=561.0,
        height=82.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    botao_historico = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaHistoricoServicoSolicitante(email, window),
        relief="flat"
    )
    botao_historico.place(
        x=233.0,
        y=487.0,
        width=560.0,
        height=82.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    botao_solicitar = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaSolicitarServicoSolicitante(email, window),
        relief="flat"
    )
    botao_solicitar.place(
        x=231.0,
        y=199.0,
        width=562.0,
        height=82.0
    )

    canvas.create_text(
        181.0,
        31.0,
        anchor="nw",
        text="SISTEMA DE SOLICITAÇÕES DE SERVIÇOS EM TI",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_text(
        34.0,
        720.0,
        anchor="nw",
        text="Usuário: ",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        125,
        720.0,
        anchor="nw",
        text=email,
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    window.resizable(False, False)
    window.mainloop()


def TelaSolicitarServicoSolicitante(email, janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\solicitar_servico")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.title('Solicitante')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#AFC6AF")

    canvas = Canvas(
        window,
        bg="#AFC6AF",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        181.0,
        31.0,
        anchor="nw",
        text="SISTEMA DE SOLICITAÇÕES DE SERVIÇOS EM TI",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_text(
        399.0,
        127.0,
        anchor="nw",
        text="Solicitar serviço",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    botao_retorna = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaInicialSolicitante(email, window),
        relief="flat"
    )
    botao_retorna.place(
        x=25.0,
        y=21.0,
        width=84.0,
        height=82.0
    )

    categoria_selecionada = StringVar()
    campo_categoria = OptionMenu(
        window, categoria_selecionada, *servicos
    )
    campo_categoria.config(bg="#0C380B", fg='white')
    campo_categoria.place(
        x=255.0,
        y=224.0,
        width=514.0,
        height=51.447998046875
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        514.0,
        340.7239990234375,
        image=entry_image_2
    )
    campo_comentario = Entry(
        bd=0,
        bg="#0C380B",
        highlightthickness=0,
        fg='white'
    )
    campo_comentario.place(
        x=257.0,
        y=314.0,
        width=514.0,
        height=51.447998046875
    )

    prioridade_selecionada = StringVar()
    prioridade_selecionada.set(prioridades[0])
    campo_prioridade = OptionMenu(
        window, prioridade_selecionada, *prioridades
    )
    campo_prioridade.config(bg="#0C380B", fg='white')
    campo_prioridade.place(
        x=257.0,
        y=404.0,
        width=514.0,
        height=51.447998046875
    )

    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
        514.0,
        519.7239990234375,
        image=entry_image_4
    )
    campo_local = Entry(
        bd=0,
        bg="#0C380B",
        highlightthickness=0,
        fg='white'
    )
    campo_local.place(
        x=257.0,
        y=493.0,
        width=514.0,
        height=51.447998046875
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    botao_enviar = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: solicitar_servico(email, categoria_selecionada.get(), campo_comentario.get(),
                                          prioridade_selecionada.get(), campo_local.get()),
        relief="flat"
    )
    botao_enviar.place(
        x=438.0,
        y=703.0,
        width=147.0,
        height=50.0
    )

    canvas.create_text(
        245.0,
        281.0,
        anchor="nw",
        text="Comentário",
        fill="#000000",
        font=("OpenSansRoman Regular", 24 * -1)
    )

    canvas.create_text(
        245.0,
        191.0,
        anchor="nw",
        text="Selecionar categoria",
        fill="#000000",
        font=("OpenSansRoman Regular", 24 * -1)
    )

    canvas.create_text(
        247.0,
        374.0,
        anchor="nw",
        text="Prioridade",
        fill="#000000",
        font=("OpenSansRoman Regular", 24 * -1)
    )

    canvas.create_text(
        247.0,
        464.0,
        anchor="nw",
        text="Local",
        fill="#000000",
        font=("OpenSansRoman Regular", 24 * -1)
    )

    canvas.create_text(
        25.0,
        724.0,
        anchor="nw",
        text="Usuário: ",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        125.0,
        724.0,
        anchor="nw",
        text=email,
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    window.resizable(False, False)
    window.mainloop()


def TelaAcompanharServicoSolicitante(email, janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\acompanhar_solicitante")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.title('Solicitante')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#AFC6AF")

    canvas = Canvas(
        window,
        bg="#AFC6AF",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        181.0,
        31.0,
        anchor="nw",
        text="SISTEMA DE SOLICITAÇÕES DE SERVIÇOS EM TI",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    botao_volta = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaInicialSolicitante(email, window),
        relief="flat"
    )
    botao_volta.place(
        x=24.0,
        y=22.0,
        width=84.0,
        height=82.0
    )

    canvas.create_text(
        326.0,
        143.0,
        anchor="nw",
        text="Acompanhar solicitações",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_rectangle(
        168.0,
        195.0,
        858.0,
        235.0,
        fill="#D9D9D9",
        outline="")

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        513.5,
        427.0,
        image=entry_image_1
    )
    caixa_texto = Text(
        bd=0,
        bg="#527C4F",
        highlightthickness=0,
        fg='white'
    )
    fila = SelectChamadoEmFilaSolicitante(email)
    fila.reverse()
    for ordem in fila:
        nome = ordem[0]
        status = ordem[1]
        tempo_medio = ordem[2]
        posicao_fila = ordem[4]
        id_ordem = ordem[3]
        descricao = f'(id:{id_ordem}) {nome}'
        caixa_texto.insert('0.0', descricao + f'{(35 - len(descricao)) * " "}' +
                           f'{status}' + f'{(20 - len(status)) * " "}' +
                           f'{posicao_fila}' + f'{(10 * " ")}' + f'{tempo_medio} minutos' + '\n')

    caixa_texto.config(state='disabled')

    caixa_texto.place(
        x=168.0,
        y=256.0,
        width=691.0,
        height=340.0
    )

    canvas.create_text(
        220.0,
        195.0,
        anchor="nw",
        text="Descrição",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        440.0,
        195.0,
        anchor="nw",
        text="Status",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        560.0,
        195.0,
        anchor="nw",
        text="Posição",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        688.0,
        195.0,
        anchor="nw",
        text="Tempo médio",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        34.0,
        720.0,
        anchor="nw",
        text="Usuário: ",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        125,
        720.0,
        anchor="nw",
        text=email,
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    window.resizable(False, False)
    window.mainloop()


def TelaHistoricoServicoSolicitante(email, janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\acompanhar_solicitante")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.title('Solicitante')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#AFC6AF")

    canvas = Canvas(
        window,
        bg="#AFC6AF",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        181.0,
        31.0,
        anchor="nw",
        text="SISTEMA DE SOLICITAÇÕES DE SERVIÇOS EM TI",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    botao_volta = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaInicialSolicitante(email, window),
        relief="flat"
    )
    botao_volta.place(
        x=24.0,
        y=22.0,
        width=84.0,
        height=82.0
    )

    canvas.create_text(
        360.0,
        143.0,
        anchor="nw",
        text="Histórico de serviços",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_rectangle(
        168.0,
        195.0,
        858.0,
        235.0,
        fill="#D9D9D9",
        outline="")

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        513.5,
        427.0,
        image=entry_image_1
    )
    caixa_texto = Text(
        bd=0,
        bg="#527C4F",
        highlightthickness=0,
        fg='white'
    )
    concluida = SelectChamadoConcluidoSolicitante(email)
    for ordem in concluida:
        nome = ordem[0]
        data = ordem[1]
        responsavel = ordem[2]
        tempo = ordem[3]
        id_ordem = ordem[4]
        descricao = f'(id:{id_ordem}) {nome}'
        caixa_texto.insert('0.0', f'{descricao}' + f'{(35 - len(descricao)) * " "}' + f'{data}' +
                           f'{8 * " " + responsavel}' + f'{(18 - len(responsavel)) * " "}' +
                           f'{tempo} min.' + '\n')

    caixa_texto.config(state='disabled')

    caixa_texto.place(
        x=168.0,
        y=256.0,
        width=691.0,
        height=340.0
    )

    canvas.create_text(
        230.0,
        195.0,
        anchor="nw",
        text="Descrição",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        420.0,
        195.0,
        anchor="nw",
        text="Data atend.",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        570.0,
        195.0,
        anchor="nw",
        text="Téc. Resp.",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        700.0,
        195.0,
        anchor="nw",
        text="Tempo exec.",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        34.0,
        720.0,
        anchor="nw",
        text="Usuário: ",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        125,
        720.0,
        anchor="nw",
        text=email,
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_feedback.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaFeedbackSolicitante(email, window),
        relief="flat"
    )
    button_3.place(
        x=430.0,
        y=629.0,
        width=162.0,
        height=55.0)

    window.resizable(False, False)
    window.mainloop()


def TelaFeedbackSolicitante(email, janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\feedback_solicitante")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.title('Solicitante')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#AFC6AF")

    canvas = Canvas(
        window,
        bg="#AFC6AF",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        181.0,
        31.0,
        anchor="nw",
        text="SISTEMA DE SOLICITAÇÕES DE SERVIÇOS EM TI",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaHistoricoServicoSolicitante(email, window),
        relief="flat"
    )
    button_1.place(
        x=26.0,
        y=22.0,
        width=83.0,
        height=81.0
    )
    # Drop down menu serviços
    opcoes = []
    concluidos = SelectChamadoConcluidoSolicitante(email)
    for c in concluidos:
        id_ordem = c[4]
        opcoes.append(id_ordem)
    opcoes.reverse()
    id_selecionado = StringVar()
    campo_chamado = OptionMenu(window, id_selecionado, *opcoes)
    campo_chamado.config(bg="#0C380B", fg='white')
    campo_chamado.place(
        x=69.0,
        y=191.0,
        width=514.0,
        height=51.447998046875
    )

    notas = [i for i in range(0, 11)]
    nota_selecionada = StringVar()
    campo_nota = OptionMenu(window, nota_selecionada, *notas)
    campo_nota.config(bg="#0C380B", fg='white')
    campo_nota.place(
        x=69.0,
        y=287.0,
        width=327.286865234375,
        height=51.447998046875
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        511.0,
        513.5,
        image=entry_image_3
    )
    entry_3 = Text(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    entry_3.place(
        x=59.0,
        y=389.0,
        width=904.0,
        height=247.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: avaliar_servico(id_selecionado.get(), entry_3.get('1.0', END), nota_selecionada.get()),
        relief="flat"
    )
    button_2.place(
        x=417.0,
        y=650.0,
        width=153.0,
        height=60.0
    )

    canvas.create_text(
        34.0,
        720.0,
        anchor="nw",
        text="Usuário:",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )
    canvas.create_text(
        125,
        720.0,
        anchor="nw",
        text=email,
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        443.0,
        103.0,
        anchor="nw",
        text="Feedback",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_text(
        60.0,
        156.0,
        anchor="nw",
        text="Serviço (id)",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        59.0,
        249.0,
        anchor="nw",
        text="Dê uma nota ao atendimento",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        60.0,
        358.0,
        anchor="nw",
        text="Insira seu comentário",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )
    window.resizable(False, False)
    window.mainloop()


# ----------------------- Técnico de informática --------------------------#
def TelaInicialTecnico(email, janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\inicial_tecnico")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.title('Técnico')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#AFC6AF")

    canvas = Canvas(
        window,
        bg="#AFC6AF",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaAcompanharServicosTecnico(email, window),
        relief="flat"
    )
    button_1.place(
        x=231.0,
        y=126.0,
        width=559.0,
        height=82.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaAtualizarChamadoTecnico(email, window),
        relief="flat"
    )
    button_2.place(
        x=233.0,
        y=247.0,
        width=559.0,
        height=82.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaAtenderChamadoTecnico(email, window),
        relief="flat"
    )
    button_3.place(
        x=231.0,
        y=362.0,
        width=559.0,
        height=82.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaHistoricoServicoTecnico(email, window),
        relief="flat"
    )
    button_4.place(
        x=234.0,
        y=483.0,
        width=559.0,
        height=82.0
    )

    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaPreencherChamadoTecnico(email, window),
        relief="flat"
    )
    button_5.place(
        x=231.0,
        y=602.0,
        width=559.0,
        height=82.0
    )

    canvas.create_text(
        181.0,
        31.0,
        anchor="nw",
        text="SISTEMA DE SOLICITAÇÕES DE SERVIÇOS EM TI",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_text(
        34.0,
        720.0,
        anchor="nw",
        text="Usuário:",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        125,
        720.0,
        anchor="nw",
        text=email,
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    window.resizable(False, False)
    window.mainloop()


def TelaAcompanharServicosTecnico(email, janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\acompanhar_tecnico")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.title('Técnico')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#AFC6AF")

    canvas = Canvas(
        window,
        bg="#AFC6AF",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaInicialTecnico(email, window),
        relief="flat"
    )
    button_1.place(
        x=26.0,
        y=22.0,
        width=83.0,
        height=81.0
    )

    canvas.create_rectangle(
        35.0,
        208.0,
        1002.0,
        248.0,
        fill="#D9D9D9",
        outline="")

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        519.0,
        440.0,
        image=entry_image_1
    )
    caixa_texto = Text(
        bd=0,
        bg="#527C4F",
        highlightthickness=0,
        fg='white'
    )
    fila = SelectChamadosEmFilaTecnico()
    fila.reverse()
    for ordem in fila:
        nome = ordem[0]
        status = ordem[1]
        prioridade = ordem[2]
        posicao_fila = ordem[-1]
        t_medio = ordem[3]
        id_ordem = ordem[4]
        descricao = f'(id:{id_ordem}) {nome}'
        caixa_texto.insert('0.0', f'{descricao}' + f'{(40 - len(descricao)) * " "}' +
                           f'{status}' + f'{(28 - len(status)) * " "}' +
                           f'{prioridade}' + f'{((20 - len(prioridade)) * " ")}' + f'{posicao_fila}' + f'{15 * " "}'
                           + f'{t_medio} minutos' + '\n')

    caixa_texto.config(state='disabled')

    caixa_texto.place(
        x=35.0,
        y=269.0,
        width=968.0,
        height=340.0
    )

    canvas.create_text(
        550.0,
        208.0,
        anchor="nw",
        text="Prioridade",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        181.0,
        31.0,
        anchor="nw",
        text="SISTEMA DE SOLICITAÇÕES DE SERVIÇOS EM TI",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_text(
        34.0,
        720.0,
        anchor="nw",
        text="Usuário: ",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        125,
        720.0,
        anchor="nw",
        text=email,
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        280.0,
        139.0,
        anchor="nw",
        text="Acompanhar solicitações em aberto",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_text(
        120.0,
        208.0,
        anchor="nw",
        text="Descrição",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        360.0,
        208.0,
        anchor="nw",
        text="Status                       ",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        700.0,
        208.0,
        anchor="nw",
        text="Posição",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        810.0,
        208.0,
        anchor="nw",
        text="Tempo médio ",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )
    window.resizable(False, False)
    window.mainloop()


def TelaAtualizarChamadoTecnico(email, janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\atualizar_chamado_tecnico")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def update_campos(value):
        dados = SelectDescricaoChamadoTecnico(value)
        # Preenche textbox
        entry_5.config(state='normal')
        entry_5.delete('1.0', END)
        servico = dados[3]
        solicitante = dados[4]
        cargo = dados[5]
        entry_5.insert('0.0', f'\n Categoria do serviço: {servico} 'f'\n Nome do solicitante: '
                              f'{solicitante} \n Cargo: {cargo}')
        entry_5.config(state='disabled')
        # Preenche text areas
        descricao = dados[0]
        prioridade = dados[1]
        local = dados[2]
        campo_descricao.delete(0, END)
        campo_descricao.insert(INSERT, descricao)
        prioridade_selecionada.set(prioridade)
        campo_local.delete(0, END)
        campo_local.insert(INSERT, local)

    window = Tk()
    window.title('Técnico')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#AFC6AF")

    canvas = Canvas(
        window,
        bg="#AFC6AF",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    botao_retorna = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaInicialTecnico(email, window),
        relief="flat"
    )

    botao_retorna.place(
        x=26.0,
        y=22.0,
        width=83.0,
        height=81.0
    )

    opcoes = []
    for chamado in SelectChamadosEmFilaTecnico():
        id_chamado = chamado[4]
        opcoes.append(id_chamado)
    chamado_selecionado = StringVar()
    campo_chamado = OptionMenu(window, chamado_selecionado, *opcoes,
                               command=update_campos)
    campo_chamado.config(bg="#0C380B", fg='white')
    campo_chamado.place(
        x=255.0,
        y=224.0,
        width=514.0,
        height=51.447998046875
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        514.0,
        340.7239990234375,
        image=entry_image_2
    )
    campo_descricao = Entry(
        bd=0,
        bg="#0C380B",
        highlightthickness=0,
        fg='white'
    )
    campo_descricao.place(
        x=257.0,
        y=314.0,
        width=514.0,
        height=51.447998046875
    )

    prioridade_selecionada = StringVar()
    campo_prioridade = OptionMenu(window, prioridade_selecionada, *prioridades)
    campo_prioridade.config(bg="#0C380B", fg='white')
    campo_prioridade.place(
        x=257.0,
        y=404.0,
        width=514.0,
        height=51.447998046875
    )

    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
        514.0,
        520.7239990234375,
        image=entry_image_4
    )
    campo_local = Entry(
        bd=0,
        bg="#0C380B",
        highlightthickness=0,
        fg='white'
    )
    campo_local.place(
        x=257.0,
        y=494.0,
        width=514.0,
        height=51.447998046875
    )

    entry_image_5 = PhotoImage(
        file=relative_to_assets("entry_5.png"))
    entry_bg_5 = canvas.create_image(
        512.5,
        632.5,
        image=entry_image_5
    )
    entry_5 = Text(
        bd=0,
        bg="#0C380B",
        highlightthickness=0,
        fg='white'
    )

    entry_5.place(
        x=255.0,
        y=591.0,
        width=515.0,
        height=81.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    botao_enviar = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: atualizar_ordem(campo_descricao.get(), prioridade_selecionada.get(),
                                        campo_local.get(), chamado_selecionado.get()),
        relief="flat"
    )
    botao_enviar.place(
        x=433.0,
        y=697.0,
        width=152.0,
        height=58.0
    )

    canvas.create_text(
        181.0,
        31.0,
        anchor="nw",
        text="SISTEMA DE SOLICITAÇÕES DE SERVIÇOS EM TI",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_text(
        300.0,
        127.0,
        anchor="nw",
        text="Consultar / Atualizar chamado",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_text(
        243.0,
        191.0,
        anchor="nw",
        text="Selecionar chamado (id)",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        246.0,
        281.0,
        anchor="nw",
        text="Descrição do problema",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        244.0,
        374.0,
        anchor="nw",
        text="Prioridade",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        247.0,
        461.0,
        anchor="nw",
        text="Local",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        34.0,
        720.0,
        anchor="nw",
        text="Usuário: ",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        125,
        720.0,
        anchor="nw",
        text=email,
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )
    canvas.create_text(
        245.0,
        558.0,
        anchor="nw",
        text="Informações",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )
    window.resizable(False, False)
    window.mainloop()


def TelaAtenderChamadoTecnico(email, janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\atender_chamado_tecnico")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def update_campos(value):
        dados = SelectDescricaoChamadoTecnico(value)
        servico = dados[3]
        solicitante = dados[4]
        cargo = dados[5]
        local = dados[2]
        prioridade = dados[1]
        descricao = dados[0]
        status = dados[6]
        # Preenche feedback
        campo_info.config(state='normal')
        campo_info.delete('1.0', END)
        campo_info.insert('0.0', f'\n Serviço: {servico} \n'
                                 f'\n Status: {status} \n'
                                 f'\n Solicitante: {solicitante} \n'
                                 f'\n Cargo: {cargo} \n'
                                 f'\n Descrição: {descricao} \n'
                                 f'\n Local: {local} \n'
                                 f'\n Prioridade: {prioridade} \n')
        campo_info.config(state='disabled')

    window = Tk()
    window.title('Técnico')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#AFC6AF")

    canvas = Canvas(
        window,
        bg="#AFC6AF",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaInicialTecnico(email, window),
        relief="flat"
    )
    button_1.place(
        x=26.0,
        y=16.0,
        width=83.0,
        height=87.0
    )

    opcoes = []
    fila = SelectChamadosEmFilaTecnico()
    for chamado in fila:
        id_chamado = chamado[4]
        opcoes.append(id_chamado)
    chamado_selecionado = StringVar()
    campo_chamado = OptionMenu(window, chamado_selecionado, *opcoes, command=update_campos)
    campo_chamado.config(bg="#0C380B", fg='white')
    campo_chamado.place(
        x=255.0,
        y=224.0,
        width=514.0,
        height=51.447998046875
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        512.0,
        498.5,
        image=entry_image_2
    )
    campo_info = Text(
        bd=0,
        bg="#D9D9D9",
        highlightthickness=0
    )
    campo_info.place(
        x=245.0,
        y=359.0,
        width=534.0,
        height=277.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: atender_ordem(email, chamado_selecionado.get()),
        relief="flat"
    )
    button_2.place(
        x=438.0,
        y=690.0,
        width=147.0,
        height=56.0
    )

    canvas.create_text(
        181.0,
        31.0,
        anchor="nw",
        text="SISTEMA DE SOLICITAÇÕES DE SERVIÇOS EM TI",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_text(
        317.0,
        127.0,
        anchor="nw",
        text="Atender/finalizar chamado",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_text(
        238.0,
        191.0,
        anchor="nw",
        text="Selecionar chamado (id)",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        245.0,
        326.0,
        anchor="nw",
        text="Informações do chamado",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        34.0,
        720.0,
        anchor="nw",
        text="Usuário: ",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        125,
        720.0,
        anchor="nw",
        text=email,
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )
    window.resizable(False, False)
    window.mainloop()


def TelaHistoricoServicoTecnico(email, janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\acompanhar_solicitante")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.title('Técnico')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#AFC6AF")

    canvas = Canvas(
        window,
        bg="#AFC6AF",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        181.0,
        31.0,
        anchor="nw",
        text="SISTEMA DE SOLICITAÇÕES DE SERVIÇOS EM TI",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    botao_volta = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaInicialTecnico(email, window),
        relief="flat"
    )
    botao_volta.place(
        x=24.0,
        y=22.0,
        width=84.0,
        height=82.0
    )

    canvas.create_text(
        360.0,
        143.0,
        anchor="nw",
        text="Histórico de serviços",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_rectangle(
        168.0,
        195.0,
        858.0,
        235.0,
        fill="#D9D9D9",
        outline="")

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        513.5,
        427.0,
        image=entry_image_1
    )
    caixa_texto = Text(
        bd=0,
        bg="#527C4F",
        highlightthickness=0,
        fg='white'
    )
    concluida = SelectChamadoConcluidoTecnico()
    for ordem in concluida:
        nome = ordem[0]
        data = ordem[1]
        responsavel = ordem[2]
        tempo = ordem[3]
        id_ordem = ordem[4]
        descricao = f'(id:{id_ordem}) {nome}'
        caixa_texto.insert('0.0', f'{descricao}' + f'{(38 - len(descricao)) * " "}' + f'{data}' +
                           f'{8 * " " + responsavel}' + f'{(18 - len(responsavel)) * " "}' +
                           f'{tempo} min.' + '\n')

    caixa_texto.config(state='disabled')

    caixa_texto.place(
        x=168.0,
        y=256.0,
        width=691.0,
        height=340.0
    )

    canvas.create_text(
        230.0,
        195.0,
        anchor="nw",
        text="Descrição",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        440.0,
        195.0,
        anchor="nw",
        text="Data atend.",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        580.0,
        195.0,
        anchor="nw",
        text="Téc. Resp.",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        710.0,
        195.0,
        anchor="nw",
        text="Tempo exec.",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        34.0,
        720.0,
        anchor="nw",
        text="Usuário: ",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        125,
        720.0,
        anchor="nw",
        text=email,
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_feedback.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaFeedbackTecnico(email, window),
        relief="flat"
    )
    button_3.place(
        x=430.0,
        y=629.0,
        width=162.0,
        height=55.0)

    window.resizable(False, False)
    window.mainloop()


def TelaFeedbackTecnico(email, janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\feedback_tecnico")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def update_campos(value):
        dados = SelectChamadosFeedbackTecnico(value)
        descricao = dados[0]
        local = dados[1]
        servico = dados[2]
        solicitante = dados[3]
        cargo = dados[4]
        data = dados[5]
        tecnico = dados[6]
        nota = dados[7]
        feedback = dados[8]
        # Preenche nota
        campo_nota.config(state='normal')
        campo_nota.delete(0, END)
        campo_nota.insert(INSERT, f'                {nota}')
        campo_nota.config(state='disabled')
        # Preenche feedback
        campo_feedback.config(state='normal')
        campo_feedback.delete('1.0', END)
        campo_feedback.insert('0.0', f'{feedback}')
        campo_feedback.config(state='disabled')
        # Preenche informações de atendimento
        campo_dados.config(state='normal')
        campo_dados.delete('1.0', END)
        campo_dados.insert('0.0', f'Solicitante: {solicitante} \n\n'
                                  f'Cargo: {cargo} \n\n'
                                  f'Serviço: {servico} \n\n'
                                  f'Descrição: {descricao} \n\n'
                                  f'Local: {local} \n\n'
                                  f'Técnico: {tecnico} \n\n'
                                  f'Data do atendimento (fim): {data}')
        campo_dados.config(state='disabled')

    window = Tk()
    window.title('Técnico')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#AFC6AF")

    canvas = Canvas(
        window,
        bg="#AFC6AF",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaHistoricoServicoTecnico(email, window),
        relief="flat"
    )
    button_1.place(
        x=26.0,
        y=15.0,
        width=83.0,
        height=88.0
    )

    opcoes = []
    chamados = SelectChamadoConcluidoTecnico()
    chamados.reverse()
    for chamado in chamados:
        id_chamado = chamado[4]
        opcoes.append(id_chamado)
    chamado_selecionado = StringVar()
    campo_chamado = OptionMenu(window, chamado_selecionado, *opcoes, command=update_campos)
    campo_chamado.config(bg="#0C380B", fg='white')
    campo_chamado.place(
        x=451.0,
        y=195.0,
        width=121.0,
        height=51.0
    )

    campo_nota = Entry(
        bd=0,
        bg="white",
        highlightthickness=0
    )
    campo_nota.place(
        x=451.0,
        y=281.0,
        width=121.0,
        height=51.0
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        274.0,
        511.5,
        image=entry_image_3
    )
    campo_dados = Text(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    campo_dados.place(
        x=74.0,
        y=387.0,
        width=400.0,
        height=247.0
    )

    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
        750.0,
        511.5,
        image=entry_image_4
    )
    campo_feedback = Text(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    campo_feedback.place(
        x=550.0,
        y=387.0,
        width=400.0,
        height=247.0
    )

    canvas.create_text(
        181.0,
        31.0,
        anchor="nw",
        text="SISTEMA DE SOLICITAÇÕES DE SERVIÇOS EM TI",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_text(
        443.0,
        103.0,
        anchor="nw",
        text="Feedback",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_text(
        448.0,
        162.0,
        anchor="nw",
        text="Serviço (id)",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        479.0,
        248.0,
        anchor="nw",
        text="Nota",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        120,
        352.0,
        anchor="nw",
        text="Informações do atendimento",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        687.0,
        352.0,
        anchor="nw",
        text="Feedback",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        34.0,
        720.0,
        anchor="nw",
        text="Usuário: ",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        125,
        720.0,
        anchor="nw",
        text=email,
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )
    window.resizable(False, False)
    window.mainloop()


def TelaPreencherChamadoTecnico(email, janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\criar_chamado_tecnico")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.title('Técnico')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#AFC6AF")

    canvas = Canvas(
        window,
        bg="#AFC6AF",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    botao_retorna = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaInicialTecnico(email, window),
        relief="flat"
    )
    botao_retorna.place(
        x=26.0,
        y=22.0,
        width=83.0,
        height=81.0
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        512.0,
        249.7239990234375,
        image=entry_image_1
    )
    campo_solicitante = Entry(
        bd=0,
        bg="#0C380B",
        highlightthickness=0,
        fg='white'
    )
    campo_solicitante.place(
        x=255.0,
        y=223.0,
        width=514.0,
        height=51.447998046875
    )

    categoria_selecionada = StringVar()
    campo_categoria = OptionMenu(
        window, categoria_selecionada, *servicos
    )
    campo_categoria.config(bg="#0C380B", fg='white')
    campo_categoria.place(
        x=254.0,
        y=313.0,
        width=514.0,
        height=51.447998046875
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        513.0,
        429.7239990234375,
        image=entry_image_3
    )
    campo_comentario = Entry(
        bd=0,
        bg="#0C380B",
        highlightthickness=0,
        fg='white'
    )
    campo_comentario.place(
        x=256.0,
        y=403.0,
        width=514.0,
        height=51.447998046875
    )

    prioridade_selecionada = StringVar()
    prioridade_selecionada.set(prioridades[0])
    campo_prioridade = OptionMenu(
        window, prioridade_selecionada, *prioridades
    )
    campo_prioridade.config(bg="#0C380B", fg='white')
    campo_prioridade.place(
        x=256.0,
        y=493.0,
        width=514.0,
        height=51.447998046875
    )

    entry_image_5 = PhotoImage(
        file=relative_to_assets("entry_5.png"))
    entry_bg_5 = canvas.create_image(
        513.0,
        609.7239990234375,
        image=entry_image_5
    )
    campo_local = Entry(
        bd=0,
        bg="#0C380B",
        highlightthickness=0,
        fg='white'
    )
    campo_local.place(
        x=256.0,
        y=583.0,
        width=514.0,
        height=51.447998046875
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    botao_enviar = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: solicitar_servico(campo_solicitante.get(), categoria_selecionada.get(),
                                          campo_comentario.get(), prioridade_selecionada.get(), campo_local.get()),
        relief="flat"
    )
    botao_enviar.place(
        x=438.0,
        y=702.0,
        width=147.0,
        height=50.0
    )

    canvas.create_text(
        181.0,
        31.0,
        anchor="nw",
        text="SISTEMA DE SOLICITAÇÕES DE SERVIÇOS EM TI",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_text(
        399.0,
        127.0,
        anchor="nw",
        text="Preencher chamado",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_text(
        244.0,
        186.0,
        anchor="nw",
        text="Solicitante (e-mail)",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        241.0,
        280.0,
        anchor="nw",
        text="Selecionar categoria",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        244.0,
        370.0,
        anchor="nw",
        text="Descrição",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        243.0,
        463.0,
        anchor="nw",
        text="Prioridade",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        245.0,
        553.0,
        anchor="nw",
        text="Local",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        34.0,
        720.0,
        anchor="nw",
        text="Usuário:",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )
    canvas.create_text(
        125,
        720.0,
        anchor="nw",
        text=email,
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )
    window.resizable(False, False)
    window.mainloop()


# ----------------------- Coordenador de informática --------------------------#
def TelaInicialCoordenador(email, janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\inicial_coordenador")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.title('Coordenador')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#AFC6AF")

    canvas = Canvas(
        window,
        bg="#AFC6AF",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaSolicitarServicoCoordenador(email, window),
        relief="flat"
    )
    button_1.place(
        x=232.0,
        y=141.0,
        width=559.0,
        height=82.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaAcompanharServicoCoordenador(email, window),
        relief="flat"
    )
    button_2.place(
        x=232.0,
        y=272.0,
        width=559.0,
        height=82.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaHistoricoServicoCoordenador(email, window),
        relief="flat"
    )
    button_3.place(
        x=232.0,
        y=414.0,
        width=559.0,
        height=82.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaRelatoriosCoordenador(email, window),
        relief="flat"
    )
    button_4.place(
        x=232.0,
        y=546.0,
        width=559.0,
        height=82.0
    )

    canvas.create_text(
        181.0,
        31.0,
        anchor="nw",
        text="SISTEMA DE SOLICITAÇÕES DE SERVIÇOS EM TI",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_text(
        34.0,
        720.0,
        anchor="nw",
        text="Usuário:",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )
    canvas.create_text(
        125,
        720.0,
        anchor="nw",
        text=email,
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )
    window.resizable(False, False)
    window.mainloop()


def TelaSolicitarServicoCoordenador(email, janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\solicitar_servico")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.title('Coordenador')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#AFC6AF")

    canvas = Canvas(
        window,
        bg="#AFC6AF",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        181.0,
        31.0,
        anchor="nw",
        text="SISTEMA DE SOLICITAÇÕES DE SERVIÇOS EM TI",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_text(
        399.0,
        127.0,
        anchor="nw",
        text="Solicitar serviço",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    botao_retorna = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaInicialCoordenador(email, window),
        relief="flat"
    )
    botao_retorna.place(
        x=25.0,
        y=21.0,
        width=84.0,
        height=82.0
    )

    categoria_selecionada = StringVar()
    campo_categoria = OptionMenu(
        window, categoria_selecionada, *servicos
    )
    campo_categoria.config(bg="#0C380B", fg='white')
    campo_categoria.place(
        x=255.0,
        y=224.0,
        width=514.0,
        height=51.447998046875
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        514.0,
        340.7239990234375,
        image=entry_image_2
    )
    campo_comentario = Entry(
        bd=0,
        bg="#0C380B",
        highlightthickness=0,
        fg='white'
    )
    campo_comentario.place(
        x=257.0,
        y=314.0,
        width=514.0,
        height=51.447998046875
    )

    prioridade_selecionada = StringVar()
    prioridade_selecionada.set(prioridades[0])
    campo_prioridade = OptionMenu(
        window, prioridade_selecionada, *prioridades
    )
    campo_prioridade.config(bg="#0C380B", fg='white')
    campo_prioridade.place(
        x=257.0,
        y=404.0,
        width=514.0,
        height=51.447998046875
    )

    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
        514.0,
        519.7239990234375,
        image=entry_image_4
    )
    campo_local = Entry(
        bd=0,
        bg="#0C380B",
        highlightthickness=0,
        fg='white'
    )
    campo_local.place(
        x=257.0,
        y=493.0,
        width=514.0,
        height=51.447998046875
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    botao_enviar = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: solicitar_servico(email, categoria_selecionada.get(), campo_comentario.get(),
                                          prioridade_selecionada.get(), campo_local.get()),
        relief="flat"
    )
    botao_enviar.place(
        x=438.0,
        y=703.0,
        width=147.0,
        height=50.0
    )

    canvas.create_text(
        245.0,
        281.0,
        anchor="nw",
        text="Comentário",
        fill="#000000",
        font=("OpenSansRoman Regular", 24 * -1)
    )

    canvas.create_text(
        245.0,
        191.0,
        anchor="nw",
        text="Selecionar categoria",
        fill="#000000",
        font=("OpenSansRoman Regular", 24 * -1)
    )

    canvas.create_text(
        247.0,
        374.0,
        anchor="nw",
        text="Prioridade",
        fill="#000000",
        font=("OpenSansRoman Regular", 24 * -1)
    )

    canvas.create_text(
        247.0,
        464.0,
        anchor="nw",
        text="Local",
        fill="#000000",
        font=("OpenSansRoman Regular", 24 * -1)
    )

    canvas.create_text(
        25.0,
        724.0,
        anchor="nw",
        text="Usuário: ",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        125.0,
        724.0,
        anchor="nw",
        text=email,
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    window.resizable(False, False)
    window.mainloop()


def TelaAcompanharServicoCoordenador(email, janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\acompanhar_solicitante")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.title('Coordenador')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#AFC6AF")

    canvas = Canvas(
        window,
        bg="#AFC6AF",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        181.0,
        31.0,
        anchor="nw",
        text="SISTEMA DE SOLICITAÇÕES DE SERVIÇOS EM TI",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    botao_volta = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaInicialCoordenador(email, window),
        relief="flat"
    )
    botao_volta.place(
        x=24.0,
        y=22.0,
        width=84.0,
        height=82.0
    )

    canvas.create_text(
        326.0,
        143.0,
        anchor="nw",
        text="Acompanhar solicitações",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_rectangle(
        168.0,
        195.0,
        858.0,
        235.0,
        fill="#D9D9D9",
        outline="")

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        513.5,
        427.0,
        image=entry_image_1
    )
    caixa_texto = Text(
        bd=0,
        bg="#527C4F",
        highlightthickness=0,
        fg='white'
    )
    fila = SelectChamadoEmFilaSolicitante(email)
    fila.reverse()
    for ordem in fila:
        nome = ordem[0]
        status = ordem[1]
        tempo_medio = ordem[2]
        posicao_fila = ordem[4]
        id_ordem = ordem[3]
        descricao = f'(id:{id_ordem}) {nome}'
        caixa_texto.insert('0.0', descricao + f'{(35 - len(descricao)) * " "}' +
                           f'{status}' + f'{(20 - len(status)) * " "}' +
                           f'{posicao_fila}' + f'{(10 * " ")}' + f'{tempo_medio} minutos' + '\n')

    caixa_texto.config(state='disabled')

    caixa_texto.place(
        x=168.0,
        y=256.0,
        width=691.0,
        height=340.0
    )

    canvas.create_text(
        220.0,
        195.0,
        anchor="nw",
        text="Descrição",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        440.0,
        195.0,
        anchor="nw",
        text="Status",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        560.0,
        195.0,
        anchor="nw",
        text="Posição",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        688.0,
        195.0,
        anchor="nw",
        text="Tempo médio",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        34.0,
        720.0,
        anchor="nw",
        text="Usuário: ",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        125,
        720.0,
        anchor="nw",
        text=email,
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    window.resizable(False, False)
    window.mainloop()


def TelaHistoricoServicoCoordenador(email, janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\acompanhar_solicitante")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.title('Coordenador')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#AFC6AF")

    canvas = Canvas(
        window,
        bg="#AFC6AF",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        181.0,
        31.0,
        anchor="nw",
        text="SISTEMA DE SOLICITAÇÕES DE SERVIÇOS EM TI",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    botao_volta = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaInicialCoordenador(email, window),
        relief="flat"
    )
    botao_volta.place(
        x=24.0,
        y=22.0,
        width=84.0,
        height=82.0
    )

    canvas.create_text(
        360.0,
        143.0,
        anchor="nw",
        text="Histórico de serviços",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_rectangle(
        168.0,
        195.0,
        858.0,
        235.0,
        fill="#D9D9D9",
        outline="")

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        513.5,
        427.0,
        image=entry_image_1
    )
    caixa_texto = Text(
        bd=0,
        bg="#527C4F",
        highlightthickness=0,
        fg='white'
    )
    concluida = SelectChamadoConcluidoSolicitante(email)
    for ordem in concluida:
        nome = ordem[0]
        data = ordem[1]
        responsavel = ordem[2]
        tempo = ordem[3]
        id_ordem = ordem[4]
        descricao = f'(id:{id_ordem}) {nome}'
        caixa_texto.insert('0.0', f'{descricao}' + f'{(35 - len(descricao)) * " "}' + f'{data}' +
                           f'{8 * " " + responsavel}' + f'{(18 - len(responsavel)) * " "}' +
                           f'{tempo} min.' + '\n')

    caixa_texto.config(state='disabled')

    caixa_texto.place(
        x=168.0,
        y=256.0,
        width=691.0,
        height=340.0
    )

    canvas.create_text(
        230.0,
        195.0,
        anchor="nw",
        text="Descrição",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        420.0,
        195.0,
        anchor="nw",
        text="Data atend.",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        570.0,
        195.0,
        anchor="nw",
        text="Téc. Resp.",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        700.0,
        195.0,
        anchor="nw",
        text="Tempo exec.",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        34.0,
        720.0,
        anchor="nw",
        text="Usuário: ",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        125,
        720.0,
        anchor="nw",
        text=email,
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_feedback.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaFeedbackCoordenador(email, window),
        relief="flat"
    )
    button_3.place(
        x=430.0,
        y=629.0,
        width=162.0,
        height=55.0)

    window.resizable(False, False)
    window.mainloop()


def TelaFeedbackCoordenador(email, janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\feedback_solicitante")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.title('Coordenador')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#AFC6AF")

    canvas = Canvas(
        window,
        bg="#AFC6AF",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        181.0,
        31.0,
        anchor="nw",
        text="SISTEMA DE SOLICITAÇÕES DE SERVIÇOS EM TI",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaHistoricoServicoCoordenador(email, window),
        relief="flat"
    )
    button_1.place(
        x=26.0,
        y=22.0,
        width=83.0,
        height=81.0
    )
    # Drop down menu serviços
    opcoes = []
    concluidos = SelectChamadoConcluidoSolicitante(email)
    for c in concluidos:
        id_ordem = c[4]
        opcoes.append(id_ordem)
    opcoes.reverse()
    id_selecionado = StringVar()
    campo_chamado = OptionMenu(window, id_selecionado, *opcoes)
    campo_chamado.config(bg="#0C380B", fg='white')
    campo_chamado.place(
        x=69.0,
        y=191.0,
        width=514.0,
        height=51.447998046875
    )

    notas = [i for i in range(0, 11)]
    nota_selecionada = StringVar()
    campo_nota = OptionMenu(window, nota_selecionada, *notas)
    campo_nota.config(bg="#0C380B", fg='white')
    campo_nota.place(
        x=69.0,
        y=287.0,
        width=327.286865234375,
        height=51.447998046875
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        511.0,
        513.5,
        image=entry_image_3
    )
    entry_3 = Text(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    entry_3.place(
        x=59.0,
        y=389.0,
        width=904.0,
        height=247.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: avaliar_servico(id_selecionado.get(), entry_3.get('1.0', END), nota_selecionada.get()),
        relief="flat"
    )
    button_2.place(
        x=417.0,
        y=650.0,
        width=153.0,
        height=60.0
    )

    canvas.create_text(
        34.0,
        720.0,
        anchor="nw",
        text="Usuário:",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )
    canvas.create_text(
        125,
        720.0,
        anchor="nw",
        text=email,
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        443.0,
        103.0,
        anchor="nw",
        text="Feedback",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_text(
        60.0,
        156.0,
        anchor="nw",
        text="Serviço (id)",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        59.0,
        249.0,
        anchor="nw",
        text="Dê uma nota ao atendimento",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        60.0,
        358.0,
        anchor="nw",
        text="Insira seu comentário",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )
    window.resizable(False, False)
    window.mainloop()


def TelaRelatoriosCoordenador(email, janela_anterior=None):
    if janela_anterior is not None:
        janela_anterior.destroy()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\Figma\elementos_graficos\relatorios_coordenador")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def exibir_relatorio(relatorio):
        if relatorio == 'Nenhum':
            campo_exibir_relatorio.config(state='normal')
            campo_exibir_relatorio.delete('1.0', END)
            campo_exibir_relatorio.insert('0.0', f'Nenhum relatório foi selecionado.')
            campo_exibir_relatorio.config(state='disabled')
        # Preenche feedback
        else:
            campo_exibir_relatorio.config(state='normal')
            campo_exibir_relatorio.delete('1.0', END)
            exibe_relatorio(relatorio, campo_exibir_relatorio)
            try:
                gera_relatorios_xlsx()
            except Exception as error:
                print(error)
            campo_exibir_relatorio.config(state='disabled')
        pass

    window = Tk()
    window.title('Coordenador')
    w = 1024
    h = 768
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y - 40))
    window.configure(bg="#AFC6AF")

    canvas = Canvas(
        window,
        bg="#AFC6AF",
        height=768,
        width=1024,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    botao_retorna = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: TelaInicialCoordenador(email, window),
        relief="flat"
    )
    botao_retorna.place(
        x=26.0,
        y=16.0,
        width=83.0,
        height=87.0
    )

    relatorio_selecionado = StringVar()
    relatorio_selecionado.set('Nenhum')
    campo_relatorio = OptionMenu(window, relatorio_selecionado, *relatorios)
    campo_relatorio.config(bg="#0C380B", fg='white')
    campo_relatorio.place(
        x=258.0,
        y=209.0,
        width=514.0,
        height=51.447998046875
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    botao_exibir = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: exibir_relatorio(relatorio_selecionado.get()),
        relief="flat"
    )
    botao_exibir.place(
        x=441.0,
        y=287.0,
        width=147.0,
        height=55.0
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        512.0,
        530.5,
        image=entry_image_2
    )
    campo_exibir_relatorio = Text(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    campo_exibir_relatorio.place(
        x=60.0,
        y=368.0,
        width=904.0,
        height=323.0
    )

    canvas.create_text(
        181.0,
        31.0,
        anchor="nw",
        text="SISTEMA DE SOLICITAÇÕES DE SERVIÇOS EM TI",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_text(
        370.0,
        103.0,
        anchor="nw",
        text="Relatórios gerenciais",
        fill="#FFFFFF",
        font=("OpenSansRoman SemiBold", 30 * -1)
    )

    canvas.create_text(
        370.0,
        176.0,
        anchor="nw",
        text="Selecionar tipo de relatório",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )

    canvas.create_text(
        34.0,
        720.0,
        anchor="nw",
        text="Usuário: ",
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )
    canvas.create_text(
        125,
        720.0,
        anchor="nw",
        text=email,
        fill="#000000",
        font=("OpenSansRoman SemiBold", 24 * -1)
    )
    window.resizable(False, False)
    window.mainloop()


# -------------------------- Roda tudo -------------------------------#
if __name__ == '__main__':
    TelaLogin()
