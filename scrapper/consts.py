from decouple import config

CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")
USER_AGENT = config("USER_AGENT")

LIST_OF_SUBREDDITS_TO_SCRAP = [
    "india",
    "delhi",
    "teenagers",
    "Asia_irl",
    "indianTeenagers",
    "delhiuniversity",
    "IndiaSpeaks",
    "JEENEETards",
    "programminghorror",
    "Weird",
]
