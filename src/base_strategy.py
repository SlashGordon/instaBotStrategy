from instapy import InstaPy
from instapy import smart_run
import json


class BaseStrategy:
    def __init__(self, config_path):
        with open(config_path) as f:
            self.data = json.load(f)
            self.session = InstaPy(
                username=self.data['username'],
                password=self.data['password'],
                headless_browser=self.get('headless_browser', True),
                disable_image_load=self.data.get('disable_image_load', False),
                multi_logs=self.data.get('multi_logs', False),
            )
        self.set_limits()

    def run(self):
        with smart_run(self.session):
            self.strategy()

    def set_limits(self):
        self.session.set_dont_include(self.data.get('black_list_friends', []))
        self.session.set_dont_like(self.data.get('black_list_tags', []))
        self.session.set_ignore_if_contains(
            self.data.get('ignore_if_contains', [])
        )

        self.session.set_skip_users(
            skip_private=self.data.get('skip_private', True),
            skip_no_profile_pic=self.data.get('skip_no_profile_pic', True),
            skip_business=self.data.get('skip_business', True),
        )

        self.session.set_relationship_bounds(
            min_posts=self.data.get('min_posts', 3),
            max_posts=self.data.get('max_posts', 1000),
            min_followers=self.data.get('min_followers', 10),
            max_followers=self.data.get('max_followers', 6000),
            potency_ratio=self.data.get('potency_ratio', 1.34),
        )

        self.session.set_mandatory_language(
            enabled=self.data.get('mandatory_enabled', True),
            character_set=self.data.get('character_set', ['LATIN']),
        )
        
        self.session.set_sleep_reduce(self.data.get('set_sleep_reduce', 100))
        self.session.set_quota_supervisor(
            enabled=True,
            sleep_after=self.data.get(
                'sleep_after',
                [
                    'likes',
                    'comments_d',
                    'follows',
                    'unfollows',
                    'server_calls_h',
                ],
            ),
            sleepyhead=self.data.get('sleepyhead', True),
            stochastic_flow=self.data.get('stochastic_flow', True),
            notify_me=self.data.get('notify_me', True),
            peak_likes_daily=self.data.get('peak_likes_daily', False),
            peak_likes_hourly=self.data.get('peak_likes_hourly', 100),
            peak_comments_daily=self.data.get('peak_comments_daily', 200),
            peak_comments_hourly=self.data.get('peak_comments_hourly', 25),
            peak_follows_daily=self.data.get('peak_follows_daily', 125),
            peak_follows_hourly=self.data.get('peak_follows_hourly', 48),
            peak_unfollows_daily=self.data.get('peak_unfollows_daily', 120),
            peak_unfollows_hourly=self.data.get('peak_unfollows_hourly', 40),
            peak_server_calls_daily=self.data.get(
                'peak_server_calls_daily', 3000
            ),
            peak_server_calls_hourly=self.data.get(
                'peak_server_calls_hourly', 300
            ),
        )

    def strategy(self):
        raise NotImplementedError('Override')
