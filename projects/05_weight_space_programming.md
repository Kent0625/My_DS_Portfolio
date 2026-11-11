---
title: "Can an LLM Give a Tiny Neural Network a Head Start?"
---

# Can an LLM Give a Tiny Neural Network a Head Start?

A neural network usually starts with random numbers. Training gradually turns those numbers into something useful. But what if its starting weights already encoded a sensible idea about the task? That question motivated this small experiment: **can LLM-written weights help a Fashion-MNIST classifier before training, and does the advantage remain after ten epochs?**

The comparison uses T-shirts/tops and trousers, three initialization methods, and the same Adam training procedure. The programmed model begins at 88.90% validation accuracy and finishes at 97.20%. Those numbers look promising, but the more useful story is what the comparison does—and does not—show.

## Starting weights are more than a technical detail

A weight controls how strongly an input contributes to a neuron's calculation. A bias shifts that calculation. A hidden layer can be written as:

$$
h = \operatorname{ReLU}(Wx+b)
$$

Here, $x$ is the input, $W$ contains the weights, $b$ contains the biases, and ReLU replaces negative values with zero. Initialization means choosing the weights and biases before training begins.

He and Xavier initialization both use random numbers, but their scales are deliberate. They are designed to help signals travel through a network without becoming excessively large or small. He initialization accounts for ReLU activations; Xavier balances the numbers of incoming and outgoing connections.

Adam is the optimizer used here. An optimizer updates parameters using gradients, which describe how changing the parameters affects prediction error. This experiment measures error with cross-entropy loss. Unlike accuracy, which counts correct predictions, cross-entropy also reflects how confident predictions are.

The research post [Sparks of Weight-Space Programming](https://rikiyat.github.io/blog/weight-space-programming/) explores LLMs directly reading and writing network weights. This pilot tests a narrower idea: use an LLM-authored numerical construction as the initialization, then let Adam refine it. It is inspired by that research, rather than an exact replication.

## What was programmed?

The model receives a 7×7 grayscale image flattened into 49 numbers. Its first programmed layer calculates average brightness in eight regions, including upper sleeve areas, lower leg areas, and the lower center. Later layers compare those regions and turn the contrasts into two class scores.

The intuition is simple: upright T-shirts and trousers tend to have different silhouettes. Encoding that expectation in weights gives the network a starting preference about which shapes matter. This is prior knowledge, not information discovered through gradient updates.

The candidate was fixed before dataset evaluation and was not revised after the results. Its construction used the task description and general garment knowledge. It was not produced in a separate blinded LLM trial, and the architecture and task were chosen during the same planning conversation. Those details matter when interpreting the outcome.

## One changed factor, nine runs

Fashion-MNIST contains grayscale clothing images. This experiment uses only class 0, T-shirt/top, and class 1, Trouser. It therefore measures binary classification, not performance on the complete ten-class benchmark.

Training examples drive parameter updates. Validation examples are kept separate and used to compare performance. Both sets are balanced between the two classes.

| Setting | Value kept fixed |
|---|---|
| Training set | 2,000 images, 1,000 per class |
| Validation set | 1,000 different images, 500 per class |
| Data source | Official Fashion-MNIST training partition |
| Preprocessing | Pixels divided by 255; each 4×4 block averaged into a 7×7 image |
| Architecture | 49 → 8 → 4 → 2; ReLU after each hidden layer |
| Model size | 446 trainable parameters, including biases |
| Optimizer | Adam; learning rate 0.001; betas (0.9, 0.999); epsilon 1e-8 |
| Training | Batch size 64; ten epochs; CPU float32 |
| Seeds | Split: 2026; training: 42, 43, 44 |
| Other settings | No augmentation, dropout, weight decay, scheduler, or early stopping |

Initialization is the changed factor. The **He baseline** uses He uniform initialization in the hidden layers and Xavier uniform in the output layer. **Xavier** uses Xavier uniform throughout. Both use zero biases. **LLM-written** uses the fixed numerical candidate, including its specified biases.

Each method receives the same minibatch order within each paired seed. Three methods across three seeds produce nine runs. All parameters are trained in every condition.

An epoch is one pass through the training set. The experiment evaluates the full training and validation sets at epoch zero, before any updates, and after every epoch. No test accuracy is evaluated or used to select settings.

## Results: a large head start, a smaller final gap

| Initialization | Initial validation accuracy | Validation accuracy after ten epochs | Final validation loss |
|---|---:|---:|---:|
| He baseline | 58.57% | 95.77% ± 0.76 pp | 0.1250 |
| Xavier | 58.57% | 95.57% ± 0.84 pp | 0.1284 |
| LLM-written | **88.90%** | **97.20% ± 0.52 pp** | **0.0835** |

*Table 1. Means across three seeds. The ± values are sample standard deviations in percentage points (pp), not confidence intervals.*

The programmed candidate finishes **1.43 percentage points above He** and **1.63 points above Xavier**. He and Xavier have identical initial accuracy here, although their initial losses differ. Equal accuracy does not mean their predictions have identical confidence.

```{figure} ../experiments/weight_space_programming/results/figure_1_loss.png
:alt: Training and validation cross-entropy loss across epochs for He, Xavier, and LLM-written initialization.

Figure 1. Full-set training and validation loss before training and after each epoch. Lines show means across three seeds; shaded bands show one sample standard deviation.
```

The programmed model's mean validation loss falls from 0.4020 to 0.0835. He falls from 0.6443 to 0.1250, and Xavier from 0.6525 to 0.1284. The lower final loss supports the accuracy comparison: the result is not limited to counting correct predictions.

```{figure} ../experiments/weight_space_programming/results/figure_2_accuracy.png
:alt: Training and validation accuracy across epochs for the three initialization methods.

Figure 2. Accuracy learning curves for the same runs. Epoch zero is measured before Adam updates; the later LLM-written curve includes training. Shading shows sample standard deviation across seeds.
```

The initial validation advantage over He is 30.33 percentage points, much larger than the final 1.43-point gap. Ordinary training closes most of the distance. The programmed model ends with 96.85% training accuracy and 97.20% validation accuracy, so these measurements do not show a large final training–validation gap.

## Why might this have worked?

The outcome is consistent with the expectation that useful starting features can help learning. Region averages already describe coarse garment shape. Adam can refine that representation instead of starting entirely from random features.

However, this is an interpretation, not an isolated demonstration of the mechanism. Initialization changes weight structure, scale, and biases together. A shuffled-weight control that preserves the weight values while disrupting their arrangement could help test whether the geometric structure explains the advantage.

The task is also deliberately small. Two visually different garment classes, downsampled images, and a tiny network make shape-based assumptions practical. The same strategy could fail on rotated clothing, more similar categories, or a larger problem.

There is only one programmed candidate. Its starting weights are identical across seeds, so its epoch-zero performance is identical too. Later variation comes from minibatch ordering, whereas the random baselines also vary their starting weights. These three runs do not measure variability across independent LLM generations.

Finally, there is one data split and only three training seeds. The results support a useful starting-point advantage in this pilot, but they do not establish statistical significance or a general advantage for weight-space programming.

## Three practical lessons

- **Evaluate epoch zero.** It reveals whether useful behavior already exists before training.
- **Compare learning curves under matched conditions.** A dramatic initial advantage can become much smaller after training.
- **Keep the claim as narrow as the evidence.** This programmed candidate helped this binary classifier; broader conclusions need more tasks, splits, and candidates.

## Reproduce the comparison

Open the [self-contained notebook](https://github.com/Kent0625/My_DS_Portfolio/blob/main/experiments/weight_space_programming/weight_space_programming.ipynb) and run its cells in order. The [README](https://github.com/Kent0625/My_DS_Portfolio/blob/main/experiments/weight_space_programming/README.md) also explains local installation and execution. The full [script](https://github.com/Kent0625/My_DS_Portfolio/blob/main/experiments/weight_space_programming/experiment.py) is available for inspection.

[Download the results ZIP](https://github.com/Kent0625/My_DS_Portfolio/raw/refs/heads/main/experiments/weight_space_programming/weight_space_programming_results.zip) for both figures, raw measurements, exact split indices, configuration, fixed weights, and checkpoints. The saved weights reproduce this candidate without requiring another LLM call.

## References and AI-use disclosure

- Takehi, Teoh, Zhang, and Khattab. [Sparks of Weight-Space Programming](https://rikiyat.github.io/blog/weight-space-programming/). Research inspiration.
- Xiao, Rasul, and Vollgraf. [Fashion-MNIST paper](https://arxiv.org/abs/1708.07747) and [official dataset repository](https://github.com/zalandoresearch/fashion-mnist).
- PyTorch documentation: [weight initialization](https://docs.pytorch.org/docs/stable/nn.init.html), [Adam](https://docs.pytorch.org/docs/stable/generated/torch.optim.Adam.html), and [cross-entropy](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html).
- Lightning documentation: [Trainer](https://lightning.ai/docs/pytorch/stable/common/trainer.html).

The class notebook was unavailable; the implementation was prepared independently using the documented APIs. The figures were generated from the recorded experiment outputs.

**AI-use disclosure:** ChatGPT assisted with brainstorming, research, code, weight construction, experiment execution, figures, and drafting this blog post.
