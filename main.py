from argparse import ArgumentParser
import sys

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--task', metavar='--t', type=str, nargs='?', default="train",
                        help="which task to perform - either 'train' or 'eval'.")
    parser.add_argument('--nb_steps', metavar='--nt', type=int, nargs='?', default=10000,
                        help="number of time steps when training RL model.")
    parser.add_argument('--nb_games', metavar='--ng', type=int, nargs='?', default=10000,
                        help="number of games to run when evaluating model after training.")
    parser.add_argument('--finetune', metavar='--fn', type=str, nargs='?', default=None,
                        help="whether to finetune using pretrained model. Provide path to model if yes.")
    parser.add_argument('--model_name', metavar='--m', type=str, nargs='?', default="rl_model",
                        help="which name to use for the model.")
    parser.add_argument('--nb_retries', metavar='--nr', type=int, nargs='?', default=1,
                        help="number of times training is restarted (continued) if it crashes. Set to -1 to train forever.")
    parser.add_argument('--infer_model', metavar='-im', type=str, nargs='?', default=None,
                        help="which model to use for deployment (give full path, without extension '.zip'.")
    ret = parser.parse_args(sys.argv[1:])
    print(ret)

    if ret.task == "train":
        from src.train_agent import train_with_masks
        train_with_masks(
            nb_timesteps=ret.nb_steps,
            nb_games=ret.nb_games,
            finetune=ret.finetune,
            model_name=ret.model_name,
            nb_retries=ret.nb_retries,
            )
    elif ret.task == "deploy":
        if ret.infer_model is None:
            raise ValueError("Please, provide the path to the model to use for deployment, by setting 'infer_model'.")
        elif not os.path.exists(ret.infer_model + ".zip"):
            raise ValueError("The model chosen for deployment does not exist. Chosen model:", ret.infer_model)

        from src.agent import run, pause
        print("\nPausing...")
        pause()
        print("\nRunning...")
        run(ret.infer_model)
    else:
        raise ValueError("Unknown task specified. Available tasks include {'train', 'deploy'}, but used:", ret.task)
