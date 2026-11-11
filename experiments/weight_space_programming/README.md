# Can an LLM Give a Tiny Neural Network a Head Start?

**Status: nine completed Fashion-MNIST runs, archived in `results/`.**
ChatGPT executed the experiment at the student’s request and prepared the accompanying
blog draft. See `results/EXECUTION_NOTE.md` and the post’s AI-use disclosure.

## The question

On a small T-shirt/top versus Trouser subset of Fashion-MNIST, how does an
LLM-written initialization affect validation performance before training and during
ten epochs of Adam training, compared with He and Xavier initialization?

Initialization means choosing the starting weights and biases. A weight controls how
strongly one numerical input contributes to a neuron's output. In this pilot, the LLM
specifies those numbers through a deterministic construction based on expected clothing
shapes. Adam then updates every parameter using the same training data and procedure
for all three methods. This tests a starting-point advantage; it does not establish that
LLMs replace training or understand arbitrary neural networks.

## Fixed protocol

| Item | Setting |
|---|---|
| Dataset | Official Fashion-MNIST training partition only |
| Classes | 0 = T-shirt/top; 1 = Trouser |
| Training set | 2,000 images; 1,000 per class |
| Validation set | 1,000 different images; 500 per class |
| Split seed | 2026; identical indices across every run |
| Input | Pixels divided by 255; average pool each 4×4 block to produce 7×7 pixels |
| Model | 49 inputs → 8 ReLU units → 4 ReLU units → 2 output logits |
| Parameters | 446, including biases; all trainable |
| Loss | Cross-entropy |
| Optimizer | Adam; learning rate 0.001; betas (0.9, 0.999); epsilon 1e-8 |
| Batch size | 64 |
| Epochs | 10 for each trained model; no early stopping |
| Training seeds | 42, 43, 44; paired across methods |
| Other settings | CPU float32; no augmentation, dropout, scheduler, or weight decay |
| Measurements | Full training and validation loss/accuracy at epoch 0 and after each epoch |
| Test data | Not loaded or evaluated; never used for selecting settings |

Three initialization methods are the controlled factor:

1. **He baseline:** Kaiming/He uniform on the two ReLU hidden layers, Xavier uniform
   on the output layer, and zero biases.
2. **Xavier:** Xavier uniform with gain 1 on every weight matrix, and zero biases.
3. **LLM-written:** one fixed numeric candidate supplied in this starter.

Every method uses the same architecture, preprocessing, splits, optimizer, epochs, and
minibatch ordering for each paired seed. The WSP candidate is evaluated before training
at epoch 0. Its later learning curve includes Adam updates. A frozen model's score is
not presented as a learning curve. Comparing three initialization strategies supplies
three settings of the chosen factor; the frozen WSP score is additional context.

## Run it

### Colab or Jupyter

Open `weight_space_programming.ipynb` and run its cells in order. It contains the full
experiment and the fixed candidate, so it does not require a GitHub token, an LLM API
key, or a paid GPU. Use a fresh runtime. If packages were already imported before you
install the pinned versions, restart the runtime and run again.

### Local Python (tested environment: Python 3.12)

From this directory:

```bash
python -m venv .venv
# Activate the virtual environment for your operating system.
python -m pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
python experiment.py --output outputs/my_first_run
```

The dataset downloads on the first run. Use a new output folder when repeating a run;
the runner deliberately refuses to overwrite earlier evidence. CPU training time
depends on the machine. An interrupted run has `status: running` in its manifest and
must not be treated as complete.

## What you will get

- `figure_1_loss.png`: training and validation loss curves, with axes and legends.
- `figure_2_accuracy.png`: training and validation accuracy curves.
- `metrics.csv`: every seed, method, and epoch, including epoch zero.
- `summary.csv`: initial and final means and sample standard deviations.
- `captions.txt`: descriptive captions; add your own sentence interpreting each figure.
- `manifest.json`: configuration, package versions, device, time, and weight checksum.
- `split_indices.json`: exact positions in the official training partition.
- `wsp_weights.json` and initial/final checkpoints: numerical parameters for inspection.
- `timings.csv`: training plus evaluation wall time; excludes LLM generation and download.

The WSP candidate is fixed across seeds. Its epoch-zero scores should be identical.
Later differences across seeds come from minibatch order. Random initializers also vary
their starting weights across seeds. Three seed runs do not measure variation across
different LLM generations. Shaded bands are sample standard deviations, not confidence
intervals or significance tests. Compare the paired runs as well as their means.

## How to interpret your own results

Start with epoch zero: is the programmed network above the balanced chance reference
of 50% accuracy? Then compare validation curves at the same epoch. Does any early
advantage persist, disappear, or reverse by epoch ten? Report exact percentages and
differences in percentage points. Cross-entropy can reveal overconfident mistakes even
when accuracy looks similar. Inspect the training–validation gap before claiming better
generalization. Do not select a favorable seed or silently discard a failed run.

Keep this protocol fixed for the first reported experiment. If you revise the weights
after inspecting validation results, that becomes a new, validation-informed experiment;
retain the original results and disclose the revision. Do not describe the revised
candidate as generated without performance feedback.

Limits to discuss include the easy binary task, downsampling, the tiny architecture,
one manually reasoned LLM candidate, the model writer's prior knowledge of clothing,
and variation in weight scale as well as weight structure. An improvement would not
isolate semantic reasoning as its cause. A later shuffled-weight control could explore
that question, but it is outside this first comparison. A poor WSP result is still useful.

## Write the 800–1,500-word post after running

Use this as a writing outline, not submission-ready prose:

1. **Hook (80–120 words):** Why did you wonder whether starting weights could be written?
2. **Explanation (200–250):** Explain weights, initialization, Adam, and WSP in your own
   words. You can use `h = ReLU(Wx + b)` to connect weights to a neuron's calculation.
3. **Setup (150–200):** State the fixed protocol and the three settings.
4. **Results (150–220):** Insert both figures, captions, and exact measured comparisons.
5. **Discussion (200–250):** Explain what you expected, what happened, and limitations.
6. **Takeaways (80–120):** Give two or three lessons supported by your actual experiment.
7. **References and AI disclosure:** Link sources, notebook/script, and archived weights;
   state exactly what you used ChatGPT for and which work you personally performed.

Your supplied brief restricts AI use to debugging and grammar. You intend to discuss
approval for using an LLM as the experimental method; that approval has not been
recorded here. This starter also uses AI-generated implementation and planning material,
so be explicit about those uses when confirming the scope with your instructor.

## Portfolio integration when the post is ready

The repository's active GitHub Pages workflow builds MyST using `myst.yml` and deploys
on pushes to `main`. Put your finished post in `projects/05_weight_space_programming.md`,
copy the figures into a committed assets folder, and add the post to the MyST table of
contents. The starter is intentionally not in the public navigation. Link the executable
notebook and script in your post. Verify the live page, images, formulas, and code links
in a private browser window, then capture the snippet required for USTeP.

## Sources

- Takehi et al., [Sparks of Weight-Space Programming](https://rikiyat.github.io/blog/weight-space-programming/).
  Research inspiration; this is a small independent pilot, not an exact replication.
- Xiao et al., [Fashion-MNIST paper](https://arxiv.org/abs/1708.07747) and
  [official dataset repository](https://github.com/zalandoresearch/fashion-mnist).
- PyTorch, [weight initialization](https://docs.pytorch.org/docs/stable/nn.init.html),
  [Adam](https://docs.pytorch.org/docs/stable/generated/torch.optim.Adam.html), and
  [cross-entropy](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html).
- Lightning, [Trainer and reproducibility](https://lightning.ai/docs/pytorch/stable/common/trainer.html).

The class notebook `hyperparameters_lightning.ipynb` was not found in this repository.
This implementation was therefore prepared independently, using the documented APIs.
