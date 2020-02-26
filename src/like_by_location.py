from like_strategy import LikeStrategy
import random


class LikeLocationStrategy(LikeStrategy):
    @classmethod
    def is_strategy_for(cls, strategy):
        return cls.__class__.__name__ == strategy

    def __init__(self, config_path):
        super(LikeLocationStrategy, self).__init__(config_path)

    def strategy(self):
        self.set_interact()
        config_like_location = {
            "locations": random.sample(
                set(self.config.get("like_locations", [])), 3
            ),
            "amount": random.randrange(
                1, self.config.get("like_loc_amount", 30)
            ),
            "skip_top_posts": self.config.get("skip_top_posts", True),
        }
        self.session.set_mandatory_words(
            self.config.get("mandatory_tags_loc", [])
        )
        self.session.like_by_locations(**config_like_location)
