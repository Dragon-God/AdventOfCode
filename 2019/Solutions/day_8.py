import os

os.chdir(r"2019\Solutions")

with open(r"..\Inputs\day_8.txt") as file:
    text = file.read().rstrip()


def make_layers(txt, height, width):
    size = height * width
    layers = [txt[i:i+size] for i in range(0, len(txt), size)]
    return layers


def checksum(layers):
    min_layer = min(layers, key=lambda x: x.count("0"))
    return min_layer.count("1") * min_layer.count("2")


layers = make_layers(text, 6, 25)


def make_image(layers):
    img = []
    for tpl in zip(*layers):
        pixel = "2"
        for px in tpl:
            if px != "2":
                pixel = px
                break
        img.append(pixel)
    return "".join(img)


def visualise(img, height, width):
    image = "\n".join(img[i:i+width] for i in range(0, len(img), width))
    image = image.replace("1", ".")
    return image.replace("0", " ")


def part_one():
    return checksum(layers)


def part_two():
    return visualise(make_image(layers), 6, 25)


print(part_one())  # 2562
print(part_two())  # ZFLBY
