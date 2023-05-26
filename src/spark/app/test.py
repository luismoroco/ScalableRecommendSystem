from sklearn import svm
import joblib

X = [[0, 0], [1, 1]]
y = [0, 1]

clf = svm.SVC()
clf.fit(X, y)

_file_ = 'model.sav'
joblib.dump(clf, _file_)