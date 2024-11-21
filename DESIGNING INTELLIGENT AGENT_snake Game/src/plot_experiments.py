import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('experiment_results.csv')

def create_plots(x, y, row, col, dataset):
    sns.set(style="whitegrid")
    
    g = sns.FacetGrid(data, col=col, row=row, margin_titles=True, height=4, aspect=1.5)
    g.map_dataframe(sns.lineplot, x, y)
    g.set_axis_labels(x, "bestLength")
    g.set_titles(col_template=f"{col} = "+"{col_name}", row_template=f"{row} = "+"{row_name}")
    
    # Render the plot
    plt.show()

# Generate the plots
# 1. BestLength vs. Epsilon with Gamma as rows and NumEpisodes as columns
create_plots('Epsilon', 'bestLength', 'Gamma', 'NumEpisodes', data)

# 2. BestLength vs. NumEpisodes with Gamma as rows and Epsilon as columns
create_plots('NumEpisodes', 'bestLength', 'Gamma', 'Epsilon', data)

# 3. BestLength vs. Gamma with Epsilon as rows and NumEpisodes as columns
create_plots('Gamma', 'bestLength', 'Epsilon', 'NumEpisodes', data)