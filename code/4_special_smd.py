import pandas as pd
import numpy as np

# File paths
input_path = "../supplementary_material/special_jade_artifacts.xlsx"
output_path = "../supplementary_material/special_smd.xlsx"

def calculate_smd(df):
    """Calculate Simple Matching Dissimilarity (SMD) for all site pairs"""
    sites = df.index
    n = len(sites)
    smd_matrix = np.zeros((n, n))  # Initialize SMD matrix

    # Compute SMD for each pair (i, j)
    for i in range(n):
        for j in range(n):
            if i == j:
                smd_matrix[i, j] = 0.0  # Self-dissimilarity is always 0
            else:
                A, B = df.iloc[i], df.iloc[j]
                M_11 = np.sum((A == 1) & (B == 1))
                M_00 = np.sum((A == 0) & (B == 0))
                total = len(A)
                smc = (M_11 + M_00) / total  # Compute SMC
                smd_matrix[i, j] = 1 - smc  # Compute SMD

    return pd.DataFrame(smd_matrix, index=sites, columns=sites).round(4)

with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    for phase in ["Phase1", "Phase2", "Phase3", "Phase4"]:
        try:
            # Read Excel sheet, remove empty rows/columns
            df = pd.read_excel(input_path, sheet_name=phase, index_col=0).dropna(how='all').dropna(axis=1, how='all')
            print(f"Processing {phase} successfully, data shape: {df.shape}")

            # Convert non-binary values (if needed)
            df = df.astype(int)  # Ensure data is integer 0/1

            # Compute and save SMD matrix
            smd_df = calculate_smd(df)
            smd_df.to_excel(writer, sheet_name=f"{phase}_SMD")

        except Exception as e:
            print(f"Failed to process {phase}, error: {str(e)}")

print("SMD calculation complete. Please check the output file.")
