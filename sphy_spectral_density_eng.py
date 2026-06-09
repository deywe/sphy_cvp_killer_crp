import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Check for the secure artifact
artifact_path = 'sphy_artifact.npz'
if not os.path.exists(artifact_path):
    print(f"ERROR: Artifact {artifact_path} missing. Execute the SPHY core generator first.")
    sys.exit(1)

print("Loading telemetry for Phase Spectral Density analysis...")
data = np.load(artifact_path)

h_theta = data['theta']  # Matrix containing the phases (angles) of all qubits
h_cvp_status = data['cvp_status']
total_frames = h_theta.shape[0]
num_qubits = h_theta.shape[1]

# Identify the collapse frame
try:
    collapse_frame = np.where(h_cvp_status == True)[0][0]
except IndexError:
    collapse_frame = total_frames - 1

# --- 2D Histogram Calculation (Spectral Density) ---
# IP is protected: we only use simple statistical binning
num_bins_y = 120  # Y-axis resolution (Angular Phase)
heatmap = np.zeros((num_bins_y, total_frames))

for t in range(total_frames):
    # Ensure angles are within the [0, 2π] range
    theta_mod = np.mod(h_theta[t], 2 * np.pi)
    
    # Count how many qubits are in each "slice" of the circle at that exact frame
    counts, _ = np.histogram(theta_mod, bins=num_bins_y, range=(0, 2*np.pi))
    heatmap[:, t] = counts

# --- Matplotlib Dashboard Configuration ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(14, 7), facecolor='#0a0a0a')
fig.canvas.manager.set_window_title('SPHY Phase Spectral Density')

# Plot the heatmap using the 'inferno' colormap to highlight density
im = ax.imshow(heatmap, aspect='auto', origin='lower', cmap='inferno',
               extent=[0, total_frames, 0, 2*np.pi], interpolation='nearest')

# Synchronization Event Marker
ax.axvline(x=collapse_frame, color='#00ffcc', linestyle='--', linewidth=2.5, 
           label='SPHY Phase Lock (CVP Extracted)')

# Professional Styling
ax.set_title('PHASE SPECTRAL DENSITY\n[Organic Qubit Convergence into Golden Synchronization]',
             color='white', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Time Horizon (Frames)', color='gray', fontsize=12)
ax.set_ylabel('Angular Phase Space (Radians)', color='gray', fontsize=12)

# Configure the Y-axis to show classic Radian markings
ax.set_yticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax.set_yticklabels(['0', 'π/2', 'π', '3π/2', '2π'], color='gray', fontsize=11)
ax.tick_params(colors='gray')

# Density Colorbar
cbar = fig.colorbar(im, ax=ax, pad=0.02)
cbar.set_label('Qubit Density (Angular Concentration)', color='gray', rotation=270, labelpad=20)
cbar.ax.tick_params(colors='gray')

ax.legend(loc='upper right', facecolor='#000000', edgecolor='#444444', labelcolor='white')

plt.tight_layout()
plt.show()