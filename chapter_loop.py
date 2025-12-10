import secrets
import sys

from auth import get_seed, save_seed, log_action, set_user_progress
from random_fs_generator import build_fs
from story import CHAPTER_GOALS
from util_dirs_file import is_dir, is_file


def run_chapter(user_id, username, chapter):
    seed = get_seed(user_id, chapter)
    if seed is None:
        seed = secrets.randbelow(2**32)
        save_seed(user_id, chapter, seed)

    fs = build_fs(user_id, chapter, seed)["root"]
    path = ["root"]

    def locate():
        node = fs
        for p in path[1:]:
            node = node[p]
        return node

    # Show chapter goal before prompt
    print("\n" + CHAPTER_GOALS.get(chapter, f"CHAPTER {chapter}"))


    while True:
        try:
            prompt = "/" + "/".join(path[1:]) if len(path) > 1 else "/"
            raw = input(f"{username}@qives:{prompt}$ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nUse 'save' to store progress or 'exit' to quit.")
            continue

        if not raw:
            continue

        parts = raw.split()
        cmd = parts[0]

        node = locate()

        if cmd == "--help":
            print("""Command Simple Meaning: 
                    ls	Show files/folders
                    cd <dir>	Go into a folder
                    cd ..	Go back one folder
                    pwd	Show current location
                    file <name>	Show file type
                    cat <file>	Show file content
                    save	Save the progress
                    exit	Close terminal\n""")
            continue

        if cmd == "ls":
            names = sorted(node.keys())
            print("  ".join(names))
            log_action(user_id, f"ls @ {'/'.join(path)}")
            continue

        if cmd == "pwd":
            print("/" + "/".join(path[1:]) if len(path) > 1 else "/")
            log_action(user_id, f"pwd @ {'/'.join(path)}")
            continue

        if cmd == "cd":
            if len(parts) < 2:
                print("cd: missing operand")
                continue
            target = parts[1]
            if target == "..":
                if len(path) > 1:
                    path.pop()
                else:
                    print("cd: already at root")
                log_action(user_id, "cd ..")
                continue
            if is_dir(node, target):
                path.append(target)
                log_action(user_id, f"cd {target} @ {'/'.join(path)}")
            else:
                print("cd: no such directory")
            continue

        if cmd == "file":
            if len(parts) < 2:
                print("file: missing argument")
                continue
            name = parts[1]
            if is_dir(node, name):
                print(f"{name}: directory")
            elif is_file(node, name):
                preview = "\n".join(node[name].splitlines()[:3])
                print(f"{name}: text file\n{preview}")
            else:
                print("file: no such file")
            log_action(user_id, f"file {name} @ {'/'.join(path)}")
            continue

        if cmd == "cat":
            if len(parts) < 2:
                print("cat: missing file")
                continue
            name = parts[1]
            if is_file(node, name):
                print(node[name])
                log_action(user_id, f"cat {name} @ {'/'.join(path)}")
                if name == "next.txt":
                    print("\n--- CHAPTER COMPLETE ---")
                    return True
            elif is_dir(node, name):
                print(f"cat: {name}: is a directory")
            else:
                print("cat: cannot open file")
            continue

        if cmd == "save":
            set_user_progress(user_id, chapter)
            print("Progress saved.")
            log_action(user_id, "save")
            return False

        if cmd == "exit":
            set_user_progress(user_id, chapter)
            print("Exiting...")
            log_action(user_id, "exit")
            sys.exit(0)

        print("Unknown command. Type 'help'.")