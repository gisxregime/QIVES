import textwrap

#naa dinhi tanan story chapter text, and hint folder names.
#textwrap.dedent() remove identation para clean ang code.

#kani na part kay mao ni makita pag mag start ang game, goal na pangitaon.
CHAPTER_GOALS = {
    1: textwrap.dedent("""\
        CHAPTER 1: 
        Zae Hung, 19, found lifeless in her apartment on March 14, 2021.
        Coroner: Suicide by ligature hanging.

        Your Goal:
        Uncover Zae’s hidden messages. Restore corrupted files. Reconstruct the events.
    """),
    2: textwrap.dedent("""\
        CHAPTER 2:
        Find Zae’s hidden notes and clues about pressures she faced.
    """),
    3: textwrap.dedent("""\
        CHAPTER 3:
        Find Zae’s unsent letter about authenticity and burnout.
    """),
    4: textwrap.dedent("""\
        CHAPTER 4:
        Locate files that reveal Zae’s last 48 hours.
    """),
    5: textwrap.dedent("""\
        CHAPTER 5:
        Locate the final message that shows what really happened.
    """)
}

#sulod sa next.txt na file per chapter
STORY_CHUNKS = {
    1: textwrap.dedent("""\
            RECOVERED MESSAGE (fragmented):

            I am trying to be okay. I really am.
            I told Mom I would get help.
            But something happened yesterday.
            Something I cannot say out loud.
            I feel watched. Followed. Misread.
            If you're reading this… please continue.
            The truth is not in one file.
            It's scattered everywhere.
            -Zae
    """),
    2: textwrap.dedent("""\
            RECOVERED NOTE (fragmented):

            They said I’m fake.
            They said I deserve to disappear.
            The messages never stop.
            Different accounts. Same words.
            I don’t know who to trust anymore.
            -Zae
    """),
    3: textwrap.dedent("""\
            RECOVERED DRAFT (unsent letter):
            
            I don't hate life. I hate noise.
            The expectations.
            The perfect image.
            I lost control of my own voice.
            If something ever happens to me...
            please understand:
            it was'nt sudden.
            It was slow.
            And no one ever noticed.
            -Zae   
    """),
    4: textwrap.dedent("""\
            TIMELINE (recovered last 48 hours):
            
            - Tried to get help.
            - Attempted therapy.
            - Texted Mom emergency.
            - Went home early after disturbing anonymous message.
            - Laptop mid-upload. Music playing.
            - Anonymous messages continuing.
            """),
    5: textwrap.dedent("""\
            FINAL RECOVERY:
            
            Zae did not plan to die that night.
            Her laptop mid-upload. Music playing.
            Final message shows her crying silently, phone in hand.
            Anonymous messages flashing.
            She tried to call someone. No one answered.
            
            Exhaustion led to her surrender.
            The world wouldn't listen.
            
            CASE CONCLUDED.
            THANK YOU FOR GIVING ZAE'S STORY THE VOICE SHE NEVER HAD.
            """)
}

#dir hint names per chapter
HINT_FOLDER_TEMP = {
    1: ["hidden_msg", "secret_notes", "in_the_other_files"],
    2: ["pressure_notes", "harassment_logs", "message_stress"],
    3: ["burnout_drafts", "unsent_letter", "identity_fragments"],
    4: ["last48_timeline", "wala_dinhi", "therapy_trace"],
    5: ["final_truth", "root_cause", "case_resolution"]
}