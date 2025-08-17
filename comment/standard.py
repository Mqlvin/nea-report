from itertools import zip_longest

from handler import CommentHandler


class StandardCommentHandler(CommentHandler):
    def __init__(self):
        super().__init__()

    def get_features(self, comment_lines: list[str]) -> dict[str, str]:

        keywords = {kw:0 for kw in ["Name", "Parameters", "Returns", "Purpose"]}
        missing_keywords = []
        for kw in keywords:
            try:
                line_index = next(i for i, s in enumerate(comment_lines) if s.lower().startswith(kw.lower()))
                keywords[kw] = line_index
            except:
                print(f"Err, couldn't find {kw} in file. Ignoring..")
                missing_keywords.append(kw)

        for mkw in missing_keywords:
            del keywords[mkw]

        keywords = sorted(keywords.items(), key=lambda item: item[1])
        features = {}

        for current, nxt in zip_longest(keywords, keywords[1:], fillvalue=None):
            lines = comment_lines[current[1]:(nxt[1] if nxt is not None else len(comment_lines))]
            lines[0] = lines[0].lstrip(current[0] + ": ")
            features[current[0]] = " ".join(lines)

        return features


