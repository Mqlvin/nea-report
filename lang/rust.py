from handler import SourceHandler


class RustHandler(SourceHandler):
    def __init__(self):
        super().__init__()

    def extract_comments(self, lined_file: list[str]) -> list[list[str]]:
        
        comment_open = False
        comments = []
        current_comment = []

        for line in lined_file:
            content = line.replace(" ", "") # just strip the line for ease
            if content.startswith("///"):
                if not comment_open:
                    comment_open = True

                if comment_open:
                    first_slash = line.find("/")
                    current_comment.append(line.strip()[first_slash:].lstrip("/").lstrip(" "))
            else:
                if comment_open:
                    comments.append([comment_line for comment_line in current_comment if comment_line != ""])
                    current_comment = []
                comment_open = False

        return comments

