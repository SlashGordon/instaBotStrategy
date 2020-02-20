from like_strategy import LikeStrategy
import random


class LikeLocationStrategy(LikeStrategy):
    def __init__(self, config_path):
        super.__init__(config_path)

    def strategy(self):
        self.set_interact()
        config_like_location = {
            "locations": random.sample(self.data["like_locations"], []),
            "amount": random.randrange(
                1, self.config.get("like_loc_amount", 30)
            ),
            "skip_top_posts": self.config.get("skip_top_posts", True),
        }
        self.session.set_mandatory_words(
            self.config.get("mandatory_tags_loc", [])
        )
        self.session.like_by_locations(**config_like_location)
