import os
import sys
import sqlite3
import hashlib
import secrets
import textwrap
from datetime import datetime
from random import Random

def main():
    init_db()
    print("HOLLOW THREAD GATEWAY - QIVES\n")
    print("*** TRIGGER WARNING ***")
    print("This game contains themes of self-harm and emotional exhaustion.\n")

    while True:
        print("(1) Log In")
        print("(2) Sign Up")
        print("(3) Quit")
        sel = input("> ").strip()
        if sel == "1":
            uid, username = login()
            if uid:
                break
        elif sel == "2":
            uid, username = signup()
            if uid:
                break
        elif sel == "3":
            print("Goodbye.")
            return
        else:
            print("Invalid option.")

    # main loop
    while True:
        chapter = get_user_progress(uid)
        if chapter > NUM_CHAPTERS:
            print("All chapters completed. Resetting progress to 1.")
            set_user_progress(uid, 1)
            chapter = 1

        print("\n================================================================")
        print("           W E L C O M E   T O   Q I V E S")
        print("================================================================")
        print("You are entering the classified digital archives for the case of Zae.\n")
        print("Type 'p' to proceed.")
        print("Type '--help' for game commands.\n")

        # fixed --help behavior on proceed prompt
        while True:
            opt = input("> ").strip().lower()
            if opt == "p":
                break
            if opt == "--help":
                print("Commands inside the game:")
                print("  ls, cd <dir>, cd .., pwd, file <name>, cat <file>, save, exit\n")
                continue
            print("[!] Invalid. Type 'p' or '--help'.")

        finished = run_chapter(uid, username, chapter)
        if finished:
            new_ch = chapter + 1
            set_user_progress(uid, new_ch)
            print(f"\nChapter {chapter} complete. Chapter {new_ch} unlocked.")
            if new_ch > NUM_CHAPTERS:
                print("\n=== ALL CHAPTERS COMPLETED ===")
                print("Case concluded. Thank you.")
                # reset for replay
                set_user_progress(uid, 1)
                return
            cont = input("Proceed to next chapter? (y/N): ").strip().lower()
            if cont == "y":
                continue
            else:
                return
        else:
            return

if __name__ == "__main__":
    main()
