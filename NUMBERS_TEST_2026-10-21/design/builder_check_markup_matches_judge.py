import sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, "/home/user/utensil-theories-transfer-protocol/experiments")
J = "/tmp/claude-0/-home-user-utensil-theories-transfer-protocol/ace947b8-053f-52e2-a284-890744a0e973/scratchpad/judge_numbers/"
import numpy as np
src = open(J + "sim_rules.py").read().split("CFG = {")[0].replace('HERE = Path(__file__).parent', f'HERE = Path("{J}")')
ns = {}
exec(src, ns)
import numbers_test as nt
verses, values = ns["verses"], ns["values"]
clear, _ = nt.clear_choices(verses, values)
assert (clear == ns["clear"]).all()
nbar, drain = nt.drain_constants(verses, values)
print("NBAR", nbar, "DRAIN", drain, "judge D", ns["D"], drain == ns["D"])
for c, CH in nt.CONFIGS.items():
    marked, rec = nt.mark_charge(verses, values, CH, drain, clear)
    jf, jR, jpin = ns["mark"](CH)
    print(c, "forms identical:", bool((rec["form"] == jf).all()), " R identical:", bool(np.array_equal(rec["R_spell"], jR)),
          " cap% mine", round(100*rec["at_cap_after"].mean(), 3), "judge", round(100*jpin, 3))
