import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Verifica o artefato seguro
artifact_path = 'sphy_artifact.npz'
if not os.path.exists(artifact_path):
    print(f"ERRO: Artefato {artifact_path} ausente. Execute o gerador SPHY primeiro.")
    sys.exit(1)

print("Carregando telemetria para Análise de Supressão Ativa de Erros...")
data = np.load(artifact_path)

h_noise = data['noise']
h_var = data['var']
h_cvp_status = data['cvp_status']
frames = np.arange(len(h_noise))

# Identifica o frame exato do colapso
try:
    collapse_frame = np.where(h_cvp_status == True)[0][0]
except IndexError:
    collapse_frame = len(frames) - 1

# --- Cálculo das Taxas de Variação (Derivadas) ---
# Proteção de PI: Usamos o gradiente numérico dos dados brutos exportados.
# Valores negativos profundos provam a força de supressão do Atrator Topológico.
delta_noise = np.gradient(h_noise)
delta_var = np.gradient(h_var)

# --- Configuração do Dashboard Matplotlib ---
plt.style.use('dark_background')
fig, axs = plt.subplots(2, 1, figsize=(12, 8), facecolor='#0a0a0a')
fig.canvas.manager.set_window_title('SPHY Error Suppression Analytics')
fig.suptitle('TAXA DE SUPRESSÃO ATIVA DE ERROS (A.E.S.R.)\n[Ação de Correção do Atrator Topológico]', 
             color='white', fontsize=15, fontweight='bold')

# Função para plotar derivadas com preenchimento termodinâmico
def plot_derivative(ax, x, y, title, ylabel, color_line):
    ax.plot(x, y, color=color_line, linewidth=2, label='Taxa de Variação (Δ)')
    
    # Preenche a área negativa: A representação visual do "Esmagamento" de Erros
    ax.fill_between(x, y, 0, where=(y < 0), color='#ff3333', alpha=0.4, label='Supressão Ativa (Esmagamento)')
    ax.fill_between(x, y, 0, where=(y >= 0), color='#444444', alpha=0.3)
    
    # Linha zero (Estabilidade Perfeita / Lock)
    ax.axhline(0, color='white', linestyle='-', linewidth=1, alpha=0.5)
    
    # Marcação do instante da Geodésica Áurea
    ax.axvline(x=collapse_frame, color='#00ffcc', linestyle='--', linewidth=2, label='Colapso de Fase (Lock)')
    
    ax.set_title(title, color='white', pad=10, fontsize=12)
    ax.set_ylabel(ylabel, color='gray')
    ax.grid(color='#222222', linestyle=':', linewidth=1)
    ax.tick_params(colors='gray')
    ax.set_facecolor('#111111')
    ax.legend(loc='lower left', facecolor='#000000', edgecolor='#444444', labelcolor='white')

# Plot 1: Derivada do Ruído Térmico
plot_derivative(axs[0], frames, delta_noise, 
                'Derivada do Ruído Térmico (Δ mK / frame)', 
                'Δ Ruído', '#ffff00')

# Plot 2: Derivada da Variância de Raio
plot_derivative(axs[1], frames, delta_var, 
                'Esmagamento de Variância Espacial (Δ σ² / frame)', 
                'Δ Variância', '#ff9900')
axs[1].set_xlabel('Horizonte de Tempo (Frames)', color='gray')

# Anotação de Impacto apontando para o pico de máxima força corretiva
min_var_idx = np.argmin(delta_var[:collapse_frame+1]) # Busca o pico negativo antes do colapso
axs[1].annotate('MÁXIMA FORÇA DO\nTORQUE GRAVITACIONAL', 
                xy=(min_var_idx, delta_var[min_var_idx]), 
                xytext=(min_var_idx - 25, delta_var[min_var_idx] * 0.7),
                arrowprops=dict(facecolor='#ff3333', shrink=0.05, width=1.5, headwidth=8),
                color='#ff3333', fontweight='bold', fontsize=10, ha='center')

plt.tight_layout()
plt.show()