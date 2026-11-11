# Provenance of the programmed weights

## Origin

The fixed candidate in `programmed_state()` was authored by ChatGPT (GPT-6 Astra,
as identified in the active session) on 11 November 2026 during the student's project
planning conversation. It is an assistant-authored starter candidate. The student did
not independently write these weights. The assistant also prepared the experimental
implementation, notebook, protocol, and writing outline.

There was no separate fresh-context or blinded LLM invocation. The writer had the
conversation context, the assignment, research summaries, class labels, and general
knowledge about garment shapes. No Fashion-MNIST images, training examples, validation
measurements, or test measurements were inspected to design this candidate. The design
was fixed before any such evaluation. Synthetic software checks are separate from
the student's dataset experiment.

## Design specification used in this session

This is a record of the specification, not a claim that the following paragraph was
the sole verbatim prompt in a new model session:

> Specify a deterministic numeric initialization for a 49 → 8 → 4 → 2 MLP with ReLU
> after both hidden layers. Inputs are upright Fashion-MNIST images pooled from 28×28
> to 7×7 by nonoverlapping 4×4 averages, scaled to [0, 1], then flattened row first.
> Output zero denotes T-shirt/top and output one denotes Trouser. All weights and biases
> must be fixed from the task description without data, evaluation, optimization, or a
> pretrained checkpoint. Preserve the architecture so the same network can subsequently
> be trained using Adam. Keep the entire numerical construction inspectable.

## What the construction does

The first layer computes mean brightness in eight specified image regions. This is an
explicit prior about upright garment silhouettes. The second layer forms signed
contrasts between broad upper regions, lower leg regions, and the lower center. Each
contrast has an opposite so ReLU can retain information of both signs. The final layer
turns these features into two scores. These are unverified hypotheses about useful
features, not findings about the dataset.

The code fills fixed tensors from region coordinates and numeric constants. It does
not ask the LLM to write an optimizer or use gradients during weight construction.
`wsp_candidate.json` archives the resulting 446 float32 parameters. Each execution
also exports and hashes its actual candidate in `wsp_weights.json`. Preserve those
artifacts together with the code version. A new chat response is not guaranteed to
regenerate the same weights, even if given the same specification.

## Boundaries of the claim

This tests one LLM-authored geometric initialization. It does not test an autonomous
system that reads and repairs arbitrary learned weights. Its model architecture and
task were selected in the same planning conversation as the candidate. This limits
independence and generalization. The experiment supplies a proof-of-concept classroom
comparison, not a benchmark of general LLM weight-programming ability.

If another model is used to generate a new candidate, save its actual prompt, raw
response, exact model identifier, generation date and settings, every attempt, any
manual corrections, and its final tensors. Make structural repairs without examining
accuracy. Record performance-informed changes as a new experiment.
