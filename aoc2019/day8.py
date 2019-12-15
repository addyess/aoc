from PIL import Image, ImageColor

with open("day8.txt") as fin:
    ins = fin.read()


class LayeredImage:
    def __init__(self, txt, x, y):
        lines = [txt[i:i + x] for i in range(0, len(txt), x)]
        self.layers = [lines[i:i +y] for i in range(0, len(lines), y)]
        self.x, self.y = x, y

    def value_in_layer(self, val, layer_id):
        return sum([
            str(val) == v
            for rows in self.layers[layer_id]
            for row in rows
            for v in row
        ])

    @property
    def verification_code(self):
        min_zero, min_zero_idx = float('inf'), 0
        for i in range(0, len(self.layers)):
            zero_ct = self.value_in_layer(0, i)
            if zero_ct < min_zero:
                min_zero = zero_ct
                min_zero_idx = i
        return (
            self.value_in_layer(1, min_zero_idx) *
            self.value_in_layer(2, min_zero_idx)
        )

    def render(self):
        final = [[2]*self.x for _ in range(self.y)]
        for l in range(len(self.layers)):
            for y in range(self.y):
                for x in range(self.x):
                    cur = final[y][x]
                    pixel = int(self.layers[l][y][x])
                    if cur == 2 and pixel != 2:
                        final[y][x] = pixel

        im = Image.new('1', (self.x, self.y))  # create the Image of size 1 pixel
        for y in range(self.y):
            for x in range(self.x):
                pixel = final[y][x]
                color = 'black' if pixel == 0 else 'white'
                im.putpixel((x, y), ImageColor.getcolor(color, '1'))
        im.show()


d = LayeredImage(ins.strip(), 25, 6)
print(f"Result 1: {d.verification_code}")
d.render()
