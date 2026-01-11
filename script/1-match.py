import os
import sys
from dataclasses import dataclass
from common import *
print(f'************************************************************', flush=True)
print(f'*                        1-match.py                        *', flush=True)
print(f'************************************************************', flush=True)
print('filter invalid reads and match position', flush=True)

pos = int(sys.argv[1])

partial_cap_seq = 'AGGAAGAAGAGTCACAG'

len_template_seq = len(template_seq)
digits = len(str(len_template_seq))

@dataclass
class Stats():
    line_count: int = 0
    seq_num: int = 0
    valid_seq_num: int = 0
    R1_min_len: int = 999999999
    R1_max_len: int = 0
    R2_min_len: int = 999999999
    R2_max_len: int = 0

def gen_pos_identifiers():
    pos_dict = {}
    for pos in range(8, len(template_seq)+1):
        pos_seq = None
        if pos == 12 or pos == 44:
            pos_seq = partial_cap_seq + reverse_and_complement(template_seq[pos-9:pos])
        else:
            pos_seq = partial_cap_seq + reverse_and_complement(template_seq[pos-8:pos])
        assert(len(pos_seq) == len(partial_cap_seq)+8 or len(pos_seq) == len(partial_cap_seq)+9)
        pos_dict[pos] = pos_seq
    assert(len(pos_dict) == len(template_seq)+1-8)
    return pos_dict

for name, R1R2_dir, R1, R2 in R1R2s:
    print(f'------------------------------------------------------------', flush=True)
    print(f'process R1 -> {R1} R2 -> {R2}', flush=True)

    in_R1 = f'{result_dir}/{R1}'
    in_R2 = f'{result_dir}/{R2}'

    # check num of lines equal
    with open(in_R1) as R1_f, open(in_R2) as R2_f:
        R1_num_lines = sum(1 for _ in R1_f)
        R2_num_lines = sum(1 for _ in R2_f)
        print(f'R1_num_lines: {R1_num_lines} in {in_R1}', flush=True)
        print(f'R2_num_lines: {R2_num_lines} in {in_R2}', flush=True)
        assert(R1_num_lines == R2_num_lines)
        assert((R1_num_lines % 4) == 0)

    pos_dict = gen_pos_identifiers()
    print(f'len(pos_dict): {len(pos_dict)}', flush=True)
    print(f'------------------------------------------------------------', flush=True)
    pos_seq = pos_dict[pos]
    forward_pos_seq = reverse_and_complement(pos_seq)
    print('pos:', pos, flush=True)
    print('pos_seq:', pos_seq, flush=True)
    print('forward pos_seq: ', forward_pos_seq, flush=True)

    save_R1_dir = f'{pos_dir}/{pos:0{digits}d}/{pos:0{digits}d}-R1'
    save_R2_dir = f'{pos_dir}/{pos:0{digits}d}/{pos:0{digits}d}-R2'

    os.makedirs(save_R1_dir)
    os.makedirs(save_R2_dir)

    out_R1 = f'{save_R1_dir}/{R1}'
    out_R2 = f'{save_R2_dir}/{R2}'

    stats = Stats()

    out_R1_f = open(out_R1, 'w')
    out_R2_f = open(out_R2, 'w')

    # filter out seq and check seq id matches
    tmp_entry_lines = []
    with open(in_R1) as R1_f, open(in_R2) as R2_f:
        for R1_line, R2_line in zip(R1_f, R2_f):
            stats.line_count += 1
            R1_l, R2_l = R1_line.strip(), R2_line.strip()
            tmp_entry_lines.append((R1_l, R2_l))
            if stats.line_count % 4 == 0:
                stats.seq_num += 1

                assert(len(tmp_entry_lines) == 4)
                R1_seq, R2_seq = tmp_entry_lines[1][0], tmp_entry_lines[1][1]
                R1_seq_id, R2_seq_id = tmp_entry_lines[0][0].split()[0][1:], tmp_entry_lines[0][1].split()[0][1:]
                R1_qv, R2_qv = tmp_entry_lines[3][0], tmp_entry_lines[3][1]
                R1_seq_len, R2_seq_len = len(R1_seq), len(R2_seq)
                assert(R1_seq_id == R2_seq_id)
                assert(R1_seq_len == len(R1_qv))
                assert(R2_seq_len == len(R2_qv))

                if R2_seq.find(pos_seq) != -1:
                    stats.valid_seq_num += 1

                    if R1_seq_len < stats.R1_min_len:
                        stats.R1_min_len = R1_seq_len
                    if R1_seq_len > stats.R1_max_len:
                        stats.R1_max_len = R1_seq_len
                    if R2_seq_len < stats.R2_min_len:
                        stats.R2_min_len = R2_seq_len
                    if R2_seq_len > stats.R2_max_len:
                        stats.R2_max_len = R2_seq_len

                    out_R1_f.write(f'{tmp_entry_lines[0][0]}\n')
                    out_R1_f.write(f'{R1_seq}\n')
                    out_R1_f.write(f'{tmp_entry_lines[2][0]}\n')
                    out_R1_f.write(f'{R1_qv}\n')
                    out_R2_f.write(f'{tmp_entry_lines[0][1]}\n')
                    out_R2_f.write(f'{R2_seq}\n')
                    out_R2_f.write(f'{tmp_entry_lines[2][1]}\n')
                    out_R2_f.write(f'{R2_qv}\n')

                tmp_entry_lines = []

    print(f'valid seq_num: {stats.valid_seq_num} '
        f'({stats.valid_seq_num/stats.seq_num*100.0:.2f})%  '
        f'total seq_num: {stats.seq_num}', flush=True)
    print(f'R1 min_len: {stats.R1_min_len}  max_len: {stats.R1_max_len}', flush=True)
    print(f'R2 min_len: {stats.R2_min_len}  max_len: {stats.R2_max_len}', flush=True)

    out_R1_f.close()
    out_R2_f.close()

