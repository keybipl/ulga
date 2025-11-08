import pandas as pd

df = pd.read_excel("bezrobocie.xlsx", header=None)

print("Liczba kolumn:", len(df.columns))
print("Liczba wierszy:", len(df))
print("\nWszystkie kolumny z pierwszymi 15 wierszami:")

for i in range(len(df.columns)):
    print(f"\n=== Kolumna {i} ===")
    print(df[i].head(15).to_string())
