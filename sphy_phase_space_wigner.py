import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Verifica o artefato seguro (PI Protegida)
artifact_path = 'sphy_artifact.npz'
if not os.path.exists(artifact_path):
    print(f"ERROR: Artifact {artifact_path} missing. Execute the core generator first.")
    sys.exit(1)

print("Carregando telemetria para Distribuição de Espaço de Fase (Pseudo-Wigner)...")
data = np.load(artifact_path)

h_r = data['r']
h_theta = data['theta']
h_cvp_status = data['cvp_status']
total_frames = h_r.shape[0]

# Identifica o frame exato do colapso
try:
    collapse_frame = np.where(h_cvp_status == True)[0][0]
except IndexError:
    collapse_frame = total_frames - 1

# Seleção de três "fotografias" temporais para provar a evolução física
frame_initial = 0
frame_mid = collapse_frame // 2
frame_final = collapse_frame

# Função para converter coordenadas e gerar a matriz de densidade
def get_phase_space_density(frame_idx, bins=100):
    r = h_r[frame_idx]
    theta = h_theta[frame_idx]
    
    # Conversão de Polar para Cartesiano (Espaço de Fase X, Y)
    X = r * np.cos(theta)
    Y = r * np.sin(theta)
    
    # Limites do gráfico baseados na dispersão máxima
    limit = 1.3
    
    # Histograma 2D (Aproximação de densidade de probabilidade)
    heatmap, xedges, yedges = np.histogram2d(X, Y, bins=bins, range=[[-limit, limit], [-limit, limit]])
    return heatmap.T, limit

# --- Configuração do Dashboard Matplotlib (Estilo Paper Científico) ---
plt.style.use('dark_background')
fig, axs = plt.subplots(1, 3, figsize=(18, 6), facecolor='#0a0a0a')
fig.canvas.manager.set_window_title('SPHY Phase Space Distribution')
fig.suptitle('EVOLUÇÃO DO ESPAÇO DE FASE (APROXIMAÇÃO DE WIGNER)\n[Transição de Estado Térmico para Estado Coerente Comprimido]', 
             color='white', fontsize=16, fontweight='bold', y=0.95)

titles = [
    f'T=0: Estado Térmico (Alta Entropia)',
    f'T={frame_mid}: Coerção Topológica',
    f'T={frame_final}: Estado Coerente SPHY (Lock)'
]

frames_to_plot = [frame_initial, frame_mid, frame_final]

for i, ax in enumerate(axs):
    heatmap, limit = get_phase_space_density(frames_to_plot[i])
    
    # Renderiza o mapa de calor com colormap 'magma' para representar energia
    im = ax.imshow(heatmap, extent=[-limit, limit, -limit, limit], origin='lower', cmap='magma', interpolation='gaussian')
    
    # Marcadores de limite geométrico (A Geodésica)
    circle = plt.Circle((0, 0), 1.0/((1+np.sqrt(5))/2)**2, color='#00ffcc', fill=False, linestyle='--', alpha=0.5, linewidth=1)
    ax.add_patch(circle)
    
    # Estilização do eixo (Padrão Físico)
    ax.set_title(titles[i], color='white', pad=15, fontsize=13)
    ax.set_xlabel('Quadratura X (Posição de Fase)', color='gray')
    if i == 0:
        ax.set_ylabel('Quadratura Y (Momento de Fase)', color='gray')
    
    ax.axhline(0, color='#333333', linewidth=1)
    ax.axvline(0, color='#333333', linewidth=1)
    ax.grid(False)
    ax.tick_params(colors='gray')
    ax.set_facecolor('#050505')

# Barra de escala de probabilidade
cbar_ax = fig.add_axes([0.92, 0.15, 0.015, 0.7])
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.set_label('Densidade de Probabilidade Quântica |Ψ|²', color='gray', rotation=270, labelpad=20)
cbar.ax.tick_params(colors='gray')

plt.subplots_adjust(left=0.05, right=0.9, wspace=0.2, top=0.8)
plt.show()
