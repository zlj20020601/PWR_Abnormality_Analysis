import matplotlib.pyplot as plt
import pandas as pd


def plot_temp_pressure_scatter(
    normal_df: pd.DataFrame,
    anomaly_df: pd.DataFrame,
    save_path: str = None
):
    plt.figure(figsize=(8, 6))

    plt.scatter(
        normal_df["Temperature"],
        normal_df["Pressure"],
        s=10,
        alpha=0.5,
        label="Normal"
    )

    plt.scatter(
        anomaly_df["Temperature"],
        anomaly_df["Pressure"],
        s=18,
        alpha=0.8,
        label="Anomaly"
    )

    plt.xlabel("Temperature")
    plt.ylabel("Pressure")
    plt.title("Temperature-Pressure Distribution")
    plt.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)

    plt.close()


def plot_score_curve(
    df_result: pd.DataFrame,
    score_col: str = "anomaly_score",
    reading_col: str = "Readings",
    title: str = "Anomaly Score vs Readings",
    save_path: str = None
):
    plt.figure(figsize=(10, 5))
    plt.plot(df_result[reading_col], df_result[score_col], linewidth=1)
    plt.xlabel(reading_col)
    plt.ylabel(score_col)
    plt.title(title)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)

    plt.close()


def plot_zoom_score_curve(
    df_result: pd.DataFrame,
    score_col: str = "anomaly_score",
    start: int = 12050,
    end: int = 12267,
    reading_col: str = "Readings",
    title: str = "Zoomed Anomaly Score",
    save_path: str = None,
    mark_window: tuple = None
):
    zoom_df = df_result[(df_result[reading_col] >= start) & (df_result[reading_col] <= end)].copy()

    plt.figure(figsize=(10, 5))
    plt.plot(zoom_df[reading_col], zoom_df[score_col], linewidth=1)

    if mark_window is not None:
        plt.axvspan(mark_window[0], mark_window[1], alpha=0.2)

    plt.xlabel(reading_col)
    plt.ylabel(score_col)
    plt.title(title)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)

    plt.close()


def plot_feature_zoom(
    df_result: pd.DataFrame,
    feature: str,
    start: int,
    end: int,
    reading_col: str = "Readings",
    save_path: str = None,
    mark_window: tuple = None,
    title: str = None
):
    zoom_df = df_result[(df_result[reading_col] >= start) & (df_result[reading_col] <= end)].copy()

    plt.figure(figsize=(10, 5))
    plt.plot(zoom_df[reading_col], zoom_df[feature], linewidth=1)

    if mark_window is not None:
        plt.axvspan(mark_window[0], mark_window[1], alpha=0.2)

    plt.xlabel(reading_col)
    plt.ylabel(feature)
    plt.title(title if title else f"{feature} vs {reading_col}")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)

    plt.close()


def plot_vrr12_full(
    df_result: pd.DataFrame,
    reading_col: str = "Readings",
    feature: str = "VRR12",
    save_path: str = None
):
    plt.figure(figsize=(12, 5))
    plt.plot(df_result[reading_col], df_result[feature], linewidth=1)
    plt.xlabel(reading_col)
    plt.ylabel(feature)
    plt.title(f"{feature} vs {reading_col}")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)

    plt.close()
