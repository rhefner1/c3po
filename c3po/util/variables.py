"""Variables used throughout the project."""

# API Endpoints
BIBLE_ENDPIONT = 'https://bibles.org/v2/chapters/%s:%s.%s/verses.js?start=%s&end=%s'
NCSU_DINING_ENDPOINT = \
    'http://www.ncsudining.com/diningapi/?method=%s&location=%s&format=json'
TRELLO_CARD_ENDPOINT = 'https://trello.com/1/boards/%s/cards?%s'
WEATHER_ENDPOINT = 'https://api.forecast.io/forecast/%s/%s,%s?units=auto'

# Bible Tools

# Regex matching 1 John 2:2-4:
#  -. any preceding characters
#  -. case insensitivity flag
#  1. a book of the Bible
#  -. whitespace character
#  2. chapter number
#  -. : character
#  3. verse number
#  -. (optional) - character to signify multiple verses
#  4. (optional) second verse number
REGEX_BIBLE = r'(?:.)*(?i)' \
              r'(genesis|exodus|leviticus|numbers|deuteronomy|joshua|' \
              r'judges|ruth|1 samuel|2 samuel|1 kings|2 kings|1 chronicles|' \
              r'2 chronicles|ezra|nehemiah|esther|job|psalms|proverbs|' \
              r'ecclesiastes|song of solomon|isaiah|jeremiah|lamentations|' \
              r'ezekiel|daniel|hosea|joel|amos|obadiah|jonah|micah|nahum|' \
              r'habakkuk|zephaniah|haggai|zechariah|malachi|matthew|mark|' \
              r'luke|john|acts|romans|1 corinthians|2 corinthians|galatians|' \
              r'ephesians|philippians|colossians|1 thessalonians|' \
              r'2 thessalonians|1 timothy|2 timothy|titus|philemon|hebrews|' \
              r'james|1 peter|2 peter|1 john|2 john|3 john|jude|revelation)' \
              r'(?:\s)(\d+)(?::)?(\d+)(?:-)?(\d+)?'
BIBLE_BOOK_ABBR = {
    "joshua": "Josh",
    "ezra": "Ezra",
    "ephesians": "Eph",
    "1 corinthians": "1Cor",
    "john": "John", "hebrews": "Heb",
    "nahum": "Nah",
    "ezekiel": "Ezek",
    "2 john": "2John",
    "philippians": "Phil",
    "numbers": "Num",
    "philemon": "Phlm",
    "2 corinthians": "2Cor",
    "ecclesiastes": "Eccl",
    "2 thessalonians": "2Thess",
    "2 timothy": "2Tim",
    "judges": "Judg",
    "james": "Jas",
    "revelation": "Rev",
    "deuteronomy": "Deut",
    "acts": "Acts",
    "song of solomon": "Song",
    "1 kings": "1Kgs",
    "mark": "Mark",
    "2 chronicles": "2Chr",
    "matthew": "Matt",
    "1 thessalonians": "1Thess",
    "daniel": "Dan",
    "malachi": "Mal",
    "galatians": "Gal",
    "colossians": "Col",
    "ruth": "Ruth",
    "genesis": "Gen",
    "obadiah": "Obad",
    "esther": "Esth",
    "exodus": "Exod",
    "jeremiah": "Jer",
    "proverbs": "Prov",
    "habakkuk": "Hab",
    "luke": "Luke",
    "haggai": "Hag",
    "jonah": "Jonah",
    "romans": "Rom",
    "1 peter": "1Pet",
    "job": "Job",
    "micah": "Mic",
    "2 kings": "2Kgs",
    "isaiah": "Isa",
    "1 chronicles": "1Chr",
    "1 timothy": "1Tim",
    "leviticus": "Lev",
    "zephaniah": "Zeph",
    "joel": "Joel",
    "2 peter": "2Pet",
    "3 john": "3John",
    "jude": "Jude",
    "hosea": "Hos",
    "zechariah": "Zech",
    "nehemiah": "Neh",
    "psalm": "Ps",
    "1 john": "1John",
    "lamentations": "Lam",
    "amos": "Amos",
    "1 samuel": "1Sam",
    "titus": "Titus",
    "2 samuel": "2Sam"
}
BIBLE_ESV = 'eng-ESV'
BIBLE_RSP_LENGTH = 750

# Dining Hall Hours
CLARK_OPEN = 8
CLARK_BREAKFAST_END = 11
CLARK_LUNCH_END = 16
CLARK_CLOSE = 21
CASE_OPEN = 8
CASE_BREAKFAST_END = 11
CASE_LUNCH_END = 16
