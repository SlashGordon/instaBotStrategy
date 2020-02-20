from like_strategy import LikeStrategy


class FollowStrategy(LikeStrategy):
    def __init__(self, config_path):
        super.__init__(config_path)

    def strategy(self):
        self.set_interact()
        self.session.set_do_follow(enabled=True, percentage=50)
        self.session.set_do_like(enabled=True, percentage=50)
        self.session.set_mandatory_words(
            self.config.get("mandatory_tags_loc", [])
        )
        config_tag = {
            "locations": self.config["locations_follow"],
            "amount": self.config.get("locations_follow_amount", 20),
            "skip_top_posts": self.config.get(
                "locations_follow_skip_top_posts", True
            ),
        }
        self.session.follow_by_locations(**config_tag)
