# Feature candidates for AI-vs-human text classification

A working list of features the classifier can use. Grouped by what's cheap to compute and what needs heavier NLP. Each one is a single column in the feature matrix.

## Length and shape
- **Average sentence length** (tokens). Humans show more variance; AI tends to converge on a mid-length norm.
- **Sentence-length variance / burstiness.** Tian's GPTZero uses this as a primary signal: human text is "bursty" (mix of short and long sentences), AI text is more uniform.
- **Average word length** (characters).
- **Sentence count, token count, type count** (use these to derive normalized rates).

## Lexical diversity
- **Type-token ratio (TTR).** Cheap; biased by document length, so use a normalized version like:
  - **Moving-average TTR (MATTR)** with a window of ~500 tokens.
  - **MTLD** (McCarthy & Jarvis 2010) which is length-robust.
- **Yule's K** and **Honoré's R**. Classical lexical-richness measures.
- **Hapax legomena ratio** (words appearing once / total types). AI tends to repeat itself; lower hapax count.

## POS distribution
- Counts (rates per 1000 tokens) for: NOUN, VERB, ADJ, ADV, DET, PRON, ADP (preposition), CCONJ, SCONJ.
- AI text trends toward: more nouns and adjectives, denser nominal style, fewer first-person pronouns.
- Use spaCy or NLTK for POS tagging.

## Function-word style (Stamatatos-style)
- Frequencies of the 100 most common function words (the, of, and, to, a, in, that, is, it, ...). These are the gold standard in authorship attribution and work well here.

## Punctuation and formatting
- Comma rate, period rate, semicolon rate.
- **Em-dash rate.** Anecdotally a strong AI tell, especially for ChatGPT.
- Question-mark rate, exclamation rate.
- Quote count (single + double).

## AI-tell vocabulary
Curated list of words ChatGPT/Claude overuse in academic/formal writing. Compute rate per 1000 tokens for each, plus an aggregate "AI-tell score":
- delve, tapestry, intricate, multifaceted, navigate, realm, embark, foster, leverage, robust, holistic, comprehensive, meticulous, paramount, pivotal, underscore, illuminate, juxtapose, overarching, nuanced
- Transitions: moreover, furthermore, however, nevertheless, in conclusion, in summary, in essence, ultimately
- Hedges: it's worth noting that, it's important to note, it's essential to

## Syntactic complexity (heavier)
- **Average parse-tree depth** per sentence (spaCy dependency parser).
- **Average dependency distance.** Liang et al. and others find AI text has shorter avg dep distance.
- **Clauses per sentence.** Count subordinate clauses with the parser.
- **Passive voice rate.**

## Repetition
- N-gram repetition (bigram, trigram). Fraction of n-grams that repeat.
- Lemma repetition rate.

## Optional: model-based signals (if there's time)
- **Perplexity under a small LM** (e.g. GPT-2 small via HF). DetectGPT-style.
- **Log-probability curvature.** Same paper. Heavier, but a strong signal.

## Sources / starting reading list
- Guo, Zhang, Wang et al. (2023). *How close is ChatGPT to human experts? Comparing corpora, evaluation, and detection.* arXiv:2301.07597. The HC3 paper. They report exactly the kind of statistical features we want and benchmark a logistic regression on them.
- Tian, E. (2023). *GPTZero.* Burstiness + perplexity as the two main features. https://gptzero.me
- Mitchell et al. (2023). *DetectGPT: Zero-shot machine-generated text detection using probability curvature.* arXiv:2301.11305.
- Stamatatos (2009). *A survey of modern authorship attribution methods.* Function-word features.
- Crothers, Japkowicz, Viktor (2022). *Machine-generated text: A comprehensive survey of threat models and detection methods.* IEEE Access.
- McCarthy & Jarvis (2010). *MTLD, vocd-D, and HD-D.* For lexical diversity.

## Practical starting set for the MVP
If we want to fit a logistic regression today, start with this small bundle (all cheap, all interpretable):
1. Avg sentence length
2. Sentence-length variance
3. Avg word length
4. MATTR (window 500)
5. Top-50 function-word frequencies
6. POS rates (NOUN, VERB, ADJ, ADV)
7. Em-dash rate
8. Comma rate
9. AI-tell aggregate score
10. Trigram repetition rate

That's ~70 features total once function words are flattened. Runs fast on a laptop and gives interpretable coefficients.
