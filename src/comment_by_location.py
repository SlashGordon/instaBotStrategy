import random
from comment_by_tag import CommentStrategy
from like_by_location import LikeLocationStrategy


class CommentByLocationStrategy(LikeLocationStrategy, CommentStrategy):
    @classmethod
    def is_strategy_for(cls, strategy):
        return cls.__name__ == strategy

    def __init__(self, config_path):
        super(CommentByLocationStrategy, self).__init__(config_path)

    def strategy(self):
        CommentStrategy.set_interact(self)
        config_comment_location = {
            "locations": random.choice(
                set(self.config.get(["like_locations"], [])),
            ),
            "amount": random.randrange(
                1, self.config.get("comment_loc_amount", 30)
            ),
            "skip_top_posts": self.config.get("skip_top_posts", True),
        }
        self.session.comment_by_locations(**config_comment_location)
