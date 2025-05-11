# Research Agent User Examples

## Example 1: Summarize Document

**User Input:**
"Research Agent, please summarize the key findings in `local_docs/papers/attention_is_all_you_need.pdf` regarding the Transformer architecture."

**Agent Output (Ideal):**
```markdown
Okay, I have reviewed `local_docs/papers/attention_is_all_you_need.pdf`. Here are the key findings regarding the Transformer architecture:

*   **Primary Innovation:** The paper introduces the Transformer, a novel network architecture based entirely on attention mechanisms, dispensing with recurrence and convolutions.
*   **Attention Mechanism:** It utilizes a specific type of attention called "Scaled Dot-Product Attention" and a "Multi-Head Attention" mechanism, allowing the model to jointly attend to information from different representation subspaces at different positions.
*   **Encoder-Decoder Structure:** The Transformer follows an encoder-decoder structure. Both are composed of a stack of identical layers.
    *   **Encoder Layers:** Each encoder layer has two sub-layers: a multi-head self-attention mechanism and a simple, position-wise fully connected feed-forward network.
    *   **Decoder Layers:** Each decoder layer, in addition to the two sub-layers in the encoder layer, inserts a third sub-layer, which performs multi-head attention over the output of the encoder stack.
*   **Positional Encoding:** Since the model contains no recurrence or convolution, positional encodings are added to the input embeddings at the bottoms of the encoder and decoder stacks to inject information about the relative or absolute position of the tokens in the sequence.
*   **Performance:** The Transformer demonstrated superior performance on machine translation tasks (WMT 2014 English-to-German and English-to-French) with significantly less training time compared to existing models.

**Source:** `local_docs/papers/attention_is_all_you_need.pdf` (Sections 3-5 primarily)
```

## Example 2: Find SOTA Method

**User Input:**
"Research Agent, what are some SOTA methods for object detection in low-light conditions, according to my cached research papers?"

**Agent Output (Ideal):**
```markdown
Searching for SOTA methods for object detection in low-light conditions based on the cached research papers...

Here are a few relevant methods found:

1.  **Method: Zero-DCE (Zero-Reference Deep Curve Estimation)**
    *   **Description:** This method formulates low-light image enhancement as a task of image-specific curve estimation with a deep network. It takes a low-light image as input and produces high-order curves as its output, which are then used to adjust the input image dynamically. It's designed to work without paired or unpaired training data.
    *   **Source:** `cached_papers/Zero-DCE_Low_Light_Enhancement.pdf` (Section 3)

2.  **Method: EnlightenGAN**
    *   **Description:** An unsupervised Generative Adversarial Network (GAN) for low-light image enhancement. It learns from unpaired low-light and normal-light images and uses a global-local discriminator structure and a self-regularized perceptual loss.
    *   **Source:** `cached_papers/EnlightenGAN_Unsupervised_Low_Light.pdf` (Abstract, Section 3)

3.  **Method: Retinex-Net**
    *   **Description:** A deep learning framework inspired by Retinex theory, which decomposes an image into reflectance and illumination. It includes a Decom-Net for decomposition and an Enhance-Net for illumination adjustment.
    *   **Source:** `cached_papers/RetinexNet_Low_Light_Enhancement.pdf` (Introduction, Section 2)

Please note: "SOTA" can change rapidly. These reflect the information within the current cached documents.
```
