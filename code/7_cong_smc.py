import pandas as pd
import numpy as np

# File paths
input_path = "../supplementary_material/cong.xlsx"
output_path = "../supplementary_material/cong_smc.xlsx"

def calculate_smc(df):
    """
    Compute the Simple Matching Coefficient (SMC) similarity matrix.
    """
    sites = df.index  # Get site names
    n = len(sites)  # Number of sites
    smc_matrix = np.zeros((n, n))  # Initialize similarity matrix

    # Compute SMC for each site pair
    for i in range(n):
        for j in range(n):
            if i == j:
                smc_matrix[i, j] = 1.0  # Similarity with itself is always 1
            else:
                A, B = df.iloc[i], df.iloc[j]
                M_11 = np.sum((A == 1) & (B == 1))  # (1,1) matches
                M_00 = np.sum((A == 0) & (B == 0))  # (0,0) matches
                total = len(A)
                smc_matrix[i, j] = (M_11 + M_00) / total

    return pd.DataFrame(smc_matrix, index=sites, columns=sites).round(4)

# Step 1: Load the file, with first 2 rows as column headers (MultiIndex)
df_raw = pd.read_excel(input_path, header=[0, 1])

# Step 2: Set the first column as the index (遗址与阶段)
df_raw.set_index(df_raw.columns[0], inplace=True)

# Step 3: Convert all remaining values to integers (0/1)
df_binary = df_raw.astype(int)

# Step 4: Compute SMC similarity matrix
smc_df = calculate_smc(df_binary)

# Step 5: Save result
smc_df.to_excel(output_path, engine="openpyxl")

print("SMC calculation complete. Please check the output file.")
