from src.data_utils import prepare_model_data, ensure_output_dirs
from src.model_utils import (
    standardize_features,
    run_isolation_forest,
    attach_if_results,
    split_normal_anomaly
)
from src.plot_utils import (
    plot_temp_pressure_scatter,
    plot_score_curve,
    plot_zoom_score_curve
)


def main():
    # 1. 创建输出目录
    ensure_output_dirs("outputs")

    # 2. 读取并清洗数据
    data_path = "data/PWR Abnormality Dataset.csv"
    df_clean, df_model = prepare_model_data(data_path)

    # 3. 标准化
    scaler, X_scaled = standardize_features(df_model)

    # 4. 跑 Isolation Forest baseline
    pred, scores = run_isolation_forest(
        X_scaled,
        contamination=0.05,
        random_state=42
    )

    # 5. 把结果加回原始表
    df_result = attach_if_results(
        df_clean,
        pred,
        scores,
        label_col="anomaly_label",
        score_col="anomaly_score"
    )

    # 6. 拆分正常样本和异常样本
    normal_df, anomaly_df = split_normal_anomaly(df_result, label_col="anomaly_label")

    # 7. 保存结果表
    table_path = "outputs/tables/pwr_anomaly_with_scores.csv"
    df_result.to_csv(table_path, index=False)

    # 8. 生成核心图
    plot_temp_pressure_scatter(
        normal_df,
        anomaly_df,
        save_path="outputs/figures/temperature_pressure_distribution.png"
    )

    plot_score_curve(
        df_result,
        score_col="anomaly_score",
        reading_col="Readings",
        title="Anomaly Score vs Readings",
        save_path="outputs/figures/anomaly_score_all.png"
    )

    plot_zoom_score_curve(
        df_result,
        score_col="anomaly_score",
        start=12050,
        end=12267,
        reading_col="Readings",
        title="Zoomed Anomaly Score (12050-12267)",
        save_path="outputs/figures/anomaly_score_zoom.png",
        mark_window=(12115, 12135)
    )

    # 9. 打印最基本结果
    print("Baseline pipeline finished.")
    print("Result table saved to:", table_path)
    print("Anomaly count:")
    print(df_result["anomaly_label"].value_counts())


if __name__ == "__main__":
    main()