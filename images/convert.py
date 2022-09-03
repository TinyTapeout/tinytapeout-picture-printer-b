from PIL import Image

# convert image to run length encoding and export as verilog 'assign' statements

wire_size = 8
img_list = ["img1_ehlab.png", "img2_lambda.png", "img3_int.png", "img4_amogus.png"]
show_decoded_img = False

def img_to_pixel_string(im):
    pixels = im.load()

    #convert image to list of boolean values
    pixel_string = []
    for lineN in range(height):
        for pixelN in range(width):
            pixel_string += [pixels[pixelN,lineN][0]<128]

    return pixel_string

def rle(pixel_string):
    counter_list = []
    counter = 1
    for last_pixel, pixel in zip(pixel_string, pixel_string[1:]):
        if(not (pixel == last_pixel)):
            counter_list += [counter]
            counter = 1
        else:
            counter += 1
    counter_list += [counter]

    return counter_list

def decode_rle(rle_list, img_width, start_char):
    width_counter = 0
    characters = "01"
    current_char = start_char

    out_str = ""
    
    for count in rle_list:
        for _ in range(count):
            out_str += characters[current_char]
            width_counter += 1
            if(width_counter == img_width):
                width_counter = 0
                out_str += "\n"

        current_char = not current_char
    return out_str


verilog_parameters = ""
verilog_assign_statements = ""
for file_name in img_list:
    im = Image.open(file_name)
    img_name = file_name.split(".")[0] + "RLE"

    (width, height) = im.size

    pixel_string = img_to_pixel_string(im)

    start_pixel = int(pixel_string[0])
    counter_list = rle(pixel_string)

    if show_decoded_img:
        print("decoded image:")
        print(decode_rle(counter_list, width, start_pixel))

    if(max(counter_list) > 2**wire_size-1):
        print(f'value {max(counter_list)} too big for {wire_size} bit wire')

    #convert to verilog
    verilog_parameters += f'''//File {file_name} , size {im.size}
parameter LEN_{img_name} = {len(counter_list)};
parameter WIDTH_{img_name} = {width};
parameter START_{img_name} = {start_pixel};
wire [{wire_size-1}:0] {img_name} [0:LEN_{img_name}-1];\n\n'''

    for i,c in enumerate(counter_list):
        verilog_assign_statements += f"assign {img_name}[{i}] = {c}; "
    verilog_assign_statements += "\n\n"

with open("output.v", "w") as f:
    f.write(verilog_parameters + verilog_assign_statements)



