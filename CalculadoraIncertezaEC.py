import streamlit as st
# Injetando CSS personalizado para definir o plano de fundo
page_bg = """
<style>
    
    .stApp {
        background-image: url("https://scontent.faqa1-1.fna.fbcdn.net/v/t39.30808-6/304020462_633025508250639_2056439598122056532_n.png?_nc_cat=104&ccb=1-7&_nc_sid=cc71e4&_nc_eui2=AeH1Pj9KkA4eYYfmgkhnTxcko9Mzb0QQJF2j0zNvRBAkXT0iC_XVk-M1KfWj4Kpr6A8WtKVjdPsHkqGzQ5haJaC9&_nc_ohc=mSGwJQEuxFwQ7kNvgGKN_bl&_nc_ht=scontent.faqa1-1.fna&_nc_gid=A2YOc5SDtBD1-hPRDmfzZjN&oh=00_AYBlz-_jMAtc11e5dAsodQQKYMiMWAl6OVXkwmj7cW7wMQ&oe=66E1454A");
    background-size: cover;
    }

</style>
"""

# Aplicando o CSS ao Streamlit
st.markdown(page_bg, unsafe_allow_html=True)

# Título do aplicativo
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: green; '>Calculadora de Estoque de Carbono e Incerteza</h1>", unsafe_allow_html=True)

# Inicializando o estado da sessão para os dados da "Área"
if 'C1' not in st.session_state:
    st.session_state.C1 = 1.0
if 'C2' not in st.session_state:
    st.session_state.C2 = 1.0
if 'C3' not in st.session_state:
    st.session_state.C3 = 1.0
if 'd1' not in st.session_state:
    st.session_state.d1 = 1.0
if 'd2' not in st.session_state:
    st.session_state.d2 = 1.0

# Inicializando o estado da sessão para os dados da MATA
if 'C1_ref' not in st.session_state:
    st.session_state.C1_ref = 1.0
if 'C2_ref' not in st.session_state:
    st.session_state.C2_ref = 1.0
if 'C3_ref' not in st.session_state:
    st.session_state.C3_ref = 1.0
if 'd1_ref' not in st.session_state:
    st.session_state.d1_ref = 1.0
if 'd2_ref' not in st.session_state:
    st.session_state.d2_ref = 1.0

col1, col2 = st.columns(2)

# Entrada do usuário - coluna 1
with col1:
    st.subheader("Área de referência (MATA) ")
    C1_ref = st.number_input(
        "Concentração de carbono MATA (Camada 00-20 cm):", value=st.session_state.C1_ref)
    C2_ref = st.number_input(
        "Concentração de carbono MATA (Camada 20-40 cm):", value=st.session_state.C2_ref)
    C3_ref = st.number_input(
        "Concentração de carbono MATA (Camada 40-60 cm):", value=st.session_state.C3_ref)
    d1_ref = st.number_input(
        "Densidade da primeira camada MATA (00-20 cm):", value=st.session_state.d1_ref)
    d2_ref = st.number_input(
        "Densidade da segunda camada MATA (20-40 cm):", value=st.session_state.d2_ref)


# Entrada do usuário - coluna 2
with col2:
    st.subheader("Área")
    C1 = st.number_input(
        "Concentração de carbono (Camada 00-20 cm):", value=st.session_state.C1)
    C2 = st.number_input(
        "Concentração de carbono (Camada 20-40 cm):", value=st.session_state.C2)
    C3 = st.number_input(
        "Concentração de carbono (Camada 40-60 cm):", value=st.session_state.C3)
    d1 = st.number_input(
        "Densidade da primeira camada (00-20 cm):", value=st.session_state.d1)
    d2 = st.number_input(
        "Densidade da segunda camada (20-40 cm):", value=st.session_state.d2)

# Funções para cálculos


def declaracao_Variavel():
    u_d = 0.094
    u_soc_1 = 0.13
    u_soc_2 = 0.21
    u_soc_3 = 0.10
    l = 0.20
    U = 0.01
    return u_d, u_soc_1, u_soc_2, u_soc_3, l, U


def incerteza_C_Profundidade(u_soc_1, u_soc_2, u_soc_3, C1, C2, C3, C1_ref, C2_ref, C3_ref):
    U_SOC_1 = u_soc_1 * C1
    U_SOC_2 = u_soc_2 * C2
    U_SOC_3 = u_soc_3 * C3
    U_SOC_1_ref = u_soc_1 * C1_ref
    U_SOC_2_ref = u_soc_2 * C2_ref
    U_SOC_3_ref = u_soc_3 * C3_ref
    return U_SOC_1, U_SOC_2, U_SOC_3, U_SOC_1_ref, U_SOC_2_ref, U_SOC_3_ref


def incerteza_densidade_profundidade(u_d, d1, d2, d1_ref, d2_ref):
    U_d1 = u_d * d1
    U_d2 = u_d * d2
    U_d1_ref = u_d * d1_ref
    U_d2_ref = u_d * d2_ref
    return U_d1, U_d2, U_d1_ref, U_d2_ref


def calculo_EC_profundidade(C1, C2, C3, d1, d2, d1_ref, d2_ref, l):
    EC1 = 10 * C1 * d1 * l
    EC2 = 10 * C2 * d2 * l
    EC3 = 10 * C3 * d2 * l
    EC1_ref = 10 * C1_ref * d1_ref * l
    EC2_ref = 10 * C2_ref * d2_ref * l
    EC3_ref = 10 * C3_ref * d2_ref * l
    return EC1, EC2, EC3, EC1_ref, EC2_ref, EC3_ref


def incerteza_EstoquedeCarbono_profundidade(C1, C2, C3, C1_ref, C2_ref, C3_ref, U, EC1, EC2, EC3, EC1_ref, EC2_ref, EC3_ref, U_SOC_1, U_SOC_2, U_SOC_3, U_SOC_1_ref, U_SOC_2_ref, U_SOC_3_ref, U_d1, U_d2, U_d1_ref, U_d2_ref):
    U_EC1 = EC1 * ((U_SOC_1 / C1) ** 2 + (U_d1 / d1)
                   ** 2 + (U / l) ** 2) ** 0.5
    U_EC2 = EC2 * ((U_SOC_2 / C2) ** 2 + (U_d2 / d2)
                   ** 2 + (U / l) ** 2) ** 0.5
    U_EC3 = EC3 * ((U_SOC_3 / C3) ** 2 + (U_d2 / d2)
                   ** 2 + (U / l) ** 2) ** 0.5
    U_EC1_ref = EC1_ref * ((U_SOC_1_ref / C1_ref) ** 2 +
                           (U_d1_ref / d1_ref) ** 2 + (U / l) ** 2) ** 0.5
    U_EC2_ref = EC2_ref * ((U_SOC_2_ref / C2_ref) ** 2 +
                           (U_d2_ref / d2_ref) ** 2 + (U / l) ** 2) ** 0.5
    U_EC3_ref = EC3_ref * ((U_SOC_3_ref / C3_ref) ** 2 +
                           (U_d2_ref / d2_ref) ** 2 + (U / l) ** 2) ** 0.5
    return U_EC1, U_EC2, U_EC3, U_EC1_ref, U_EC2_ref, U_EC3_ref


def calculo_MassaSeca(l, d1, d2, d1_ref, d2_ref):
    Ms1 = l * d1 * 10000
    Ms2 = l * d2 * 10000
    Ms1_ref = l * d1_ref * 10000
    Ms2_ref = l * d2_ref * 10000
    return Ms1, Ms2, Ms1_ref, Ms2_ref


def incerteza_MassaSeca_profundidade(Ms1, Ms2, Ms1_ref, Ms2_ref, U, l, U_d1, U_d2, U_d1_ref, U_d2_ref):
    U_Ms1 = Ms1 * ((U / l) ** 2 + (U_d1 / d1) ** 2) ** 0.5
    U_Ms2 = Ms2 * ((U / l) ** 2 + (U_d2 / d2) ** 2) ** 0.5
    U_Ms1_ref = Ms1_ref * ((U / l) ** 2 + (U_d1_ref / d1_ref) ** 2) ** 0.5
    U_Ms2_ref = Ms2_ref * ((U / l) ** 2 + (U_d2_ref / d2_ref) ** 2) ** 0.5
    return U_Ms1, U_Ms2, U_Ms1_ref, U_Ms2_ref


def calculo_EC(EC1, EC2, Ms1, Ms2, Ms1_ref, Ms2_ref, C3):
    Cti = EC1 + EC2
    Mti = Ms1 + 2 * Ms2
    Msi = Ms1_ref + 2 * Ms2_ref
    Ctn = C3 / 1000
    EC = Cti + (Ms2 - (Mti - Msi)) * Ctn
    return EC, Cti, Mti, Msi, Ctn


def calculo_incertezas_ind(U_EC1, U_EC2, U_Ms1, U_Ms2, U_Ms1_ref, U_Ms2_ref):
    U_Cti = (U_EC1 ** 2 + U_EC2 ** 2) ** 0.5
    U_Mti = (U_Ms1 ** 2 + U_Ms2 ** 2 + U_Ms2 ** 2) ** 0.5
    U_Msi = (U_Ms1_ref ** 2 + U_Ms2_ref ** 2 + U_Ms2_ref ** 2) ** 0.5
    U_Ctn = U_SOC_3 / 1000
    return U_Cti, U_Mti, U_Msi, U_Ctn


def calculos_A(Msi, Mti, Ms2, U_Msi, U_Mti):
    A = Msi - Mti + Ms2
    U_A = (U_Msi ** 2 + U_Mti ** 2 + U_Mti ** 2) ** 0.5
    return A, U_A


def calculo_B(A, Ctn):
    B = A * Ctn
    return B


def calculo_UB(B, U_A, U_Ctn, A, Ctn):
    U_B = B * ((U_A / A) ** 2 + (U_Ctn / Ctn) ** 2) ** 0.5
    return U_B


def calculo_Incerteza_EC(U_B, U_Cti):
    U_EC = (U_B ** 2 + U_Cti ** 2) ** 0.5
    return U_EC


# Obtendo os valores de entrada
u_d, u_soc_1, u_soc_2, u_soc_3, l, U = declaracao_Variavel()

# Cálculos das incertezas
U_SOC_1, U_SOC_2, U_SOC_3, U_SOC_1_ref, U_SOC_2_ref, U_SOC_3_ref = incerteza_C_Profundidade(
    u_soc_1, u_soc_2, u_soc_3, C1, C2, C3, C1_ref, C2_ref, C3_ref
)
U_d1, U_d2, U_d1_ref, U_d2_ref = incerteza_densidade_profundidade(
    u_d, d1, d2, d1_ref, d2_ref
)

# Cálculo do estoque de carbono
EC1, EC2, EC3, EC1_ref, EC2_ref, EC3_ref = calculo_EC_profundidade(
    C1, C2, C3, d1, d2, d1_ref, d2_ref, l)

# Cálculo da massa seca
Ms1, Ms2, Ms1_ref, Ms2_ref = calculo_MassaSeca(l, d1, d2, d1_ref, d2_ref)

# Incerteza do estoque de carbono
U_EC1, U_EC2, U_EC3, U_EC1_ref, U_EC2_ref, U_EC3_ref = incerteza_EstoquedeCarbono_profundidade(
    C1, C2, C3, C1_ref, C2_ref, C3_ref, U, EC1, EC2, EC3, EC1_ref, EC2_ref, EC3_ref,
    U_SOC_1, U_SOC_2, U_SOC_3, U_SOC_1_ref, U_SOC_2_ref, U_SOC_3_ref,
    U_d1, U_d2, U_d1_ref, U_d2_ref
)

# Cálculo da massa seca e incertezas
U_Ms1, U_Ms2, U_Ms1_ref, U_Ms2_ref = incerteza_MassaSeca_profundidade(
    Ms1, Ms2, Ms1_ref, Ms2_ref, U, l, U_d1, U_d2, U_d1_ref, U_d2_ref
)


# Cálculos finais
EC, Cti, Mti, Msi, Ctn = calculo_EC(EC1, EC2, Ms1, Ms2, Ms1_ref, Ms2_ref, C3)
U_Cti, U_Mti, U_Msi, U_Ctn = calculo_incertezas_ind(
    U_EC1, U_EC2, U_Ms1, U_Ms2, U_Ms1_ref, U_Ms2_ref)
A, U_A = calculos_A(Msi, Mti, Ms2, U_Msi, U_Mti)
B = calculo_B(A, Ctn)
U_B = calculo_UB(B, U_A, U_Ctn, A, Ctn)
U_EC = calculo_Incerteza_EC(U_B, U_Cti)


# Defina a cor desejada
C = "#f0f0f5"  # Exemplo de cor de fundo

# CSS para estilizar o container
container_style = f"""
    <style>
    .custom-container {{
        background-color: {C};  /* Cor de fundo personalizada */
        padding: 30px;           /* Espaçamento interno */
        border-radius: 10px;    /* Bordas arredondadas */
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);  /* Sombra */
        border: 1px solid #ccc; /* Borda */
    }}
    </style>
"""

# Injetar o CSS no aplicativo
st.markdown(container_style, unsafe_allow_html=True)

if st.button("Calcular"):
    # Criar um container e adicionar conteúdo HTML
    with st.container():
        st.markdown(f"""
                        <div class="custom-container">
                            <p>Estoque de Carbono: <b>{EC:.2f} Mg ha⁻¹</b></p>
                            <p>Incerteza do Estoque de Carbono:<b> {U_EC:.2f} Mg ha⁻¹</b></p>
                        </div>
                    """, unsafe_allow_html=True)
