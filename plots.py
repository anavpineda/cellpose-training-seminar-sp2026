import matplotlib.pyplot as plt
import os

path = "/hpc/projects/jacobo_group/projects/cellpose/Membranes/2_Channel/HCR/git/cellpose-training-seminar-sp2026"
save_path = os.path.join(path, "train_vs_test_loss.png")

train_losses = [
    0.5164, 0.2412, 0.2204, 0.2113, 0.2011, 0.1941, 0.1880, 0.1817, 0.1784, 0.1716,
    0.1694, 0.1648, 0.1619, 0.1604, 0.1572, 0.1547, 0.1541, 0.1515, 0.1490, 0.1485,
    0.1460, 0.1453, 0.1440, 0.1440, 0.1415, 0.1418, 0.1390, 0.1204, 0.1117, 0.1078, 0.1078
]

test_losses = [
    0.3793, 0.1790, 0.1724, 0.1665, 0.1641, 0.1570, 0.1544, 0.1543, 0.1514, 0.1485,
    0.1465, 0.1496, 0.1420, 0.1417, 0.1367, 0.1391, 0.1333, 0.1338, 0.1356, 0.1301,
    0.1355, 0.1329, 0.1305, 0.1250, 0.1274, 0.1291, 0.1187, 0.1132, 0.1116, 0.1108, 0.1105
]

epochs = [
    0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
    110, 120, 130, 140, 150, 160, 170, 180, 190, 200,
    210, 220, 230, 240, 250, 260, 270, 280, 290
]

plt.figure(figsize=(10,6))
plt.plot(epochs, train_losses, label="Train Loss")
plt.plot(epochs, test_losses, label="Test Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training vs Test Loss")
plt.legend()
plt.grid(True)


plt.savefig(save_path)
