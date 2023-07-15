import pickle
import matplotlib.pyplot as plt

path = '/home/jakob/Documents/asteroids-with-neat/resources/parameterGraphs/'
file_name = '_temp'
file_path = path + file_name

file_name_x = file_path+ '_x'
file_name_y = file_path + '_y'

file_x = open(file_name_x, 'rb')
x = pickle.load(file_x)
file_x.close()

file_y = open(file_name_y, 'rb')
y = pickle.load(file_y)
file_y.close()

fig, ax = plt.subplots()
ax.plot(x, y, linewidth=2.5)
ax.set_xlabel(file_name)
ax.set_ylabel('Fitness Score')
ax.set_yticks([0, 1000, 2000,3000,4000,5000,6000, 7000, 8000, 9000])
ax.set_title('Fitness Scores for Different Configurations')
plt.tight_layout()
plt.show()

