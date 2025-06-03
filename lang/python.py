from handler import SourceHandler


class PythonHandler(SourceHandler):
    def __init__(self):
        super().__init__()

    def extract_comments(self, lined_file: list[str]) -> list[list[str]]:

        comment_open = False
        comments = []
        current_comment = []
        waiting_for_prim = False

        for line in lined_file:
            content = line.replace(" ", "")  # just strip the line for ease

            if content.startswith("'''"):
                if not comment_open:
                    comment_open = True
                else:
                    comment_open = False
                    waiting_for_prim = True
                    comments.append([comment_line.strip() for comment_line in current_comment if comment_line != ""])
                    current_comment = []
                continue

            if comment_open:
                current_comment.append(line)
            elif waiting_for_prim:
                prim = line.split(' ')[0]
                if prim != "def":
                    comments.pop() # only list for functions
                waiting_for_prim = False

        return comments
