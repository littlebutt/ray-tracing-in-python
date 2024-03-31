if __name__ == '__main__':
    image_width, image_height = 256, 256
    print(f"P3\n{image_width} {image_height}\n255")
    for j in range(image_height):
        for i in range(image_width):
            r = int(float(i) / (image_width - 1) * 255.999)
            g = int(float(j) / (image_height - 1) * 255.999)
            b = int(0 * 255.999)

            print(f"{r} {g} {b}")