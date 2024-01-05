import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Paths to the results
tcp_folder = "../../results/tcp/"
udp_folder = "../../results/udp/"

# Experiment names and index to indicate which experiment is being run
experiment_name_list = ['Benchmark', 'Packet Corruption %0', 'Packet Corruption %5', 'Packet Corruption %10', 'Packet Duplicate %0', 'Packet Duplicate %5', 
                        'Packet Duplicate %10', 'Packet Loss %0', 'Packet Loss %5', 'Packet Loss %10', 'Packet Loss %15']
experiment_index = 0

# Experiment paths for TCP
tcp_benchmark = tcp_folder + "tcp_benchmark.txt"
tcp_corrupt_0 = tcp_folder + "tcp_corrupt_0%.txt"
tcp_corrupt_5 = tcp_folder + "tcp_corrupt_5%.txt"
tcp_corrupt_10 = tcp_folder + "tcp_corrupt_10%.txt"
tcp_duplicate_0 = tcp_folder + "tcp_duplicate_0%.txt"
tcp_duplicate_5 = tcp_folder + "tcp_duplicate_5%.txt"
tcp_duplicate_10 = tcp_folder + "tcp_duplicate_10%.txt"
tcp_loss_0 = tcp_folder + "tcp_loss_0%.txt"
tcp_loss_5 = tcp_folder + "tcp_loss_5%.txt"
tcp_loss_10 = tcp_folder + "tcp_loss_10%.txt"
tcp_loss_15 = tcp_folder + "tcp_loss_15%.txt"
tcp_path_list = [tcp_benchmark, tcp_corrupt_0, tcp_corrupt_5, tcp_corrupt_10, tcp_duplicate_0, tcp_duplicate_5, tcp_duplicate_10, 
                 tcp_loss_0, tcp_loss_5, tcp_loss_10, tcp_loss_15]


# Experiment paths for UDP
udp_benchmark = '../../results/udp/udp_benchmark.txt'
udp_corrupt_0 = udp_folder + "udp_corrupt_0%.txt"
udp_corrupt_5 = udp_folder + "udp_corrupt_5%.txt"
udp_corrupt_10 = udp_folder + "udp_corrupt_10%.txt"
udp_duplicate_0 = udp_folder + "udp_duplicate_0%.txt"
udp_duplicate_5 = udp_folder + "udp_duplicate_5%.txt"
udp_duplicate_10 = udp_folder + "udp_duplicate_10%.txt"
udp_loss_0 = udp_folder + "udp_loss_0%.txt"
udp_loss_5 = udp_folder + "udp_loss_5%.txt"
udp_loss_10 = udp_folder + "udp_loss_10%.txt"
udp_loss_15 = udp_folder + "udp_loss_15%.txt"
udp_path_list = [udp_benchmark, udp_corrupt_0, udp_corrupt_5, udp_corrupt_10, udp_duplicate_0, udp_duplicate_5, udp_duplicate_10,
                    udp_loss_0, udp_loss_5, udp_loss_10, udp_loss_15]



def draw_plot(tcp_path_list, udp_path_list):
    # This function will be called 11 times, each time with a different experiment
    # The experiment name will be passed as a string
    # The function should plot the results for the experiment 
    # The plot should have a title, axis labels and a legend

    global experiment_index
    tcp_results_list = []
    udp_results_list = []
    while experiment_index < len(experiment_name_list):
        with open(tcp_path_list[experiment_index], 'r') as file:
            for line in file:
                stripped_line = line.strip()
                if stripped_line:
                    tcp_results_list.append(float(stripped_line))

        with open(udp_path_list[experiment_index], 'r') as file:
            for line in file:
                stripped_line = line.strip()
                if stripped_line:
                    udp_results_list.append(float(stripped_line))
        plot_graphs(tcp_results_list, udp_results_list, experiment_name_list[experiment_index])
        experiment_index += 1    

def scatter_plot(tcp_list, udp_list, experiment_name):
    plt.figure(figsize=(15, 5))  
    plt.subplot(1, 3, 1)  # 4 rows, 3 columns, 1st subplot
    plt.scatter(range(len(tcp_list)), tcp_list, color='blue')
    plt.title('Elapsed Time for TCP')
    plt.xlabel(f'{experiment_name} Experiment Run')
    plt.ylabel('Elapsed Time (s)')

    plt.subplot(1, 3, 2)  # 2nd subplot
    plt.scatter(range(len(udp_list)), udp_list, color='red')
    plt.title('Elapsed Time for UDP')
    plt.xlabel(f'{experiment_name} Experiment Run')
    plt.ylabel('Elapsed Time (s)')

    plt.subplot(1, 3, 3)  # 3rd subplot for both together
    plt.scatter(range(len(tcp_list)), tcp_list, color='blue', label='TCP')
    plt.scatter(range(len(udp_list)), udp_list, color='red', label='UDP')
    plt.title('Elapsed Time for Both')
    plt.xlabel(f'{experiment_name} Experiment Run')
    plt.ylabel('Elapsed Time (s)')
    plt.legend()
    plt.tight_layout() 
    plt.show()


def box_plot(tcp_list, udp_list, experiment_name):
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)  # 1st subplot
    plt.boxplot(tcp_list, patch_artist=True, boxprops=dict(facecolor='blue'))
    plt.title(f'TCP {experiment_name} Time')
    plt.ylabel('Elapsed Time (s)')

    plt.subplot(1, 3, 2)  # 2nd subplot
    plt.boxplot(udp_list, patch_artist=True, boxprops=dict(facecolor='red'))
    plt.title(f'UDP {experiment_name} Time')
    plt.ylabel('Elapsed Time (s)')

    plt.subplot(1, 3, 3)  # 3rd subplot for both together
    plt.boxplot([tcp_list, udp_list], patch_artist=True, labels=["TCP", "UDP"], boxprops=dict(facecolor='red'), medianprops=dict(color='black'))
    plt.title(f'Comparison of {experiment_name} Time')
    plt.ylabel('Elapsed Time (s)')
    plt.legend()
    plt.tight_layout() 
    plt.show()


def histogram_plot(tcp_list, udp_list, experiment_name):
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)  # 1st subplot
    plt.hist(tcp_list, alpha=0.5, color='blue')
    plt.title(f'TCP {experiment_name} Times Distribution')
    plt.xlabel('Elapsed Time (s)')
    plt.ylabel('Frequency')

    plt.subplot(1, 3, 2)  # 2nd subplot
    plt.hist(udp_list, alpha=0.5, color='red')
    plt.title(f'UDP {experiment_name} Times Distribution')
    plt.xlabel('Elapsed Time (s)')
    plt.ylabel('Frequency')

    plt.subplot(1, 3, 3)  # 3rd subplot for both together
    plt.hist(tcp_list, alpha=0.5, color='blue', label='TCP')
    plt.hist(udp_list, alpha=0.5, color='red', label='UDP')
    plt.title(f'Distribution of Both {experiment_name} Times')
    plt.xlabel('Elapsed Time (s)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.tight_layout() 
    plt.show()

def confidence_plot(mean_tcp, mean_udp, margin_of_error_tcp, margin_of_error_udp, experiment_name):
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)  # 1st subplot
    plt.plot(range(1, 31), [mean_tcp]*30, 'b-', label='TCP Mean')
    plt.fill_between(range(1, 31), [mean_tcp - margin_of_error_tcp]*30, [mean_tcp + margin_of_error_tcp]*30, color='blue', alpha=0.1)
    plt.title('TCP Mean Elapsed Time with 95% CI')
    plt.xlabel(f'{experiment_name} Experiment Run')
    plt.ylabel('Elapsed Time (s)')

    plt.subplot(1, 3, 2)  # 2nd subplot
    plt.plot(range(1, 31), [mean_udp]*30, 'r-', label='UDP Mean')
    plt.fill_between(range(1, 31), [mean_udp - margin_of_error_udp]*30, [mean_udp + margin_of_error_udp]*30, color='red', alpha=0.1)
    plt.title('UDP Mean Elapsed Time with 95% CI')
    plt.xlabel(f'{experiment_name} Experiment Run')
    plt.ylabel('Elapsed Time (s)')

    plt.subplot(1, 3, 3)  # 3rd subplot for both together
    plt.plot(range(1, 31), [mean_tcp]*30, 'b-', label='TCP Mean')
    plt.plot(range(1, 31), [mean_udp]*30, 'r-', label='UDP Mean')
    plt.fill_between(range(1, 31), [mean_tcp - margin_of_error_tcp]*30, [mean_tcp + margin_of_error_tcp]*30, color='blue', alpha=0.1)
    plt.fill_between(range(1, 31), [mean_udp - margin_of_error_udp]*30, [mean_udp + margin_of_error_udp]*30, color='red', alpha=0.1)
    plt.title('Mean Elapsed Time with 95% CI for Both')
    plt.xlabel(f'{experiment_name} Experiment Run')
    plt.ylabel('Elapsed Time (s)')
    plt.legend()
    plt.tight_layout()  # This helps to ensure there is space between plots
    plt.show()          # Display all the plots as subplots in one figure

def plot_graphs(tcp_list, udp_list, experiment_name):
    # Calculate the mean and standard deviation for each protocol
    mean_tcp = np.mean(tcp_list)
    std_dev_tcp = np.std(tcp_list, ddof=1)  # ddof = 1 for sample standard deviation

    mean_udp = np.mean(udp_list)
    std_dev_udp = np.std(udp_list, ddof=1)

    # Calculate the standard error
    standard_error_tcp = std_dev_tcp / np.sqrt(len(tcp_list))
    standard_error_udp = std_dev_udp / np.sqrt(len(udp_list))

    # Find the margin of error for 95% confidence
    z_score = 1.96 
    margin_of_error_tcp = z_score * standard_error_tcp
    margin_of_error_udp = z_score * standard_error_udp

    # Calculate the 95% confidence interval
    confidence_interval_tcp = (mean_tcp - margin_of_error_tcp, mean_tcp + margin_of_error_tcp)
    confidence_interval_udp = (mean_udp - margin_of_error_udp, mean_udp + margin_of_error_udp)

    scatter_plot(tcp_list, udp_list, experiment_name)
    box_plot(tcp_list, udp_list, experiment_name)
    histogram_plot(tcp_list, udp_list, experiment_name)
    confidence_plot(mean_tcp, mean_udp, margin_of_error_tcp, margin_of_error_udp, experiment_name)

# Below is the code to run the plot
# draw_plot(tcp_path_list, udp_path_list)