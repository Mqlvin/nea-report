from handler import CommentHandler
from itertools import zip_longest


class StandardCommentHandler(CommentHandler):
    def __init__(self):
        super().__init__()

    def get_features(self, comment_lines: list[str]) -> dict[str, str]:

        keywords = {kw:0 for kw in ["Name", "Parameters", "Returns", "Purpose"]}
        for kw in keywords:
            line_index = next(i for i, s in enumerate(comment_lines) if s.lower().startswith(kw.lower()))
            keywords[kw] = line_index

        keywords = sorted(keywords.items(), key=lambda item: item[1])
        features = {}

        for current, nxt in zip_longest(keywords, keywords[1:], fillvalue=None):
            lines = comment_lines[current[1]:(nxt[1] if nxt is not None else len(comment_lines))]
            lines[0] = lines[0].lstrip(current[0] + ": ")
            features[current[0]] = " ".join(lines)

        return features


