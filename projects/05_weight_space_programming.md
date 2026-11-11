---
title: "Weight-Space Programming: Fashion-MNIST Results"
---

# Weight-Space Programming: Fashion-MNIST Results

All **nine training runs completed successfully** on Fashion-MNIST’s T-shirt/top versus Trouser task.

| Starting weights | Validation accuracy before training | After 10 epochs |
|---|---:|---:|
| He | 58.57% | 95.77% |
| Xavier | 58.57% | 95.57% |
| LLM-written | **88.90%** | **97.20%** |

Values are averages across three seeds. All models received the same Adam training.

The LLM-written weights provided a strong initial advantage and finished **1.43 percentage points above He**. This finding applies to this tiny binary classifier and single programmed candidate; it does not prove that weight-space programming is generally better.

## Learning curves

```{figure} ../experiments/weight_space_programming/results/figure_1_loss.png
:alt: Training and validation loss over ten epochs for He, Xavier, and LLM-written initialization.

Figure 1. Training and validation cross-entropy loss. Curves show means across three seeds; shading shows sample standard deviation. The programmed candidate has lower mean validation loss before training and after ten epochs.
```

```{figure} ../experiments/weight_space_programming/results/figure_2_accuracy.png
:alt: Training and validation accuracy over ten epochs for the three initialization methods.

Figure 2. Training and validation accuracy. Epoch zero measures performance before training. The initial advantage narrows during Adam training but remains at epoch ten; shading shows sample standard deviation across three seeds.
```

## Experiment files

[Download weight_space_programming_results.zip](https://github.com/Kent0625/My_DS_Portfolio/raw/refs/heads/main/experiments/weight_space_programming/weight_space_programming_results.zip) for both figures, raw measurements, checkpoints, configuration, and the exact script.

[Open the runnable notebook](https://github.com/Kent0625/My_DS_Portfolio/blob/main/experiments/weight_space_programming/weight_space_programming.ipynb) or read the [setup and reproduction instructions](https://github.com/Kent0625/My_DS_Portfolio/blob/main/experiments/weight_space_programming/README.md).

The comparison used 2,000 training images, 1,000 separate validation images, a 446-parameter network (49 → 8 → 4 → 2), Adam with learning rate 0.001, batch size 64, ten epochs, and seeds 42, 43, and 44. The split seed was 2026. Inputs were scaled to [0, 1] and average-pooled to 7×7. No test accuracy was evaluated.

**AI-use disclosure:** ChatGPT assisted with code, weight construction, experiment execution, figures, and preparation of this results summary. The runs were executed by ChatGPT at the student's request; the student is not represented as having personally executed them.

This is a short results update, rather than the full 800–1,500-word assignment post.

Research inspiration: [Takehi et al., Sparks of Weight-Space Programming](https://rikiyat.github.io/blog/weight-space-programming/). Dataset: [Fashion-MNIST](https://github.com/zalandoresearch/fashion-mnist).
