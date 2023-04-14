import csv
import matplotlib.pyplot as plt

# Open the CSV file and read in the data
with open('../data/n=30_regular.csv', 'r') as f:
    reader = csv.reader(f)
    headers = next(reader)
    data = [list(map(float, row)) for row in reader]

# Transpose the data to make it easier to work with
data = list(map(list, zip(*data)))

# Set up the plot
fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle('Comparison of Voting Methods, |V| = 30')

plt.xlabel('Number of Papers')
plt.ylabel('Normalized Score')

# Plot the data
ax1.plot(data[0], data[1], label='RBTL')
ax1.plot(data[0], data[2], label='BTL')
ax1.plot(data[0], data[3], label='KEMENY')
ax1.plot(data[0], data[4], label='BORDA')
ax1.plot(data[0], data[5], label='WEIGHTED BORDA')
ax1.plot(data[0], data[6], label='WIN COUNT')

ax2.plot(data[0], data[7], label='ITER RBTL')
ax2.plot(data[0], data[8], label='ITER BTL')
ax2.plot(data[0], data[9], label='ITER KEMENY')
ax2.plot(data[0], data[10], label='ITER BORDA')
ax2.plot(data[0], data[11], label='ITER WEIGHTED BORDA')
ax2.plot(data[0], data[12], label='ITER WIN COUNT')

# Add a legend
ax1.legend()
ax2.legend()

# Show the plot
plt.show()
