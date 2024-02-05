import pandas as pd
import json
import consts as c

#data = util.load_csv()

def save_articles_with_keywords():
    """
    From the ENRArticles file, find any articles that mention the mental health keywords specified in keywords.json.
    """
    ENR = pd.read_csv(c.ENR_file)
    new_enr = pd.DataFrame(columns = ENR.columns)

    with open(c.Kword_file) as file:
        keywords = json.load(file)

    columns = list(ENR.columns)
    columns.extend(keywords)

    new_ls = []

    missed_articles = 0

    for i in range(ENR.shape[0]):
        include = False
        for kwrd in keywords:
            article = ENR.iloc[i].copy()
            try:
                count = article["Text"].lower().count(kwrd.lower())
                if count > 0:
                    include = True
                    article[kwrd] = count
            except Exception:
                missed_articles += 1
                print(f"Error reading on line {i}")

        if include:
            new_ls.append(article)
    new_enr = pd.DataFrame(data = new_ls, columns = columns)
    new_enr.to_csv("ExtractedArticles.csv")
    print(f"Missed articles: {missed_articles}")




save_articles_with_keywords()