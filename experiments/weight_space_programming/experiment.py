"""WSP initialization pilot. Assistant-authored starter; no measured results bundled.

Run: python experiment.py --output outputs/my_run
Only the official TRAINING partition is read. No test-set selection is performed.
"""
# %% Imports and fixed settings
import argparse
import csv
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import lightning as L
import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader, TensorDataset
from torchvision.datasets import FashionMNIST


@dataclass(frozen=True)
class Config:
    epochs: int = 10
    batch_size: int = 64
    learning_rate: float = 0.001
    train_per_class: int = 1000
    val_per_class: int = 500
    split_seed: int = 2026
    seeds: tuple = (42, 43, 44)
    methods: tuple = ("he", "xavier", "wsp")


LABELS = {"he": "He + Adam", "xavier": "Xavier + Adam", "wsp": "LLM-written + Adam"}

# %% Fixed LLM-written candidate, specified before any dataset evaluation
def programmed_state():
    """Deterministically materialize the assistant's numeric weight specification.

    No data, training, randomness, downloaded checkpoint, or feedback is used.
    This is a geometric heuristic written by ChatGPT (GPT-6 Astra) in the planning
    conversation, not a separately blinded LLM trial. See PROVENANCE.md.
    """
    w1 = torch.zeros(8, 49)
    # Each tuple names rows and columns of the 7x7 pooled image, zero-indexed.
    regions = [
        ([1, 2], [0, 1]),             # upper-left sleeve area
        ([1, 2], [5, 6]),             # upper-right sleeve area
        ([4, 5, 6], [1, 2]),          # lower-left leg area
        ([4, 5, 6], [4, 5]),          # lower-right leg area
        ([4, 5, 6], [3]),             # lower central gap / fabric
        ([1, 2, 3], [2, 3, 4]),       # central upper body
        ([3, 4], [0, 1, 5, 6]),       # middle outer edges
        (list(range(7)), list(range(7))),  # whole-image mean
    ]
    for unit, (rows, cols) in enumerate(regions):
        for row in rows:
            for col in cols:
                w1[unit, 7 * row + col] = 1.0 / (len(rows) * len(cols))
    # Signed contrasts and their opposites survive the following ReLU.
    w2 = torch.tensor([
        [0.9, 0.9, -0.5, -0.5, 0.1, 0.1, 0.2, -0.1],
        [-0.9, -0.9, 0.5, 0.5, -0.1, -0.1, -0.2, 0.1],
        [0., 0., 0.5, 0.5, -1., 0., 0., 0.],
        [0., 0., -0.5, -0.5, 1., 0., 0., 0.],
    ])
    return {
        "fc1.weight": w1, "fc1.bias": torch.zeros(8),
        "fc2.weight": w2, "fc2.bias": torch.full((4,), 0.05),
        "fc3.weight": torch.tensor([[2., -2., -0.5, 0.5], [-2., 2., 0.5, -0.5]]),
        "fc3.bias": torch.zeros(2),
    }


class TinyMLP(L.LightningModule):
    def __init__(self, method, learning_rate):
        super().__init__()
        self.fc1, self.fc2, self.fc3 = nn.Linear(49, 8), nn.Linear(8, 4), nn.Linear(4, 2)
        self.learning_rate = learning_rate
        if method == "wsp":
            self.load_state_dict(programmed_state(), strict=True)
        elif method in ("he", "xavier"):
            for layer in (self.fc1, self.fc2, self.fc3):
                if method == "he" and layer is not self.fc3:
                    nn.init.kaiming_uniform_(layer.weight, nonlinearity="relu")
                else:
                    nn.init.xavier_uniform_(layer.weight, gain=1.0)
                nn.init.zeros_(layer.bias)
        else:
            raise ValueError(f"Unknown initialization: {method}")

    def forward(self, x):
        return self.fc3(F.relu(self.fc2(F.relu(self.fc1(x)))))

    def training_step(self, batch, batch_idx):
        x, y = batch
        return F.cross_entropy(self(x), y)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.learning_rate,
                                betas=(0.9, 0.999), eps=1e-8, weight_decay=0.0)

# %% Fixed balanced split; no test dataset is instantiated
def prepare_data(config, root):
    # Use the dataset authors' HTTPS mirror rather than torchvision 0.20's
    # legacy HTTP endpoint. Torchvision still verifies the published checksums.
    class OfficialFashionMNIST(FashionMNIST):
        mirrors = ["https://raw.githubusercontent.com/zalandoresearch/fashion-mnist/master/data/fashion/"]

    source = OfficialFashionMNIST(root=root, train=True, download=True)
    rng = np.random.default_rng(config.split_seed)
    train_ids, val_ids = [], []
    for label in (0, 1):  # original labels: T-shirt/top, Trouser
        ids = np.flatnonzero(source.targets.numpy() == label)
        ids = rng.permutation(ids)
        n, v = config.train_per_class, config.val_per_class
        if n <= 0 or v <= 0 or n + v > len(ids):
            raise ValueError("Invalid split sizes")
        train_ids.extend(ids[:n].tolist())
        val_ids.extend(ids[n:n + v].tolist())
    train_ids, val_ids = rng.permutation(train_ids), rng.permutation(val_ids)
    assert not set(train_ids) & set(val_ids)

    def make(ids):
        images = source.data[torch.tensor(ids)].float().unsqueeze(1) / 255.0
        x = F.avg_pool2d(images, kernel_size=4, stride=4).flatten(1)
        y = source.targets[torch.tensor(ids)].long()
        return TensorDataset(x, y)

    return make(train_ids), make(val_ids), {"train": train_ids.tolist(), "validation": val_ids.tolist()}

# %% Evaluation at epoch zero and after each complete epoch
@torch.inference_mode()
def evaluate(model, dataset):
    was_training = model.training
    model.eval()
    total_loss, correct = 0.0, 0
    for x, y in DataLoader(dataset, batch_size=512, shuffle=False):
        logits = model(x.to(model.device))
        y = y.to(model.device)
        total_loss += F.cross_entropy(logits, y, reduction="sum").item()
        correct += (logits.argmax(1) == y).sum().item()
    model.train(was_training)
    return total_loss / len(dataset), correct / len(dataset)


class LearningCurves(L.Callback):
    def __init__(self, train_data, val_data, method, seed):
        self.train_data, self.val_data = train_data, val_data
        self.method, self.seed, self.rows = method, seed, []

    def record(self, model, epoch):
        train_loss, train_acc = evaluate(model, self.train_data)
        val_loss, val_acc = evaluate(model, self.val_data)
        self.rows.append(dict(method=self.method, seed=self.seed, epoch=epoch,
                              train_loss=train_loss, val_loss=val_loss,
                              train_accuracy=train_acc, val_accuracy=val_acc))

    def on_train_epoch_end(self, trainer, pl_module):
        self.record(pl_module, trainer.current_epoch + 1)


def run_one(config, method, seed, train_data, val_data):
    L.seed_everything(seed, workers=True, verbose=False)
    model = TinyMLP(method, config.learning_rate)
    initial = {k: v.detach().clone() for k, v in model.state_dict().items()}
    callback = LearningCurves(train_data, val_data, method, seed)
    callback.record(model, 0)
    # A separate generator ensures identical minibatch order across methods.
    loader = DataLoader(train_data, batch_size=config.batch_size, shuffle=True,
                        generator=torch.Generator().manual_seed(seed), num_workers=0)
    trainer = L.Trainer(accelerator="cpu", devices=1, precision="32-true",
                        max_epochs=config.epochs, deterministic=True, logger=False,
                        callbacks=[callback],
                        enable_checkpointing=False, enable_progress_bar=False,
                        enable_model_summary=False, num_sanity_val_steps=0)
    start = time.perf_counter()
    trainer.fit(model, train_dataloaders=loader)
    elapsed = time.perf_counter() - start
    return callback.rows, initial, model.state_dict(), elapsed

# %% Tables, labelled learning curves, and export
def write_csv(path, rows):
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows, config):
    summary = []
    for method in config.methods:
        for epoch in (0, config.epochs):
            selected = [r for r in rows if r["method"] == method and r["epoch"] == epoch]
            row = {"method": method, "epoch": epoch, "runs": len(selected)}
            for metric in ("train_loss", "val_loss", "train_accuracy", "val_accuracy"):
                values = np.array([r[metric] for r in selected])
                row[metric + "_mean"] = float(values.mean())
                row[metric + "_sd"] = float(values.std(ddof=1)) if len(values) > 1 else 0.0
            summary.append(row)
    return summary


def plot_curves(rows, config, output):
    plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
    colors = {"he": "#2563eb", "xavier": "#d97706", "wsp": "#0f766e"}
    for metric, label, scale, filename in (
        ("loss", "Cross-entropy loss", 1, "figure_1_loss.png"),
        ("accuracy", "Accuracy (%)", 100, "figure_2_accuracy.png"),
    ):
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.4), sharey=True)
        for ax, split, title in zip(axes, ("train", "val"), ("Training set", "Validation set")):
            for method in config.methods:
                curves = np.array([[r[f"{split}_{metric}"] for r in rows
                                    if r["method"] == method and r["seed"] == seed]
                                   for seed in config.seeds]) * scale
                mean = curves.mean(0)
                sd = curves.std(0, ddof=1) if len(curves) > 1 else np.zeros_like(mean)
                epochs = np.arange(config.epochs + 1)
                ax.plot(epochs, mean, label=LABELS[method], color=colors[method], linewidth=2)
                ax.fill_between(epochs, mean - sd, mean + sd, color=colors[method], alpha=0.12)
            ax.set(title=title, xlabel="Completed training epochs", ylabel=label)
            ax.set_xticks(np.arange(config.epochs + 1))
            ax.grid(alpha=0.18)
            ax.legend(fontsize=9)
            if metric == "accuracy":
                ax.set_ylim(0, 100)
        fig.suptitle("Initialization comparison · T-shirt/top vs Trouser")
        fig.tight_layout()
        fig.savefig(output / filename, dpi=180, bbox_inches="tight")
        plt.close(fig)


def run_experiment(config=Config(), output="outputs/my_run", data_root="data"):
    if config.epochs < 1 or len(config.seeds) < 1:
        raise ValueError("Use at least one epoch and one seed")
    output = Path(output)
    if output.exists() and any(output.iterdir()):
        raise FileExistsError("Choose a new empty output directory to preserve earlier runs")
    output.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    state_json = {k: v.tolist() for k, v in programmed_state().items()}
    weight_bytes = json.dumps(state_json, sort_keys=True, indent=2).encode()
    (output / "wsp_weights.json").write_bytes(weight_bytes)
    manifest = {
        "status": "running", "started_utc": datetime.now(timezone.utc).isoformat(),
        "config": asdict(config), "device": "cpu", "parameter_count": 446,
        "classes": {"0": "T-shirt/top", "1": "Trouser"},
        "preprocessing": "pixels / 255; nonoverlapping 4x4 average pooling; flatten 7x7",
        "wsp_weights_sha256": hashlib.sha256(weight_bytes).hexdigest(),
        "python": platform.python_version(), "platform": platform.platform(),
        "versions": {p: importlib.metadata.version(p) for p in
                     ("torch", "torchvision", "lightning", "numpy", "matplotlib")},
        "test_set_used": False,
    }
    try:
        manifest["git_commit"] = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        manifest["git_commit"] = None
    manifest_path = output / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    train_data, val_data, indices = prepare_data(config, data_root)
    (output / "split_indices.json").write_text(json.dumps(indices))
    rows, timings = [], []
    for seed in config.seeds:
        for method in config.methods:
            print(f"Running {method}, seed {seed} ...", flush=True)
            run_rows, initial, final, elapsed = run_one(config, method, seed, train_data, val_data)
            rows.extend(run_rows)
            write_csv(output / "metrics.csv", rows)
            torch.save(initial, output / f"{method}_seed{seed}_initial.pt")
            torch.save(final, output / f"{method}_seed{seed}_final.pt")
            timings.append(dict(method=method, seed=seed, training_and_evaluation_seconds=elapsed))
    write_csv(output / "timings.csv", timings)
    summary = summarize(rows, config)
    write_csv(output / "summary.csv", summary)
    plot_curves(rows, config, output)
    captions = (
        f"Figure 1. Training and validation cross-entropy after each epoch. Lines show means "
        f"across {len(config.seeds)} seeds; shaded bands show one sample standard deviation, "
        "not confidence intervals. Lower loss is better. Epoch 0 is before Adam updates.\n\n"
        "Figure 2. Training and validation accuracy for the same runs. Higher is better. "
        "Epoch 0 for LLM-written weights is its performance without data-based training. "
        "The subsequent LLM-written curve includes Adam training.\n\n"
        "Table: summary.csv contains initial and final metrics, with accuracy recorded as "
        "fractions (multiply by 100 for percentages). Add your own sentence explaining "
        "what each figure shows after inspecting the measured results.\n"
    )
    (output / "captions.txt").write_text(captions)
    manifest["status"] = "complete"
    manifest["finished_utc"] = datetime.now(timezone.utc).isoformat()
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"Saved measured outputs to {output.resolve()}")
    return rows, summary

# CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="outputs/my_run")
    parser.add_argument("--data-root", default="data")
    args = parser.parse_args()
    run_experiment(output=args.output, data_root=args.data_root)
