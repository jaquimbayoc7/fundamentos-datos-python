# 🌊 Predicción de Caudal — Estación Pueblo Nuevo (CAM / IDEAM)

> **Proyecto de ciencia de datos aplicado a la predicción del caudal medio diario de una estación hidrológica del sistema DHIME-IDEAM, en la jurisdicción de la Corporación Autónoma Regional del Alto Magdalena (CAM).**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![License](https://img.shields.io/badge/Licencia-Educativa-green.svg)](#licencia)

---

## 📌 Descripción General

Este proyecto implementa un pipeline completo de ciencia de datos — desde la adquisición de datos crudos hasta el pronóstico a 30 días — sobre la serie de **caudal medio diario** de la estación **PUEBLO NUEVO (código 21117100)**, operada por el IDEAM dentro de la jurisdicción de la **CAM** (Corporación Autónoma Regional del Alto Magdalena) en el departamento del Huila, Colombia.

### Pregunta de Investigación

> *¿Es posible pronosticar el caudal medio diario de la estación Pueblo Nuevo con un horizonte de 30 días, utilizando modelos de series temporales (SARIMA, Holt-Winters, Prophet) y aprovechando la estacionalidad anual identificada?*

### Objetivos

1. **Explorar y caracterizar** la serie temporal de caudal (tendencia, estacionalidad, estacionariedad)
2. **Limpiar e imputar** valores faltantes preservando la estructura temporal
3. **Analizar componentes** mediante descomposición STL, ACF/PACF y pruebas formales (ADF, KPSS)
4. **Entrenar y comparar** tres modelos de pronóstico: SARIMA, Holt-Winters y Prophet
5. **Generar un pronóstico operacional** a 30 días con el modelo de menor error

---

## 🗂️ Estructura del Repositorio

```
fundamentos-datos-python/
│
├── README.md                                         ← Este archivo
│
├── Week_1/                                           ── Semana 1: Carga y Exploración
│   ├── 01_carga_exploracion_caudal.ipynb             ← Notebook principal
│   ├── descargaDhime.csv                             ← Datos brutos descargados del DHIME
│   └── carga-exploracion-serie-caudal.html           ← Material teórico de referencia
│
├── Week_2/                                           ── Semana 2: Limpieza e Imputación
│   ├── 02_tratamiento_nan_imputacion_caudal.ipynb    ← Notebook principal
│   ├── caudal_limpio_diario.csv                      ← Serie limpia exportada (output)
│   └── tratamiento-nan-imputacion-caudal.html        ← Material teórico de referencia
│
├── Week_3/                                           ── Semana 3: EDA Avanzado y Estacionariedad
│   ├── 03_eda_avanzado_estacionariedad_caudal.ipynb  ← Notebook principal
│   └── eda-avanzado-estacionariedad-caudal.html      ← Material teórico de referencia
│
└── Week_4/                                           ── Semana 4: Modelado Predictivo
    ├── 04_forecasting_sarima_hw_prophet_caudal.ipynb  ← Notebook principal
    └── forecasting-sarima-hw-prophet-caudal.html      ← Material teórico de referencia
```

---

## 🚀 Inicio Rápido

### 1. Clonar el repositorio

```bash
git clone https://github.com/jaquimbayoc7/fundamentos-datos-python.git
cd fundamentos-datos-python
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Instalar dependencias

```bash
pip install pandas numpy matplotlib seaborn plotly scipy statsmodels scikit-learn prophet jupyter
```

> **Nota sobre Prophet:** en algunos sistemas requiere `pystan` o `cmdstanpy`. Si hay errores:
> ```bash
> pip install prophet --no-build-isolation
> ```

### 4. Ejecutar los notebooks en orden

```bash
jupyter notebook
```

Abrir en secuencia: `Week_1/` → `Week_2/` → `Week_3/` → `Week_4/`

---

## 📅 Paso a Paso del Proyecto

### Semana 1 — Carga de Datos y Exploración Inicial

**Notebook:** `01_carga_exploracion_caudal.ipynb`

**Objetivo:** Adquirir los datos crudos del sistema DHIME y realizar un diagnóstico inicial de la serie temporal.

| Paso | Descripción |
|------|-------------|
| **1. Fuente de datos** | Descarga desde el sistema DHIME del IDEAM — plataforma oficial de datos hidrológicos y meteorológicos de Colombia |
| **2. Carga del CSV** | `pd.read_csv()` con `parse_dates=True`, `index_col="Fecha"`, encoding UTF-8 |
| **3. Exploración temporal** | Identificación del rango temporal (2010–2017), frecuencia de la serie, detección de gaps |
| **4. Diagnóstico de calidad** | Cuantificación de NaN, detección de valores cero (físicamente imposibles para caudal), outliers extremos |
| **5. Visualización interactiva** | Serie completa con `plotly.graph_objects`, zoom en períodos críticos, distribución con histogramas |

**Producto:** Diagnóstico completo de la serie cruda con identificación de problemas a resolver en la Semana 2.

---

### Semana 2 — Tratamiento de NaN e Imputación

**Notebook:** `02_tratamiento_nan_imputacion_caudal.ipynb`

**Objetivo:** Generar una serie diaria completa, libre de valores faltantes y outliers extremos, lista para análisis estadístico y modelado.

| Paso | Descripción |
|------|-------------|
| **1. Mapa de nulidad** | Heatmap de valores faltantes para identificar patrones (MCAR, MAR, MNAR) |
| **2. Imputación temporal** | `interpolate(method='time')` — interpolación lineal ponderada por distancia temporal |
| **3. Forward/Backward fill** | Relleno por propagación hacia adelante y hacia atrás para gaps en extremos |
| **4. Capping de outliers** | Percentiles P1–P99 para limitar crecidas extremas sin eliminar datos |
| **5. Validación** | Comparación de distribuciones antes/después con violin plots y estadísticos |
| **6. Exportación** | `to_csv('caudal_limpio_diario.csv')` — artefacto consumido por Semanas 3 y 4 |

**Producto:** `caudal_limpio_diario.csv` — serie diaria completa con ~2.900 registros, imputada y sin outliers extremos.

---

### Semana 3 — EDA Avanzado y Análisis de Estacionariedad

**Notebook:** `03_eda_avanzado_estacionariedad_caudal.ipynb`

**Objetivo:** Caracterizar la estructura estadística de la serie (tendencia, estacionalidad, estacionariedad) para fundamentar la elección de modelos en la Semana 4.

| Paso | Descripción |
|------|-------------|
| **1. Descomposición STL** | Seasonal-Trend decomposition using Loess → separación en tendencia + estacionalidad + residuo |
| **2. ACF / PACF** | Función de autocorrelación y autocorrelación parcial con bandas de confianza al 95% |
| **3. Pruebas de estacionariedad** | ADF (Augmented Dickey-Fuller) y KPSS — hipótesis complementarias para confirmar raíz unitaria |
| **4. Estadísticas rolling** | Media y desviación estándar móvil (ventana 30 días) para verificar estabilidad |
| **5. Estacionalidad mensual** | Violin plots, boxplots por mes, tablas de estadísticos mensuales descriptivos |
| **6. Análisis anual** | Superposición de curvas anuales, barras de caudal medio por año |
| **7. Régimen hidrológico** | Clasificación en épocas seca/lluviosa, análisis por percentil P90 |
| **8. Dashboard resumen** | Panel 4x1 con tendencia, estacionalidad, ACF y estadístico rolling |

**Hallazgo clave:** La serie es **no estacionaria** (ADF p > 0.05, KPSS p < 0.05) con **estacionalidad anual bimodal** (dos picos de caudal), coherente con el régimen de precipitación de la zona andina colombiana. Esto justifica:
- Diferenciación regular (d=1) y estacional (D=1) en SARIMA
- Componente estacional aditiva en Holt-Winters
- Estacionalidad anual activada en Prophet

---

### Semana 4 — Modelado Predictivo (SARIMA, Holt-Winters, Prophet)

**Notebook:** `04_forecasting_sarima_hw_prophet_caudal.ipynb`

**Objetivo:** Entrenar, evaluar y comparar tres modelos de pronóstico de series temporales para predecir el caudal medio diario a 30 días.

#### División de datos

| Conjunto | Período | Propósito |
|----------|---------|-----------|
| **Train** | Serie completa menos los últimos 60 días | Entrenar los modelos |
| **Test** | Últimos 60 días | Evaluar precisión out-of-sample |

#### Modelos implementados

| Modelo | Configuración | Descripción |
|--------|--------------|-------------|
| **SARIMA** | `(1,1,1)(1,1,1)₃₀` | Autorregresivo integrado de media móvil con componente estacional (período 30 días) |
| **Holt-Winters** | `trend="add", seasonal="add", periods=30` | Suavización exponencial triple con tendencia y estacionalidad aditivas |
| **Prophet** | `yearly_seasonality=True, changepoint_prior_scale=0.05` | Modelo aditivo bayesiano con detección automática de puntos de cambio |

#### Pipeline de evaluación

| Paso | Descripción |
|------|-------------|
| **1. Entrenamiento** | Cada modelo se ajusta sobre el conjunto train |
| **2. Pronóstico en test** | Generación de pronósticos para los 60 días de test |
| **3. Diagnóstico de residuos** | Histograma de residuos de SARIMA (verificación de ruido blanco) |
| **4. Métricas de error** | RMSE, MAE, MAPE para cada modelo sobre el test |
| **5. Comparación visual** | Superposición de los tres pronósticos vs datos reales |
| **6. Tabla comparativa** | `highlight_min` identifica el mejor modelo por cada métrica |
| **7. Reentrenamiento final** | El modelo ganador se reentrena con la serie completa (train + test) |
| **8. Pronóstico a futuro** | Generación del pronóstico operacional a 30 días |

#### Métricas de evaluación

| Métrica | Interpretación |
|---------|----------------|
| **RMSE** | Error en m³/s — penaliza errores grandes |
| **MAE** | Error absoluto medio en m³/s — más robusto ante outliers |
| **MAPE** | Error porcentual — independiente de escala |

**Producto final:** Pronóstico a 30 días con el modelo de menor RMSE, reentrenado con toda la serie disponible.

---

## 📊 Datos

### Estación hidrológica

| Atributo | Detalle |
|----------|---------|
| **Nombre** | PUEBLO NUEVO |
| **Código** | 21117100 |
| **Corporación** | CAM — Corporación Autónoma Regional del Alto Magdalena |
| **Sistema** | DHIME — IDEAM Colombia |
| **Variable** | Caudal Medio Diario |
| **Unidad** | m³/s |
| **Período** | 2010 – 2017 |
| **Registros** | ~2.900 días |
| **Frecuencia** | Diaria |

### Archivos de datos

| Archivo | Ubicación | Descripción |
|---------|-----------|-------------|
| `descargaDhime.csv` | `Week_1/` | Datos brutos descargados directamente del DHIME (con NaN y posibles errores) |
| `caudal_limpio_diario.csv` | `Week_2/` | Serie limpia: sin NaN, outliers capped (P1-P99), interpolación temporal aplicada |

---

## 🧰 Stack Tecnológico

| Librería | Uso en el proyecto |
|----------|-------------------|
| `pandas` | Manipulación de la serie temporal, DatetimeIndex, asfreq, resample |
| `numpy` | Operaciones numéricas, cálculo de métricas |
| `plotly` | Visualizaciones interactivas (series, distribuciones, comparaciones) |
| `matplotlib` / `seaborn` | Gráficos estáticos (ACF/PACF, violin plots, heatmaps) |
| `statsmodels` | SARIMAX, ExponentialSmoothing, STL, ADF, KPSS, ACF/PACF |
| `prophet` | Modelo aditivo bayesiano con estacionalidad anual |
| `scikit-learn` | Métricas de evaluación (RMSE, MAE, MAPE) |
| `scipy` | Pruebas estadísticas complementarias |

---

## 🧑‍🏫 Convención de Documentación

Cada celda de código está documentada en español con bloques explicativos:

```python
# =============================================================================
# CONCEPTO: [Nombre del concepto técnico]
# -----------------------------------------------------------------------------
# • Descripción de cada función, parámetro y criterio de elección
# • Fórmulas matemáticas cuando corresponde
# • Advertencias sobre errores comunes (data leakage, overfitting, etc.)
#
# CRITERIO DE USO: Cuándo aplicar este enfoque vs. alternativas
# =============================================================================
```

Esto permite que cada notebook sea autocontenido como material de estudio.

---

## 📈 Flujo del Pipeline

```
SEMANA 1                SEMANA 2                  SEMANA 3                    SEMANA 4
────────                ────────                  ────────                    ────────
Descarga DHIME  ──→  Imputación NaN      ──→  Descomposición STL    ──→  SARIMA(1,1,1)(1,1,1)₃₀
descargaDhime.csv     Capping P1-P99           ACF / PACF                 Holt-Winters (add)
Exploración           Interpolación            ADF / KPSS                 Prophet (anual)
Diagnóstico           temporal                 Estacionalidad             ─────────────────
                      ─────────────────        mensual/anual              Comparación métricas
                      caudal_limpio_diario.csv  Régimen seca/lluviosa     Pronóstico 30 días
```

---

## 📝 Licencia

Material académico de uso educativo. Los datos del IDEAM son de dominio público bajo la política de datos abiertos del gobierno colombiano.

---

**Proyecto desarrollado con datos del DHIME – IDEAM Colombia**
*Estación 21117100 – PUEBLO NUEVO | CAM | Caudal Medio Diario (m³/s) | 2010–2017*
