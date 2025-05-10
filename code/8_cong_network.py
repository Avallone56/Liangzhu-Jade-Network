import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# === 读数据 ===
input_path = '../supplementary_material/cong_smc_processed.xlsx'
output_path = '../figures/cong_network.png'

similarity_df = pd.read_excel(input_path, sheet_name='Sheet1', index_col=0)
stages_df = pd.read_excel(input_path, sheet_name='Sheet2')

similarity_df = similarity_df.apply(pd.to_numeric, errors='coerce').fillna(0)

# === 构建图 ===
G = nx.Graph()
for i in similarity_df.index:
    for j in similarity_df.columns:
        if i != j:
            weight = similarity_df.loc[i, j]
            if weight > 0.5:
                G.add_edge(i, j, weight=weight)

# === 节点颜色 ===
color_map = {
    1: '#4a7ec0',
    2: '#83a6d4',
    3: '#fa9a9b',
    4: '#f75153'
}
node_colors = []
for node in G.nodes():
    stage = stages_df.loc[stages_df.iloc[:, 0] == node, stages_df.columns[1]].values
    node_color = color_map.get(stage[0], '#d3d3d3') if len(stage) > 0 else '#d3d3d3'
    node_colors.append(node_color)

# === 布局 ===
pos = nx.spring_layout(G, weight='weight', seed=20)

# === 绘图 ===
fig, ax = plt.subplots(figsize=(20, 15))

# 绘制节点
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=300, alpha=0.8, ax=ax)

# 绘制边（用灰度）
edges = G.edges(data=True)
edge_weights = [d['weight'] for (u, v, d) in edges]
max_weight, min_weight = max(edge_weights), min(edge_weights)
normalized_weights = [(w - min_weight) / (max_weight - min_weight) for w in edge_weights]
nx.draw_networkx_edges(G, pos, edge_color=normalized_weights, edge_cmap=plt.cm.Greys,
                       edge_vmin=0, edge_vmax=1, width=2, ax=ax)

# 绘制标签
nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)

# === 图例设置 ===

# === 图例1：Phase 图例（上方）===
phase_legend = [
    Patch(facecolor='#4a7ec0', edgecolor='k', label='Phase 1'),
    Patch(facecolor='#83a6d4', edgecolor='k', label='Phase 2'),
    Patch(facecolor='#fa9a9b', edgecolor='k', label='Phase 3'),
    Patch(facecolor='#f75153', edgecolor='k', label='Phase 4')
]
legend1 = ax.legend(handles=phase_legend, loc='upper right', bbox_to_anchor=(1.0, 1.0), title='Phases')

# === 图例2：Similarity 图例（稍微下移）===
similarity_legend = [
    Line2D([0], [0], color='#bbbbbb', lw=3, label='0.5–0.75'),
    Line2D([0], [0], color='#444444', lw=3, label='0.75–1.0')
]
legend2 = ax.legend(handles=similarity_legend, loc='upper right', bbox_to_anchor=(1.0, 0.9), title='Similarity')

# 添加图例1，否则会被覆盖
ax.add_artist(legend1)
# 标题 & 保存
ax.set_title('Similarity Matrix Network Graph - Spring Layout', fontsize=15)
plt.savefig(output_path, format='png', dpi=600, bbox_inches='tight')
plt.show()
