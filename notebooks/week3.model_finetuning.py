# Databricks notebook source

"""
Ray Tune + MLflow Nested Runs for House Price Prediction
"""
import mlflow
import numpy as np
import pandas as pd
from ray import tune
from ray.tune.search.optuna import OptunaSearch
from functools import partial
from datetime import datetime
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from pyspark.sql import SparkSession

from house_price.config import ProjectConfig, Tags
from house_price.models.basic_model import BasicModel

# COMMAND ----------
config = ProjectConfig.from_yaml(config_path="../project_config.yml", env="dev")
tags = Tags(**{"git_sha": "abcd12345", "branch": "week3"})
spark = SparkSession.builder.getOrCreate()

basic_model = BasicModel(config=config, tags=tags, spark=spark)
basic_model.load_data()

# Split train set into train/validation for tuning
from sklearn.model_selection import train_test_split
X_train, X_valid, y_train, y_valid = train_test_split(
    basic_model.X_train, basic_model.y_train, test_size=0.2, random_state=42
)

# --- Define Ray Tune search space ---
# param_space = {
#     "n_estimators": tune.choice([50, 100, 200, 300, 400]),
#     "max_depth": tune.choice([3, 5, 10, 15]),
#     "learning_rate": tune.choice([0.01, 0.03, 0.05, 0.1, 0.15]),
# }

param_space = {
    "n_estimators": tune.choice([50, 100]),
    "max_depth": tune.choice([3, 5]),
    "learning_rate": tune.choice([0.01, 0.03]),
}

# --- Trainable function for Ray Tune with nested MLflow runs ---
""" This is the function that Ray Tune will call for each hyperparameter combination. 
For each trial:
1.Start a nested MLflow run (grouped under a parent run for easy tracking).
2.Update the model’s hyperparameters for this trial.
3.Prepare the pipeline using BasicModel.prepare_features().
4.Train the model on the training set.
5.Predict on the validation set.
6.Compute metrics: MSE, RMSE, MAE, R².
7.Log parameters and metrics to MLflow.
8.Report metrics back to Ray Tune for optimization."""
def train_with_nested_mlflow(config, X_train, X_valid, y_train, y_valid, project_config, tags, parent_run_id=None):
    n_estimators, max_depth, learning_rate = (
        config["n_estimators"],
        config["max_depth"],
        config["learning_rate"],
    )
    with mlflow.start_run(
        run_name=f"trial_n{n_estimators}_md{max_depth}_lr{learning_rate}",
        nested=True,
        parent_run_id=parent_run_id
    ):
        # Update parameters for this trial
        trial_params = dict(project_config.parameters)
        trial_params.update({
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "learning_rate": learning_rate,
        })

        # Train model
        model = BasicModel(config=project_config, tags=tags, spark=None)
        model.parameters = trial_params
        model.prepare_features()
        model.pipeline.set_params(
            regressor__n_estimators=n_estimators,
            regressor__max_depth=max_depth,
            regressor__learning_rate=learning_rate
        )
        model.pipeline.fit(X_train, y_train)

        y_pred = model.pipeline.predict(X_valid)
        mse = mean_squared_error(y_valid, y_pred)
        rmse = np.sqrt(mse)
        metrics = {
            "mse": mse,
            "rmse": rmse,
            "mae": mean_absolute_error(y_valid, y_pred),
            "r2_score": r2_score(y_valid, y_pred),
        }
        mlflow.log_params(config)
        mlflow.log_metrics(metrics)
        tune.report(metrics)

# --- Launch Ray Tune experiment with MLflow parent run ---
mlflow.set_experiment("/Shared/house-prices-finetuning")
parent_run = mlflow.start_run(
    run_name=f"ray-finetuning-{datetime.now().strftime('%Y-%m-%d')}",
    tags=tags.dict(),
    description="Hyperparameter tuning with Ray & Optuna"
)

#You use partial to pass fixed arguments (data, config, tags, parent run ID) to the trainable function.
trainable = partial(
    train_with_nested_mlflow,
    X_train=X_train,
    X_valid=X_valid,
    y_train=y_train,
    y_valid=y_valid,
    project_config=config,
    tags=tags,
    parent_run_id=parent_run.info.run_id,
)

"""
Create a Tuner object with:
- The trainable function.
- The search algorithm (OptunaSearch).
- The number of samples (trials).
- The metric to optimize (rmse, minimized).
- The search space.
"""
tuner = tune.Tuner(
    trainable,
    tune_config=tune.TuneConfig(
        search_alg=OptunaSearch(),
        num_samples=2,
        metric="rmse",
        mode="min",
    ),
    param_space=param_space,
)
results = tuner.fit()
mlflow.end_run()

# --- Retrieve best parameters ---
best_result = results.get_best_result(metric="rmse", mode="min")
print("Best hyperparameters:", best_result.config)

trainable = partial(
    train_with_nested_mlflow,
    X_train=X_train,
    X_valid=X_valid,
    y_train=y_train,
    y_valid=y_valid,
    project_config=project_config,
    parent_run_id=run.info.run_id
)

tuner = tune.Tuner(
    trainable,
    tune_config=tune.TuneConfig(
        search_alg=OptunaSearch(),
        num_samples=2,
        metric="rmse",
        mode="min",
    ),
    param_space=param_space,
)

# COMMAND ----------
# For distributed runs, only on Databricks all-purpose or jobs compute
# import ray
# from ray.util.spark import setup_ray_cluster

# _, remote_conn_str = setup_ray_cluster(num_worker_nodes=2)
# ray.init(remote_conn_str)

results = tuner.fit()
mlflow.end_run()

# COMMAND ----------
best_result=results.get_best_result(metric="rmse", mode="min")
best_result.config

# COMMAND ----------