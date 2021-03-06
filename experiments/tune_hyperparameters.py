from omegaconf import OmegaConf
import optuna
from optuna.samplers import TPESampler

from run_lstm import main as lstm_main


def optimize(trial):
    # Get default configuration
    YAML_CONFIG = OmegaConf.load("lstm.yaml")
    CLI_CONFIG = OmegaConf.from_cli()
    DEFAULT_CONFIG = OmegaConf.merge(YAML_CONFIG, CLI_CONFIG)

    # Get hyperparameters from Optuna
    OPTUNA_CONFIG = OmegaConf.create({
        "LR": trial.suggest_loguniform("LR", 1e-5, 1e-2),
    })
    CONFIG = OmegaConf.merge(DEFAULT_CONFIG, OPTUNA_CONFIG)

    # Run and return validation loss
    return lstm_main(CONFIG)


def main():
    sampler = TPESampler(seed=1)
    study = optuna.create_study(direction="minimize", sampler=sampler)
    study.optimize(optimize, n_trials=3)


if __name__ == "__main__":
    main()
