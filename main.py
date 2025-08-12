import os

import comment
import lang
import word
from lang.python import PythonHandler

### edit this if you need a different comment handler
comment_handler = comment.standard.StandardCommentHandler
### ok dont edit anything else though
handler = comment_handler()
doc = word.Doc()


# base_dir = os.path.expanduser(input("Enter the top-level source directory: "))
base_dir = "./test"
input("Press enter to generate function listing...")
# what the fuck
rel_items = {os.path.join(dp, f):os.path.relpath(os.path.join(dp, f), base_dir) for dp, _, fn in os.walk(os.path.expanduser(base_dir)) for f in fn}

ext_map = {"py": lang.python.PythonHandler, "rs": lang.rust.RustHandler}
rel_items = {base:rel for (base, rel) in rel_items.items() if rel[0] != "."} # trim hidden items n stuff

# at this point, we have a list of paths <-> relative paths, which aren't prefixed with a '.xyz'

target_items = {}
for (ext, handler_class) in ext_map.items():
    target_items.update({base:ext for (base, rel) in rel_items.items() if rel.endswith(ext)})


for (file_path, ext) in target_items.items():
    # try read file
    with open(file_path, "r") as fh:
        lines = fh.readlines()
        lines = [line.rstrip('\n') for line in lines]
        lines = list(filter(lambda line: line.replace(" ", "").strip() != "", lines)) # remove blank lines

        print(f"from {file_path}")
        blocks = PythonHandler().extract_comments(lines)

        # transform content field into array of stripped lines, remove empty lines
        for b in blocks:
            lines = b["content"].split("\n")

            # if ''' type comment, strip it from the start and end lines
            if b["type"] == "triple_quote":

                remove_pad = lines[0].lstrip()
                lines[0] = remove_pad[3:len(remove_pad)].rstrip()

                remove_pad = lines[len(lines) - 1].lstrip()
                lines[len(lines) - 1] = remove_pad[3:len(remove_pad)].rstrip()

                b["content"] = [line for line in lines if line != ""]

            # if its a hashtag # # # # on each line strip that
            elif b["type"] == "hash_block":

                new_lines = []
                for line in lines:
                    stripped = line.lstrip().rstrip()
                    stripped = stripped[1:len(stripped)]
                    stripped = stripped.lstrip()

                    if stripped != "":
                        new_lines.append(stripped)

                b["content"] = new_lines

            else:
                print(f"Unknown type: {b["type"]}. Ignoring.")


        for b in blocks:
            if b["function"]:
                print(b["content"])


        comments = [b["content"] for b in blocks]

        all_features = []
        for comment in comments:
            features = handler.get_features(comment)
            all_features.append(features)

        print(all_features)

        doc.add_features(rel_items[file_path], all_features)

doc.save("./functions.docx")

