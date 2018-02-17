
def encode(ByteArray):
    DNAString=''
    for byte in ByteArray:
        nucleobaseGroup=''
        #int.from_bytes(b'y\xcc\xa6\xbb', byteorder='big')

        nucleobaseGroup=nucleobaseGroup+bits_to_nucleobase((int.from_bytes(byte,byteorder='big') & 192)>>6)
        nucleobaseGroup = nucleobaseGroup +bits_to_nucleobase((int.from_bytes(byte,byteorder='big') & 48)>>4)
        nucleobaseGroup = nucleobaseGroup +bits_to_nucleobase((int.from_bytes(byte,byteorder='big') & 12)>>2)
        nucleobaseGroup = nucleobaseGroup +bits_to_nucleobase(int.from_bytes(byte,byteorder='big') & 3)
        DNAString=DNAString+nucleobaseGroup

    return DNAString
def byte_to_binString(byte):
    return{0:'00',
           1:'01',
           2:'10',
           3:'11'}[byte]
def bits_to_nucleobase(int):
    return {0:'A',
           1:'C',
           2:'G',
           3:'T'}[int]
def nucleobase_to_int(nucleobase):
    return{'A':0,
           'C':1,
           'G':2,
           'T':3}[nucleobase]

def decode(DNAString):
    DNAArray = list(DNAString)
    byteArray=[]
    for i in range(0,len(DNAArray),4):
        nucleobaseGroup=DNAArray[i:i+4]
    #bitsArray=[]
        byteValue=0
        for j in range(3,-1,-1):

            byteValue +=(4**j)*nucleobase_to_int(nucleobaseGroup[3-j])
        byteArray.append(byteValue.to_bytes(1,byteorder='big'))
    return byteArray
encode(decode('ATGCATGC'))