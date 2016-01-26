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
            out_str = ''
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
                ).strip().strip('">')
            elif line.startswith('#CHROM'):
                header = line.strip().strip('#').split('\t')
            elif not line.startswith('##'):
                orig_line = line
                line = line.replace('|', '\t').strip().split('\t')
                is_vep_info_col = [z.startswith(info_key) for z in line]
                if True in is_vep_info_col:
                    info_index = is_vep_info_col.index(True)
                    if not wrote_header:
                        out_str = '%s\t%s\t%s\n' % (
                            '\t'.join(header[:info_index]),
                            info_header,
                            '\t'.join(header[info_index + 1:])
                        )
                        wrote_header = True

                    out_str += '\t'.join(line[:info_index]) + '\t'
                    for i, value in enumerate(line[info_index:]):
                        if value.startswith(','):
                            out_str += '\n%s\t' % '\t'.join(line[:info_index])
                        out_str += '%s\t' % value.strip(',').strip(info_key)
                else:
                    if not wrote_header:
                        out_str = '%s\n' % '\t'.join(header)
                        wrote_header = True
                    out_str += orig_line.strip()
            # output
            if out_str:
                if args.output_file:
                    out_f.write(out_str + '\n')
                else:
                    print out_str

        if args.output_file:
            out_f.close()


def parse_args():
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

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


if __name__ == '__main__':
    main()
