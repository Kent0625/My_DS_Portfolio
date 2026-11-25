# Comparing CNN learning-rate schedules

PyTorch Lightning · Fashion-MNIST · Image classification

I compared three learning-rate schedules for a convolutional neural network on Fashion-MNIST. For each run, I used the highest validation accuracy recorded in the per-epoch training logs.

| Learning-rate schedule | Peak validation accuracy |
|---|---:|
| Cosine | 90.28% |
| Fixed | 89.57% |
| Step decay | 89.20% |

Cosine scheduling finished 0.71 percentage points ahead of the fixed-rate run on this metric. The comparison describes the observed runs. Repeating each schedule across multiple seeds would help estimate how much of the gap is stable.
