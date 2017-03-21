filep = "line10_label_train15000/data/"

f_in = open(filep+"train_encode.ids176.txt", "wb")
f_out = open(filep+"train_decode.ids176.txt", "wb")

with open(filep+"chat.ids176.in", "rb") as f:
    line_in = f.readline()
    while(line_in):
        f_in.write(line_in)
        line_out = f.readline()
        f_out.write(line_out)    
        line_in = f.readline()

