import csv
import matplotlib.pyplot as plt

# Read data from CSV file
filename = "./complete_information.csv"
with open(filename, "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    data = list(reader)

# Extract data into separate lists
num_students = []
rbtl = []
btl = []
kemeny = []
borda = []
weighted_borda = []
win_count = []

for row in data:
    num_students.append(int(row[0]))
    rbtl.append(float(row[1]))
    btl.append(float(row[2]))
    kemeny.append(float(row[3]))
    borda.append(float(row[4]))
    weighted_borda.append(float(row[5]))
    win_count.append(float(row[6]))

# Create a line plot
plt.plot(num_students, rbtl, label="RBTL")
plt.plot(num_students, btl, label="BTL")
plt.plot(num_students, kemeny, label="Kemeny")
plt.plot(num_students, borda, label="Borda")
plt.plot(num_students, weighted_borda, label="Weighted Borda")
plt.plot(num_students, win_count, label="Win Count")

# Add labels and legend
plt.xlabel("Number of Students")
plt.ylabel("Normalised Kendall-Tau Score")
plt.title("Rankings with complete information")
plt.legend()

# Show plot
plt.show()
