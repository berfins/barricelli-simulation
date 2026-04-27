import numpy as np
import matplotlib.pyplot as plt

# --- Parameters ---
SIZE = 512
TIMESTEPS = 128
MAX_VAL = 2
SEED = 42


def gather_replication_candidates(state: np.ndarray, max_chain: int = 20) -> list[list]:
    size = len(state)
    candidates = [[] for _ in range(size)]
    nonzero_positions = np.nonzero(state)[0]

    for pos in nonzero_positions:
        current_val = int(state[pos])
        seen = set()
        seen.add(current_val)
        offsets = [current_val]
        queue = [current_val]
        hops = 0

        while queue and hops < max_chain:
            check_offset = queue.pop()
            value_at_offset = int(state[(pos + check_offset) % size])
            if value_at_offset != 0 and value_at_offset not in seen:
                seen.add(value_at_offset)
                offsets.append(value_at_offset)
                queue.append(value_at_offset)
            hops += 1

        for offset in offsets:
            new_pos = (pos + offset) % size
            candidates[new_pos].append(current_val)

    return candidates


def norm_zero(current_state: np.ndarray, collisions: list[list]) -> np.ndarray:
    return np.array([
        vals[0] if len(vals) == 1 else 0
        for vals in collisions
    ])


def run_simulation() -> np.ndarray:
    rng = np.random.default_rng(seed=SEED)
    grid = np.zeros((TIMESTEPS, SIZE), dtype=int)

    # Initialise with sparse random integers
    grid[0, :] = rng.integers(-MAX_VAL, MAX_VAL + 1, size=SIZE)
    grid[0, rng.choice(np.arange(SIZE), size=int(SIZE * 4 / 5), replace=False)] = 0

    for step in range(1, TIMESTEPS):
        candidates = gather_replication_candidates(grid[step - 1, :])
        grid[step, :] = norm_zero(grid[step - 1, :], candidates)

    return grid


def plot_grid(grid: np.ndarray, filename: str = "out/basic.png") -> None:
    fig, ax = plt.subplots(1, 1)
    ax.imshow(grid, aspect="auto", interpolation="none")
    plt.axis("off")
    plt.savefig(filename, bbox_inches="tight", transparent=True, dpi=200)
    plt.close()
    print(f"Saved to {filename}")


if __name__ == "__main__":
    grid = run_simulation()
    plot_grid(grid)