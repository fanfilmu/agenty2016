import simpy
import tasksim

params = tasksim.Params()
params.parse()

env = simpy.Environment()
grid = tasksim.Grid(env, params)

snapshot = tasksim.Snapshot(env, grid, params)

env.run(until=params.steps)

print "generating images..."
snapshot.generate_images()
print "generating statistics..."
snapshot.generate_statistics()
