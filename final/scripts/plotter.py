import csv
import matplotlib.pyplot as plt

# Open the CSV file and read in the data
with open('./n=10_regular.csv', 'r') as f:
    reader = csv.reader(f)
    headers = next(reader)
    data10 = [list(map(float, row)) for row in reader]

# Transpose the data to make it easier to work with
data10 = list(map(list, zip(*data10)))

# Open the CSV file and read in the data
with open('./n=15_regular.csv', 'r') as f:
    reader = csv.reader(f)
    headers = next(reader)
    data15 = [list(map(float, row)) for row in reader]
# Transpose the data to make it easier to work with
data15 = list(map(list, zip(*data15)))

# Open the CSV file and read in the data
with open('./n=20_regular.csv', 'r') as f:
    reader = csv.reader(f)
    headers = next(reader)
    data20 = [list(map(float, row)) for row in reader]

# Transpose the data to make it easier to work with
data20 = list(map(list, zip(*data20)))


# Set up the plot
fig, axs = plt.subplots(3, 2)
fig.suptitle("Comparison of Voting Methods, |V| = 10, 15, 20")
plt.xlabel('Number of Papers per student')
plt.ylabel('Normalized Score')
plt.legend()

axs_flat = [item for sub_list in axs for item in sub_list]
for ax in axs_flat: 
    ax.set_ylim([0, 0.5])
    
axs[0,0].set_title("Non-Iterative")
axs[0,1].set_title("Iterative")

# Plot the data
axs[0,0].plot(data10[0], data10[1], label='RBTL')
axs[0,0].plot(data10[0], data10[2], label='BTL')
axs[0,0].plot(data10[0], data10[3], label='KEMENY')
axs[0,0].plot(data10[0], data10[4], label='BORDA')
axs[0,0].plot(data10[0], data10[5], label='WEIGHTED BORDA')
axs[0,0].plot(data10[0], data10[6], label='WIN COUNT')

axs[1,0].plot(data15[0], data15[1], label='RBTL')
axs[1,0].plot(data15[0], data15[2], label='BTL')
axs[1,0].plot(data15[0], data15[3], label='KEMENY')
axs[1,0].plot(data15[0], data15[4], label='BORDA')
axs[1,0].plot(data15[0], data15[5], label='WEIGHTED BORDA')
axs[1,0].plot(data15[0], data15[6], label='WIN COUNT')

axs[2,0].plot(data20[0], data20[1], label='RBTL')
axs[2,0].plot(data20[0], data20[2], label='BTL')
axs[2,0].plot(data20[0], data20[3], label='KEMENY')
axs[2,0].plot(data20[0], data20[4], label='BORDA')
axs[2,0].plot(data20[0], data20[5], label='WEIGHTED BORDA')
axs[2,0].plot(data20[0], data20[6], label='WIN COUNT')

axs[0,1].plot(data10[0], data10[7], label='ITER RBTL')
axs[0,1].plot(data10[0], data10[8], label='ITER BTL')
axs[0,1].plot(data10[0], data10[9], label='ITER KEMENY')
axs[0,1].plot(data10[0], data10[10], label='ITER BORDA')
axs[0,1].plot(data10[0], data10[11], label='ITER WEIGHTED BORDA')
axs[0,1].plot(data10[0], data10[12], label='ITER WIN COUNT')

axs[1,1].plot(data15[0], data15[7], label='ITER RBTL')
axs[1,1].plot(data15[0], data15[8], label='ITER BTL')
axs[1,1].plot(data15[0], data15[9], label='ITER KEMENY')
axs[1,1].plot(data15[0], data15[10], label='ITER BORDA')
axs[1,1].plot(data15[0], data15[11], label='ITER WEIGHTED BORDA')
axs[1,1].plot(data15[0], data15[12], label='ITER WIN COUNT')

axs[2,1].plot(data20[0], data20[7], label='ITER RBTL')
axs[2,1].plot(data20[0], data20[8], label='ITER BTL')
axs[2,1].plot(data20[0], data20[9], label='ITER KEMENY')
axs[2,1].plot(data20[0], data20[10], label='ITER BORDA')
axs[2,1].plot(data20[0], data20[11], label='ITER WEIGHTED BORDA')
axs[2,1].plot(data20[0], data20[12], label='ITER WIN COUNT')

# Add a legend
handles, labels = axs[0,0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper left')

plt.show()
