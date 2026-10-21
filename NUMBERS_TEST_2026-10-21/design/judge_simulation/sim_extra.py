exec(open("sim_rules.py").read().split("CFG = {")[0])
a = mark((32, 16, 34, 47, 17))[0]
for name, ch in {"sorted cycle 16,17,32,34,47 from 17": (32, 34, 47, 16, 17),
                 "reversed": (47, 34, 16, 32, 17), "charge16": (16,), "charge32": (32,), "charge34": (34,)}.items():
    b = mark(ch)[0]
    print(f"{name:38s} differs from seq on {100*np.mean(a!=b):.1f}%")
c17 = mark((17,))[0]
for n in (16, 32, 34):
    print(n, "vs charge17", round(100*np.mean(mark((n,))[0]!=c17),1), " vs charge47", round(100*np.mean(mark((n,))[0]!=mark((47,))[0]),1), " vs const29", round(100*np.mean(mark((n,))[0]!=mark((29.2,))[0]),1))
# neutral steady state check: charge 17, verse of NBAR zero-valued words
R = 0.0
for _ in range(30):
    W = R + 17; R = W * (1 - D) ** NBAR
print("steady state W, R:", round(W, 3), round(R, 3))
