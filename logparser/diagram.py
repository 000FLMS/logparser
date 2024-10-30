import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os



# Function to load all CSV files and create the combined DataFrame
def load_data(benchmark_dir):
    # Create an empty DataFrame to hold the combined data
    combined_df = pd.DataFrame()
    for csv_file in os.listdir(benchmark_dir):
        file_path = os.path.join(benchmark_dir, csv_file)
        # Read each CSV file into a temporary DataFrame
        temp_df = pd.read_csv(file_path)
        # Extract the relevant "Accuracy" column and rename it based on the CSV filename (without extension)
        parser_name = csv_file.split('_')[0]
        combined_df[parser_name] = temp_df['Accuracy']

    # Add the "Dataset" column from the first CSV file (assuming all CSVs have the same dataset order)
    combined_df.insert(0, 'Dataset', temp_df['Dataset'])
    return combined_df

def draw_benchmark_table(df):
    # Exclude Dataset and current Best column
    columns_to_consider = df.columns.difference(['Dataset', 'Best'])  
    # Calculate the "Average" row for each column
    average_values = df.iloc[:, 1:].mean().tolist()
    print(average_values)
    average_row = ['Average'] + average_values

    # Append the average row to the DataFrame
    df.loc[len(df)] = average_row

    df['Best'] = df.iloc[:, 1:].max(axis=1)
    # Round all numerical columns to three decimal places
    for col in df.columns[1:]:  # Skip the 'Dataset' column
        df[col] = df[col].apply(lambda x: round(float(x), 3) if isinstance(x, (int, float)) else x)

    # Plotting the updated table using matplotlib
    _, ax = plt.subplots(figsize=(15, 8))

    # Hide the axes
    ax.xaxis.set_visible(False) 
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)

    # Create a table in the plot
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    # Style the table with highlights
    for (i, j), cell in table.get_celld().items():
        # Header row or Dataset column
        if i == 0 or j == 0:
            cell.set_text_props(weight='bold')  # Make header and dataset names bold
        # Highlight max values
        elif j != 0 and i > 0:
            try:
                if float(cell.get_text().get_text()) == df.iloc[i-1][columns_to_consider].max():
                    cell.set_text_props(weight='bold')
            except ValueError:
                pass  # Skip non-numeric cells

    # Style the table font and size
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.5, 1.5)

    # Title
    plt.title('ACCURACY OF LOG PARSERS ON DIFFERENT DATASETS', fontsize=14, weight='bold')

    # Save and display the updated plot
    plt.savefig("benchmark_table.png", bbox_inches="tight", dpi=300)
    plt.show()



def draw_distribution_plot(df):
    columns_to_consider = df.columns.difference(['Dataset', 'Best'])  
    
    # Melting the DataFrame to create "variable" and "value" columns for plotting
    df_melted = df.melt(id_vars=['Dataset'], value_vars=df[columns_to_consider], var_name='LogParser', value_name='Accuracy')
    print(df_melted)
    # Calculate the average accuracy for each LogParser
    log_parser_means = df_melted.groupby('LogParser')['Accuracy'].mean().sort_values()

    # Sort the 'LogParser' column based on these average values
    df_melted['LogParser'] = pd.Categorical(df_melted['LogParser'], categories=log_parser_means.index, ordered=True)

    # Plotting the boxplot using seaborn
    plt.figure(figsize=(15, 8))
    sns.boxplot(x='LogParser', y='Accuracy', data=df_melted, palette='coolwarm')

    # Rotate the x labels to match the reference image
    plt.xticks(rotation=45, ha='right')

    # Labeling
    plt.title('Accuracy Distribution of Log Parsers across Different Types of Logs')
    plt.ylabel('Accuracy')

    # Save and display the plot
    plt.savefig("accuracy_distribution_plot.png", bbox_inches="tight", dpi=300)
    plt.show()

if __name__ == "__main__":
    benchmark_dir = "./BenchmarkResult"
    # benchmark_dir = "TestBenchmark"
    df = load_data(benchmark_dir)
    # print(df)
    draw_distribution_plot(df)
    draw_benchmark_table(df)
    