import streamlit as st
from fpdf import FPDF
import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Empire Fitness - Avaliação Física", layout="wide")

# Estilo CSS para melhorar o visual
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #e2e8f0;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #1E3A8A !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CLASSE PARA GERAR PDF ---
class PDF(FPDF):
    def header(self):
        self.set_fill_color(0, 0, 0)
        self.rect(0, 0, 210, 35, 'F')
        try:
            self.image('logo.png', x=135, y=7, w=50)
        except: pass
        self.set_font('Arial', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 12)
        self.cell(0, 10, 'RELATÓRIO DE AVALIAÇÃO FÍSICA', 0, 1, 'L')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

# --- INTERFACE POR ABAS ---
st.title("🛡️ Empire Fitness - Gestão de Avaliações")
abas = st.tabs([
    "👤 Dados Pessoais", "📏 Antropometria", "⭕ Perímetros", 
    "📉 Dobras Cutâneas", "🏃 Av. Funcional", "❤️ Risco Cardio", "🏁 Conclusão"
])

# --- ABA 1: DADOS PESSOAIS ---
with abas[0]:
    st.header("1. Dados Pessoais")
    
    col1, col2 = st.columns(2)
    nome = col1.text_input("Nome:")
    # 1. Configuração do Input de Data
    hoje = datetime.date.today()
    data_padrao = datetime.date(1920, 1, 1)
   # O parâmetro 'format' altera a máscara de exibição para o padrão BR
    nascimento = col2.date_input(
    "Data de nascimento:",
    value=datetime.date(), # Data que aparece selecionada por padrão
    min_value=data_padrao,           # Limite inferior
    max_value=hoje,                   # Limite superior
    format="DD/MM/YYYY" )             # Formato de exibição brasileiro
    # 2. Cálculo Lógico da Idade
    # Subtrai os anos e ajusta -1 se o dia/mês atual for anterior ao nascimento
    idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
    col1.markdown("Idade:") 
    col1.info(f"{idade} anos")
    sexo = col2.selectbox("Sexo:", ["Masculino", "Feminino"])
    modalidade = col1.multiselect("Modalidade:", ["CrossFit", "Musculação", "Ambas"])
    tempo_atividade = col2.number_input("Tempo de prática de atividade física:", min_value=0, step=1) 
    objetivo = col2.multiselect("Objetivo:", ["Saúde", "Emagrecimento", "Hipertrofia", "Performance", "Reabilitação"])
    
    st.header("1.1 Questionário De Prontidão Para Atividade Física")
    prontidao1 = st.radio("1. Algum médico já disse que você possui problema cardíaco?", ["Sim", "Não"], horizontal=True)
    prontidao2 = st.radio("2. Você sente dor no peito durante atividades físicas?", ["Sim", "Não"], horizontal=True)
    prontidao3 = st.radio("3. No último mês, sentiu dor no peito em repouso?", ["Sim", "Não"], horizontal=True)
    prontidao4 = st.radio("4. Já perdeu o equilíbrio por tontura ou perdeu a consciência?", ["Sim", "Não"], horizontal=True)
    prontidao5 = st.radio("5. Possui problema ósseo ou articular que possa ser agravado com exercício?", ["Sim", "Não"], horizontal=True)
    prontidao6 = st.radio("6. Usa medicamentos para pressão arterial ou coração?", ["Sim", "Não"], horizontal=True)
    prontidao7 = st.radio("7. Conhece alguma outra razão pela qual não deveria praticar atividade física?", ["Sim", "Não"], horizontal=True)
    
    st.text ("Se alguma resposta for SIM, é recomendada liberação médica.")

    st.header("1.2 Histórico de Saúde")
    colh1, colh2 = st.columns(2)
    histsaude1 = colh2.text_area("1. Doenças diagnosticadas:")
    histsaude2 = colh2.text_area("2. Cirurgias prévias:")
    histsaude3 = colh1.text_area("3. Lesões musculares/articulares:")
    histsaude4 = colh2.text_area("4. Dores atuais:")
    histsaude5 = colh1.text_area("5. Uso de medicamentos:")
       
    st.text ("Se alguma resposta for SIM, é recomendada liberação MÉDICA.")
    
   
    
# --- ABA 2: ANTROPOMETRIA ---
with abas[1]:
    st.header("2. Avaliação Antropométrica")
    peso = st.number_input("Peso corporal (kg):", format="%.2f")
    altura = st.number_input("Altura (m):", format="%.2f")
    imc = peso / (altura ** 2) if altura > 0 else 0
    st.info(f"IMC Calculado: {imc:.2f}")

# --- ABA 3: PERÍMETROS ---
with abas[2]:
    st.header("3. Perímetros Corporais")
    cintura = st.number_input("Cintura (cm):", format="%.1f")
    quadril = st.number_input("Quadril (cm):", format="%.1f")
    rcq = cintura / quadril if quadril > 0 else 0
    st.info(f"RCQ Calculado: {rcq:.2f}")

# --- ABA 4: DOBRAS CUTÂNEAS ---
with abas[3]:
    st.header("4. Pollock Sete Dobras (mm)")
    c1, c2 = st.columns(2)
    tri = c1.number_input("Tríceps:")
    sub = c2.number_input("Subescapular:")
    sup = c1.number_input("Supra-ilíaca:")
    abd = c2.number_input("Abdominal:")
    cox = c1.number_input("Coxa:")
    pei = c2.number_input("Peitoral:")
    axi = c1.number_input("Axilar média:")
    
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
    agachamento = st.selectbox("Agachamento livre:", ["Bom padrão", "Compensações", "Dor"])
    flexao = st.selectbox("Flexão de braços:", ["Executa bem", "Dificuldade", "Não executa"])
    mobilidade_o = st.radio("Mobilidade de ombros:", ["Boa", "Regular", "Limitada"])
    mobilidade_q = st.radio("Mobilidade de quadril:", ["Boa", "Regular", "Limitada"])

# --- ABA 6: RISCO CARDIO ---
with abas[5]:
    st.header("6. Risco Cardiometabólico")
    sedentarismo = st.radio("Sedentarismo prévio?", ["Sim", "Não"])
    risco_imc = "Sim" if imc > 25 else "Não"
    st.write(f"IMC elevado (>25)? **{risco_imc}**")

# --- ABA 7: CONCLUSÃO ---
with abas[6]:
    st.header("7. Conclusão do Avaliador")
    perfil = st.select_slider("Perfil do aluno:", ["Iniciante", "Intermediário", "Avançado"])
    treino = st.selectbox("Tipo de treino indicado:", ["Musculação", "CrossFit adaptado", "CrossFit padrão", "Treino combinado"])
    obs = st.text_area("Observações finais:")
    avaliador = st.text_input("Responsável pela avaliação:")
    cref = st.text_input("CREF:")

    if st.button("🖨️ GERAR RELATÓRIO COMPLETO (PDF)"):
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Montagem do PDF
        secoes = {
            "DADOS PESSOAIS": f"Nome: {nome}   nIdade: {idade} Data de Nascimento: {nascimento} nIdade: {idade} nObjetivo: {objetivo} \nSexo: {sexo}",
            "COMPOSIÇÃO CORPORAL": f"IMC: {imc:.2f}\nRCQ: {rcq:.2f}\n% Gordura: {gordura:.2f}%",
            "AVALIAÇÃO FUNCIONAL": f"Agachamento: {agachamento}\nFlexão: {flexao}",
            "ANTROPOMETRIA":f"Peso Corporal: {peso}     Altura (m): {altura}",
            "PERÍMETROS":"",
            "DOBRAS CUTÂNEAS":"",
            "AV. FUNCIONAL":"",
            "RISCO CARDIO":"",
            "CONCLUSÃO": f"Treino: {treino}\nObs: {obs}"
        }
        
        for titulo, conteudo in secoes.items():
            pdf.set_fill_color(230, 230, 230)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, titulo, 0, 1, 'L', 1)
            pdf.set_font("Arial", '', 12)
            pdf.multi_cell(0, 8, conteudo)
            pdf.ln(5)
            
        pdf.ln(20)
        pdf.line(60, pdf.get_y(), 150, pdf.get_y())
        pdf.cell(0, 10, f"{avaliador} - {cref}", 0, 1, 'C')
        
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button("📥 Baixar PDF", pdf_bytes, f"Avaliacao_{nome}.pdf")