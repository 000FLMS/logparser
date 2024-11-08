import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

def load_combined_data(data_dir):
    combined_df = pd.DataFrame()
    for csv_file in os.listdir(data_dir):
        if csv_file.endswith('memo_result.csv'):
            file_path = os.path.join(data_dir, csv_file)
            temp_df = pd.read_csv(file_path)
            # Extract parser name from the file name (before '_')
            parser_name = csv_file.split('_')[0]
            # Rename the "Mean" and "Std" columns to include parser name
            temp_df = temp_df.rename(columns={"Mean": f"{parser_name}_Mean", "Std": f"{parser_name}_Std"})
            # Merge with the combined DataFrame based on Dataset
            if combined_df.empty:
                combined_df = temp_df[['Dataset', f"{parser_name}_Mean"]]
            else:
                combined_df = pd.merge(combined_df, temp_df[['Dataset', f"{parser_name}_Mean"]], on='Dataset', how='outer')
    return combined_df

# Draw table for combined time or memory data
def draw_comparison_table(df, title, filename):
    columns_to_consider = df.columns.difference(['Dataset', 'Best']) 
    _, ax = plt.subplots(figsize=(15, 8))
    ax.axis('tight')
    ax.axis('off')
    df['Best'] = df.iloc[:, 1:].min(axis=1)
    # Round all numerical columns to three decimal places
    for col in df.columns[1:]:  # Skip the 'Dataset' column
        df[col] = df[col].apply(lambda x: round(float(x), 3) if isinstance(x, (int, float)) else x)
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    # Style the table with highlights
    for (i, j), cell in table.get_celld().items():
        # Header row or Dataset column
        if i == 0 or j == 0:
            cell.set_text_props(weight='bold')  # Make header and dataset names bold
        # Highlight max values
        elif j != 0 and i > 0:
            try:
                if float(cell.get_text().get_text()) == df.iloc[i-1][columns_to_consider].min():
                    cell.set_text_props(weight='bold')
            except ValueError:
                pass  # Skip non-numeric cells

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)
    plt.title(title, fontsize=14, weight='bold')
    plt.savefig(filename, bbox_inches="tight", dpi=300)
    plt.show()

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


def draw_bar_chart(data_dir, dataset, type):
    # Function to load and combine data from multiple CSV files
    def load_time_data():
        combined_data = pd.DataFrame()
        for csv_file in os.listdir(data_dir):
            if csv_file.endswith(f'{dataset.lower()}_{type}.csv'):
                file_path = os.path.join(data_dir, csv_file)
                temp_df = pd.read_csv(file_path)
                # Extract method name from the filename (up to the first underscore)
                method_name = csv_file.split('_')[0]
                temp_df['Method'] = method_name  # Add a column for method
                combined_data = pd.concat([combined_data, temp_df], ignore_index=True)
        return combined_data
        
    dataset_order = [f'{dataset}_10k', f'{dataset}_50k', f'{dataset}_100k']
    df = load_time_data()
    print(df)
    df = df[df['Dataset'] != f'{dataset}_500k']
    if type == "memo":
        df ["Mean"] = df["Mean"] / 1024
        df ["Std"] = df["Std"] / 1024
    df['Dataset'] = pd.Categorical(df['Dataset'], categories=dataset_order, ordered=True)
    df.sort_values(['Dataset', 'Method'], inplace=True)


    # Pivot the DataFrame to have datasets as index and methods as columns
    mean_df = df.pivot(index='Dataset', columns='Method', values='Mean')
    std_df = df.pivot(index='Dataset', columns='Method', values='Std')

    # Fill missing values if necessary
    mean_df.fillna(0, inplace=True)
    std_df.fillna(0, inplace=True)

    # # Define a color mapping for each method
    if type == "memo":
        color_mapping = {
            'AEL': 'red',
            'Brain': 'yellow',
            'Drain': 'purple'
        }

        # Get the list of colors for the methods in the same order as the columns
        colors = [color_mapping.get(method, '#333333') for method in mean_df.columns]
        # Plotting
        ax = mean_df.plot(kind='bar', yerr=std_df, capsize=4, figsize=(10,6), rot=0, color=colors)
    else:
        # Plotting
        ax = mean_df.plot(kind='bar', yerr=std_df, capsize=4, figsize=(10,6), rot=0)

    if type == "time":
        prompt = "Mean time (s)"
    else:
        prompt = "Mean memory cost (MB)"
    # Customize the plot
    plt.xlabel('Dataset')
    plt.ylabel(prompt)
    plt.title(f'{prompt} per Method for Each Dataset')
    plt.legend(title='Method')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"{type}_{dataset.lower()}.png", bbox_inches="tight", dpi=300)
    plt.show()

if __name__ == "__main__":
    # benchmark_dir = "./BenchmarkCorrected"
    # # benchmark_dir = "TestBenchmark"
    # df = load_data(benchmark_dir)
    # # print(df)
    # draw_distribution_plot(df)
    # draw_benchmark_table(df)

    # # Load and draw combined time data
    # time_dir = "./TimeMemoResult"  # Directory containing time sample CSVs
    # combined_time_df = load_combined_data(time_dir)
    # draw_comparison_table(combined_time_df, "Time Benchmark Comparison for Log Parsers", "time_comparison_table.png")

    # memo_dir = "./TimeMemoResult"  # Directory containing time sample CSVs
    # combined_time_df = load_combined_data(memo_dir)
    # draw_comparison_table(combined_time_df, "Memo Benchmark Comparison for Log Parsers", "memo_comparison_table.png")
    draw_bar_chart("./TimeMemoAll", "Spark", "memo")


    