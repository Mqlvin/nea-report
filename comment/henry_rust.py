from handler import CommentHandler


class HenryRustHandler(CommentHandler):
    def __init__(self):
        super().__init__()

    def get_features(self, comment_lines: list[str]) -> dict[str, str]:

        for comment in comment_lines:
            print(comment)

        return {}


