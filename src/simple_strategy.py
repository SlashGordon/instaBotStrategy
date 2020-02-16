from instapy import InstaPy
from instapy import smart_run
import json
import random
import argparse
import os


class SimpleInstaStrategy:
    def __init__(self, config_path):
        with open(config_path) as f:
            self.data = json.load(f)
            self.session = InstaPy(
                username=self.data["username"],
                password=self.data["password"],
                headless_browser=self.data["headless_browser"],
                disable_image_load=self.data["disable_image_load"],
                multi_logs=self.data["multi_logs"],
            )
            self.random_targets = random.choices(self.data["follow_by"])

    def run(self):
        with smart_run(self.session):
            self.session.set_relationship_bounds(
                enabled=True,
                potency_ratio=-0.50,
                delimit_by_numbers=True,
                max_followers=self.data["max_followers"],
                max_following=self.data["max_following"],
                min_followers=self.data["min_followers"],
                min_following=self.data["min_following"],
            )
            self.session.set_sleep_reduce(200)
            self.session.set_quota_supervisor(
                enabled=True,
                sleep_after=[
                    "likes",
                    "comments_d",
                    "follows",
                    "unfollows",
                    "server_calls_h",
                ],
                sleepyhead=True,
                stochastic_flow=True,
                notify_me=True,
                peak_likes_daily=100,
                peak_likes_hourly=700,
                peak_comments_daily=200,
                peak_comments_hourly=25,
                peak_follows_daily=125,
                peak_follows_hourly=48,
                peak_unfollows_daily=400,
                peak_unfollows_hourly=35,
                peak_server_calls_daily=3000,
            )

            self.session.set_dont_include(self.data["black_list_friends"])
            self.session.set_dont_like(self.data["black_list_tags"])

            self.session.set_sleep_reduce(200)
            self.session.set_skip_users(
                skip_private=True, skip_no_profile_pic=True, skip_business=True
            )

            self.session.set_relationship_bounds(
                min_posts=self.data["min_posts"],
                max_posts=self.data["max_posts"],
            )
            self.session.set_mandatory_language(
                enabled=True, character_set=self.data["character_set"]
            )

            for target in self.random_targets:
                try:
                    self.session.follow_user_followers(
                        [target],
                        amount=random.randint(30, 60),
                        randomize=True,
                        sleep_delay=600,
                        interact=True,
                    )
                except:
                    pass

            try:
                self.session.unfollow_users(
                    amount=25,
                    InstapyFollowed=(True, "nonfollowers"),
                    style="RANDOM",
                    unfollow_after=48 * 60 * 60,
                    sleep_delay=600,
                )
            except:
                pass

            try:
                if len(self.data["like_tags"]) > 0:
                    self.session.set_mandatory_words(
                        self.data["mandatory_tags_like"]
                    )
                    self.session.like_by_tags(
                        self.data["like_tags"],
                        amount=self.data["like_tags_amount"],
                    )
            except:
                pass

            try:
                if len(self.data["like_loc"]) > 0:
                    self.session.set_mandatory_words(
                        self.data["mandatory_tags_loc"]
                    )
                    self.session.like_by_locations(
                        self.data["like_loc"],
                        amount=self.data["like_loc_amount"],
                    )
            except:
                pass

            print("Job is done")


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


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
    SimpleInstaStrategy(args.config).run()
