import pandas as pd
# Importar otras librerías necesarias para la transformación de datos RobustScaler y OneHotEncoder
from sklearn.preprocessing import RobustScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer, KNNImputer

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply transformations and feature engineering.
    Parameters:
        df (pd.DataFrame): Raw data.
    Returns:
        pd.DataFrame: Clean and transformed data.
    """
    # Validaciones iniciales o limpieza
    df = df.drop_duplicates()  # eliminar duplicados
    df = df[df["Credit amount"] > 0]  # filtrar créditos no positivos o cero
    df = df[df["Duration"] > 0]  # filtrar duraciones no positivas o cero
    df = df[df["Age"] > 17]  # filtrar edades no válidas (menores de edad)
    
    if "Unnamed: 0" in df.columns:
        df.drop("Unnamed: 0", axis=1, inplace=True)  # eliminar columna de índice si existe
    
    # Manejo de valores nulos
    # Saving accounts -- Completar con la moda
    # Checking account -- Completar con la moda
    # Purpose -- Completar con la moda
    
    # Definir la moda para cada columna categórica
    saving_accounts_mode = df["Saving accounts"].mode()[0]
    checking_account_mode = df["Checking account"].mode()[0]
    purpose_mode = df["Purpose"].mode()[0]
    
    if df["Saving accounts"].isnull().sum() > 0:
        df["Saving accounts"] = df["Saving accounts"].fillna(saving_accounts_mode)
    if df["Checking account"].isnull().sum() > 0:
        df["Checking account"] = df["Checking account"].fillna(checking_account_mode)
    if df["Purpose"].isnull().sum() > 0:
        df["Purpose"] = df["Purpose"].fillna(purpose_mode)
    
    # Definir la media para cada columna numérica
    credit_amount_mean = df["Credit amount"].mean()
    age_mean = df["Age"].mean()
    duration_mean = df["Duration"].mean()
    
    # Este proceso se puede hacer tambien con modelos de regresion, pero para este caso se hace con la media
    if df["Credit amount"].isnull().sum() > 0:
        df["Credit amount"] = df["Credit amount"].fillna(credit_amount_mean)
    if df["Age"].isnull().sum() > 0:
        df["Age"] = df["Age"].fillna(age_mean,)
    if df["Duration"].isnull().sum() > 0:
        df["Duration"] = df["Duration"].fillna(duration_mean)
        
    # Eliminar filas adicionales con valores nulos después de la imputación
    df = df.dropna()
    
    # Escalado de variables numéricas
    scaler = RobustScaler()
    df[["Credit amount", "Age", "Duration"]] = scaler.fit_transform(df[["Credit amount", "Age", "Duration"]]) # Se escalan las variables numéricas utilizando RobustScaler para reducir el impacto de los valores atípicos
    
    # Codificación de variables categóricas
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    encoded = encoder.fit_transform(df[["Sex","Housing","Saving accounts", "Checking account", "Purpose"]])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(), index=df.index)
    # Concatenar y eliminar originales
    df = pd.concat([df.drop(columns=["Sex","Housing","Saving accounts", "Checking account", "Purpose"]), encoded_df], axis=1)

    # Codificación de variable objetivo
    le = LabelEncoder()
    df["Risk"] = le.fit_transform(df["Risk"]) # Codificar la variable objetivo "Risk" utilizando LabelEncoder, donde "good" se codifica como 0 y "bad" como 1
    
    # Ingeniería de características
    # df["credit_per_month"] = df["Credit amount"] / df["Duration"]
    df["duration_per_year"] = df["Duration"] / 12  
    
    return df