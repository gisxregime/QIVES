from random import Random

from auth import register_evidence
from config import DIRS_MIN, DIRS_MAX, FILES_MIN
from story import STORY_CHUNKS


def random_name(rng, kind="file"):
    adjectives = ["old","archive","meta","anon","user","session","temp","dump","trace","sys","log","note"]
    nouns = ["logs","msg","data","img","rec","cache","profile","anomaly","case","entry"]
    if kind == "file":
        ext = rng.choice([".txt",".log",".tmp",".dat",".md"])
        return f"{rng.choice(adjectives)}_{rng.randint(100,9999)}{ext}"
    else:
        return f"{rng.choice(adjectives)}_{rng.choice(nouns)}_{rng.randint(100,999)}"

def fake_file_content(rng):
    choices = [
        "System trace: " + hex(rng.getrandbits(64)),
        "Corrupted block: " + hex(rng.getrandbits(128)),
        "Timestamp: %d-%02d-%02d %02d:%02d" % (
            rng.randint(2018,2021),
            rng.randint(1,12),
            rng.randint(1,28),
            rng.randint(0,23),
            rng.randint(0,59)
        ),
        "Log: user=%s" % rng.choice(["alpha","beta","charlie","delta"]),
        "Fragment: %s" % rng.choice(["lost","missing","error","partial"])
    ]
    if rng.random() < 0.15:
        return "HINT: " + rng.choice(["follow timestamps", "check anomalies", "inspect drafts"])
    return rng.choice(choices)

def build_fs(user_id, chapter, seed, FILES_MAX=40, HINT_FOLDER_TEMPLATES=None):
    rng = Random(seed)
    root = {}
    # generate base directories
    num_dirs = rng.randint(DIRS_MIN, DIRS_MAX)
    dirs = set()
    base_dirs = ["logs", "messages", "media", "anomalies", "dumps", "tmp", "backups", "configs"]
    for name in base_dirs:
        if len(dirs) >= num_dirs:
            break
        if rng.random() < 0.7:
            dirs.add(name)
    while len(dirs) < num_dirs:
        dirs.add(random_name(rng, "dir"))
    for d in dirs:
        root[d] = {}
    root["root_files"] = {}

    # place a bunch of files
    total_files = rng.randint(FILES_MIN, FILES_MAX)
    all_targets = list(root.keys())
    for _ in range(total_files):
        fname = random_name(rng, "file")
        folder = rng.choice(all_targets)
        root[folder][fname] = fake_file_content(rng)

    # add nested decoys
    for d in rng.sample(list(root.keys()), min(3, len(root))):
        if rng.random() < 0.5:
            for _ in range(rng.randint(1, 3)):
                sub = random_name(rng, "dir")
                root[d][sub] = {}
                for __ in range(rng.randint(1, 3)):
                    root[d][sub][random_name(rng, "file")] = fake_file_content(rng)

    # create the themed real folder name
    templates = HINT_FOLDER_TEMPLATES.get(chapter, ["evidence"])
    theme_name = rng.choice(templates) + f"_{rng.randint(100,999)}"

    # decide whether to nest (probability ~ 0.6 for nested as requested)
    nested_prob = 0.6
    is_nested = rng.random() < nested_prob

    if is_nested:
        # pick a parent folder to nest into (prefer non-root_files)
        parents = [k for k in root.keys() if k != "root_files"]
        if not parents:
            parent = "root_files"
        else:
            parent = rng.choice(parents)
        # add themed folder under parent
        root[parent][theme_name] = {}
        # put next.txt inside this themed folder
        root[parent][theme_name]["next.txt"] = STORY_CHUNKS.get(chapter, "NO STORY")
        evidence_path = f"/root/{parent}/{theme_name}/next.txt"
    else:
        # place themed folder at top level
        root[theme_name] = {}
        root[theme_name]["next.txt"] = STORY_CHUNKS.get(chapter, "NO STORY")
        evidence_path = f"/root/{theme_name}/next.txt"

    # register evidence path in DB for teacher/debugging
    register_evidence(user_id, chapter, evidence_path)
    return {"root": root}
