import matplotlib as mpl
import matplotlib.font_manager as fm
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.lines import Line2D

input_path1 = '../supplementary_material/special_smd.xlsx'
input_path2 = '../supplementary_material/special_coordinate_and_total.xlsx'
output_path = '../figures/special_network.png'

def plot_network(ax, similarity_df, coordinates_df, title, labels_to_show, site_jade_count_sheet):
    G = nx.Graph()

    # add nodes
    for i in similarity_df.index:
        G.add_node(i)

    edges_with_weights = []
    for i in similarity_df.index:
        for j in similarity_df.columns:
            if i != j and similarity_df.at[i, j] >= 0:
                edges_with_weights.append((i, j, similarity_df.at[i, j]))

    edges_with_weights.sort(key=lambda x: x[2], reverse=True)

    num_edges_to_show = max(1, int(len(edges_with_weights) * 0.09))

    for u, v, weight in edges_with_weights[:num_edges_to_show]:
        G.add_edge(u, v, weight=weight)

    # coordinate
    pos = {
        row['Id']: (float(row['Longitude']), float(row['Latitude']))
        for _, row in coordinates_df.iterrows()
    }

    # jade count
    jade_count_df = pd.read_excel(input_path2, sheet_name=site_jade_count_sheet, index_col=0)
    jade_counts = jade_count_df.to_dict()['total']

    # weighted degree
    weighted_degree = dict(G.degree(weight='weight'))
    max_degree = max(weighted_degree.values())
    min_degree = min(weighted_degree.values())

    # node size
    node_sizes = []
    node_colors = []
    for node in G.nodes():
        count = jade_counts.get(node, 0)
        if count == 0:
            node_sizes.append(50)
            node_colors.append('none')
        else:
            node_sizes.append(count * 20)

            degree = weighted_degree[node]
            normalized_degree = (degree - min_degree) / (max_degree - min_degree) if max_degree > min_degree else 0
            if normalized_degree >= 0.75:
                node_colors.append('#f8696b')
            elif normalized_degree >= 0.5:
                node_colors.append('#f98788')
            elif normalized_degree >= 0.25:
                node_colors.append('#8cadd7')
            else:
                node_colors.append('#7099cd')

                # map
    m = Basemap(projection='merc', llcrnrlat=30.2, urcrnrlat=32, llcrnrlon=119.5, urcrnrlon=121.7, resolution='i',
                ax=ax)
    m.drawstates(linewidth=1, color='black')
    m.drawcountries(linewidth=1, color='black')
    m.drawmapboundary(fill_color='lightblue')
    m.fillcontinents(color='lightgray', lake_color='lightblue')

    lake_x, lake_y = m(120.2, 31.2)
    ax.text(
        lake_x, lake_y,
        'Tai Hu',
        fontsize=20,
        color='grey',
        ha='center',
        va='center',
        fontname='Arial',
        style='italic',
        rotation=0
    )

    bay_x, bay_y = m(121.3, 30.39)
    ax.text(
        bay_x, bay_y,
        'Hangzhou Bay',
        fontsize=20,
        color='grey',
        ha='center',
        va='center',
        fontname='Arial',
        style='italic',
        rotation=0
    )

    # coordinate
    mapped_pos = {node: m(lon, lat) for node, (lon, lat) in pos.items()}

    # node
    for node, size in zip(G.nodes(), node_sizes):

        nx.draw_networkx_nodes(G, mapped_pos, nodelist=[node], node_size=size, node_color='white',
                               linewidths=1, ax=ax)


    edges = G.edges(data=True)
    edge_colors = []
    for u, v, d in edges:
        weight = d['weight']
        if weight <= 0.25:
            edge_colors.append('#4a7ec0')
        elif weight <= 0.5:
            edge_colors.append('#83a6d4')
        elif weight <= 0.75:
            edge_colors.append('#fa9a9b')
        else:
            edge_colors.append('#f75153')

    nx.draw_networkx_edges(G, mapped_pos, edge_color=edge_colors, width=2, alpha=0.5, ax=ax)

    nx.draw_networkx_edges(G, mapped_pos, edge_color=edge_colors, width=2, alpha=0.5, ax=ax)

    # node label
    labels = {node: node for node in labels_to_show if node in G.nodes()}
    nx.draw_networkx_labels(G, mapped_pos, labels=labels, font_size=15, ax=ax)

    ax.set_title(title, fontsize=14)


fig, axs = plt.subplots(2, 2, figsize=(20, 18))

plt.subplots_adjust(wspace=0.01, hspace=0.1)

plot_network(axs[0, 0],
             pd.read_excel(input_path1, sheet_name='Phase1_SMD', index_col=0),
             pd.read_excel(input_path2, sheet_name='Phase1_coordinate'),
             "Phase 1",
             labels_to_show=["Fanshan", "Gaochengdun", "Fuquanshan", "Shaoqingshan", "Yaoshan"],
             site_jade_count_sheet='Phase1_total')

plot_network(axs[0, 1],
             pd.read_excel(input_path1, sheet_name='Phase2_SMD', index_col=0),
             pd.read_excel(input_path2, sheet_name='Phase2_coordinate'),
             "Phase 2",
             labels_to_show=["Zhanglingshan", "Yaoshan", "Fanshan", "Gaochengdun", "Pu'anqiao", "Fuquanshan"],
             site_jade_count_sheet='Phase2_total')

plot_network(axs[1, 0],
             pd.read_excel(input_path1, sheet_name='Phase3_SMD', index_col=0),
             pd.read_excel(input_path2, sheet_name='Phase3_coordinate'),
             "Phase 3",
             labels_to_show=["Fanshan", "Fuquanshan", "Caoxieshan", "Qiuchengdun"],
             site_jade_count_sheet='Phase3_total')

plot_network(axs[1, 1],
             pd.read_excel(input_path1, sheet_name='Phase4_SMD', index_col=0),
             pd.read_excel(input_path2, sheet_name='Phase4_coordinate'),
             "Phase 4",
             labels_to_show=["Fanshan", "Sidun", "Tinglin", "Fuquanshan"],
             site_jade_count_sheet='Phase4_total')

legend_elements = [

    Line2D([0], [0], color='#4a7ec0', lw=4, label='0 - 0.25'),
    Line2D([0], [0], color='#83a6d4', lw=4, label='0.25 - 0.5'),
    Line2D([0], [0], color='#fa9a9b', lw=4, label='0.5 - 0.75'),
    Line2D([0], [0], color='#f75153', lw=4, label='0.75 - 1'),

]

fig.legend(
    handles=legend_elements,
    loc='upper left',
    fontsize=12,
    bbox_to_anchor=(0.5, 1.05),
    ncol=len(legend_elements),
    title='SMD range',
    title_fontsize=14,
    frameon=True,
    framealpha=1,
    labelspacing=1.5,
    handlelength=4
)

plt.savefig(output_path, format='png', dpi=600, bbox_inches='tight')

plt.show()

