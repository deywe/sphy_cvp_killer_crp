import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import sys

# Check for the secure opaque artifact
artifact_path = 'sphy_artifact.npz'
if not os.path.exists(artifact_path):
    print(f"ERROR: Artifact {artifact_path} missing. Run the core generator first.")
    sys.exit(1)

print("Loading secure SPHY telemetry...")
data = np.load(artifact_path)
h_var = data['var']
h_cvp_status = data['cvp_status']
total_frames = len(h_var)

# Find the point of absolute convergence
try:
    collapse_frame = np.where(h_cvp_status == True)[0][0]
except IndexError:
    collapse_frame = total_frames - 1

# --- 3D Grid Generation for the Cost Landscape ---
# We map Frames (Time) vs Angular Domain (Phase Space) 
# to calculate the Lattice Vector Error Margin (Z-axis)
frames_grid = np.arange(total_frames)
phase_domain = np.linspace(0, 2 * np.pi, 60)
F, P = np.meshgrid(frames_grid, phase_domain)

# Initialize the Lattice Distance Surface
Z_surface = np.zeros_like(F, dtype=float)

for t in range(total_frames):
    # The mathematical topology of the traditional Lattice hardness (CVP)
    # is modeled dynamically using the radius variance as its amplitude.
    # As SPHY synchronizes, the "impenetrable wall" of LWE collapses into a needle.
    base_error = h_var[t]
    if h_cvp_status[t]:
        # Lock state: the surface collapses to the bottom of the well
        Z_surface[:, t] = 0.0
    else:
        # Before collapse: shows the complex, highly difficult topological landscape
        Z_surface[:, t] = base_error * (3.0 + np.sin(P[:, t] * 4) * np.cos(P[:, t] * 2))

# --- Matplotlib 3D Presentation Setup ---
plt.style.use('dark_background')
fig = plt.figure(figsize=(14, 9), facecolor='#0a0a0a')
ax = fig.add_subplot(111, projection='3d', facecolor='#0a0a0a')
fig.canvas.manager.set_window_title('SPHY Geometric Cryptanalysis')

# Plot the 3D surface with a high-contrast quantum aesthetic
surf = ax.plot_surface(F, P, Z_surface, cmap='magma', edgecolor='none', 
                       alpha=0.85, antialiased=True, rstride=1, cstride=1)

# Design and layout polishes
ax.set_title('SPHY COGNITIVE ORACLE: LATTICE DISTANCE COLLAPSE SURFACE\n[CVP Search Space Hardness Dissolution]', 
             color='white', fontsize=14, fontweight='bold', pad=20)

ax.set_xlabel('Time Horizon (Frames)', color='gray', labelpad=15)
ax.set_ylabel('Phase Geometric Space (rad)', color='gray', labelpad=15)
ax.set_zlabel('Lattice Error Margin / CVP Distance', color='gray', labelpad=15)

# Adjusting visual ticks and boundaries
ax.tick_params(colors='gray', labelsize=9)
ax.grid(True, color='#222222', linestyle=':')
ax.view_init(elev=30, azim=-55) # Perfect angle to view the funnel descent

# Add a colorbar to act as a "Complexity Index"
cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, pad=0.05)
cbar.set_label('Lattice Complexity Bound', color='gray', rotation=275, labelpad=15)
cbar.ax.tick_params(colors='gray')

# Draw a distinct indicator line at the exact moment of collapse
z_max = np.max(Z_surface)
ax.plot([collapse_frame, collapse_frame], [0, 2*np.pi], [0, z_max], 
        color='#ff3333', linestyle='--', linewidth=2, alpha=0.9, label='SPHY Phase Lock Event')

plt.tight_layout()
plt.show()