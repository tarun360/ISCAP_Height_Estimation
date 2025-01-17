import numpy as np
import torch
from torch import nn
from torchmetrics import MeanSquaredError
from torchmetrics import MeanAbsoluteError
from pytorch_lightning import Trainer, seed_everything
from pytorch_lightning.loggers.csv_logs import CSVLogger
from pytorch_lightning.callbacks.early_stopping import EarlyStopping

from modules_height.pytorch_environment import pytorch_env
from modules_height.data_module_height_age_multitask import Data_Module_height_age_multitask
from modules_height.model_lstm_height_age_multitask import lstm_height_age_multitask

if __name__ == '__main__': 
    print(">>>>>> Model 4: LSTM + Cross_Attention + MAE_Loss | FBank Features | MultiTask Estimation (both age & height) <<<<<<")

    # 1. LOAD ENVIRONMENT
    ################ Loading GPU or CPU ###########################################################################
    device = pytorch_env()

    ##### Change to the location that the trained model is stored
    checkpoint_path="best_model/height_age_multitask/height_age_multitask_bestmodel.ckpt"

    ########### Tracking Test MSE & MAE ###########################################################################
    mse_male = MeanSquaredError().to(device)
    mae_male = MeanAbsoluteError().to(device)
    mse_female = MeanSquaredError().to(device)
    mae_female = MeanAbsoluteError().to(device)

    mse_all = MeanSquaredError().to(device)
    mae_all = MeanAbsoluteError().to(device)
    ################################################################################################################

    # 2. EDIT THESE PARAMETERS TO CHANGE THE MODEL HYPER-PARAMETERS 
    params = dict(
        seq_len = 800,                  # Number of timeframes used per sample
        batch_size = 32,                # Number of samples in each batch
        criterion = nn.MSELoss(),       # Loss of BackProp     
        max_epochs = 100,                 # Max Number of Epochs to run the model
        n_features = 84,                # Number of Features per timeframe (84 for this experiment: 80 FBank + 3 Pitch + 1 Gender)
        hidden_size = 64,               # Number of Hidden Units of LSTM
        num_layers = 1,                 # Number of LSTM Layers
        dropout = 0.2,                  # Dropout for LSTM and Dense Layer
        learning_rate = 0.001,          # Learning Rate
        output_size = 1,                # Number of Outputs (1 for height estimation)
        early_stop_patience = 10        # Number of consecutive epochs without any loss reduction after which training stops 
    )
    ################################################################################################################

    trainer = Trainer()
    dm = Data_Module_height_age_multitask(
        seq_len = params['seq_len'],
        batch_size = params['batch_size'], num_workers=4,     # Number of workers for Train_Data_Loader
    )
    test_loader = dm.test_dataloader()
    ###################################################################################################
    # 3. SELECT THE MODEL TO USE

    model = lstm_height_age_multitask.load_from_checkpoint(checkpoint_path,
                    n_features = params['n_features'],
                    hidden_size = params['hidden_size'],
                    seq_len = params['seq_len'],
                    batch_size = params['batch_size'],
                    criterion = params['criterion'],
                    num_layers = params['num_layers'],
                    dropout = params['dropout'],
                    learning_rate = params['learning_rate'], 
                    output_size = params['output_size'],
                    mse_female = mse_female, mae_female = mae_female,
                    mse_male = mse_male, mae_male = mae_male,
                    mse_all = mse_all, mae_all = mae_all
    )
    ####################################################################################################

    # 4. TEST THE MODEL
    trainer.test(model, test_loader)                    

    print()
    print('##################### TESTING for HEIGHT ESTIMATION on Test_Set #####################################')
    err_mse_female = mse_female.compute()
    err_mae_female = mae_female.compute()
    err_mse_male = mse_male.compute()
    err_mae_male = mae_male.compute()
    err_mse_all = mse_all.compute()
    err_mae_all = mae_all.compute()
    print(f"RMSE Height on all Female data: {np.sqrt(err_mse_female.cpu().numpy())}")
    print(f"MAE Height on all Female data: {err_mae_female}")
    print(f"RMSE Height on all Male data: {np.sqrt(err_mse_male.cpu().numpy())}")
    print(f"MAE Height on all Male data: {err_mae_male}")
    print(f"RMSE Height on both Male and Female data: {np.sqrt(err_mse_all.cpu().numpy())}")
    print(f"MAE Height on both Male and Female data: {err_mae_all}")
    print()