import simpy
import tasksim

params = tasksim.Params()
params.parse()

env = simpy.Environment()
grid = tasksim.Grid(env, params)

snapshot = tasksim.Snapshot(env, grid, params)

env.run(until=1000)
