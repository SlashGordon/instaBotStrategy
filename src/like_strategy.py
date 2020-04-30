from base_strategy import BaseStrategy
import random


class LikeStrategy(BaseStrategy):

    @classmethod
    def is_strategy_for(cls, strategy):
        return cls.__class__.__name__ == strategy

    def __init__(self, config_path):
        super(LikeStrategy, self).__init__(config_path)

    def set_interact(self):
        config_interact = {
            'amount': self.config.get('interact_amount', 3),
            'randomize': self.config.get('interact_randomize', True),
            'percentage': self.config.get(
                'interact_percentage',
                random.randrange(20, 90)
                ),
            'media': self.config.get('interact_media', 'Photo'),
        }

        config_interact_story = {
            'enabled': self.config.get('story_enabled', True),
            'percentage': self.config.get(
                'story_percentage',
                random.randrange(20, 90)
                ),
            'simulate': self.config.get('story_simulate', False),
        }
        self.session.set_do_story(**config_interact_story)
        # Like posts based on hashtags and like n posts of its poster
        self.session.set_user_interact(**config_interact)

    def strategy(self):
        self.set_interact()
        config_like = {
            'tags': random.sample(set(self.config['like_tags']), 3),
            'amount': random.randrange(
                1, self.config.get('like_tags_amount', 30)
            ),
            'interact': self.config.get('like_interact', True),
        }
        self.session.like_by_tags(**config_like)
