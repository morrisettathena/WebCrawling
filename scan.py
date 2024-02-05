import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
import consts as c
import util as u

#data = util.load_csv()

def save_articles_with_keywords():
    """
    From the ENRArticles file, find any articles that mention the mental health keywords specified in keywords.json.
    """
    ENR = pd.read_csv(c.ENR_file)
    new_enr = pd.DataFrame(columns = ENR.columns)

    keywords = u.get_keywords()    

    columns = list(ENR.columns)
    columns = ["Title", "Title_URL", "Summary2", "Text"]
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
                    article[kwrd] = 1
            except Exception:
                missed_articles += 1
                print(f"Error reading on line {i}")

        if include:
            new_ls.append(article[columns])
    new_enr = pd.DataFrame(data = new_ls, columns = columns).rename(columns={"Summary2": "Date"})
    new_enr = new_enr.set_index(pd.to_datetime(new_enr["Date"]))
    new_enr.to_csv("ExtractedArticles.csv")
    print(f"Missed articles: {missed_articles}")

def visualize():
    """
    To be run after save_articles
    """
    keywords = u.get_keywords()
    ENR = pd.read_csv(c.Extracted_file, index_col="Date", parse_dates=True)
    ENR.index = pd.to_datetime(ENR.index)

    monthly_sum = ENR["Mental Health"].resample('3M').sum()
    
    
    ax = monthly_sum.plot(kind='bar', xlabel='Month', ylabel='Instances of keyword', title='Mental Health mentions in ENR articles')
    print(ax.xaxis.get_major_formatter())
    
    plt.xticks(rotation=45, ha='right') 
    plt.show()


#save_articles_with_keywords()
visualize()