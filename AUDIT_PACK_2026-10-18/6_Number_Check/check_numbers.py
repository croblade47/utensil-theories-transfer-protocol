import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "4_Raw_Results"))  # read the copied results files
import json
from math import comb
def binom_greater(k,n):
    return sum(comb(n,i) for i in range(k,n+1))/2**n if n else 1.0
print('--- exp 8/10 judging (v2_judge), per seed')
for f in ['results_confirm.json','results_methods.json']:
    d=json.load(open(f))
    meth={}
    for k,v in d.items():
        m,s=k.split('/'); meth.setdefault(m,{})[s]=v
    for m,ss in meth.items():
        j=[sum(ss[s]['v2_judge']) for s in sorted(ss)]
        sh=[sum(ss[s]['v2_shift']) for s in sorted(ss)]
        print(f,m,'judge',j,'avg',round(sum(j)/len(j),1),'shift',sh)
d=json.load(open('results_methods.json'))
def pair(a,b,key='v2_judge'):
    A=[sum(d[f'{a}/seed{i}'][key][p] for i in range(3)) for p in range(100)]
    B=[sum(d[f'{b}/seed{i}'][key][p] for i in range(3)) for p in range(100)]
    bet=sum(x>y for x,y in zip(A,B)); wor=sum(x<y for x,y in zip(A,B))
    return bet,wor,round(binom_greater(bet,bet+wor),4)
for a,b in [('shifting','label'),('shifting','baseline'),('shifting','scrambled'),('label','baseline'),('shifting','carry3')]:
    print(a,'vs',b, pair(a,b))
print('--- exp 11 long story')
d=json.load(open('results_long_story.json'))
meth={}
for k,v in d.items():
    m,s,ver=k.split('/'); meth.setdefault((m,ver),{})[s]=v['correct']
for (m,ver),ss in sorted(meth.items()):
    sc=[sum(ss[s]) for s in sorted(ss)]
    ties=[sum(x==0.5 for x in ss[s]) for s in sorted(ss)]
    dec=[(sum(x==1 for x in ss[s]),sum(x==0 for x in ss[s])) for s in sorted(ss)]
    print(m,ver,sc,'ties',ties,'decided R-W',dec)
for ver in ['A','B']:
  for a in ['shifting','carry3']:
    A=meth[(a,ver)];B=meth[('label',ver)]
    sa=[sum(A[s][p] for s in A) for p in range(100)]; sb=[sum(B[s][p] for s in B) for p in range(100)]
    bet=sum(x>y for x,y in zip(sa,sb)); wor=sum(x<y for x,y in zip(sa,sb))
    print(ver,a,'vs label',bet,wor,round(binom_greater(bet,bet+wor),4))
