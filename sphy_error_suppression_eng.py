import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Check for the secure artifact
artifact_path = 'sphy_artifact.npz'
if not os.path.exists(artifact_path):
    print(f"ERROR: Artifact {artifact_path} missing. Execute the core generator first.")
    sys.exit(1)

print("Loading telemetry for Active Error Suppression Rate Analysis...")
data = np.load(artifact_path)

h_noise = data['noise']
h_var = data['var']
h_cvp_status = data['cvp_status']
frames = np.arange(len(h_noise))

# Identify the exact frame of collapse
try:
    collapse_frame = np.where(h_cvp_status == True)[0][0]
except IndexError:
    collapse_frame = len(frames) - 1

# --- Rate of Change Calculation (Derivatives) ---
delta_noise = np.gradient(h_noise)
delta_var = np.gradient(h_var)

# --- Matplotlib Dashboard Configuration (English Version) ---
plt.style.use('dark_background')
fig, axs = plt.subplots(2, 1, figsize=(12, 8), facecolor='#0a0a0a')
fig.canvas.manager.set_window_title('SPHY Error Suppression Analytics')
fig.suptitle('ACTIVE ERROR SUPPRESSION RATE (A.E.S.R.)\n[Topological Attractor Corrective Action]', 
             color='white', fontsize=15, fontweight='bold')

# Helper function for derivative plotting
def plot_derivative(ax, x, y, title, ylabel, color_line):
    ax.plot(x, y, color=color_line, linewidth=2, label='Variation Rate (Δ)')
    
    # Fill negative area: Visual representation of Error "Crushing"
    ax.fill_between(x, y, 0, where=(y < 0), color='#ff3333', alpha=0.4, label='Active Suppression (Crushing)')
    ax.fill_between(x, y, 0, where=(y >= 0), color='#444444', alpha=0.3)
    
    # Zero line (Perfect Stability / Lock)
    ax.axhline(0, color='white', linestyle='-', linewidth=1, alpha=0.5)
    
    # Golden Geodesic Mark
    ax.axvline(x=collapse_frame, color='#00ffcc', linestyle='--', linewidth=2, label='Phase Collapse (Lock)')
    
    ax.set_title(title, color='white', pad=10, fontsize=12)
    ax.set_ylabel(ylabel, color='gray')
    ax.grid(color='#222222', linestyle=':', linewidth=1)
    ax.tick_params(colors='gray')
    ax.set_facecolor('#111111')
    ax.legend(loc='lower left', facecolor='#000000', edgecolor='#444444', labelcolor='white')

# Plot 1: Thermal Noise Derivative
plot_derivative(axs[0], frames, delta_noise, 
                'Thermal Noise Derivative (Δ mK / frame)', 
                'Δ Noise', '#ffff00')

# Plot 2: Radius Variance Derivative
plot_derivative(axs[1], frames, delta_var, 
                'Spatial Variance Crushing (Δ σ² / frame)', 
                'Δ Variance', '#ff9900')
axs[1].set_xlabel('Time Horizon (Frames)', color='gray')

# Maximum Corrective Force Annotation
min_var_idx = np.argmin(delta_var[:collapse_frame+1])
axs[1].annotate('MAXIMUM GRAVITATIONAL\nTORQUE FORCE', 
                xy=(min_var_idx, delta_var[min_var_idx]), 
                xytext=(min_var_idx - 25, delta_var[min_var_idx] * 0.7),
                arrowprops=dict(facecolor='#ff3333', shrink=0.05, width=1.5, headwidth=8),
                color='#ff3333', fontweight='bold', fontsize=10, ha='center')

plt.tight_layout()
plt.show()