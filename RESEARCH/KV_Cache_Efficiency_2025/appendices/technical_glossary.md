# Technical Glossary: KV-Cache Efficiency Terms

## Core Concepts

**KV Cache (Key-Value Cache)**
A memory optimization technique in transformer models that stores previously computed key and value vectors from attention mechanisms to avoid recomputation during autoregressive generation. Essential for efficient inference in large language models.

**Attention Mechanism**
The core component of transformer architectures that allows models to focus on relevant parts of the input sequence when generating each new token. Requires key (K), query (Q), and value (V) matrices for computation.

**Autoregressive Generation**
The process by which language models generate text token by token, where each new token depends on all previously generated tokens. Creates the fundamental need for KV caching.

**Context Length**
The maximum number of input tokens a model can process simultaneously. Longer context lengths require proportionally more KV cache memory.

## Quantization Techniques

**Quantization**
The process of reducing the precision of numerical representations (e.g., from 32-bit to 8-bit or lower) to decrease memory usage and computational requirements, typically with some accuracy trade-off.

**Asymmetric Quantization**
A quantization approach that treats different components (keys vs. values) with different strategies. KIVI pioneered per-channel quantization for keys and per-token quantization for values.

**Per-Channel Quantization**
Quantization strategy that groups elements along the channel dimension, optimizing for the statistical properties of key vectors that show higher magnitudes of outliers in specific channels.

**Per-Token Quantization**
Quantization approach that treats each token independently, more suitable for value vectors that don't exhibit the same channel-wise outlier patterns as keys.

**Mixed Precision**
Using different numerical precisions for different parts of the model or computation, such as 4-bit for salient tokens and 2-bit for less important tokens.

## Advanced Optimization Methods

**Salient Token Identification**
Techniques for determining which tokens in a sequence are most important for maintaining model quality, enabling selective compression or higher precision allocation.

**Layer-Discriminative Optimization**
Approaches that recognize different transformer layers have varying importance for KV cache quality, allowing layer-specific optimization strategies.

**Coupled Quantization (CQ)**
An extreme quantization method that couples multiple key/value channels together to exploit their interdependence, enabling 1-bit per channel compression.

**Non-Uniform Quantization**
Adaptive bit allocation where different parts of the KV cache receive different precision levels based on sensitivity analysis or importance scoring.

## Architectural Innovations

**YOCO (You Only Cache Once)**
A decoder-decoder architecture where a self-decoder creates global KV caches that are reused by a cross-decoder, fundamentally changing the caching paradigm.

**MoR (Mixture of Recursions)**
An architectural approach that uses parameter sharing and adaptive recursion depth to achieve better efficiency than standard transformers.

**Ring Attention**
A distributed attention mechanism that partitions context across multiple devices, enabling ultra-long context processing without requiring all context to fit in a single device's memory.

**PagedAttention**
A memory management technique (popularized by vLLM) that applies virtual memory concepts to KV cache management, enabling efficient handling of variable-length sequences.

## Hardware and Performance Terms

**Tensor Cores**
Specialized processing units in modern GPUs (particularly NVIDIA H100/H200) optimized for mixed-precision matrix operations commonly used in AI workloads.

**WGMMA (Warpgroup Matrix Multiply-Accumulate)**
A new instruction set in Hopper GPUs (H100/H200) that enables higher throughput matrix operations compared to previous generations.

**TMA (Tensor Memory Accelerator)**  
A hardware unit in modern GPUs that accelerates data transfer between global memory and shared memory, reducing the overhead of memory operations.

**HBM3e (High Bandwidth Memory 3e)**
The latest generation of high-bandwidth memory used in advanced GPUs like the H200, providing increased capacity and bandwidth for AI workloads.

**FP8 (8-bit Floating Point)**
A reduced precision numerical format that maintains reasonable accuracy while significantly reducing memory and computational requirements.

## Framework and Implementation Terms

**vLLM**
A high-throughput serving framework for large language models that pioneered PagedAttention and achieves 14-24× throughput improvements over baseline implementations.

**TensorRT-LLM**
NVIDIA's optimized inference framework specifically designed for transformer models, with hardware-specific optimizations for tensor cores.

**FlashAttention**
A family of IO-aware attention algorithms that optimize memory access patterns to achieve significant speedups. FlashAttention-3 represents the latest iteration with H100 optimizations.

**Hugging Face Transformers**
A popular open-source library for transformer models that has integrated quantization support and various cache strategies.

## Compression and Efficiency Metrics

**Compression Ratio**
The factor by which memory usage is reduced, calculated as (original size / compressed size). For example, 4× compression means the compressed version uses 25% of the original memory.

**Throughput**
Typically measured in tokens per second, representing the rate at which a model can process or generate text.

**Latency**
The time delay between input and output, critical for interactive applications. Often measured as time-to-first-token (TTFT) and inter-token latency.

**Perplexity**
A measure of how well a language model predicts text, where lower values indicate better performance. Used to evaluate the quality impact of optimization techniques.

**FLOPS (Floating Point Operations Per Second)**
A measure of computational performance, often used to evaluate GPU utilization efficiency.

## Distributed and Scaling Terms

**Context Parallelism**
A technique for distributing long contexts across multiple devices, where each device handles a portion of the total context length.

**Sequence Parallelism**
Methods for parallelizing computation across the sequence dimension, enabling processing of longer sequences than would fit on a single device.

**Multi-Modal Sequence Parallelism (MM-SP)**
An extension of sequence parallelism to handle multi-modal inputs (text, images, etc.) across distributed systems.

**Prefill**
The initial processing phase where the model processes the input prompt to generate initial KV cache states before beginning autoregressive generation.

## Quality and Evaluation Terms

**Needle-in-Haystack**
A benchmark for evaluating long-context performance where models must retrieve specific information from very long input sequences.

**LongBench**
A standardized evaluation suite for long-context language model capabilities.

**Accuracy Retention**
The percentage of original model performance maintained after applying optimization techniques.

**Quality Degradation**
The measurable reduction in model performance (accuracy, perplexity, etc.) resulting from efficiency optimizations.

## Production and Deployment Terms

**Prompt Caching**
A service-level optimization where frequently used context is cached between API calls to reduce costs and latency.

**Batch Size**
The number of requests processed simultaneously, which can be increased with memory-efficient techniques like quantization.

**GPU Utilization**
The percentage of theoretical maximum performance achieved by a GPU, with higher utilization indicating more efficient use of hardware resources.

**Cost per Token**
A business metric measuring the economic cost of processing each token, important for evaluating the business impact of optimizations.

**Production Ready**
Indicates that a technique has been validated for real-world deployment with appropriate testing, monitoring, and reliability measures.

## Research and Academic Terms

**Ablation Study**
A research methodology where different components of a technique are systematically removed or modified to understand their individual contributions.

**Baseline**
The reference implementation against which new techniques are compared, typically representing standard or unoptimized approaches.

**State-of-the-Art (SOTA)**
The best currently available performance or technique in a particular area.

**Reproducibility**
The ability for other researchers to replicate results using the same methods and data, often facilitated by open-source code releases.

**Peer Review**
The academic validation process where research is evaluated by expert reviewers before publication in conferences or journals.

## Emerging and Specialized Terms

**Sparse Representation**
Techniques that exploit the observation that not all elements in KV caches are equally important, allowing aggressive compression of less critical components.

**Dynamic Precision**
Adaptive approaches that change quantization precision based on runtime conditions or importance scoring.

**Hardware-Software Co-Design**
Development approaches where software algorithms and hardware capabilities are optimized together for maximum efficiency.

**Edge AI**
The deployment of AI models on resource-constrained devices like mobile phones or embedded systems, requiring aggressive optimization.

**Inference Engine**
Specialized software frameworks optimized specifically for running trained models in production, as opposed to training frameworks.

---

*This glossary covers technical terms specific to KV-cache efficiency and transformer optimization as used in 2024-2025 research and industry implementations. Terms are defined in the context of current state-of-the-art techniques and applications.*