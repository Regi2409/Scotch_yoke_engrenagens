import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.gridspec as gridspec

# PARÂMETROS E DADOS DE ENTRADA
R_mm = 41.21             
R_m  = R_mm / 1000.0     
RPM_motor_in = 60.0      
i_red = 1              
m_yoke_kg = 0.061        

# Cálculos de Frequência
w_motor = (RPM_motor_in * 2 * np.pi) / 60.0
w_out   = w_motor * i_red                    

# Vetores de Tempo
periodo = 2 * np.pi / w_out
t_max = 2 * periodo
num_points = 1000
t_vals = np.linspace(0, t_max, num_points)
theta_vals = w_out * t_vals

# CÁLCULOS CINEMÁTICOS
x_vals = R_mm * np.cos(theta_vals)
v_vals = -R_mm * w_out * np.sin(theta_vals)
a_vals = -R_mm * (w_out**2) * np.cos(theta_vals) # em mm/s²

# CÁLCULOS DINÂMICOS 
a_vals_si = a_vals / 1000.0 # Convertendo para m/s²
F_inercial = m_yoke_kg * a_vals_si # Newton

# Torque na Manivela (Saída)
Torque_crank = m_yoke_kg * (R_m**2) * (w_out**2) * np.sin(theta_vals) * np.cos(theta_vals)

# Torque no Motor (Entrada) - Conservação de Potência
Torque_motor = Torque_crank * (w_out / w_motor)

# Potência
Power_vals = Torque_crank * w_out

# IMPRESSÃO DO RELATÓRIO COMPLETO
print("\n" + "="*50)
print(f"RELATORIO DE ANALISE DINAMICA - SCOTCH YOKE (Grupo 2)")
print("="*50)
print(f"DADOS DE ENTRADA:")
print(f" > Raio (r):             {R_mm} mm")
print(f" > Massa Movel (m):      {m_yoke_kg*1000} g")
print(f" > Rotacao Entrada:      {RPM_motor_in} RPM")
print(f" > Rotacao Saida:        {RPM_motor_in * i_red} RPM ({w_out:.2f} rad/s)")
print("-" * 50)
print(f"RESULTADOS MAXIMOS (PICOS CINEMATICOS):")
print(f" > Posicao Max (+/-):    {np.max(np.abs(x_vals)):.2f} mm")
print(f" > Velocidade Max:       {np.max(np.abs(v_vals)):.2f} mm/s")
print(f" > Aceleracao Max:       {np.max(np.abs(a_vals_si)):.3f} m/s²")
print("-" * 50)
print(f"ANALISE CINETICA (DINAMICA):")
print(f" > Forca Inercial Max:   {np.max(np.abs(F_inercial)):.4f} N")
print(f" > Torque Max Manivela:  {np.max(np.abs(Torque_crank)):.4f} N.m")
print(f" > Torque Max Motor:     {np.max(np.abs(Torque_motor)):.4f} N.m")
print(f" > Potencia Maxima:      {np.max(np.abs(Power_vals)):.4f} W")
print("="*50 + "\n")

# CONFIGURAÇÃO VISUAL
fig = plt.figure(figsize=(19, 12)) 
fig.canvas.manager.set_window_title('Simulação Completa - Grupo 2 CEFET-MG')

gs = gridspec.GridSpec(4, 2, width_ratios=[1, 1.6]) 

# Lado Esquerdo: O Mecanismo 
ax_mech = fig.add_subplot(gs[:, 0])
ax_mech.set_title("Visualização do Mecanismo", fontsize=20, pad=25, fontweight='bold')

ax_mech.set_xlim(-120, 120)
ax_mech.set_ylim(-190, 130) 
ax_mech.set_aspect('equal')
ax_mech.axis('off')

# Desenhos Estáticos
ax_mech.add_patch(plt.Circle((0, 0), R_mm, color='lightgray', fill=True, alpha=0.3))
ax_mech.add_patch(plt.Circle((0, 0), R_mm, color='gray', fill=False, linestyle='--'))
ax_mech.text(0, -R_mm-12, 'Centro Rotação', ha='center', fontsize=12, color='gray')

# Elementos Móveis 
line_crank, = ax_mech.plot([], [], 'o-', lw=7, color='#333333', ms=12, label='Manivela')
line_slot,  = ax_mech.plot([], [], '-', lw=4, color='#d62728')
rect_yoke,  = ax_mech.plot([], [], '-', lw=9, color='#1f77b4')
point_pin,  = ax_mech.plot([], [], 'o', color='#ff7f0e', ms=16, zorder=5)

text_info = ax_mech.text(0, -110, '', ha='center', va='center', fontsize=18, fontweight='bold',
                         bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=1.0, edgecolor='gray'))

# Lado Direito: 4 Gráficos Empilhados 

# Configuração comum de fonte
LABEL_SIZE = 16
TICK_SIZE = 14
LINE_WIDTH = 3.5

# Posição
ax_pos = fig.add_subplot(gs[0, 1])
ax_pos.plot(t_vals, x_vals, 'b-', lw=LINE_WIDTH)
ax_pos.set_ylabel('Pos. (mm)', fontsize=LABEL_SIZE, fontweight='bold')
ax_pos.tick_params(axis='both', labelsize=TICK_SIZE)
ax_pos.grid(True, linestyle=':', alpha=0.6)
ax_pos.set_xticklabels([]) 
point_pos, = ax_pos.plot([], [], 'bo', ms=10)

# Velocidade
ax_vel = fig.add_subplot(gs[1, 1], sharex=ax_pos)
ax_vel.plot(t_vals, v_vals, 'g-', lw=LINE_WIDTH)
ax_vel.set_ylabel('Vel. (mm/s)', fontsize=LABEL_SIZE, fontweight='bold')
ax_vel.tick_params(axis='both', labelsize=TICK_SIZE)
ax_vel.grid(True, linestyle=':', alpha=0.6)
ax_vel.set_xticklabels([])
point_vel, = ax_vel.plot([], [], 'go', ms=10)

# Aceleração
ax_acc = fig.add_subplot(gs[2, 1], sharex=ax_pos)
ax_acc.plot(t_vals, a_vals_si, color='purple', lw=LINE_WIDTH) 
ax_acc.set_ylabel('Acel. (m/s²)', fontsize=LABEL_SIZE, fontweight='bold')
ax_acc.tick_params(axis='both', labelsize=TICK_SIZE)
ax_acc.grid(True, linestyle=':', alpha=0.6)
ax_acc.set_xticklabels([])
point_acc, = ax_acc.plot([], [], 'o', color='purple', ms=10)

# Torque
ax_tor = fig.add_subplot(gs[3, 1], sharex=ax_pos)
ax_tor.plot(t_vals, Torque_crank, 'r-', lw=LINE_WIDTH)
ax_tor.set_ylabel('Torque (N.m)', fontsize=LABEL_SIZE, fontweight='bold')
ax_tor.set_xlabel('Tempo (s)', fontsize=LABEL_SIZE, fontweight='bold')
ax_tor.tick_params(axis='both', labelsize=TICK_SIZE)
ax_tor.grid(True, linestyle=':', alpha=0.6)
point_tor, = ax_tor.plot([], [], 'ro', ms=10)

# Linha vertical comum
vlines = [ax.axvline(0, color='k', ls='--', alpha=0.5, lw=2) for ax in [ax_pos, ax_vel, ax_acc, ax_tor]]

# UPDATE LOOP
def update(val):
    t_curr = val
    idx = (np.abs(t_vals - t_curr)).argmin()
    
    # Valores Instantâneos
    theta = theta_vals[idx]
    x_c = x_vals[idx]
    v_c = v_vals[idx]
    a_c = a_vals_si[idx]
    tau_c = Torque_crank[idx]
    
    # Mecanismo
    pin_x = R_mm * np.cos(theta)
    pin_y = R_mm * np.sin(theta)
    line_crank.set_data([0, pin_x], [0, pin_y])
    point_pin.set_data([pin_x], [pin_y])
    rect_yoke.set_data([pin_x - 55, pin_x + 55], [0, 0])
    line_slot.set_data([pin_x, pin_x], [-30, 30])
    
    # Texto
    text_info.set_text(
        f"Tempo: {t_curr:.2f} s\n"
        f"Ângulo: {np.degrees(theta)%360:.0f}°\n"
        f"-----------------\n"
        f"X: {x_c:.1f} mm\n"
        f"V: {v_c:.1f} mm/s\n"
        f"A: {a_c:.2f} m/s²\n"
        f"T: {tau_c:.4f} N.m"
    )
    
    # Gráficos
    point_pos.set_data([t_curr], [x_c])
    point_vel.set_data([t_curr], [v_c])
    point_acc.set_data([t_curr], [a_c])
    point_tor.set_data([t_curr], [tau_c])
    
    for line in vlines:
        line.set_xdata([t_curr])
        
    fig.canvas.draw_idle()

# Slider
ax_slider = plt.axes([0.25, 0.01, 0.50, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Tempo', 0, t_max, valinit=0)
slider.on_changed(update)

update(0)
plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.show()