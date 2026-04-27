import numpy as np
import matplotlib.pyplot as plt

# --- Parameters ---
SIZE = 512
TIMESTEPS = 128
MAX_VAL = 2
SEED = 42


def gather_replication_candidates(state: np.ndarray) -> list[set]:
    size = len(state)
    candidates = [set() for _ in range(size)]

    for pos, current_val in enumerate(state):
        if current_val == 0:
            continue

        offsets = {current_val}
        offset_queue = [current_val]

        while offset_queue:
            check_offset = offset_queue.pop()
            value_at_offset = state[(pos + check_offset) % size]
            if value_at_offset not in offsets:
                offsets.add(value_at_offset)
                offset_queue.append(value_at_offset)
            else:
                break

        for offset in offsets:
            new_pos = (pos + offset) % size
            if offset != 0:
                candidates[new_pos].add(int(current_val))

    return candidates


def norm_zero(current_state: np.ndarray, collisions: list[set]) -> np.ndarray:
    return np.array([
        list(vals)[0] if len(vals) == 1 else 0
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