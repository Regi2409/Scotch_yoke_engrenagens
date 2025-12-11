import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button # Importei Button para o recurso extra
import matplotlib.gridspec as gridspec

# CONFIGURAÇÃO
R = 41.21
RPM_motor = 60
i = 0.5
w_motor = (RPM_motor * 2 * np.pi) / 60
w_out = w_motor * i

# LAYOUT
fig = plt.figure(figsize=(12, 8))
gs = gridspec.GridSpec(3, 2, width_ratios=[1, 1.5], hspace=0.4, wspace=0.3)

ax_mech = fig.add_subplot(gs[:, 0])
ax_mech.set_title("Simulação Visual: Scotch Yoke", fontsize=16, fontweight='bold')

ax_mech.set_xlim(-110, 110)
ax_mech.set_ylim(-160, 80) 
ax_mech.set_aspect('equal')
ax_mech.axis('off')

# Subplots Gráficos
ax_pos = fig.add_subplot(gs[0, 1])
ax_vel = fig.add_subplot(gs[1, 1], sharex=ax_pos)
ax_acc = fig.add_subplot(gs[2, 1], sharex=ax_pos)

# Dados
t_max = 4 * np.pi / w_out
t_vals = np.linspace(0, t_max, 500)
theta_vals = w_out * t_vals
x_vals = R * np.cos(theta_vals)
v_vals = -R * w_out * np.sin(theta_vals)
a_vals = -R * (w_out**2) * np.cos(theta_vals)

# Estilização
label_font = {'size': 12, 'weight': 'bold'}
ax_pos.plot(t_vals, x_vals, 'b-', lw=2)
ax_pos.set_ylabel('Posição (mm)', **label_font)
ax_pos.grid(True, linestyle='--', alpha=0.6)

ax_vel.plot(t_vals, v_vals, 'orange', lw=2)
ax_vel.set_ylabel('Vel. (mm/s)', **label_font)
ax_vel.grid(True, linestyle='--', alpha=0.6)

ax_acc.plot(t_vals, a_vals, 'r-', lw=2)
ax_acc.set_ylabel('Acel. (mm/s²)', **label_font)
ax_acc.set_xlabel('Tempo (s)', **label_font)
ax_acc.grid(True, linestyle='--', alpha=0.6)

# DESENHOS 
# Mecanismo
gear_circle = plt.Circle((0, 0), 40, color='#8B4513', fill=False, lw=3)
ax_mech.add_patch(gear_circle)
pin_dot, = ax_mech.plot([], [], 'o', color='green', ms=15, zorder=5)
crank_line, = ax_mech.plot([], [], '-', color='gray', lw=3)
rack_line, = ax_mech.plot([], [], '-', color='#FFD700', lw=10, solid_capstyle='round')
slot_line, = ax_mech.plot([], [], '-', color='black', lw=1.5)

# Pontos nos gráficos
dot_pos, = ax_pos.plot([], [], 'bo', ms=10)
dot_vel, = ax_vel.plot([], [], 'o', color='orange', ms=10)
dot_acc, = ax_acc.plot([], [], 'ro', ms=10)
vertical_lines = [ax.axvline(0, color='k', linestyle=':', alpha=0.5) for ax in [ax_pos, ax_vel, ax_acc]]

info_text = ax_mech.text(0, -110, '', ha='center', va='center', fontsize=16, fontweight='bold',
                         bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=1.0, edgecolor='gray'))

# ATUALIZAÇÃO
def update(val):
    t_current = val
    theta = w_out * t_current
    
    # Física
    x = R * np.cos(theta)
    v = -R * w_out * np.sin(theta)
    a = -R * (w_out**2) * np.cos(theta)
    
    # Desenho Mecanismo
    pin_x = R * np.cos(theta)
    pin_y = R * np.sin(theta)
    
    pin_dot.set_data([pin_x], [pin_y])
    crank_line.set_data([0, pin_x], [0, pin_y])
    rack_line.set_data([pin_x - 60, pin_x + 60], [0, 0]) # Y=0 fixo para a cremalheira
    slot_line.set_data([pin_x, pin_x], [-30, 30])
    
    # Desenho Gráficos
    dot_pos.set_data([t_current], [x])
    dot_vel.set_data([t_current], [v])
    dot_acc.set_data([t_current], [a])
    
    for line in vertical_lines:
        line.set_xdata([t_current])
        
    info_text.set_text(
        f"Tempo: {t_current:.2f} s\n"
        f"Manivela: {np.degrees(theta)%360:.1f}°\n"
        f"-----------------\n"
        f"X: {x:.2f} mm\n"
        f"V: {v:.2f} mm/s\n"
        f"A: {a:.2f} mm/s²"
    )
    fig.canvas.draw_idle()

# SLIDER 
ax_slider = plt.axes([0.2, 0.02, 0.6, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Tempo (s)', 0, t_max, valinit=0)
slider.on_changed(update)

# Inicializa
update(0)
plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.show()