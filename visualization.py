import matplotlib.pyplot as plt
from file_manager import get_disk

def show_disk():
    disk = get_disk()
    fig, ax = plt.subplots(figsize=(12, 2))
    unique_files = list(set(b for b in disk if b != 'free'))
    color_map = {name: f"#{hash(name) % 0xFFFFFF:06x}" for name in unique_files}
    color_map['free'] = "#d3d3d3"

    for i, block in enumerate(disk):
        color = color_map.get(block, "#d3d3d3")
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, edgecolor='black', facecolor=color))
        ax.text(i + 0.5, 0.5, '.' if block == 'free' else '■', ha='center', va='center', fontsize=8, color='black')

    ax.set_xlim(0, len(disk))
    ax.set_ylim(0, 1)
    ax.axis('off')

    legend_labels = [plt.Rectangle((0, 0), 1, 1, color=color_map[k]) for k in color_map]
    ax.legend(legend_labels, color_map.keys(), loc="upper center", ncol=5, bbox_to_anchor=(0.5, 1.2))
    return fig
