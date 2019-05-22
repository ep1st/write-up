# **scramble**

#### tag : rev, angr

-----------------------------------------------

#### Description

-----------------------------------------------

#### Solution

```python
import angr

proj = angr.Project("./scramble", load_options={"auto_load_libs":False})
pg = proj.factory.simgr()
pg.explore(find=0x400000+0x737, avoid=[0x400000+0x6FB])

print pg.found[0].state.posix.dumps(0)
```
