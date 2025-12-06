import matplotlib.pyplot as plt
import numpy as np

# --- 1. DADOS DE ENTRADA (Módulo 4 / Z=30) ---
# Propriedades da Carga
Potencia_cv = 0.5   # cv
Rotacao_rpm = 60    # RPM
Distancia = 40      # mm (Braço de alavanca: Centro Engrenagem até Centro Mancal)
Angulo_Pressao = 20 # graus

# Propriedades Geométricas
Modulo = 4          # mm
Z_dentes = 30       
Diametro_Primitivo = Modulo * Z_dentes # 120 mm
Raio_Coroa = Diametro_Primitivo / 2    # 60 mm

# Propriedades do Material (Aço 1045) e Segurança
Tau_admissivel = 6.0 # kgf/mm² (Cisalhamento com rasgo de chaveta)
Km = 1.5             # Fator de Choque (Flexão)
Kt = 1.0             # Fator de Choque (Torção)

# --- 2. CÁLCULOS DE ENGENHARIA ---

# A. Torque (T = P / w)
# 0.5 cv = 37.5 kgf.m/s -> convertendo para mm e rad/s
Omega = (Rotacao_rpm * 2 * np.pi) / 60
Torque = (Potencia_cv * 75 * 1000) / Omega  # kgf.mm

# B. Forças no Engrenamento
F_tangencial = Torque / Raio_Coroa
F_radial = F_tangencial * np.tan(np.radians(Angulo_Pressao))
F_resultante = np.sqrt(F_tangencial**2 + F_radial**2) # Carga W

# C. Momento Fletor Máximo (M = W * L)
Momento_Max = F_resultante * Distancia

# D. Dimensionamento do Eixo (Critério ASME)
# d = [ (16 / (pi * tau)) * sqrt( (Km*M)^2 + (Kt*T)^2 ) ]^(1/3)
Termo_Flexao = (Km * Momento_Max)**2
Termo_Torcao = (Kt * Torque)**2
Diametro_Minimo = ((16 / (np.pi * Tau_admissivel)) * np.sqrt(Termo_Flexao + Termo_Torcao))**(1/3)

# --- 3. PREPARAÇÃO DOS DADOS PARA PLOTAGEM ---
x = np.linspace(0, Distancia, 100) # Eixo X: 0 (Engrenagem) -> 40 (Mancal)

# Vetores
y_torque = np.full_like(x, Torque)          # Torque constante ao longo do eixo
y_shear = np.full_like(x, F_resultante)     # Cortante constante (Carga Pontual)
y_moment = F_resultante * x                 # Momento linear (0 na ponta, Max no apoio)

# --- 4. PLOTAGEM DOS DIAGRAMAS ---
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 14), sharex=True)
plt.subplots_adjust(hspace=0.3)
fig.suptitle(f'Análise de Esforços - Eixo de Saída (Scotch Yoke)\nAço SAE 1045 - Módulo {Modulo}', fontsize=16, fontweight='bold')

# Gráfico 1: Torque
ax1.plot(x, y_torque, color='#2ca02c', linewidth=2.5) # Verde
ax1.fill_between(x, y_torque, alpha=0.2, color='#2ca02c')
ax1.set_ylabel('Torque $M_t$ (kgf.mm)', fontsize=12)
ax1.set_title(f'1. Diagrama de Momento Torsor (Constante)', fontweight='bold', loc='left')
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.text(Distancia/2, Torque, f'{Torque:.0f} kgf.mm', ha='center', va='bottom', fontsize=11, fontweight='bold', backgroundcolor='white')

# Gráfico 2: Força Cortante (Shear)
ax2.plot(x, y_shear, color='#1f77b4', linewidth=2.5) # Azul
ax2.fill_between(x, y_shear, alpha=0.2, color='#1f77b4')
ax2.set_ylabel('Cortante $V$ (kgf)', fontsize=12)
ax2.set_title(f'2. Diagrama de Força Cortante (Resultante W)', fontweight='bold', loc='left')
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.text(Distancia/2, F_resultante, f'W = {F_resultante:.1f} kgf', ha='center', va='bottom', fontsize=11, fontweight='bold', backgroundcolor='white')
# Anotação das componentes
text_props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax2.text(Distancia*0.05, F_resultante*0.9, f'$F_t$: {F_tangencial:.1f} kgf\n$F_r$: {F_radial:.1f} kgf', fontsize=10, bbox=text_props)

# Gráfico 3: Momento Fletor
ax3.plot(x, y_moment, color='#d62728', linewidth=2.5) # Vermelho
ax3.fill_between(x, y_moment, alpha=0.2, color='#d62728')
ax3.set_ylabel('Fletor $M_f$ (kgf.mm)', fontsize=12)
ax3.set_xlabel('Comprimento do Eixo (mm) [0 = Engrenagem | 40 = Mancal]', fontsize=12, fontweight='bold')
ax3.set_title(f'3. Diagrama de Momento Fletor (Máximo no Mancal)', fontweight='bold', loc='left')
ax3.grid(True, linestyle='--', alpha=0.7)
# Ponto Máximo
ax3.plot(Distancia, Momento_Max, 'ko') # Ponto preto no máximo
ax3.annotate(f'M_max\n{Momento_Max:.0f} kgf.mm', 
             xy=(Distancia, Momento_Max), 
             xytext=(Distancia-10, Momento_Max),
             arrowprops=dict(facecolor='black', shrink=0.05),
             ha='right', fontsize=11, fontweight='bold')

# --- 5. RESULTADOS TEXTUAIS NO CONSOLE ---
print("="*50)
print(f"RELATÓRIO DE CÁLCULO - EIXO ÁRVORE")
print("="*50)
print(f"1. GEOMETRIA E CARGA")
print(f"   Potência: {Potencia_cv} cv @ {Rotacao_rpm} RPM")
print(f"   Torque Real: {Torque:.2f} kgf.mm")
print(f"   Braço de Alavanca: {Distancia} mm")
print("-" * 30)
print(f"2. FORÇAS NO ENGRENAMENTO (Módulo {Modulo})")
print(f"   Força Tangencial (Ft): {F_tangencial:.2f} kgf")
print(f"   Força Radial (Fr):     {F_radial:.2f} kgf")
print(f"   Carga Resultante (W):  {F_resultante:.2f} kgf")
print("-" * 30)
print(f"3. DIMENSIONAMENTO (ASME Code)")
print(f"   Momento Fletor Max:    {Momento_Max:.2f} kgf.mm")
print(f"   Diâmetro Mínimo Calc:  {Diametro_Minimo:.2f} mm")
print(f"   Diâmetro Escolhido:    30.00 mm")
print(f"   Status: {'APROVADO' if 30 >= Diametro_Minimo else 'REPROVADO'}")
print("="*50)
plt.savefig('diagramas_eixo_scotch_yoke.png', dpi=300)
plt.show()