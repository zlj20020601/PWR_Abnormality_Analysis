import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor


def standardize_features(df_model: pd.DataFrame):
    """
    对建模特征做标准化

    返回：
    - scaler
    - X_scaled
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_model)
    return scaler, X_scaled


def run_isolation_forest(X_scaled, contamination: float = 0.05, random_state: int = 42):
    """
    运行 Isolation Forest

    返回：
    - pred: 1 正常, -1 异常
    - scores: decision_function，越小越异常
    """
    model = IsolationForest(contamination=contamination, random_state=random_state)
    pred = model.fit_predict(X_scaled)
    scores = model.decision_function(X_scaled)
    return pred, scores


def attach_if_results(
    df_clean: pd.DataFrame,
    pred,
    scores,
    label_col: str = "anomaly_label",
    score_col: str = "anomaly_score"
) -> pd.DataFrame:
    """
    把 IF 的异常标签和分数加回原始表
    """
    df_result = df_clean.copy()
    df_result[label_col] = pred
    df_result[score_col] = scores
    return df_result


def split_normal_anomaly(df_result: pd.DataFrame, label_col: str = "anomaly_label"):
    """
    按标签拆分正常样本和异常样本
    """
    normal_df = df_result[df_result[label_col] == 1].copy()
    anomaly_df = df_result[df_result[label_col] == -1].copy()
    return normal_df, anomaly_df


def run_lof(X_scaled, n_neighbors: int = 20, contamination: float = 0.05):
    """
    运行 LOF

    返回：
    - pred: 1 正常, -1 异常
    - scores: negative_outlier_factor_，越小越异常
    """
    lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination)
    pred = lof.fit_predict(X_scaled)
    scores = lof.negative_outlier_factor_
    return pred, scores


def attach_lof_results(
    df_clean: pd.DataFrame,
    pred,
    scores,
    label_col: str = "lof_label",
    score_col: str = "lof_score"
) -> pd.DataFrame:
    """
    把 LOF 的异常标签和分数加回原始表
    """
    df_result = df_clean.copy()
    df_result[label_col] = pred
    df_result[score_col] = scores
    return df_result