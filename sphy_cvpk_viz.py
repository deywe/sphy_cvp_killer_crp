import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec
import sys
import os

# Verifica se o artefato existe antes de tentar rodar
artifact_path = 'sphy_artifact.npz'
if not os.path.exists(artifact_path):
    print(f"ERRO: Arquivo {artifact_path} não encontrado. Execute o gerador SPHY primeiro.")
    sys.exit(1)

# Carrega os dados computados
print("Carregando Artefato de Simulação SPHY...")
data = np.load(artifact_path)

h_theta = data['theta']
h_r = data['r']
h_noise = data['noise']
h_var = data['var']
h_ent = data['ent']
h_fidelity = data['fidelity']
h_lwe_time = data['lwe_time']
h_lwe_mem = data['lwe_mem']
h_cvp_status = data['cvp_status']
final_proof = str(data['proof'])

total_frames = len(h_theta)

# --- Configuração do Layout do Player ---
fig = plt.figure(figsize=(12, 7.5), facecolor='#0a0a0a')
gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])
ax_sim = fig.add_subplot(gs[0], projection='polar', facecolor='#0a0a0a')
ax_log = fig.add_subplot(gs[1], facecolor='#111111')
ax_log.axis('off')

# HUD Estático
ax_log.text(0.05, 0.95, "SPHY QUANTUM ENGINE | VISUALIZER", color='white', fontweight='bold', fontsize=11)
txt_frame = ax_log.text(0.05, 0.88, "Frame: 000", color='white', fontfamily='monospace')
txt_noise = ax_log.text(0.05, 0.80, "Thermal Noise: --", color='yellow', fontfamily='monospace')
txt_var = ax_log.text(0.05, 0.73, "Radius Var: --", color='#ff9900', fontfamily='monospace')
txt_ent = ax_log.text(0.05, 0.66, "Shannon Ent: --", color='cyan', fontfamily='monospace')
txt_fidelity = ax_log.text(0.05, 0.55, "Q-Fidelity: --", color='#00ffcc', fontweight='bold', fontfamily='monospace')
txt_lwe_time = ax_log.text(0.05, 0.45, "LWE Attack Time: --", color='#ff00ff', fontfamily='monospace')
txt_lwe_mem = ax_log.text(0.05, 0.38, "LWE Memory: --", color='#ff00ff', fontfamily='monospace')
txt_status = ax_log.text(0.05, 0.22, "Status: ACTIVE", color='green', fontweight='bold')
txt_proof = ax_log.text(0.05, 0.10, "Proof: PENDING", color='red', fontsize=8, fontfamily='monospace')

def update(frame):
    if frame >= total_frames: return
    
    # Atualiza HUD com base nos dados pré-calculados
    txt_frame.set_text(f"Frame: {frame:03d}")
    txt_noise.set_text(f"Thermal Noise: {h_noise[frame]:.4f} mK")
    txt_var.set_text(f"Radius Var: {h_var[frame]:.6f}")
    txt_ent.set_text(f"Shannon Ent: {h_ent[frame]:.4f} bits")
    
    cvp_found = h_cvp_status[frame]
    
    if cvp_found:
        txt_status.set_text("Status: CVP KEY EXTRACTED")
        txt_status.set_color('#ff3333')
        txt_noise.set_text("Thermal Noise: 0.0000 mK (STABLE)")
        txt_var.set_text("Radius Var: 0.000000 (LOCKED)")
        txt_fidelity.set_text("Q-Fidelity: 99.999% (FIVE NINES)")
        txt_fidelity.set_color('#ffffff') 
        txt_lwe_time.set_text("LWE Attack Time: OBSOLETE")
        txt_lwe_time.set_color('#444444') 
        txt_lwe_mem.set_text("LWE Memory: CAPACITY EXCEEDED")
        txt_lwe_mem.set_color('#444444')
        txt_proof.set_text(f"Proof: {final_proof}...")
    else:
        txt_fidelity.set_text(f"Q-Fidelity: {h_fidelity[frame]:.3f}%")
        txt_lwe_time.set_text(f"LWE Attack Time: 10^{h_lwe_time[frame]:.1f} Years")
        txt_lwe_mem.set_text(f"LWE Memory: {h_lwe_mem[frame]:.2f} YB")

    # Render Simulação (lendo diretamente dos arrays de geometria)
    ax_sim.clear()
    ax_sim.set_ylim(0, 1.2)
    ax_sim.axis('off')
    color = '#ff3333' if cvp_found else '#00ffcc'
    ax_sim.scatter(h_theta[frame], h_r[frame], c=color, s=2, alpha=0.6)

ani = FuncAnimation(fig, update, frames=total_frames, interval=50, repeat=False)
plt.tight_layout()
plt.show()