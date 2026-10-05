# GLACIER Molecular Embeddings

GLACIER encodes molecules into 512 features using a student-teacher arrangement in which a lightweight student learns to reproduce representations from larger multimodal teachers. Nguyen and colleagues designed it so that the expressive power of heavy foundation models becomes available at a fraction of the inference cost, with the student trained to match teacher embeddings rather than to predict properties. The embedding is task-independent, and its dimensions carry no interpretable chemical meaning individually.

This model was incorporated on 2026-08-03.Last packaged on 2026-08-03.

## Information
### Identifiers
- **Ersilia Identifier:** `eos5g6m`
- **Slug:** `glacier-embeddings`

### Domain
- **Task:** `Representation`
- **Subtask:** `Featurization`
- **Biomedical Area:** `Any`
- **Target Organism:** `Any`
- **Tags:** `Descriptor`, `Embedding`, `Chemical graph model`

### Input
- **Input:** `Compound`
- **Input Dimension:** `1`

### Output
- **Output Dimension:** `512`
- **Output Consistency:** `Fixed`
- **Interpretation:** 512 features encoding molecular structure from a student-teacher foundation model.

Below are the **Output Columns** of the model:
| Name | Type | Direction | Description |
|------|------|-----------|-------------|
| feat_000 | float |  | GLACIER multimodal fused embedding dimension 0 |
| feat_001 | float |  | GLACIER multimodal fused embedding dimension 1 |
| feat_002 | float |  | GLACIER multimodal fused embedding dimension 2 |
| feat_003 | float |  | GLACIER multimodal fused embedding dimension 3 |
| feat_004 | float |  | GLACIER multimodal fused embedding dimension 4 |
| feat_005 | float |  | GLACIER multimodal fused embedding dimension 5 |
| feat_006 | float |  | GLACIER multimodal fused embedding dimension 6 |
| feat_007 | float |  | GLACIER multimodal fused embedding dimension 7 |
| feat_008 | float |  | GLACIER multimodal fused embedding dimension 8 |
| feat_009 | float |  | GLACIER multimodal fused embedding dimension 9 |

_10 of 512 columns are shown_
### Source and Deployment
- **Source:** `Local`
- **Source Type:** `External`
- **DockerHub**: [https://hub.docker.com/r/ersiliaos/eos5g6m](https://hub.docker.com/r/ersiliaos/eos5g6m)
- **Docker Architecture:** `AMD64`, `ARM64`
- **S3 Storage**: [https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos5g6m.zip](https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos5g6m.zip)

### Resource Consumption
- **Model Size (Mb):** `26`
- **Environment Size (Mb):** `1862`
- **Image Size (Mb):** `1863.77`

**Computational Performance (seconds):**
- 10 inputs: `39.09`
- 100 inputs: `29.49`
- 10000 inputs: `384.8`

### References
- **Source Code**: [https://github.com/eemokey/glacier](https://github.com/eemokey/glacier)
- **Publication**: [https://doi.org/10.1145/3770855.3819032](https://doi.org/10.1145/3770855.3819032)
- **Publication Type:** `Peer reviewed`
- **Publication Year:** `2026`
- **Ersilia Contributor:** [TiagoJanela](https://github.com/TiagoJanela)

### License
This package is licensed under a [GPL-3.0](https://github.com/ersilia-os/ersilia/blob/master/LICENSE) license. The model contained within this package is licensed under a [MIT](LICENSE) license.

**Notice**: Ersilia grants access to models _as is_, directly from the original authors, please refer to the original code repository and/or publication if you use the model in your research.


## Use
To use this model locally, you need to have the [Ersilia CLI](https://github.com/ersilia-os/ersilia) installed.
The model can be **fetched** using the following command:
```bash
# fetch model from the Ersilia Model Hub
ersilia fetch eos5g6m
```
Then, you can **serve**, **run** and **close** the model as follows:
```bash
# serve the model
ersilia serve eos5g6m
# generate an example file
ersilia example -n 3 -f my_input.csv
# run the model
ersilia run -i my_input.csv -o my_output.csv
# close the model
ersilia close
```

## About Ersilia
The [Ersilia Open Source Initiative](https://ersilia.io) is a tech non-profit organization fueling sustainable research in the Global South.
Please [cite](https://github.com/ersilia-os/ersilia/blob/master/CITATION.cff) the Ersilia Model Hub if you've found this model to be useful. Always [let us know](https://github.com/ersilia-os/ersilia/issues) if you experience any issues while trying to run it.
If you want to contribute to our mission, consider [donating](https://www.ersilia.io/donate) to Ersilia!
