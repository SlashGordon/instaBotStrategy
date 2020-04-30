from instapy import InstaPy
from instapy import smart_run
import json
import os


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]


class BaseStrategy(metaclass=Singleton):

    @staticmethod
    def load_config(config_path):
        if not os.path.exists(config_path):
            return
        with open(config_path) as f:
            return json.load(f)

    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.session = InstaPy(
            username=self.config["username"],
            password=self.config["password"],
            headless_browser=self.config.get("headless_browser", True),
            disable_image_load=self.config.get("disable_image_load", False),
            multi_logs=self.config.get("multi_logs", False),
        )
        self.set_limits()

    @classmethod
    def is_strategy_for(cls, strategy):
        raise NotImplementedError()

    def run(self):
        with smart_run(self.session):
            self.strategy()

    def set_limits(self):
        self.session.set_dont_include(
            self.config.get("black_list_friends", [])
        )
        self.session.set_dont_like(self.config.get("black_list_tags", []))
        self.session.set_ignore_if_contains(
            self.config.get("ignore_if_contains", [])
        )

        self.session.set_skip_users(
            skip_private=self.config.get("skip_private", True),
            skip_no_profile_pic=self.config.get("skip_no_profile_pic", True),
            skip_business=self.config.get("skip_business", True),
        )

        self.session.set_relationship_bounds(
            min_posts=self.config.get("min_posts", 3),
            max_posts=self.config.get("max_posts", 1000),
            min_followers=self.config.get("min_followers", 10),
            max_followers=self.config.get("max_followers", 6000),
            potency_ratio=self.config.get("potency_ratio", 1.34),
        )

        self.session.set_mandatory_language(
            enabled=self.config.get("mandatory_enabled", True),
            character_set=self.config.get("character_set", ["LATIN"]),
        )

        self.session.set_sleep_reduce(self.config.get("set_sleep_reduce", 100))
        self.session.set_quota_supervisor(
            enabled=True,
            sleep_after=self.config.get(
                "sleep_after",
                [
                    "likes",
                    "comments_d",
                    "follows",
                    "unfollows",
                    "server_calls_h",
                ],
            ),
            sleepyhead=self.config.get("sleepyhead", True),
            stochastic_flow=self.config.get("stochastic_flow", True),
            notify_me=self.config.get("notify_me", True),
            peak_likes_daily=self.config.get("peak_likes_daily", False),
            peak_likes_hourly=self.config.get("peak_likes_hourly", 100),
            peak_comments_daily=self.config.get("peak_comments_daily", 200),
            peak_comments_hourly=self.config.get("peak_comments_hourly", 25),
            peak_follows_daily=self.config.get("peak_follows_daily", 125),
            peak_follows_hourly=self.config.get("peak_follows_hourly", 48),
            peak_unfollows_daily=self.config.get("peak_unfollows_daily", 120),
            peak_unfollows_hourly=self.config.get("peak_unfollows_hourly", 40),
            peak_server_calls_daily=self.config.get(
                "peak_server_calls_daily", 3000
            ),
            peak_server_calls_hourly=self.config.get(
                "peak_server_calls_hourly", 300
            ),
        )

    def strategy(self):
        raise NotImplementedError("Override")
