import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Carregar CSV
df = pd.read_csv("github_repositories_data.csv")

# Converter idade de dias para anos
df["age_years"] = df["age_days"] / 365.25

# -------------------------
# RQ01 – Maturidade (idade)
# -------------------------
plt.figure(figsize=(6,5))
sns.boxplot(x=df["age_years"], color="skyblue")
plt.title("RQ01 – Idade dos Repositórios (anos)")
plt.xlabel("Idade (anos)")
plt.savefig("RQ01_maturidade.png")
plt.close()

# -------------------------
# RQ02 – Contribuição externa (PRs aceitos)
# -------------------------
plt.figure(figsize=(6,5))
sns.boxplot(x=np.log1p(df["merged_prs"]), color="lightgreen")
plt.title("RQ02 – PRs Aceitos (escala log)")
plt.xlabel("log(1 + PRs aceitos)")
plt.savefig("RQ02_contribuicao.png")
plt.close()

# -------------------------
# RQ03 – Releases
# -------------------------
plt.figure(figsize=(6,5))
sns.boxplot(x=np.log1p(df["total_releases"]), color="violet")
plt.title("RQ03 – Releases (escala log)")
plt.xlabel("log(1 + Releases)")
plt.savefig("RQ03_releases.png")
plt.close()

# -------------------------
# RQ04 – Atualizações
# -------------------------
plt.figure(figsize=(7,6))
sns.scatterplot(x="age_years", y="days_since_update", data=df, alpha=0.6)
plt.title("RQ04 – Idade vs Dias desde última atualização")
plt.xlabel("Idade (anos)")
plt.ylabel("Dias desde última atualização")
plt.savefig("RQ04_atualizacoes.png")
plt.close()

# -------------------------
# RQ05 – Linguagens utilizadas
# -------------------------
top_langs = df["primary_language"].value_counts().head(10).index
df_top = df[df["primary_language"].isin(top_langs)]

plt.figure(figsize=(10,6))
heatmap_data = df_top.pivot_table(values="stars", index="primary_language", aggfunc="median")
sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", fmt=".0f")
plt.title("RQ05 – Mediana de Stars por Linguagem (Top 10)")
plt.xlabel("Métrica")
plt.ylabel("Linguagem")
plt.savefig("RQ05_linguagens.png")
plt.close()

# -------------------------
# RQ06 – Issues fechadas
# -------------------------
plt.figure(figsize=(6,5))
sns.boxplot(x=df["closed_issues_ratio"], color="orange")
plt.title("RQ06 – Percentual de Issues Fechadas")
plt.xlabel("% de Issues Fechadas")
plt.savefig("RQ06_issues.png")
plt.close()

# -------------------------
# RQ07 – Comparação por linguagem
# -------------------------
top_langs = df["primary_language"].value_counts().head(5).index
df_top = df[df["primary_language"].isin(top_langs)]

summary = df_top.groupby("primary_language").agg({
    "merged_prs": "median",
    "total_releases": "median",
    "days_since_update": "median"
})

plt.figure(figsize=(8,6))
sns.heatmap(summary, annot=True, cmap="coolwarm", fmt=".0f")
plt.title("RQ07 – Comparação por Linguagem (Medianas)")
plt.savefig("RQ07_comparacao_linguagens.png")
plt.close()

print("✅ Gráficos gerados: RQ01 a RQ07 (boxplot, scatter e heatmap).")
