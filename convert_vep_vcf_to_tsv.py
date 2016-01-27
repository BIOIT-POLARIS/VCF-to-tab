#!/usr/bin/python
"""Converts VEP VCF output to tab-delimited file."""

import sys
import argparse

def main():
    args = parse_args()
    with open(args.input_file) as in_f:
        if args.output_file:
            out_f = open(args.output_file, 'w')
        info_header = ''
        info_key = 'CSQ'
        wrote_header = False
        for line in in_f:
            out_str = None
            # find VEP INFO in header
            if (
                (line.startswith('##INFO') or line.startswith('"##INFO')) and
                'Ensembl VEP' in line
            ):
                info_key = '%s=' % line[
                    line.index('ID=') + 3:line.index(',')
                ]
                info_header = line.split('Format: ')[1].replace(
                    '|', '\t'
                ).strip().strip('">').split('\t')
            elif line.startswith('#CHROM'):
                header = line.strip().strip('#').split('\t')
            elif not line.startswith('##'):
                out_str = process_variant(
                    line.strip(), info_key, header, info_header, wrote_header
                )
                wrote_header = True
            # output
            if out_str:
                if args.output_file:
                    out_f.write('%s\n' % out_str)
                else:
                    print out_str

        if args.output_file:
            out_f.close()


def process_variant(line, info_key, header, info_header, wrote_header):
    """Process a single variant. (Single line in input file.)
    Return output string.
    """
    out_str = ''
    orig_line = line
    line = line.replace('|', '\t').strip().split('\t')
    is_vep_info_col = [info_key in z for z in line]
    if True in is_vep_info_col:
        info_index = is_vep_info_col.index(True)
        info_end_index = info_index + len(line) - len(orig_line.split('\t'))
        # get header output str
        if not wrote_header:
            out_header = (
                header[:info_index] + ['INFO'] + info_header +
                header[info_index + 1:]
            )
            out_str = '%s\n' % '\t'.join(out_header)
        # get variant output str
        info_per_transcript = get_info_per_transcript(
            line[info_index:info_end_index + 1], info_key
        )
        info = line[info_index]
        if info_key in info:
            info_out = info[:info.index(info_key)].strip(';')
            end_info = info[info.index(info_key):]
            if ';' in end_info:
                info_out += end_info[end_info.index(';'):]
        for tx_info in info_per_transcript:
            out_str += '%s\t%s\t%s\t%s\n' % (
                '\t'.join(line[:info_index]),
                info_out,
                '\t'.join(tx_info),
                '\t'.join(line[info_end_index + 1:])
            )
    else:
        if not wrote_header:
            out_str = '%s\n' % '\t'.join(header)
            wrote_header = True
        out_str += orig_line.strip()

    return out_str.strip()


def get_info_per_transcript(info_list, info_key):
    """Convert list of values in info field to list of list of values
    in info field for each transcript. Return the latter.
    """
    info_per_transcript = []
    curr_transcript = []
    for i, value in enumerate(info_list):
        if info_key in value:
            curr_transcript.append(
                value[value.index(info_key) + len(info_key):]
            )
        elif ',' in value:
            curr_transcript.append(value[:value.index(',')])
            info_per_transcript.append(curr_transcript)
            curr_transcript = []
            if len(value) > 1:
                curr_transcript = [value[value.index(',') + 1:]]
        else:
            curr_transcript.append(value)
    return info_per_transcript


def parse_args():
    """Parse command-line arguments. Return parsed arguments."""
    parser = argparse.ArgumentParser(
        description='%s: Converts VEP VCF output to tab-delimited file.' % (
            sys.argv[0]
        )
    )
    parser.add_argument(
        'input_file',
        help='Name of VEP VCF input file to be converted to '
             'tab-delimited format.'
    )
    parser.add_argument(
        '-o', '--output_file',
        help='Name of file to which to output tab-delimited version '
             'of input file. (Default: standard output.)'
    )
    parser.add_argument(
        '--separate_transcripts', action='store_true',
        help='Put each transcript in a separate row. '
             '(Default: Combine all transcripts into a single row.)'
    )
    parser.add_argument(
        '--separate_samples', action='store_true',
        help='Put each sample in a separate row. '
             '(Default: Put each sample in a different column, '
            'in a single row.)'
    )
    parser.add_argument(
        '--separate_genotype', action='store_true',
        help='Separate genotype data into columns. '
             '(Default: leave colon-separated genotype data as is.) '
    )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


if __name__ == '__main__':
    main()
