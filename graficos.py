import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.gridspec as gridspec

# --- 1. CONFIGURAÇÃO DOS PARÂMETROS DO SEU MECANISMO ---
# Baseado nas medidas que você forneceu e análise das imagens
R = 41.21          # Raio da manivela (mm)
RPM_motor = 60     # Rotação de entrada (Arbitrado para simulação)
i = 0.5            # Relação de transmissão (15 dentes / 30 dentes)

# Cálculos iniciais de frequência
w_motor = (RPM_motor * 2 * np.pi) / 60
w_out = w_motor * i  # Velocidade angular da engrenagem amarela (rad/s)

# --- 2. PREPARAÇÃO DA ÁREA DE PLOTAGEM ---
fig = plt.figure(figsize=(12, 8))
gs = gridspec.GridSpec(3, 2, width_ratios=[1, 1.5])

# Subplot do Mecanismo (Esquerda)
ax_mech = fig.add_subplot(gs[:, 0])
ax_mech.set_title("Simulação Visual: Scotch Yoke", fontsize=14, fontweight='bold')
ax_mech.set_xlim(-100, 100)
ax_mech.set_ylim(-100, 100)
ax_mech.set_aspect('equal')
ax_mech.axis('off') # Remove eixos para ficar mais limpo

# Subplots dos Gráficos (Direita)
ax_pos = fig.add_subplot(gs[0, 1])
ax_vel = fig.add_subplot(gs[1, 1], sharex=ax_pos)
ax_acc = fig.add_subplot(gs[2, 1], sharex=ax_pos)

# Dados para os gráficos (2 ciclos completos)
t_max = 4 * np.pi / w_out # Tempo para 2 voltas
t_vals = np.linspace(0, t_max, 500)
theta_vals = w_out * t_vals

# Equações Cinemáticas (Baseado na Aula 08 e seus dados)
x_vals = R * np.cos(theta_vals)
v_vals = -R * w_out * np.sin(theta_vals)
a_vals = -R * (w_out**2) * np.cos(theta_vals)

# Desenhar as curvas estáticas
ax_pos.plot(t_vals, x_vals, 'b-')
ax_pos.set_ylabel('Posição (mm)')
ax_pos.grid(True, linestyle='--', alpha=0.6)

ax_vel.plot(t_vals, v_vals, 'orange')
ax_vel.set_ylabel('Vel. (mm/s)')
ax_vel.grid(True, linestyle='--', alpha=0.6)

ax_acc.plot(t_vals, a_vals, 'r-')
ax_acc.set_ylabel('Acel. (mm/s²)')
ax_acc.set_xlabel('Tempo (s)')
ax_acc.grid(True, linestyle='--', alpha=0.6)

# --- 3. ELEMENTOS GRÁFICOS MÓVEIS (O QUE VAI SE MEXER) ---

# No mecanismo
# Engrenagem (Círculo)
gear_circle = plt.Circle((0, 0), 40, color='#8B4513', fill=False, lw=3, label='Engrenagem') 
ax_mech.add_patch(gear_circle)
# Pino (Ponto Verde)
pin_dot, = ax_mech.plot([], [], 'o', color='green', ms=15, zorder=5)
# Raio da Manivela (Linha)
crank_line, = ax_mech.plot([], [], '-', color='gray', lw=2)
# Cremalheira (Retângulo Amarelo e Linha de Centro)
rack_line, = ax_mech.plot([], [], '-', color='#FFD700', lw=8, solid_capstyle='round') # Amarelo Ouro
slot_line, = ax_mech.plot([], [], '-', color='black', lw=1) # Ranhura vertical imaginária

# Nos gráficos (Pontos que indicam o valor atual)
dot_pos, = ax_pos.plot([], [], 'bo', ms=8)
dot_vel, = ax_vel.plot([], [], 'o', color='orange', ms=8)
dot_acc, = ax_acc.plot([], [], 'ro', ms=8)
vertical_lines = [ax.axvline(0, color='k', linestyle=':', alpha=0.5) for ax in [ax_pos, ax_vel, ax_acc]]

# Texto de Leitura de Dados
info_text = ax_mech.text(0, -80, '', ha='center', fontsize=12, 
                         bbox=dict(boxstyle="round", facecolor='white', alpha=0.9))

# --- 4. FUNÇÃO DE ATUALIZAÇÃO
def update(val):
    t_current = val
    theta = w_out * t_current
    
    # 1. Calcular valores instantâneos (Cinemática Analítica)
    x = R * np.cos(theta)
    v = -R * w_out * np.sin(theta)
    a = -R * (w_out**2) * np.cos(theta)
    
    # 2. Atualizar desenho do Mecanismo
    # Posição do pino (Gira)
    pin_x = R * np.cos(theta)
    pin_y = R * np.sin(theta)
    
    pin_dot.set_data([pin_x], [pin_y])
    crank_line.set_data([0, pin_x], [0, pin_y])
    
    # Posição da Cremalheira (Translada Horizontalmente)
    # Desenhamos uma linha longa horizontal que se move junto com o pino em X
    rack_line.set_data([pin_x - 60, pin_x + 60], [0, 0]) # Cremalheira tem 120mm visuais
    
    # Ranhura (Linha vertical onde o pino corre)
    slot_line.set_data([pin_x, pin_x], [-30, 30])
    
    # 3. Atualizar Gráficos
    dot_pos.set_data([t_current], [x])
    dot_vel.set_data([t_current], [v])
    dot_acc.set_data([t_current], [a])
    
    for line in vertical_lines:
        line.set_xdata([t_current])
        
    # 4. Atualizar Texto
    info_text.set_text(
        f"Tempo: {t_current:.2f} s\n"
        f"Ângulo Manivela: {np.degrees(theta)%360:.1f}°\n"
        f"-----------------------\n"
        f"POSIÇÃO (X): {x:.2f} mm\n"
        f"VELOCIDADE: {v:.2f} mm/s\n"
        f"ACELERAÇÃO: {a:.2f} mm/s²"
    )
    
    fig.canvas.draw_idle()

# --- 5. CRIAR O SLIDER ---
# Posição do slider [esquerda, baixo, largura, altura]
ax_slider = plt.axes([0.2, 0.02, 0.6, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Tempo (s)', 0, t_max, valinit=0)

# Conectar o slider à função de atualização
slider.on_changed(update)

# Chamada inicial para desenhar o estado zero
update(0)

plt.tight_layout(rect=[0, 0.05, 1, 1]) # Ajusta margens para o slider não sumir
plt.show()