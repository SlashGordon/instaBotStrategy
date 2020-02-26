from like_strategy import LikeStrategy


class FollowStrategy(LikeStrategy):

    @classmethod
    def is_strategy_for(cls, strategy):
        return cls.__class__.__name__ == strategy

    def __init__(self, config_path):
        super.__init__(config_path)

    def strategy(self):
        self.set_interact()
        self.session.set_do_follow(enabled=True, percentage=50)
        self.session.set_do_like(enabled=True, percentage=50)
        config_tag = {
            'tags': self.config['tags_follow'],
            'amount': self.config.get('tags_follow_amount', 20),
            'interact': self.config.get('tags_follow_interact', True),
        }
        self.session.follow_by_tags(**config_tag)
