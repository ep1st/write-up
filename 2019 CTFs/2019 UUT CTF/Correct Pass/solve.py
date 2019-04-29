import angr

proj = angr.Project("./pass", load_options={"auto_load_libs":False})
pg = proj.factory.simgr()
pg.explore(find=0x8048A99, avoid=[0x08048A5F,0x08048A23,0x080489E7,0x080489AB,0x0804896F,0x08048AC4])

print pg.found[0].state.posix.dumps(0)
