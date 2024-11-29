import matplotlib.pyplot as plt
import numpy as np

def create_histogram(data, title):
    bins = np.arange(0,1.1,0.1)

    print(bins)

    t = "Histogram of cosine similarity counts for "+title

    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=bins, edgecolor='black', color='skyblue', histtype='bar',rwidth=0.8, alpha=0.7, linewidth=1.2)

    plt.xticks(bins, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    plt.xlabel('Cosine Similarity',fontsize=14)
    plt.ylabel('Counts',fontsize=14)

    plt.axhline(0, color='black', linewidth=1)


    plt.title(t)

    plt.tight_layout()
    plt.show()


def create_horizontal_bar_chart(data):
    
    fig = plt.figure(figsize=(10, 5))

    plt.barh(data['categories'], data['values'], color='maroon')

    plt.xlabel("Courses offered")
    plt.ylabel("No. of students enrolled")
    plt.title("Students enrolled in different courses")
    plt.show()


create_horizontal_bar_chart({'categories': ['Recursive Chunking','Semantic Chunking','Token Chunking'],
                             'values':[2987,26188,3417]})


