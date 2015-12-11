import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn import svm

digits = datasets.load_digits()

clf = svm.SVC(gamma=0.001, C=100)  # Gamma menentukan tingkat presisi hasil prediksi

print(len(digits.data))

n = -10

x, y = digits.data[:n], digits.target[:n]
clf.fit(x, y)

target_data = -3
print('Prediction: ', clf.predict(digits.data[target_data]))

plt.imshow(digits.images[target_data], cmap=plt.cm.gray_r, interpolation="nearest" )
plt.show()