import numpy as np
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class SimpleNN(nn.Module):
    def __init__(self, input_dim, hidden_dim=64, output_dim=2):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, output_dim)
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

def select_best_model(df):
    if df.shape[1] < 2:
        raise ValueError("Nombre de colonnes insuffisant pour la classification.")
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {}
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    pred_rf = rf.predict(X_test)
    acc_rf = accuracy_score(y_test, pred_rf)
    models["RandomForest"] = (rf, acc_rf)

    xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    xgb.fit(X_train, y_train)
    pred_xgb = xgb.predict(X_test)
    acc_xgb = accuracy_score(y_test, pred_xgb)
    models["XGBoost"] = (xgb, acc_xgb)

    input_dim = X_train.shape[1]
    output_dim = len(np.unique(y))
    model_nn = SimpleNN(input_dim, hidden_dim=64, output_dim=output_dim)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model_nn.parameters(), lr=0.01)
    X_train_tensor = torch.tensor(X_train.values, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train.values, dtype=torch.long)
    X_test_tensor = torch.tensor(X_test.values, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test.values, dtype=torch.long)
    for epoch in range(50):
        optimizer.zero_grad()
        outputs = model_nn(X_train_tensor)
        loss = criterion(outputs, y_train_tensor)
        loss.backward()
        optimizer.step()
    with torch.no_grad():
        outputs = model_nn(X_test_tensor)
        _, predicted = torch.max(outputs, 1)
        acc_nn = (predicted == y_test_tensor).float().mean().item()
    models["NeuralNetwork"] = (model_nn, acc_nn)

    best_model_name = max(models, key=lambda k: models[k][1])
    best_model, best_acc = models[best_model_name]
    print(f"Modèle sélectionné : {best_model_name} avec une précision de {best_acc:.2f}")
    return best_model
