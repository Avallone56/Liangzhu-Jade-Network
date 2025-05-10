import pandas as pd


input_path = "../supplementary_material/special_smd.xlsx"
output_path = "../supplementary_material/weighted_degrees.xlsx"
sheets = ["Phase1_SMD", "Phase2_SMD", "Phase3_SMD", "Phase4_SMD"]


weighted_degrees = {}

for sheet in sheets:

    df = pd.read_excel(input_path, sheet_name=sheet, index_col=0)

    weighted_degree = df.sum(axis=1).to_frame(name='weighted_degrees')

    weighted_degrees[sheet] = weighted_degree

    print(f"\n{sheet} Weighted Degrees:")
    print(weighted_degree)


with pd.ExcelWriter(output_path) as writer:
    for sheet, degree_series in weighted_degrees.items():
        degree_series.to_excel(writer, sheet_name=sheet)

print(f"\nsave as  {output_path}")