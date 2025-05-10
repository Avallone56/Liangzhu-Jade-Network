import pandas as pd
import networkx as nx
import numpy as np

input_path = '../supplementary_material/all_smc.xlsx'
output_path = '../supplementary_material/all_measurement.xlsx'

sheets = ['Phase1_SMC', 'Phase2_SMC', 'Phase3_SMC', 'Phase4_SMC']
similarity_dfs = {sheet: pd.read_excel(input_path, sheet_name=sheet, index_col=0) for sheet in sheets}

network_metrics = {}


def calculate_network_metrics(G):
    metrics = {}
    metrics['number of nodes'] = G.number_of_nodes()
    metrics['number of edges'] = G.number_of_edges()
    metrics['average degree'] = np.mean([d for _, d in G.degree()])
    metrics['weighted average degree'] = np.mean([d for _, d in G.degree(weight='weight')])

    return metrics


for sheet, df in similarity_dfs.items():
    G = nx.Graph()

    for node in df.index:
        G.add_node(node)

    for i in df.index:
        for j in df.columns:
            if i != j and df.at[i, j] > 0:
                G.add_edge(i, j, weight=df.at[i, j])

    network_metrics[sheet] = calculate_network_metrics(G)

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    for sheet, metrics in network_metrics.items():
        metrics_df = pd.DataFrame(metrics.items(), columns=['measurement', 'value'])
        metrics_df.to_excel(writer, sheet_name=sheet, index=False)

print(f'save in {output_path}')