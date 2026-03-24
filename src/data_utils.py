import pandas as pd
from pathlib import Path


def load_data(path: str) -> pd.DataFrame:
    """
    读取原始 csv 数据
    """
    return pd.read_csv(path)


def clean_flow2(df: pd.DataFrame) -> pd.DataFrame:
    """
    修复 Flow2 的格式问题：
    - 转为字符串
    - 去掉首尾空格
    - 把逗号小数改成点
    - 再转成数值型
    """
    df = df.copy()
    df["Flow2"] = df["Flow2"].astype(str).str.strip().str.replace(",", ".", regex=False)
    df["Flow2"] = pd.to_numeric(df["Flow2"], errors="coerce")
    return df


def drop_readings(df: pd.DataFrame) -> pd.DataFrame:
    """
    删除编号列 Readings
    """
    return df.drop(columns=["Readings"])


def prepare_model_data(path: str):
    """
    一步完成：
    1. 读取数据
    2. 清洗 Flow2
    3. 保留原始表 df_clean
    4. 删除 Readings 得到建模表 df_model

    返回：
    - df_clean: 保留原始列，后续挂异常标签和分数
    - df_model: 真正给模型用的特征表
    """
    df = load_data(path)
    df = clean_flow2(df)

    df_clean = df.copy()
    df_model = drop_readings(df)

    return df_clean, df_model


def ensure_output_dirs(base_dir: str = "outputs"):
    """
    确保输出文件夹存在：
    outputs/
    ├── figures/
    └── tables/
    """
    base = Path(base_dir)
    (base / "figures").mkdir(parents=True, exist_ok=True)
    (base / "tables").mkdir(parents=True, exist_ok=True)