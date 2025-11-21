import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

dataframe = pd.read_csv('adatok.csv')
X = dataframe[['jatekos_dx', 'jatekos_dy']]
Y = dataframe['kimenet'] # Cél (0, 1, 2, vagy 3)

# 2. Adatok szétválasztása
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# 3. Modell létrehozása és tanítása
model = MLPClassifier(hidden_layer_sizes=(4,), max_iter=500, activation='relu', solver='adam')
model.fit(X_train, y_train)

# 4. Kiértékelés
predictions = model.predict(X_test)
print(f"A modell pontossága: {accuracy_score(y_test, predictions) * 100:.2f}%")

# 5. Modell elmentése
with open('gonosz_ai_model.pkl', 'wb') as file:
    pickle.dump(model, file)
print("Modell elmentve: gonosz_ai_model.pkl")