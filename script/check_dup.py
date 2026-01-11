import os

template_seq = ''
with open('template_seq.txt') as f:
    for line in f:
        if line[0] == '#' or line.strip() == '':
            continue
        template_seq = line.strip()

end_seq_len = 8
for pos in range(end_seq_len, len(template_seq)+1):
    end_seq = template_seq[pos-end_seq_len:pos]
    count = template_seq.count(end_seq)
    if count != 1:
        print(f'pos: {pos}', flush=True)
        print(f'seq: {end_seq}', flush=True)
        print(f'count: {count}', flush=True)
