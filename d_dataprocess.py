import re

regex_str = [
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token.lower() for token in tokens]
    return tokens

def extract_keyword_from_title(title):
    keywords = []
    title = str(title)
    for token in preprocess(title):
        keywords.append(token)
    ALL_KEYWORDS.extend(keywords)
    return keywords

ALL_KEYWORDS = []

articles = pd.read_csv('dblp_dump/output_article.csv',
                               delimiter=';',
                               usecols=['key','author','title','year','ee', 'cite',
                                        'mdate','pages','journal','volume'], dtype=str)

# Extract Keyword
articles['keyword'] = articles['title'].apply(extract_keyword_from_title).str.join('|')

# Store keyword
ALL_KEYWORDS = pd.DataFrame(ALL_KEYWORDS, columns=["keyword"]).drop_duplicates()

articles.to_csv('out/papers.csv', index=None, header=True)
ALL_KEYWORDS.to_csv('out/keywords.csv', index=None, header=True)
