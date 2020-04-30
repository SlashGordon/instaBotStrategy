from like_strategy import LikeStrategy
import random
import itertools


class CommentStrategy(LikeStrategy):
    @classmethod
    def is_strategy_for(cls, strategy):
        return cls.__class__.__name__ == strategy

    def __init__(self, config_path):
        super(CommentStrategy, self).__init__(config_path)

    def comment_generator(self):
        emoji_list = {
            ":joy:",
            ":heart:",
            ":heart_eyes:",
            ":yum:",
            ":blush:",
            ":heartbeat:",
            ":fire:",
            ":grinning:",
            ":wave:",
            ":see_no_evil:",
            ":kissing_heart:",
            ":v:",
            "",
            ":monkey_face:",
        }

        list_comments_combinations = []
        comments_str = self.config.get("comments", "")
        for comments in comments_str.split(";"):
            list_comments_combinations.append(comments.split(","))

        comments = [
            " ".join(x) for x in itertools.product(*list_comments_combinations)
        ]

        if len(comments) == 1 and comments[0] == "":
            return None

        return list(
            map(
                lambda x: str(f"{x} {random.choice(emoji_list)}", "utf-8"),
                comments
            )
        )

    def set_interact(self):
        super(CommentStrategy, self).set_interact()
        self.session.set_do_follow(
            enabled=True, percentage=random.randrange(0, 5)
        )
        self.session.set_do_like(
            enabled=True, percentage=random.randrange(60, 100)
        )
        self.session.set_do_comment(
            enabled=True, percentage=random.randrange(90, 100)
        )
        self.session.set_comments(self.comment_generator())

    def strategy(self):
        super(CommentStrategy, self).strategy()
