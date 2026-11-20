import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models

# Configuration
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "leaf_disease")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "leaf_disease_model.pt")
CHECKPOINT_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "leaf_disease_checkpoint.pt")
NUM_EPOCHS = 10
BATCH_SIZE = 32
LEARNING_RATE = 1e-3
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Simple transform pipeline
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

if not os.path.isdir(DATA_DIR):
    raise FileNotFoundError(f"Leaf disease dataset not found at {DATA_DIR}. Please place images in subfolders per class.")

dataset = datasets.ImageFolder(root=DATA_DIR, transform=transform)
class_names = dataset.classes

torch.manual_seed(42)
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

# Model – MobileNetV2
model = models.mobilenet_v2(weights=None)
model.classifier[1] = nn.Linear(model.last_channel, len(class_names))
model = model.to(DEVICE)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

start_epoch = 1
best_acc = 0.0

# Resume from checkpoint if present
if os.path.exists(CHECKPOINT_PATH):
    try:
        ckpt = torch.load(CHECKPOINT_PATH, map_location=DEVICE)
        model.load_state_dict(ckpt['model_state_dict'])
        optimizer.load_state_dict(ckpt['optimizer_state_dict'])
        start_epoch = ckpt['epoch'] + 1
        best_acc = ckpt.get('best_acc', 0.0)
        print(f"Resumed from checkpoint at epoch {start_epoch}, previous best val acc: {best_acc:.4f}", flush=True)
    except Exception as e:
        print(f"Could not load checkpoint: {e}. Starting fresh.", flush=True)

def train_one_epoch():
    model.train()
    running_loss = 0.0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * inputs.size(0)
    return running_loss / len(train_loader.dataset)

def evaluate():
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
    return correct / total if total > 0 else 0

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
print(f"Starting training on {DEVICE} with {len(class_names)} classes ({len(dataset)} images)", flush=True)

for epoch in range(start_epoch, NUM_EPOCHS + 1):
    loss = train_one_epoch()
    acc = evaluate()
    print(f"Epoch {epoch}/{NUM_EPOCHS} – Loss: {loss:.4f} – Val Accuracy: {acc:.4f}", flush=True)
    
    # Save checkpoint after every epoch
    torch.save({
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'best_acc': max(best_acc, acc),
        'class_names': class_names
    }, CHECKPOINT_PATH)
    
    # Save best model
    if acc > best_acc:
        best_acc = acc
        torch.save({
            'model_state_dict': model.state_dict(),
            'class_names': class_names,
            'val_accuracy': acc,
            'epoch': epoch
        }, MODEL_PATH)
        print(f"--> Saved best model checkpoint (Val Acc: {acc*100:.2f}%) to {MODEL_PATH}", flush=True)

print(f"Training complete! Best validation accuracy: {best_acc:.4f}", flush=True)
