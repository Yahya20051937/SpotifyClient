def get_borders(x, y, width, height, windows, color=(0, 0, 0)):
    borders = []
    from components.border import VerticalBorder, HorizontalBorder
    borders.append(
        HorizontalBorder(x=x, y=y, width=width, height=0.01 * height, color=color,
                         windows=windows))

    borders.append(VerticalBorder(x=x + width - 0.005 * width, y=y, width=0.005 * width,
                                  height=height,
                                  color=color, windows=windows))
    borders.append(HorizontalBorder(x=x, y=y + height - 0.01 * height, width=width, height=0.01 * height,
                                    color=color, windows=windows))
    borders.append(VerticalBorder(x=x, y=y, width=0.005 * width, height=height, color=color,
                                  windows=windows))
    return borders


def get_element_from_list_by_index_attribute(list_, index):
    for element in list_:
        if element.index == index:
            return element
    return None


def get_element_index_in_a_list(list_, element):
    i = 0
    for e in list_:
        if e == element:
            return i
        i += 1


def get_element_by_id_from_list(list_, id_):
    for element in list_:
        if element.id == id_:
            return element
    return None


def round_(n):
    integer_part = int(n)
    decimal_part = n - integer_part
    if decimal_part >= 0.5:
        return integer_part + 1
    else:
        return integer_part


def get_element_from_list_by_percentage(list_, percentage):
    index_as_float = percentage * (len(list_) - 1)
    index_as_integer = round_(index_as_float)
    return list_[index_as_integer]
