from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

def calculate_metrics(y_actual, predictions):
    '''
    A function that calculates and prints the RMSE, MAE, sMAPE and R2 score of a given actual and predicted series.
    A caveat of sMAPE, we measure it as outlined by Makridakis and Hibon (2000). Further information can be found in:
    https://robjhyndman.com/hyndsight/smape/. As well as both sources defined in the references folder.
    '''
    # Calculate Mean Squared Error and Root Mean Squared Error
    mse = mean_squared_error(y_actual, predictions)
    rmse = np.sqrt(mse)
    
    # Calculate Mean Absolute Error
    mae = mean_absolute_error(y_actual, predictions)
    
    # Calculate Symmetric Mean Absolute Percentage Error (SMAPE)
    smape = np.mean(2.0 * np.abs(y_actual - predictions) / ((np.abs(y_actual) + np.abs(predictions)) + 1e-10)) * 100
    
    # Calculate R-squared
    r2 = r2_score(y_actual, predictions)

    print(f'RMSE: {rmse}')
    print(f'MAE: {mae}')
    print(f'sMAPE(0-200): {smape}%')
    print(f'R-squared: {r2}')