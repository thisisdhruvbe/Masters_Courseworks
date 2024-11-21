import itertools
import pandas as pd
from QLearning_new import runGameSimulate  # Make sure to import your simulation function correctly

def run_experiments(gamma_values, epsilon_values, episode_counts):
    """
    Run experiments with all combinations of gamma, epsilon, and numEpisodes.
    """
    # Create a DataFrame to store the results
    results = pd.DataFrame(columns=['Gamma', 'Epsilon', 'NumEpisodes', 'bestLength'])
    
    # Generate all combinations of gamma, epsilon, and numEpisodes
    for gamma, epsilon, numEpisodes in itertools.product(gamma_values, epsilon_values, episode_counts):
        #print(f"Running simulation with Gamma: {gamma}, Epsilon: {epsilon}, Episodes: {numEpisodes}")
        # Run the simulation
        bestLength = runGameSimulate(gamma, epsilon, numEpisodes)
        # Append the results to the DataFrame
        results = results.append({'Gamma': gamma, 'Epsilon': epsilon, 'NumEpisodes': numEpisodes, 'bestLength': bestLength}, ignore_index=True)
    
    # Save the results to a CSV file
    results.to_csv('experiment_results.csv', index=False)
    print("Results saved to 'experiment_results.csv'.")

# Define the range of values for each parameter
gamma_values =[0.8, 0.9, 0.95, 0.99]  
epsilon_values = [0.1, 0.3, 0.5, 0.7]  
episode_counts = [10001, 12001, 17501, 20001] 

if __name__ == '__main__':
    run_experiments(gamma_values, epsilon_values, episode_counts)
