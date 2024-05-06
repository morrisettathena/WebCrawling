import pandas as pd
import matplotlib.pyplot as plt
import consts as c
import os
import datetime as dt

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

def save_articles_with_keywords(main_keyword):
    """
    From the ENRArticles file, find any articles that mention the main keyword.
    """
    ENR = pd.read_csv(c.ENR_file)

    columns = list(ENR.columns)
    columns = ["Title", "Title_URL", "Summary2", "Text"]
    columns.extend(keyword_list)
    new_ls = []
    missed_articles = 0

    for i in range(ENR.shape[0]):
        include = False
        article = ENR.iloc[i].copy()
        try:
            content = article["Text"].lower()

            count = content.count(main_keyword.lower())
            # Determine if the article contains the main keyword.  In this case, "mental health".
            # If true, include this article.  If not, skip over.
            if count > 0:
                include = True
                article[main_keyword] = 1

                # Determine if the article also contains the other keywords.
                for related_word in keyword_list:
                    related_count = content.count(related_word.lower())
                    if related_count > 0:
                        related_count = 1
                    article[related_word] = related_count

        except Exception:
            missed_articles += 1

        if include:
            new_ls.append(article[columns])

    # Write results to csv.
    new_enr = pd.DataFrame(data = new_ls, columns = columns)
    new_enr = new_enr.rename(columns={"Summary2": "Date"})
    new_enr = new_enr.set_index(pd.to_datetime(new_enr["Date"]))
    new_enr.to_csv("ExtractedArticles.csv")
    print(f"Missed articles: {missed_articles}")

def make_individual_graph(monthly_sum, keyword, savepath):
    """ Make a graph of one individual keyword over time."""
    fig = plt.figure(figsize=(10, 6))
    
    monthly_sum.plot(label = keyword)

    plt.xlabel("Time")
    plt.ylabel(f"Instances of {keyword} in 3 month period")

    plt.title(f"Mentions of {keyword} over time")
    plt.legend(loc='upper left')
    plt.savefig(os.path.join(savepath, keyword))
    plt.close(fig)
    pass

def visualize_top_n(monthly_sums: list[pd.Series], savepath: str, ENR: pd.DataFrame, n = 5):
    """Make a graph showing the progression of the n most mentioned keywords over time."""

    df = pd.DataFrame(monthly_sums).T.sum()
    topn = list(df.sort_values(ascending=False)[:n].keys())

    # Determine the monthly sums of all topics
    monthly_sums_new = []
    for item in topn:
        monthly_sums_new.append(ENR[item].resample('3ME').sum())

    # Also, find the cumulative value of all topics.
    cumulative = ENR[topn].sum(axis=1)
    cumulative_sums = cumulative.resample("3ME").sum()

    # Graph.
    fig = plt.figure(figsize=(10, 6))
    cumulative_sums.plot(label = "Cumulative", linestyle="--")
    for i in range(n):
        keyword = topn[i]
        monthly_sums_new[i].plot(label = keyword)

    plt.title(f"Mentions of top {n} keywords over time")
    plt.xlabel("Time")
    plt.ylabel(f"Instances of top {n} keywords in 3 month period")
    plt.legend(loc="upper left")
    plt.savefig(os.path.join(savepath, f"Top {n} words"))
    plt.close(fig)

def visualize_cumulative(ENR: pd.DataFrame, savepath: str):
    """Visualize, cumulatively, the mentions of every keyword per aritcle over time."""
    
    fig = plt.figure(figsize=(10, 6))
    ENR[keyword_list].sum(axis = 1).resample("3ME").sum().plot(label = "3 month divides")
    ENR[keyword_list].sum(axis = 1).rolling("90D").sum().plot(label = "Rolling sum over 90 days")
    plt.xlabel("Time")
    plt.title("Cumulative mentions of keywords over time")
    plt.ylabel(f"Cumulative instances of keywords in 3 month periods")
    plt.legend(loc="upper left")
    plt.savefig(os.path.join(savepath, f"Cumulative"))
    plt.close(fig)
    
def visualize():
    """Make visualizations of all the data."""

    # To store the figures, make a new figure path if necessary
    figures_path = os.path.join(os.getcwd(), "figures")
    if not os.path.exists(figures_path):
        os.mkdir(figures_path)

    # Make a new directory to store figures.
    timestamp = dt.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    current_figures = os.path.join(figures_path, timestamp)
    os.mkdir(current_figures)
    individual_figs = os.path.join(current_figures, "individual")
    os.mkdir(individual_figs)

    # Read in the extracted files
    ENR = pd.read_csv(c.Extracted_file, index_col="Date", parse_dates=True)
    ENR.index = pd.to_datetime(ENR.index)

    # Determine monthly sums of every keyword
    monthly_sums = []
    for item in keyword_list:
        monthly_sums.append(ENR[item].resample('3ME').sum())

    # Make a graph of every individual keyword over time.
    for i in range(len(monthly_sums)):
        keyword = keyword_list[i]
        data = monthly_sums[i]
        make_individual_graph(data, keyword, individual_figs)

    # Display the top 3, 5, and 7 keywords over time.
    for n in [3, 5, 7]:
        visualize_top_n(
            monthly_sums = monthly_sums, 
            savepath=current_figures, 
            ENR = ENR, 
            n = n)
        
    # Visualize the cumulative figures over time.
    visualize_cumulative(ENR, current_figures)
    print(f"All visualizations saved in {current_figures}")

save_articles_with_keywords("Mental Health")
visualize()
