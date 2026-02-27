import streamlit as st
from fpdf import FPDF
import datetime
import base64

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Empire Fitness - Avaliação Física", layout="wide")

# Estilo CSS Personalizado
st.markdown("""
    <style>
    .main { background-color: #fffff0; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #d0d0c4;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { 
        background-color:#004564 !important; 
        color: #FFFFFF !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES AUXILIARES ---
def format_text(txt):
    """Garante compatibilidade de caracteres com FPDF latin-1"""
    return str(txt).encode('latin-1', 'replace').decode('latin-1')

def desenhar_checkbox(pdf, x, y, marcado=False):
    pdf.set_line_width(0.3)
    pdf.rect(x, y, 4, 4) # Desenha o quadrado
    if marcado:
        pdf.set_font("Arial", 'I', 10)
        pdf.text(x + 0.8, y + 3.2, "X") # Desenha o X se marcado

# --- CLASSE PARA GERAR PDF ---
class PDF(FPDF):
    def header(self):
        self.set_fill_color(0, 0, 0)
        self.rect(0, 0, 210, 35, 'F')
        try:
            self.image('logo.png', x=145, y=7, w=50)
        except:
            pass
        self.set_font('Arial', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 12)
        self.cell(0, 10, 'RELATORIO DE AVALIACAO FISICA', 0, 1, 'L')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Empire Fitness - Pagina {self.page_no()}', 0, 0, 'C')

# --- INTERFACE ---
st.title("Empire Fitness - Gestão de Avaliações")

abas = st.tabs([
    "👤 Dados Pessoais", "📏 Antropometria", "⭕ Perímetros", 
    "📉 Dobras Cutâneas", "🏃 Av. Funcional", "❤️ Risco Cardio", "🏁 Conclusão"
])

# --- ABA 1: DADOS PESSOAIS ---
with abas[0]:
    st.header("1. Dados Pessoais")
    col1, col2 = st.columns(2)
    nome = col1.text_input("Nome:")
    hoje = datetime.date.today()
    nascimento = col2.date_input("Data de nascimento:", value=datetime.date.today(),min_value=datetime.date(1900, 1, 1), max_value=hoje, format="DD/MM/YYYY")
    idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
    col1.info(f"Idade calculada: {idade} anos")
    sexo = col2.selectbox("Sexo:", ["Masculino", "Feminino"])
    contato = col1.text_input("Contato:", "27 99999-9999")
    email = col2.text_input("Email:")
    modalidade = col1.multiselect("Modalidade:", ["CrossFit", "Musculação", "Ambas"])
    tempo_atividade = col2.number_input("Tempo de prática (meses):", min_value=0, step=1) 
    objetivo = col1.multiselect("Objetivo:", ["Saúde", "Emagrecimento", "Hipertrofia", "Performance", "Reabilitação"])
    
    st.divider()
    st.header("1.1 PAR-Q (Prontidão Física)")
    texto_p1 = "1. Algum médico já disse que você possui problema cardíaco?"
    texto_p2 = "2. Você sente dor no peito durante atividades físicas?"
    texto_p3 = "3. No último mês, sentiu dor no peito em repouso?"
    texto_p4 = "4. Já perdeu o equilíbrio por tontura ou perdeu a consciência?"
    texto_p5 = "5. Possui problema ósseo ou articular que possa ser agravado?"
    texto_p6 = "6. Usa medicamentos para pressão arterial ou coração?"
    texto_p7 = "7. Conhece alguma outra razão para não praticar exercício?"

    p1 = st.checkbox(texto_p1)
    p2 = st.checkbox(texto_p2)
    p3 = st.checkbox(texto_p3)
    p4 = st.checkbox(texto_p4)
    p5 = st.checkbox(texto_p5)
    p6 = st.checkbox(texto_p6)
    p7 = st.checkbox(texto_p7)

    st.divider()
    st.header("1.2 Histórico de Saúde")
    colh1, colh2 = st.columns(2)
    h_doencas = colh1.text_input("Doenças diagnosticadas:")
    h_cirurgias = colh2.text_input("Cirurgias prévias:")
    h_lesoes = colh1.text_input("Lesões musculares/articulares:")
    h_dores = colh2.text_input("Dores atuais:")
    h_remedios = colh1.text_input("Uso de medicamentos:")

# --- ABA 2: ANTROPOMETRIA ---
with abas[1]:
    st.header("2. Avaliação Antropométrica")
    col_ant1, col_ant2 = st.columns(2)
    peso = col_ant1.number_input("Peso corporal (kg):", format="%.2f", value=70.0)
    altura = col_ant2.number_input("Altura (m):", format="%.2f", value=1.70)
    imc = peso / (altura ** 2) if altura > 0 else 0
    st.info(f"IMC Calculado: {imc:.2f}")

# --- ABA 3: PERÍMETROS 2---
with abas[2]:
    st.header("3. Perímetros Corporais")
    col_per1, col_per2 = st.columns(2)
    cintura = col_per1.number_input("Cintura (cm):", format="%.1f")
    quadril = col_per2.number_input("Quadril (cm):", format="%.1f")
    rcq = cintura / quadril if quadril > 0 else 0
    st.info(f"RCQ Calculado: {rcq:.2f}")

# --- ABA 4: DOBRAS CUTÂNEAS ---
with abas[3]:
    st.header("4. Pollock Sete Dobras (mm)")
    c_dob1, c_dob2 = st.columns(2)
    tri = c_dob1.number_input("Tríceps:")
    sub = c_dob2.number_input("Subescapular:")
    sup = c_dob1.number_input("Supra-ilíaca:")
    abd = c_dob2.number_input("Abdominal:")
    cox = c_dob1.number_input("Coxa:")
    pei = c_dob2.number_input("Peitoral:")
    axi = c_dob1.number_input("Axilar média:")
    
    soma = tri + sub + sup + abd + cox + pei + axi
    if sexo == "Masculino":
        dc = 1.112 - (0.00043499 * soma) + (0.00000055 * (soma**2)) - (0.00028826 * idade)
    else:
        dc = 1.097 - (0.00046971 * soma) + (0.00000056 * (soma**2)) - (0.00012828 * idade)
    
    gordura = ((4.95 / dc) - 4.50) * 100 if dc > 1 else 0
    st.warning(f"% de Gordura Corporal Estimado: {gordura:.2f}%")

# --- ABA 5: AV. FUNCIONAL ---
with abas[4]:
    st.header("5. Avaliação Funcional Básica")
    col_f1, col_f2 = st.columns(2)
    agachamento = col_f1.selectbox("Agachamento livre:", ["Bom padrão", "Compensações", "Dor"])
    flexao = col_f2.selectbox("Flexão de braços:", ["Executa bem", "Dificuldade", "Não executa"])
    mobilidade_o = col_f1.radio("Mobilidade de ombros:", ["Boa", "Regular", "Limitada"])
    mobilidade_q = col_f2.radio("Mobilidade de quadril:", ["Boa", "Regular", "Limitada"])

    st.divider()
    st.header("5.1 Salto Vertical")
    col_f3, col_f4 = st.columns(2)
    Elasticidade = col_f3.number_input("Elasticidade:")
    peso_salto = col_f4.number_input("Peso corporal p/ salto (kg):", value=peso)
    Altura_salto = col_f3.number_input("Altura do Salto:")
    Tempodevoo = col_f4.number_input("Tempo de Voo:")
    Velocidade = col_f3.number_input("Velocidade do Salto:")
    Forçammii = col_f4.number_input("Força MMII:")
    Potencia = col_f3.number_input("Potência:")

# --- ABA 6: RISCO CARDIO ---
with abas[5]:
    st.header("6. Risco Cardiometabólico")
    sedentarismo = st.radio("Sedentarismo prévio?", ["Não", "Sim"])
    risco_imc = "Sim" if imc > 25 else "Não"
    st.write(f"Risco por IMC elevado (>25): **{risco_imc}**")

# --- ABA 7: CONCLUSÃO E PDF ---
with abas[6]:
    st.header("7. Conclusão e Exportação")
    perfil = st.select_slider("Perfil do aluno:", ["Iniciante", "Intermediário", "Avançado"])
    treino = st.selectbox("Tipo de treino indicado:", ["Musculação", "CrossFit adaptado", "CrossFit padrão", "Treino combinado"])
    obs = st.text_area("Observações finais:")
    avaliador = st.text_input("Avaliador Responsável:")
    cref = st.text_input("CREF:")

    if st.button("🖨️ GERAR RELATÓRIO COMPLETO (PDF)"):
        pdf = PDF()
        pdf.add_page()
        
        # --- SEÇÃO 1: DADOS PESSOAIS ---
        pdf.set_fill_color(230, 230, 230)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, format_text("1. DADOS PESSOAIS"), 0, 1, 'L', 1)
            
        pdf.set_font("Arial", 'B', 10)
        pdf.write(7, format_text("Nome: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(7, format_text(f"{nome}\n"))
        pdf.set_font("Arial", 'B', 10)
        pdf.write(7, format_text("Data de Nasc: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(7, format_text(f"{nascimento.strftime('%d/%m/%Y')} ({idade} anos)\n"))
        pdf.set_font("Arial", 'B', 10)
        pdf.write(7, format_text("Sexo: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(7, format_text(f"{sexo}"))

        pdf.set_x (45)
        pdf.set_font("Arial", 'B', 10)
        pdf.write(7, format_text("Contato: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(7, format_text(f"{contato}"))

        pdf.set_x (100)
        pdf.set_font("Arial", 'B', 10)
        pdf.write(7, format_text("E-mail: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(7, format_text(f"{email}\n"))

        pdf.set_font("Arial", 'B', 10)
        pdf.write(7, format_text("Objetivo: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(7, format_text(f"{', '.join(objetivo)}\n"))

        pdf.set_font("Arial", 'B', 10)
        pdf.write(7, format_text("Modalidade: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(7, format_text(f"{', '.join(modalidade)}"))

        pdf.set_x(100)
        pdf.set_font("Arial", 'B', 10)
        pdf.write(7, format_text("Tempo de pratica: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(7, format_text(f"{tempo_atividade} meses\n"))

        # --- SEÇÃO 2: QUESTIONARIO DE PRONTIDÃO (PAR-Q) ---
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, format_text("2. QUESTIONARIO DE PRONTIDÃO (PAR-Q) e HISTÓRICO DE SAÚDE"), 0, 1, 'L', 1)
        pdf.set_font("Arial", '', 10)
        
        parq_perguntas = [
            (texto_p1, p1), (texto_p2, p2), (texto_p3, p3),
            (texto_p4, p4), (texto_p5, p5), (texto_p6, p6), (texto_p7, p7)
        ]

        for texto, valor in parq_perguntas:
            y = pdf.get_y()
            desenhar_checkbox(pdf, 12, y + 1.5, marcado=valor)
            pdf.set_x(18)
            pdf.cell(0, 7, format_text(texto), 0, 1)

         # --- SEÇÃO 2.2 HISTÓRICO DE SAÚDE ---
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, format_text("2.2 HISTÓRICO DE SAÚDE"), 0, 1, 'L', 1)
        pdf.set_font("Arial", '', 10)
        linha = 6
        parq_txt = ("")
        pdf.set_font("Arial", 'B', 10)
        pdf.write(linha, format_text("Doenças diagnosticadas: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(linha, format_text(f"{parq_txt}"f"{h_doencas if h_doencas else 'Nada consta'}\n"))

        pdf.set_font("Arial", 'B', 10)
        pdf.write(linha, format_text("Cirurgias prévias: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(linha, format_text(f"{parq_txt}"f"{h_cirurgias if h_cirurgias else 'Nada consta'}\n")) 

        pdf.set_font("Arial", 'B', 10)
        pdf.write(linha, format_text("Lesões musculares/articulares: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(linha, format_text(f"{parq_txt}"f"{h_lesoes if h_lesoes else 'Nada consta'}\n"))

        pdf.set_font("Arial", 'B', 10)
        pdf.write(linha, format_text("Uso de Medicamentos: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(linha, format_text(f"{parq_txt}"f"{h_remedios if h_remedios else 'Não utiliza'}\n"))
        
# --- SEÇÃO 3: COMPOSICAO CORPORAL E MEDIDAS ---
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, format_text("3. COMPOSICAO CORPORAL E MEDIDAS"), 0, 1, 'L', 1)

        # --- LINHA 1: PESO ---
        pdf.set_font("Arial", 'B', 10)
        pdf.write(linha, format_text("Peso: ")) # .write não precisa de largura, ele apenas "escreve"
        pdf.set_font("Arial", '', 10)
        pdf.write(linha, format_text(f"{peso}kg"))

        # --- LINHA 1: ALTURA ---
        pdf.set_x(55) 
        pdf.set_font("Arial", 'B', 10)
        pdf.write(linha, format_text("Altura: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(linha, format_text(f"{altura}m"))

        # --- LINHA 1: IMC ---
        pdf.set_x(110) # Espaçamento para o IMC na mesma linha
        pdf.set_font("Arial", 'B', 10)
        pdf.write(linha, format_text("IMC: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(linha, format_text(f"{imc:.2f}\n")) # \n pula a linha

        # --- LINHA 2: CINTURA ---
        pdf.set_font("Arial", 'B', 10)
        pdf.write(linha, format_text("Cintura: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(linha, format_text(f"{cintura}cm"))
        
        # --- LINHA 2: QUADRIL ---
        pdf.set_x(55) 
        pdf.set_font("Arial", 'B', 10)
        pdf.write(linha, format_text("Quadril: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(linha, format_text(f"{quadril}cm"))

        # --- LINHA 2: RCQ ---
        pdf.set_x(110)
        pdf.set_font("Arial", 'B', 10)
        pdf.write(linha, format_text("RCQ: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(linha, format_text(f"{rcq:.2f}\n"))

        # --- DOBRAS ---
        pdf.set_font("Arial", 'B', 10)
        pdf.write(linha, format_text("Dobras (mm): "))
        pdf.set_font("Arial", 'I', 10)
        pdf.write(linha, format_text(f"Tri: {tri} | Sub: {sub} | Sup: {sup} | Abd: {abd} | Coxa: {cox} | Peit: {pei} | Axi: {axi}\n"))

        # --- RESULTADO FINAL ---
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(linha, 10, format_text(f"PERCENTUAL DE GORDURA: {gordura:.2f}%"), 0, 1)


        # --- SEÇÃO 4: AVALIACAO FUNCIONAL E SALTO ---
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, format_text("4. AVALIACAO FUNCIONAL E SALTO"), 0, 1, 'L', 1)
        pdf.set_font("Arial", 'B', 10)
        pdf.write(linha, format_text("Agachamento: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(linha, format_text(f"{agachamento}"))

        pdf.set_x(65)
        pdf.set_font("Arial", 'B', 10)
        pdf.write(linha, format_text("Flexão: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(linha, format_text(f"{flexao}"))

        pdf.set_x(105)
        pdf.set_font("Arial", 'B', 10)
        pdf.write(linha, format_text("Mob. Ombros: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(linha, format_text(f"{mobilidade_o}"))
        
        pdf.set_x(155)
        pdf.set_font("Arial", 'B', 10)
        pdf.write(linha, format_text("Mob. Quadril: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(linha, format_text(f"{mobilidade_q}\n"))
        
        pdf.set_font("Arial", 'B', 10)
        pdf.write(linha, format_text("Elasticidade: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(linha, format_text(f"{Elasticidade}"))

        pdf.set_x(65)
        pdf.set_font("Arial", 'B', 10)
        pdf.write(linha, format_text("Altura: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(linha, format_text(f"{Altura_salto}cm"))

        pdf.set_x(105)
        pdf.set_font("Arial", 'B', 10)
        pdf.write(linha, format_text("Tempo Voo: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(linha, format_text(f"{Tempodevoo}ms"))

        pdf.set_x(155)
        pdf.set_font("Arial", 'B', 10)
        pdf.write(linha, format_text("Potencia: "))
        pdf.set_font("Arial", '', 10)
        pdf.write(linha, format_text(f"{Potencia}\n \n"))

        # --- SEÇÃO 5: CONCLUSAO DO AVALIADOR ---
       
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, format_text("5. CONCLUSAO DO AVALIADOR"), 0, 1, 'L', 1)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 8, format_text(f"Perfil: {perfil} | Treino Indicado: {treino}\nObservacoes: {obs}"))
            
        # ASSINATURA
        pdf.ln(20)
        pdf.line(60, pdf.get_y(), 150, pdf.get_y())
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 10, format_text(f"{avaliador}"), 0, 1, 'C')
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 5, format_text(f"CREF: {cref}"), 0, 1, 'C')
        
        # --- LÓGICA DE VISUALIZAÇÃO ---
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        
        st.markdown("### 👁️ Pré-visualização do Relatório")
        st.markdown(pdf_display, unsafe_allow_html=True)
        
        st.download_button(
            label="📥 Confirmar e Baixar PDF",
            data=pdf_bytes,
            file_name=f"Avaliacao_{nome.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )