import argparse
import os
from base_strategy import BaseStrategy
from comment_by_tag import CommentStrategy
from comment_by_location import CommentByLocationStrategy
from follow_by_location import FollowByLocationStrategy
from follow_strategy import FollowStrategy
from like_by_location import LikeLocationStrategy
from like_strategy import LikeStrategy


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def StrategyFactory(strategy, args):
    for strategy_cls in [
        CommentByLocationStrategy,
        CommentStrategy,
        FollowByLocationStrategy,
        FollowStrategy,
        LikeLocationStrategy,
        LikeStrategy,
    ]:
        if strategy_cls.is_strategy_for(strategy):
            return strategy_cls(args.config)
    raise ValueError


def run(args):
    config = BaseStrategy.load_config(args.config)
    if config is None:
        return

    strategies = config.get(
        "strategies", []
    )
    for strategy in map(lambda name: StrategyFactory(name, args), strategies):
        strategy.run()


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
