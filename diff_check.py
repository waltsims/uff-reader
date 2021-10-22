

with open('/Users/faridyagubbayli/Work/pumba_linux/original.txt', 'r') as f:
    original = set(f.read().split('\n'))
    # original = list(original)
    # original.sort()

with open('/Users/faridyagubbayli/Work/pumba_linux/mine.txt', 'r') as f:
    mine = set(f.read().split('\n'))
    # mine = list(mine)
    # mine.sort()

print('Length original:', len(original))
print('Length mine:', len(mine))
print('How many in original but not in mine:', len(original - mine))
print('How many not in original but in mine:', len(mine - original))

# mine_missing = sorted(list(original - mine))
# for m in mine_missing:
#     print(m)

# mine_excess = sorted(list(mine - original))
# for m in mine_excess:
#     print(m)
print('done')
