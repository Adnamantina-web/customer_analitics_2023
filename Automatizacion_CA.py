"""
Customer Analytics Pipeline — Super Compras 2023
=================================================
Pipeline completo: carga → limpieza → RFM → cohortes → LTV → export

Uso:
    python src/Automatizacion_CA.py

Outputs generados en data/processed/:
    - productos_final.csv
    - clientes_final.csv
    - tablon_cliente.csv
    - tablon_analitico_clientes.csv
    - ltv_mes.csv
"""

import pandas as pd
from pathlib import Path

# ── Rutas ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR  = BASE_DIR / "data" / "raw"
OUT_DIR  = BASE_DIR / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── 1. Carga de datos ──────────────────────────────────────────────────────
print("📂 Cargando datos...")
productos = pd.read_csv(RAW_DIR / "productos_1224.csv")
clientes  = pd.read_csv(RAW_DIR / "clientes_1224.csv")

# ── 2. Limpieza y preparación ──────────────────────────────────────────────
print("🧹 Limpiando datos...")

# Tipos de fecha
productos["Fecha"]            = pd.to_datetime(productos["Fecha"])
clientes["Fecha_Nacimiento"]  = pd.to_datetime(clientes["Fecha_Nacimiento"])

# Variable de venta total
productos["Total_Venta"] = productos["Cantidad"] * productos["Precio_Unitario"]

# Imputación de nulos en clientes
moda_hogar = clientes["Tamano_Hogar"].mode()[0]
clientes["Tamano_Hogar"]       = clientes["Tamano_Hogar"].fillna(moda_hogar)
clientes["Nivel_Educativo"]    = clientes["Nivel_Educativo"].fillna("Desconocido")
clientes["Ocupacion"]          = clientes["Ocupacion"].fillna("Desconocido")

# Guardar datasets limpios
productos.to_csv(OUT_DIR / "productos_final.csv", index=False)
clientes.to_csv(OUT_DIR  / "clientes_final.csv",  index=False)
print("  ✓ productos_final.csv y clientes_final.csv guardados")

# ── 3. Análisis RFM ────────────────────────────────────────────────────────
print("📊 Calculando RFM...")
fecha_max = productos["Fecha"].max()

rfm = productos.groupby("ID_Cliente").agg(
    Recency   = ("Fecha", lambda x: (fecha_max - x.max()).days),
    Frequency = ("ID_Transaccion", "nunique"),
    Monetary  = ("Total_Venta", "sum")
)

# Scoring (quintiles)
rfm["r"] = pd.cut(rfm["Recency"],   bins=[0, 60, 120, 180, 240, rfm["Recency"].max()],
                  labels=[5, 4, 3, 2, 1], include_lowest=True)
rfm["f"] = pd.cut(rfm["Frequency"], bins=[1, 2, 4, 6, 9, rfm["Frequency"].max()],
                  labels=[1, 2, 3, 4, 5], include_lowest=True)
rfm["m"] = pd.cut(rfm["Monetary"],  bins=[0, 30, 70, 150, 300, rfm["Monetary"].max()],
                  labels=[1, 2, 3, 4, 5])

rfm["RFM"] = rfm["r"].astype(str) + rfm["f"].astype(str) + rfm["m"].astype(str)


def segmentar_clientes(fila):
    r, f, m = str(fila["r"]), str(fila["f"]), str(fila["m"])
    alto_r  = r in ["4", "5"];  alto_f  = f in ["4", "5"];  alto_m  = m in ["4", "5"]
    medio_r = r in ["3"];       medio_f = f in ["3"];       medio_m = m in ["3"]
    bajo_r  = r in ["1", "2"];  bajo_f  = f in ["1", "2"];  bajo_m  = m in ["1", "2"]

    if   alto_r and alto_f and alto_m:                     return "Campeones"
    elif alto_r and alto_f and (alto_m or medio_m):        return "Clientes Leales"
    elif medio_r and alto_f and alto_m:                    return "Clientes Rentables"
    elif bajo_r and medio_f and medio_m:                   return "Leales Potenciales"
    elif bajo_r and bajo_f and alto_m:                     return "Grandes Gastadores"
    elif alto_r and bajo_f and bajo_m:                     return "Clientes Recientes"
    elif medio_r and medio_f and medio_m:                  return "Prometedores"
    elif bajo_r and bajo_f and bajo_m:                     return "En Riesgo"
    else:                                                  return "Dudosos"


rfm["Segmento"] = rfm.apply(segmentar_clientes, axis=1)
print("  ✓ RFM calculado — 8 segmentos")

# ── 4. Análisis de cohortes ────────────────────────────────────────────────
print("📅 Calculando cohortes...")
productos["MesTransaccion"] = productos["Fecha"].dt.to_period("M")
productos["MesCohorte"]     = productos.groupby("ID_Cliente")["MesTransaccion"].transform("min")

# Cohortes completas (hasta julio 2023 para tener 6 meses de seguimiento)
resultados = productos[productos["MesCohorte"] <= "2023-07"].copy()
resultados["MesTransaccion"] = pd.to_datetime(resultados["MesTransaccion"].astype(str))
resultados["MesCohorte"]     = pd.to_datetime(resultados["MesCohorte"].astype(str))

# Solo primeros 6 meses por cliente
resultados = resultados[
    resultados["MesTransaccion"] <= resultados["MesCohorte"] + pd.DateOffset(months=5)
]

# Mes del cliente (M1, M2, …, M6)
mes_diff = (resultados["MesTransaccion"].dt.to_period("M")
            - resultados["MesCohorte"].dt.to_period("M"))
resultados["MesCliente"] = "M" + mes_diff.apply(lambda x: str(x.n + 1))

tabla_cohortes = pd.pivot_table(
    resultados,
    index="MesCohorte",
    columns="MesCliente",
    values="ID_Cliente",
    aggfunc="nunique"
)
print("  ✓ Tabla de cohortes calculada")

# ── 5. LTV ─────────────────────────────────────────────────────────────────
print("💰 Calculando LTV...")
ltv_mes = (resultados.groupby("MesCliente")
           .agg(Total_Venta=("Total_Venta", "sum"),
                ID_Cliente=("ID_Cliente", "nunique"))
           .reset_index())

clientes_m1 = ltv_mes.loc[ltv_mes["MesCliente"] == "M1", "ID_Cliente"].values[0]
ltv_mes["M1"] = clientes_m1
ltv_mes["Ventas_por_M1"] = ltv_mes["Total_Venta"] / clientes_m1

ltv_mes.to_csv(OUT_DIR / "ltv_mes.csv", index=False)
print("  ✓ ltv_mes.csv guardado")

# ── 6. Tablón analítico final ──────────────────────────────────────────────
print("📋 Construyendo tablón analítico...")

# Unir RFM + datos demográficos
rfm_reset = rfm.reset_index()
tablon_cliente = rfm_reset.merge(clientes, on="ID_Cliente", how="left")

# LTV: suma de ventas por cliente
ltv = productos.groupby("ID_Cliente")["Total_Venta"].sum().reset_index()
ltv.columns = ["ID_Cliente", "ltv"]
tablon_cliente = tablon_cliente.merge(ltv, on="ID_Cliente", how="left")

# LTV ajustado para campeones con cohortes
tablon_cliente.loc[tablon_cliente["Segmento"] == "Campeones", "ltv"] = (
    tablon_cliente.loc[tablon_cliente["Segmento"] == "Campeones", "ltv"]
    * ltv_mes["Ventas_por_M1"].sum() / ltv_mes.loc[0, "Ventas_por_M1"]
)

tablon_cliente.to_csv(OUT_DIR / "tablon_cliente.csv", index=False)
print("  ✓ tablon_cliente.csv guardado")

# Tablón completo transaccional (para Tableau)
tablon_analitico = resultados.merge(rfm_reset, on="ID_Cliente", how="left")
tablon_analitico = tablon_analitico.merge(clientes, on="ID_Cliente", how="left")
tablon_analitico = tablon_analitico.merge(ltv, on="ID_Cliente", how="left")

tablon_analitico.to_csv(OUT_DIR / "tablon_analitico_clientes.csv", index=False)
print("  ✓ tablon_analitico_clientes.csv guardado")

print("\n✅ Pipeline completado. Archivos disponibles en data/processed/")
