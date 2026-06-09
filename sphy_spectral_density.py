import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Verifica o artefato seguro
artifact_path = 'sphy_artifact.npz'
if not os.path.exists(artifact_path):
    print(f"ERRO: Artefato {artifact_path} ausente. Execute o gerador SPHY primeiro.")
    sys.exit(1)

print("Carregando telemetria para análise de Densidade Espectral de Fase...")
data = np.load(artifact_path)

h_theta = data['theta']  # Matriz com as fases (ângulos) de todos os qubits
h_cvp_status = data['cvp_status']
total_frames = h_theta.shape[0]
num_qubits = h_theta.shape[1]

# Identifica o frame de colapso
try:
    collapse_frame = np.where(h_cvp_status == True)[0][0]
except IndexError:
    collapse_frame = total_frames - 1

# --- Cálculo do Histograma 2D (Densidade Espectral) ---
# A PI está protegida: usamos apenas agrupamento estatístico simples (bins)
num_bins_y = 120  # Resolução do eixo Y (Fase Angular)
heatmap = np.zeros((num_bins_y, total_frames))

for t in range(total_frames):
    # Garante que os ângulos estejam no intervalo [0, 2π]
    theta_mod = np.mod(h_theta[t], 2 * np.pi)
    
    # Conta quantos qubits estão em cada "fatia" do círculo naquele exato frame
    counts, _ = np.histogram(theta_mod, bins=num_bins_y, range=(0, 2*np.pi))
    heatmap[:, t] = counts

# --- Configuração do Dashboard Matplotlib ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(14, 7), facecolor='#0a0a0a')
fig.canvas.manager.set_window_title('SPHY Phase Spectral Density')

# Plota o mapa de calor usando colormap 'inferno' para destacar a densidade
im = ax.imshow(heatmap, aspect='auto', origin='lower', cmap='inferno',
               extent=[0, total_frames, 0, 2*np.pi], interpolation='nearest')

# Marcador do Evento de Sincronização
ax.axvline(x=collapse_frame, color='#00ffcc', linestyle='--', linewidth=2.5, 
           label='SPHY Phase Lock (CVP Extracted)')

# Estilização Profissional
ax.set_title('DENSIDADE ESPECTRAL DE FASE (PHASE SPECTRAL DENSITY)\n[Convergência Orgânica de Qubits em Sincronização Áurea]',
             color='white', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Horizonte de Tempo (Frames)', color='gray', fontsize=12)
ax.set_ylabel('Espaço de Fase Angular (Radianos)', color='gray', fontsize=12)

# Configura o eixo Y para mostrar marcações em Radianos clássicos
ax.set_yticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax.set_yticklabels(['0', 'π/2', 'π', '3π/2', '2π'], color='gray', fontsize=11)
ax.tick_params(colors='gray')

# Barra de Densidade (Colorbar)
cbar = fig.colorbar(im, ax=ax, pad=0.02)
cbar.set_label('Densidade de Qubits (Concentração Angular)', color='gray', rotation=270, labelpad=20)
cbar.ax.tick_params(colors='gray')

ax.legend(loc='upper right', facecolor='#000000', edgecolor='#444444', labelcolor='white')

plt.tight_layout()
plt.show()