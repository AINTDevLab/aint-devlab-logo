from PIL import Image, ImageDraw, ImageFont, ImageFilter


def draw_linear_gradient(size, start_color, end_color, horizontal=False):
    width, height = size
    base = Image.new("RGBA", (width, height), start_color)
    top = Image.new("RGBA", (width, height), end_color)
    mask = Image.new("L", (width, height))
    mask_data = []
    for i in range(width if horizontal else height):
        v = int(255 * (i / (width - 1 if horizontal else height - 1)))
        mask_data.extend([v] * (height if horizontal else width))
    mask.putdata(mask_data)
    if horizontal:
        mask = mask.rotate(90, expand=True)
    base.paste(top, (0, 0), mask)
    return base


def main():
    # Ventana central
    win_w, win_h = 620, 330

    # Canvas transparente 1:1 ajustado al ancho
    margin_x, margin_y = 20, 70
    content_w = win_w + margin_x * 2
    content_h = win_h + margin_y * 2
    canvas_size = max(content_w, content_h)
    img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    win_x = (canvas_size - win_w) // 2
    win_y = (canvas_size - win_h) // 2

    # Sombra
    shadow = Image.new("RGBA", (win_w + 30, win_h + 30), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle(
        (15, 15, win_w + 15, win_h + 15),
        radius=22,
        fill=(0, 0, 0, 120),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    img.paste(shadow, (win_x - 15, win_y - 10), shadow)

    # Fondo ventana en negro
    win = Image.new("RGBA", (win_w, win_h), (0, 0, 0, 0))
    win.paste((0, 0, 0, 255), (0, 0, win_w, win_h))
    wdraw = ImageDraw.Draw(win)
    wdraw.rounded_rectangle(
        (0, 0, win_w, win_h),
        radius=20,
        outline=(80, 82, 86, 255),
        width=2,
    )

    # Máscara para esquinas transparentes
    mask = Image.new("L", (win_w, win_h), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle((0, 0, win_w, win_h), radius=20, fill=255)
    win.putalpha(mask)

    # Barra superior
    bar_h = 42
    wdraw.rounded_rectangle((0, 0, win_w, bar_h), radius=20, fill=(50, 52, 55, 255))
    wdraw.rectangle((0, bar_h - 10, win_w, bar_h), fill=(50, 52, 55, 255))

    # Botones tipo macOS
    cx, cy = 26, 22
    colors = [(255, 95, 86, 255), (255, 189, 46, 255), (40, 201, 64, 255)]
    for i, c in enumerate(colors):
        wdraw.ellipse(
            (cx + i * 24 - 6, cy - 6, cx + i * 24 + 6, cy + 6),
            fill=c,
            outline=(30, 30, 30, 255),
        )

    # Fuente monoespaciada
    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", 46)
    except:
        font = ImageFont.load_default()

    # Colores de sintaxis
    c_text = (235, 235, 235, 255)  # texto base
    c_kw = (156, 220, 254, 255)    # etiqueta
    c_str = (106, 214, 132, 255)   # string
    c_attr = (156, 220, 254, 255)  # atributo
    c_op = (156, 220, 254, 255)    # operador
    c_class = (206, 145, 120, 255) # class

    # Texto con colores
    tx, ty = 44, 78
    line_gap = 74

    # Línea 1: <h1>AINT</h1>
    parts1 = [
        ("<", c_text),
        ("h1", c_kw),
        (">", c_text),
        ("AINT", c_class),
        ("</", c_text),
        ("h1", c_kw),
        (">", c_text),
    ]

    # Línea 2: <div>DevLab</div>
    parts2 = [
        ("<", c_text),
        ("div", c_kw),
        (">", c_text),
        ("DevLab", c_str),
        ("</", c_text),
        ("div", c_kw),
        (">", c_text),
    ]

    def draw_parts(x, y, parts):
        cur_x = x
        for text, color in parts:
            wdraw.text((cur_x, y), text, fill=color, font=font)
            cur_x += wdraw.textlength(text, font=font)

    draw_parts(tx, ty, parts1)
    draw_parts(tx, ty + line_gap, parts2)

    # Pegar ventana en el canvas
    img.paste(win, (win_x, win_y), win)

    # Guardar con transparencia
    img.save("aint-devlab-logo.png")


if __name__ == "__main__":
    main()
