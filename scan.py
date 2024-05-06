import pandas as pd
import matplotlib.pyplot as plt
import consts as c
import os
import datetime as dt

#data = util.load_csv()

keyword_list = [
    "Mental Health",
    "Opioid",
    "Addiction",
    "Program",
    "Drug",
    "Recovery",
    "Overdose",
    "Pain",
    "Treatment",
    "Substance Abuse",
    "Prescription",
    "Gun",
    "Help",
    "Provide",
    "Stigma",
    "Disorder",
    "Suicide",
    "Suicide Prevention",
    "Awareness",
    "Compassion",
    "Attempt",
    "Depression",
    "Drinking",
    "Pandemic",
    "Insurance",
    "Counseling",
    "Medical",
    "Veteran",
    "Hospital",
    "Safety",
    "Clinic"
]

#keyword_list = ["Mental Health"]




def save_articles_with_keywords(main_keyword):
    """
    From the ENRArticles file, find any articles that mention the mental health keywords specified in keywords.json.
    """

    
    ENR = pd.read_csv(c.ENR_file)


    columns = list(ENR.columns)
    columns = ["Title", "Title_URL", "Summary2", "Text"]
    columns.extend(keyword_list)
    print(columns)

    print(columns)

    new_ls = []

    missed_articles = 0

    for i in range(ENR.shape[0]):
        include = False
        article = ENR.iloc[i].copy()
        try:
            content = article["Text"].lower()

            count = content.count(main_keyword.lower())
            if count > 0:
                include = True
                article[main_keyword] = 1

                for related_word in keyword_list:
                    related_count = content.count(related_word.lower())
                    if related_count > 0:
                        related_count = 1
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


    columns = list(dfile.columns)
    columns = ["title", "text", "publish_date"]
    columns.extend(keyword_list)

    new_ls = []

    missed_articles = 0

    for i in range(dfile.shape[0]):
        include = False
        for kwrd in keyword_list:
            article = dfile.iloc[i].copy()
            try:
                content = article["text"].lower()

                count = content.count(kwrd.lower())
                if count > 0:
                    include = True
                    article[kwrd] = 1

                    for related_word in keyword_list:
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

def make_individual_graph(monthly_sum, keyword, savepath):
    fig = plt.figure(figsize=(10, 6))
    
    monthly_sum.plot(label = keyword)

    plt.xlabel("Time")
    plt.ylabel(f"Instances of {keyword} in 3 month period")

    plt.legend(loc='upper left')
    plt.savefig(os.path.join(savepath, keyword))
    plt.close(fig)
    pass

def visualize_top_n(monthly_sums: list[pd.Series], savepath: str, ENR: pd.DataFrame, n = 5):

    df = pd.DataFrame(monthly_sums).T.sum()
    topn = list(df.sort_values(ascending=False)[:n].keys())

    monthly_sums_new = []

    for item in topn:
        monthly_sums_new.append(ENR[item].resample('3M').sum())

    
    cumulative = ENR[topn].sum(axis=1)
    cumulative_sums = cumulative.resample("3M").sum()


    fig = plt.figure(figsize=(10, 6))
    cumulative_sums.plot(label = "cumulative", linestyle="--")
    for i in range(n):
        keyword = topn[i]
        monthly_sums_new[i].plot(label = keyword)

    
    plt.xlabel("Time")
    plt.ylabel(f"Instances of top {n} keywords in 3 month period")
    plt.legend(loc="upper left")
    plt.savefig(os.path.join(savepath, f"Top {n} words"))

    plt.close(fig)

def visualize_cumulative(ENR: pd.DataFrame, savepath: str):
    fig = plt.figure(figsize=(10, 6))
    ENR[keyword_list].sum(axis = 1).resample("3M").sum().plot(label = "3 month divides")
    ENR[keyword_list].sum(axis = 1).rolling("90D").sum().plot(label = "Rolling sum over 90 days")
    plt.xlabel("Time")
    plt.ylabel(f"Cumulative instances of keywords in 3 month periods")
    plt.legend(loc="upper left")
    plt.savefig(os.path.join(savepath, f"Cumulative"))
    plt.close(fig)
    
def visualize():

    figures_path = os.path.join(os.getcwd(), "figures")

    if not os.path.exists(figures_path):
        os.mkdir(figures_path)

    timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_figures = os.path.join(figures_path, timestamp)
    os.mkdir(current_figures)
    individual_figs = os.path.join(current_figures, "individual")
    os.mkdir(individual_figs)

    """
    To be run after save_articles
    """
    ENR = pd.read_csv(c.Extracted_file, index_col="Date", parse_dates=True)
    ENR.index = pd.to_datetime(ENR.index)

    monthly_sums = []

    for item in keyword_list:
        monthly_sums.append(ENR[item].resample('3M').sum())

    for i in range(len(monthly_sums)):
        keyword = keyword_list[i]
        data = monthly_sums[i]
        make_individual_graph(data, keyword, individual_figs)

    for n in [3, 5, 7]:
        visualize_top_n(
            monthly_sums = monthly_sums, 
            savepath=current_figures, 
            ENR = ENR, 
            n = n)
    visualize_cumulative(ENR, current_figures)


    


#save_articles_with_keywords("Mental Health")
visualize()