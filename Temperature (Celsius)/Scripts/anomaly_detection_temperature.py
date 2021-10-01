"""Anomaly Detection (Isolation Forest)."""
# Import relevant libraries
import pandas as pd
from sklearn.ensemble import IsolationForest
import time

# Time the script execution
start = time.time()

def get_excel_data(file_path):
    """Load excel data as Pandas DataFrame.

    Parameters
    ----------
    file_path : string
        Define the absolute or relative location of the Excel file.

    Returns
    -------
    data : DataFrame
        A DataFrame containing the information from the Excel file.

    """
    data = pd.read_excel(file_path)

    return data


def create_model(n_estimators, max_samples, contamination, max_features,
                 bootstrap, n_jobs, random_state, verbose):
    """Create machine learning model for anomaly detection.

    Parameters
    ----------
    n_estimators : int
        The number of base estimators in the ensemble.
    max_samples : int
        The number of samples to draw from X to train each base estimator.
    contamination : float
        The proportion of outliers in the data set.
    max_features : int or float
        The number of features to draw from X to train each base estimator.
        If int, then draw max_features features.
        If float, then draw max_features * X.shape[1] features.
    bootstrap : boolean
        If True, individual trees are fit on random subsets of the training
        data sampled with replacement.
        If False, sampling without replacement is performed.
    n_jobs : int or None
        The number of jobs to run in parallel for both fit and predict.
        None means 1 unless in a joblib.parallel_backend context.
        -1 means using all processors.
    random_state : int
        The seed used by the random number generator.
    verbose : int
        Controls the verbosity of the tree building process.

    Returns
    -------
    model : Isolation Forest Algorithm
        The IsolationForest 'isolates' observations by randomly selecting a
        feature and then randomly selecting a split value between the maximum
        and minimum values of the selected feature.
    """
    model = IsolationForest(n_estimators = n_estimators,
                            max_samples = max_samples,
                            contamination = contamination,
                            max_features = max_features,
                            bootstrap = bootstrap,
                            n_jobs = n_jobs,
                            random_state = random_state,
                            verbose = verbose)

    return model


def main():

    # Define the file paths and load the data
    for i in range(1, 11):
        exec(f'file_path_{i} = r"C:\\Users\\user\\Desktop\\Project\\Temperature (Celsius)\\Datasets\\Temperature Datasets\\Temperature_Dataset_{i}.xlsx"')
        exec(f'df_{i} = get_excel_data(file_path_{i})')

    # Create machine learning model for anomaly detection
    isolation_forest_1 = create_model(n_estimators = 100,
                                      max_samples = 'auto',
                                      contamination = float(0.05),
                                      max_features = 1.0,
                                      bootstrap = False,
                                      n_jobs = -1,
                                      random_state = 42,
                                      verbose = 0)

    isolation_forest_2 = create_model(n_estimators = 100,
                                      max_samples = 'auto',
                                      contamination = float(0.02),
                                      max_features = 1.0,
                                      bootstrap = False,
                                      n_jobs = -1,
                                      random_state = 42,
                                      verbose = 0)

    for i in range(1, 4):
        # Train the models using the data given
        exec(f'isolation_forest_1.fit(df_{i}[["Temperature (Celsius)"]])')

        # After the models are defined and fit, find the scores and anomaly column

        # Find out the values of scores column by calling decision_function() of
        # the trained model and passing the target column as parameter
        exec(f'df_{i}["scores"] = isolation_forest_1.decision_function(df_{i}[["Temperature (Celsius)"]])')

        # Find the values of anomaly column by calling the predict() function of
        # the trained model and passing the target column as parameter
        exec(f'df_{i}["anomaly"] = isolation_forest_1.predict(df_{i}[["Temperature (Celsius)"]])')
        exec(f'df_{i}.loc[(df_{i}["anomaly"] == 1), "anomaly"] = 0')
        exec(f'df_{i}.loc[(df_{i}["anomaly"] == -1), "anomaly"] = 1')

        # A negative score value and a 1 for the value of anomaly columns
        # indicate the presence of anomaly
        # A value of 0 for the anomaly represents the normal data
        exec(f'anomaly_{i} = df_{i}.loc[df_{i}["anomaly"] == 1]')
        exec(f'anomaly_index_{i} = list(anomaly_{i}.index)')

        # Save the dataframes in CSV format
        exec(f'df_{i}.to_csv("isolation_forest_temperature_{i}.csv", index = False)')

    for i in range(4, 11):
        # Train the models using the data given
        exec(f'isolation_forest_2.fit(df_{i}[["Temperature (Celsius)"]])')

        # After the models are defined and fit, find the scores and anomaly column

        # Find out the values of scores column by calling decision_function() of
        # the trained model and passing the target column as parameter
        exec(f'df_{i}["scores"] = isolation_forest_2.decision_function(df_{i}[["Temperature (Celsius)"]])')

        # Find the values of anomaly column by calling the predict() function of
        # the trained model and passing the target column as parameter
        exec(f'df_{i}["anomaly"] = isolation_forest_2.predict(df_{i}[["Temperature (Celsius)"]])')
        exec(f'df_{i}.loc[(df_{i}["anomaly"] == 1), "anomaly"] = 0')
        exec(f'df_{i}.loc[(df_{i}["anomaly"] == -1), "anomaly"] = 1')

        # A negative score value and a 1 for the value of anomaly columns
        # indicate the presence of anomaly
        # A value of 0 for the anomaly represents the normal data
        exec(f'anomaly_{i} = df_{i}.loc[df_{i}["anomaly"] == 1]')
        exec(f'anomaly_index_{i} = list(anomaly_{i}.index)')

        # Save the dataframes in CSV format
        exec(f'df_{i}.to_csv("isolation_forest_temperature_{i}.csv", index = False)')


if __name__ == '__main__':
    main()

# Script execution time
print("\nScript Execution Time")
print("--------------------------")
print('It took {0:0.1f} seconds'.format(time.time() - start))
