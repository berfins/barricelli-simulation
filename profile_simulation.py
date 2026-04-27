import cProfile
import pstats
import io
from barricelli import run_simulation

profiler = cProfile.Profile()
profiler.enable()

run_simulation()

profiler.disable()

stream = io.StringIO()
stats = pstats.Stats(profiler, stream=stream)
stats.sort_stats("cumulative")
stats.print_stats(15)
print(stream.getvalue())