import angr
import claripy

proj = angr.Project("./chal_re_med.so", load_options={"auto_load_libs":False})
argv1 = claripy.BVS("argv1", 100*8)
initial_state = proj.factory.entry_state(args=["./chal_re_med.so", argv1])

pg = proj.factory.simgr(initial_state)
pg.explore(find=0xad5+0x400000, avoid=0xaa4+0x400000)
print pg.found[0].state.se.any_str(argv1)
