import argparse
import os
from base_strategy import BaseStrategy


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def StrategyFactory(strategy, args):
    for strategy_cls in BaseStrategy.__subclasses__():
        if strategy_cls.is_strategy_for(args):
            return strategy_cls(strategy)
    raise ValueError


def run(args):
    strategies = BaseStrategy(args).data.get('strategies', [])
    for strategy in map(strategies, lambda name: StrategyFactory(name, args)
        strategy.start()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        dest="config",
        required=True,
        help="config file",
        metavar="FILE",
        type=lambda x: is_valid_file(parser, x),
    )
    args = parser.parse_args()
    run(args)