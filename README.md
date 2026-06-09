# 📊 Customer Analytics — Análisis Integral de Clientes 2023

> Proyecto de análisis de datos aplicado a la segmentación y retención de clientes de un supermercado con programa de tarjeta de fidelización.

---

## 🗂️ Descripción del proyecto

Este proyecto forma parte del **Caso Final 2** del Máster en Data Analyst (D4BS) y aborda tres de las principales metodologías de Customer Analytics sobre datos reales de transacciones del ejercicio 2023:

| Metodología | Objetivo |
|---|---|
| **EDA** | Exploración y limpieza de datos · Perfilado demográfico · KPIs de negocio |
| **Análisis RFM** | Segmentación de clientes por Recency, Frequency y Monetary Value |
| **Análisis de Cohortes** | Retención mensual por cohorte de primera compra (6 meses) |
| **Análisis LTV** | Cálculo del Lifetime Value y proyección de valor por cohortes |
| **Script automatizado** | Pipeline completo de datos → tableau-ready CSV |
| **Dashboard Tableau** | Visualización interactiva de KPIs y segmentos |

---

## 📈 Resultados clave

```
Revenue total 2023 ........ €2.147.812
Margen bruto .............. 30,1%
Clientes únicos ........... 20.688
Ticket medio (AOV) ........ €49,32
LTV medio ................. €103,82
Ratio LTV/CAC ............. 1,46x  ⚠️ (objetivo: ≥ 3x)
Clientes con 1 sola compra  56,1%
Campeones (top clientes) .. 582 clientes · recencia media 8 días
```

---

## 🗃️ Estructura del repositorio

```
customer-analytics-2023/
│
├── data/
│   ├── raw/                        # Datos originales (no incluidos — ver .gitignore)
│   │   ├── productos_1224.csv      # 78.266 líneas de transacción
│   │   └── clientes_1224.csv       # 20.688 clientes con perfil demográfico
│   └── processed/
│       ├── productos_final.csv     # Dataset limpio de productos
│       ├── clientes_final.csv      # Dataset limpio de clientes
│       ├── tablon_cliente.csv      # Tablón analítico por cliente (RFM + LTV)
│       ├── tablon_analitico_clientes.csv  # Tablón completo para Tableau
│       └── ltv_mes.csv             # LTV acumulado por mes de cliente
│
├── notebooks/
│   ├── 01_EDA.ipynb                # Exploración y calidad de datos
│   ├── 02_Análisis_RFM.ipynb       # Segmentación RFM (8 segmentos)
│   ├── 03_Análisis_Cohortes.ipynb  # Retención por cohortes (6 meses)
│   ├── 04_Análisis_LTV.ipynb       # Lifetime Value y predicción
│   └── 05_Script_final.ipynb       # Notebook del pipeline integrado
│
├── src/
│   └── Automatizacion_CA.py        # Script Python listo para producción
│
├── dashboard/
│   ├── Dashboard_DA.twbx           # Workbook Tableau (local)
│   └── tableau_public_link.txt     # Enlace al dashboard publicado
│
├── reports/
│   ├── Informe_Analitico_2023.docx
│   └── Informe_CustomerAnalytics_2023.docx
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Cómo ejecutar el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/begoarmillas/customer-analytics-2023.git
cd customer-analytics-2023
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Añadir los datos

Coloca los archivos originales en `data/raw/`:
```
data/raw/productos_1224.csv
data/raw/clientes_1224.csv
```

> ⚠️ Los datasets no están incluidos en el repositorio por privacidad. Si quieres reproducir el análisis, adapta las rutas en los notebooks o en `src/Automatizacion_CA.py`.

### 4. Ejecutar el pipeline completo

```bash
python src/Automatizacion_CA.py
```

O ejecuta los notebooks en orden desde `notebooks/`.

---

## 📓 Resumen de cada notebook

### `01_EDA.ipynb` — Análisis Exploratorio
- Carga y validación de calidad de datos (nulos, duplicados, tipologías)
- Creación de `Total_Venta = Cantidad × Precio_Unitario`
- Perfil demográfico: género, ocupación, nivel educativo, tamaño de hogar
- KPIs globales: revenue, márgenes, AOV, estacionalidad mensual

### `02_Análisis_RFM.ipynb` — Segmentación de clientes
- Cálculo de Recency, Frequency y Monetary Value por cliente
- Scoring RFM (quintiles 1–5)
- Clasificación en 8 segmentos: Campeones, Clientes Leales, Clientes Rentables, Prometedores, Leales Potenciales, Grandes Gastadores, Clientes Recientes, En Riesgo

### `03_Análisis_Cohortes.ipynb` — Retención mensual
- Agrupación de clientes por mes de primera compra (cohortes enero–julio 2023)
- Tabla pivotada de retención a 6 meses
- Cálculo de tasas de retención y churn por cohorte

### `04_Análisis_LTV.ipynb` — Lifetime Value
- LTV observado por cliente
- Curva de LTV acumulado por mes de vida del cliente
- Proyección de valor futuro basada en comportamiento de cohortes

### `05_Script_final.ipynb` / `src/Automatizacion_CA.py` — Pipeline automatizado
- Pipeline completo: carga → limpieza → RFM → cohortes → LTV → export
- Genera los CSVs procesados listos para conectar con Tableau

---

## 📊 Dashboard

El dashboard interactivo está publicado en Tableau Public:

🔗 **[Ver dashboard en Tableau Public](https://public.tableau.com/app/profile/bego.a.armillas.alonso/viz/DashboardCA-curso/Lifetimevalue)**

Incluye:
- KPIs principales (revenue, margen, LTV/CAC)
- Distribución por segmento RFM
- Mapa de calor de retención por cohortes
- Evolución mensual de ventas

---

## 🛠️ Tecnologías utilizadas

| Herramienta | Uso |
|---|---|
| Python 3.x | Análisis y pipeline de datos |
| pandas | Manipulación y transformación de datos |
| matplotlib / seaborn | Visualización exploratoria |
| Tableau Public | Dashboard interactivo |
| Google Colab | Entorno de desarrollo |

---

## 👤 Autora

**Begoña Armillas Alonso**
Máster Data Analyst — D4BS (en curso)
[LinkedIn][(https://www.linkedin.com/in/bego%C3%B1a-armillas-alonso-b31a0562/)]
---

## 📄 Licencia

Este proyecto es de carácter educativo. Los datos han sido anonimizados y no corresponden a ninguna empresa real.


