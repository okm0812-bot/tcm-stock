import os
p1 = r'C:\Program Files\QClaw\resources\openclaw\config\skills'
p2 = r'C:\Users\user\.qclaw\workspace\skills'
for p in [p1, p2]:
    print(p)
    if os.path.exists(p):
        print(os.listdir(p))
    else:
        print('NOT_EXIST')
