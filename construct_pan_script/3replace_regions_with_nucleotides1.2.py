import sys
import argparse
import subprocess
# bedtools didn't need the parameter '-name'. So I delete it at 2021.1.11
def parseArguments(args):
    """Set up the command-line parser and call it on the command-line arguments to the program.

    arguments:
    args -- command-line arguments to the program"""
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, 
        description='This script takes a bed file of SVs with genomic coordinates in the 7th column \
        and replaces these coordinates with the actual nucleotide sequences at these coordinates.')
    parser.add_argument('bed', type=argparse.FileType('r'), help='bed file with genomic coordinates in 7th column')
    parser.add_argument('reference', type=str, help='Reference genome (used for deletion coordinates')
    parser.add_argument('query', type=str, help='Query genome (used for insertion coordinates)')
    parser.add_argument('name', type=str, help='Some unique name for temporary files (e.g. sample name)')
    return parser.parse_args()

def main(args):
    options = parseArguments(args)

    #This files will be filled with reference coordinates (for deletions)
    del_coord_file = open("temp/del_coords_{0}.bed".format(options.name), "w")
    #This files will be filled with query coordinates (for insertions)
    ins_coord_file = open("temp/ins_coords_{0}.bed".format(options.name), "w")

    for line in options.bed:
        fields = line.strip().split()
        if fields[5] == "Deletion":
            del_location = fields[6]
            chr = del_location.split(":")[0]
            start = int(del_location.split(":")[1].split("-")[0])
            end = int(del_location.split(":")[1].split("-")[1])
            #We need to fetch from start-1 because the VCF format requires an anchoring base for deletions
            del_coord_file.write("{0}\t{1}\t{2}\t{0}:{1}-{2}\n".format(chr, start-1, end))
        elif fields[5] == "Insertion":
            ref_chr = fields[0]
            ref_pos = int(fields[1])
            ins_location = fields[6]
            chr = ins_location.split(":")[0]
            start = int(ins_location.split(":")[1].split("-")[0])
            end = int(ins_location.split(":")[1].split("-")[1])
            ins_coord_file.write("{0}\t{1}\t{2}\t{0}:{1}-{2}\n".format(chr, start, end))
            #We need to fetch the one ref base before the insertion because the VCF format requires an anchoring base for insertions
            del_coord_file.write("{0}\t{1}\t{2}\t{0}:{1}-{2}\n".format(ref_chr, ref_pos-1, ref_pos))
    
    del_coord_file.close()
    ins_coord_file.close()

    #These files will be filled with the actual nucleotide sequences
    del_seq_file_name = "temp/del_seqs_{0}.fa".format(options.name)
    ins_seq_file_name = "temp/ins_seqs_{0}.fa".format(options.name)

    #bedtools getfasta fetches the sequences for the coordinates in the bed files
    subprocess.run(["bedtools", "getfasta", "-fi", options.reference, "-bed", del_coord_file.name,  "-fo", del_seq_file_name])
    subprocess.run(["bedtools", "getfasta", "-fi", options.query, "-bed", ins_coord_file.name,  "-fo", ins_seq_file_name])

    del_seq_file = open(del_seq_file_name, "r")
    ins_seq_file = open(ins_seq_file_name, "r")

    #Read the bed file another time from the beginning
    options.bed.seek(0)
    for line in options.bed:
        fields = line.strip().split()
        if fields[5] == "Deletion":
            del_location = fields[6]
            chr = del_location.split(":")[0]
            start = int(del_location.split(":")[1].split("-")[0])
            end = int(del_location.split(":")[1].split("-")[1])
            header_line = del_seq_file.readline().rstrip()
            #We check whether the genomic coordinate in this line is indeed the next sequence in the sequence file
            if header_line == ">{0}:{1}-{2}".format(chr, start-1, end):
                sequence_line = del_seq_file.readline().rstrip()
                print("\t".join(fields[:6] + [sequence_line] + fields[7:]))
            else:
                print("Mismatch between sequence file produced by bedtools and original bed file")
                print("{0} != >{1}:{2}-{3}".format(header_line, chr, start-1, end))
                return
        elif fields[5] == "Insertion":
            ref_chr = fields[0]
            ref_pos = int(fields[1])
            ins_location = fields[6]
            chr = ins_location.split(":")[0]
            start = int(ins_location.split(":")[1].split("-")[0])
            end = int(ins_location.split(":")[1].split("-")[1])
            header_line = ins_seq_file.readline().rstrip()
            #We check whether the genomic coordinate in this line is indeed the next sequence in the sequence file
            if header_line == ">{0}:{1}-{2}".format(chr, start, end):
                sequence_line = ins_seq_file.readline().rstrip()
                header_line2 = del_seq_file.readline().rstrip()
                #We need to check for the single ref base as well
                if header_line2 == ">{0}:{1}-{2}".format(ref_chr, ref_pos-1, ref_pos):
                    ref_base = del_seq_file.readline().rstrip()
                    sequence_line = ref_base + sequence_line
                else:
                    print("Mismatch between sequence file produced by bedtools and original bed file")
                    print("{0} != >{1}:{2}-{3}".format(header_line2, ref_chr, ref_pos-1, ref_pos))
                    return
                print("\t".join(fields[:6] + [sequence_line] + fields[7:]))
            else:
                print("Mismatch between sequence file produced by bedtools and original bed file")
                print("{0} != >{1}:{2}-{3}".format(header_line, chr, start, end))
                return
        else:
            print(line.strip())
    del_seq_file.close()
    ins_seq_file.close()


if __name__ == "__main__" :
    sys.exit(main(sys.argv))
