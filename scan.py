import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import consts as c
import util as u
import numpy as np

#data = util.load_csv()

related_words = ["suicide", "opioids", "overdose", "addiction","drug",
"recovery",
"pain",
"treatment",
"substance abuse",
"prescription",
"help",
"stigma",
"disorder"]   

related_words = []

#related_words = ["opioids"]
#related_words = []



def save_articles_with_keywords():
    """
    From the ENRArticles file, find any articles that mention the mental health keywords specified in keywords.json.
    """

    
    ENR = pd.read_csv(c.ENR_file)

    keywords = u.get_keywords() 


    columns = list(ENR.columns)
    columns = ["Title", "Title_URL", "Summary2", "Text"]
    columns.extend(keywords)
    columns.extend(related_words)

    print(columns)

    new_ls = []

    missed_articles = 0

    for i in range(ENR.shape[0]):
        include = False
        for kwrd in keywords:
            article = ENR.iloc[i].copy()
            try:
                content = article["Text"].lower()

                count = content.count(kwrd.lower())
                if count > 0:
                    include = True
                    article[kwrd] = 1

                    for related_word in related_words:
                        related_count = content.count(related_word.lower())
                        article[related_word] = related_count

            except Exception:
                missed_articles += 1
                #print(f"Error reading on line {i}")

        if include:
            new_ls.append(article[columns])
    new_enr = pd.DataFrame(data = new_ls, columns = columns)
    new_enr = new_enr.rename(columns={"Summary2": "Date"})
    new_enr = new_enr.set_index(pd.to_datetime(new_enr["Date"]))
    new_enr.to_csv("ExtractedArticles.csv")
    print(f"Missed articles: {missed_articles}")

def save_enr_processed_jsonl():
    
    dfile = pd.read_json("./enr-processed.jsonl", lines=True)
    print(dfile.head())
    keywords = u.get_keywords() 


    columns = list(dfile.columns)
    columns = ["title", "text", "publish_date"]
    columns.extend(keywords)
    columns.extend(related_words)

    new_ls = []

    missed_articles = 0

    for i in range(dfile.shape[0]):
        include = False
        for kwrd in keywords:
            article = dfile.iloc[i].copy()
            try:
                content = article["text"].lower()

                count = content.count(kwrd.lower())
                if count > 0:
                    include = True
                    article[kwrd] = 1

                    for related_word in related_words:
                        related_count = content.count(related_word.lower())
                        if related_count > 0:
                            article[related_word] = 1

            except Exception:
                missed_articles += 1
                print(f"Error reading on line {i}")

        if include:
            try:
                new_ls.append(article[columns])
            except Exception:
                missed_articles += 1
                print(f"Error reading on line {i}")
    new_enr = pd.DataFrame(data = new_ls, columns = columns).rename(columns={"publish_date": "Date"})
    new_enr = new_enr.set_index(pd.to_datetime(new_enr["Date"]))
    new_enr.to_csv("ExtractedArticlesENR-Processed.csv")
    print(f"Missed articles: {missed_articles}")

def visualize():
    """
    To be run after save_articles
    """
    #ENR = pd.read_csv("ExtractedArticlesENR-Processed.csv", index_col="Date", parse_dates=True)
    ENR = pd.read_csv(c.Extracted_file, index_col="Date", parse_dates=True)
    ENR.index = pd.to_datetime(ENR.index)

    monthly_sum = ENR["Mental Health"].resample('3M').sum()
    related_words_sums = []

    for item in related_words:
        related_words_sums.append(ENR[item].resample('3M').sum())

    #related_words_sums.append(monthly_sum)
    plt.figure(figsize=(10, 6))

    x = np.arange(len(monthly_sum))

    #plt.bar(x, monthly_sum, width=bar_width/(len(related_words)*2), label='Mental Health', color='skyblue')

    #plt.plot(monthly_sum.index, monthly_sum.values, label="Mental Health")
    
    # Plot monthly sums of related words
    monthly_sum.plot(label="Mental Health")
    
    for i in range(len(related_words_sums)):
        data = related_words_sums[i]
        data.plot(label=related_words[i])
    """
    # Set x-axis major locator to yearly
    ax.xaxis.set_major_locator(mdates.MonthLocator())

    # Set x-axis major formatter to display only year
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    """
    plt.xlabel("Month")
    plt.ylabel("Instances of articles containing keyword")
    plt.legend(loc='upper left')
    plt.show()


#save_enr_processed_jsonl()
#save_articles_with_keywords()
visualize()