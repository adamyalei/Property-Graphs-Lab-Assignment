def extract_keyword_from_title(title):
    keywords = []
    title = str(title)
    for token in nlp(title):
        if token.pos_ == "NOUN":
            keywords.append(token.lower_)
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
