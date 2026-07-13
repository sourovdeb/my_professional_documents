# Presentations

Slide decks, version-controlled. Each deck should have a `.pptx` file and,
where it was generated programmatically, the build script that produced it.

## Minds, Words, Particles, Machines

`minds_words_particles_machines.pptx` — a 10-slide deck (with full speaker
notes on every slide) touring rarely-taught ideas across five fields:

1. Title
2. Psychology — productivity, ultradian rhythm, implementation intentions
3. Psychology — the ego depletion replication failure
4. Linguistics — phonology and why English spelling looks broken
5. Linguistics — linguistic relativity (Guugu Yimithirr, Kuuk Thaayorre, Russian blues)
6. Evolutionary biology — cognitive biases as old adaptations (smoke-detector principle)
7. AI — how LLMs work (tokenization, attention, next-token prediction, scaling laws)
8. AI — hallucination, grokking, and in-context learning
9. Quantum physics — superposition, entanglement, tunneling, the quantum Zeno effect
10. Synthesis — prediction under uncertainty as the thread linking all four fields

Built with [python-pptx](https://python-pptx.readthedocs.io/) (see
`requirements.txt`). To regenerate after editing `build_deck.py`:

```bash
pip install -r requirements.txt
python3 presentations/build_deck.py
```
