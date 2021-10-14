n = 25
file_path = "./data/" + "square_image_" + str(n)
with open(file_path, 'w') as f:
    line = n*"0 "+"\n"    
    for i in range(n):
        f.write(line)    
