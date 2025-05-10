import pandas as pd
import numpy as np

# File paths
input_path = "../supplementary_material/all_jade_artifacts.xlsx"
output_path = "../supplementary_material/all_smc.xlsx"

def calculate_smc(df):
    """Calculate Simple Matching Coefficient (SMC) for all site pairs"""
    sites = df.index
    n = len(sites)
    smc_matrix = np.zeros((n, n))  # Initialize SMC matrix

    # Compute SMC for each pair (i, j)
    for i in range(n):
        for j in range(n):
            if i == j:
                smc_matrix[i, j] = 1.0  # Self-similarity is always 1
            else:
                A, B = df.iloc[i], df.iloc[j]
                M_11 = np.sum((A == 1) & (B == 1))
                M_00 = np.sum((A == 0) & (B == 0))
                total = len(A)
                smc_matrix[i, j] = (M_11 + M_00) / total  # Compute SMC

    return pd.DataFrame(smc_matrix, index=sites, columns=sites).round(4)

with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    for phase in ["Phase1", "Phase2", "Phase3", "Phase4"]:
        try:
            # Read Excel sheet, remove empty rows/columns
            df = pd.read_excel(input_path, sheet_name=phase, index_col=0).dropna(how='all').dropna(axis=1, how='all')
            print(f"Processing {phase} successfully, data shape: {df.shape}")

            # Convert non-binary values (if needed)
            df = df.astype(int)  # Ensure data is integer 0/1

            # Compute and save SMC matrix
            smc_df = calculate_smc(df)
            smc_df.to_excel(writer, sheet_name=f"{phase}_SMC")

        except Exception as e:
            print(f"Failed to process {phase}, error: {str(e)}")

print("SMC calculation complete. Please check the output file.")