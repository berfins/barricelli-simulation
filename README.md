# Barricelli Numerical Evolution

A Python simulation of Nils Aall Barricelli's 1953 numerical evolution experiments —
one of the earliest artificial life simulations ever run on a computer.

## Background

In 1953, mathematician Nils Barricelli ran experiments on one of the first computers
at Princeton, treating integers in a 1D array as "living organisms" that could
replicate, collide, and evolve. This project reimplements that simulation.

## How it works

The world is a circular array of 512 cells. Each nonzero integer is an organism.
At every time step, each organism tries to **replicate itself** by jumping to a new
position at a distance equal to its own value:

organism 3 at position 5 → tries to copy itself to position 8
organism -2 at position 10 → tries to copy itself to position 8


If two organisms target the same cell, they **collide** and both die (the cell
becomes 0). This simple rule produces surprisingly complex patterns over time.

The output is a 2D image where each row is one time step — a visual history of
the entire simulation.

## How to run

This project uses [uv](https://github.com/astral-sh/uv) for environment management.

```bash
uv sync
uv run barricelli.py
```

Output is saved to `out/basic.png`.

## Files

- `barricelli.py` — the simulation
- `profile_simulation.py` — profiling script used during optimization

## Optimization (dev branch)

Profiling with `cProfile` showed that `gather_replication_candidates` accounted for
**85% of total runtime**:

ncalls tottime cumtime filename
127 0.073 0.096 gather_replication_candidates ← bottleneck
154084 0.011 0.011 {method 'add' of 'set' objects}
106505 0.007 0.007 {method 'pop' of 'list' objects}


The bottleneck had two causes:
1. **512 Python `set` objects allocated every timestep** (one per cell)
2. **Iterating over all 512 cells** including empty ones on every step

The fix:
- Replaced per-cell `set` allocations with plain `list`s
- Used `np.nonzero()` to skip empty cells at C level instead of Python `enumerate`
- Added a `max_chain` bound to prevent unbounded chain-following loops

Result:

ncalls tottime cumtime filename
127 0.038 0.052 gather_replication_candidates ← after fix


- Total runtime: **0.113s → 0.065s (~42% faster)**
- Function calls: **381,756 → 252,447 (~34% fewer)**

## References

- Barricelli, N.A. (1954). *Esempi numerici di processi di evoluzione*
- Ashford, J.E. et al. (2026). *Evolving Symbiosis, from Barricelli's Legacy to
  Collective Intelligence*. [arXiv:2603.08463](https://arxiv.org/abs/2603.08463)