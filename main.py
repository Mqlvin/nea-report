import os
import lang
import comment
import word

### edit this if you need a different comment handler
comment_handler = comment.standard.StandardCommentHandler
### ok dont edit anything else though
handler = comment_handler()
doc = word.Doc()


# base_dir = os.path.expanduser(input("Enter the top-level source directory: "))
base_dir = "./"
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
        lines = list(filter(lambda line: line.replace(" ", "").strip() != "", lines)) # remove blank lines
        comments = ext_map[ext]().extract_comments(lines)


        all_features = []
        for comment in comments:
            features = handler.get_features(comment)
            all_features.append(features)

        doc.add_features(rel_items[file_path], all_features)

doc.save("./functions.docx")

