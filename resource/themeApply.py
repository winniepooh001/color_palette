from PySide6.QtGui import QPalette
from colour import Color

import json

color_state = [QPalette.Active, QPalette.Disabled, QPalette.Inactive]
color_role = [QPalette.Button,
              QPalette.Light, QPalette.Midlight, QPalette.Mid, QPalette.Dark,
              QPalette.WindowText, QPalette.Text, QPalette.BrightText, QPalette.ButtonText, QPalette.HighlightedText, QPalette.ToolTipText,
              QPalette.PlaceholderText,
              QPalette.Base, QPalette.AlternateBase,
              QPalette.Window, QPalette.ToolTipBase,
              QPalette.Shadow, QPalette.Highlight,
              QPalette.Link, QPalette.LinkVisited]

def color_convert(html, return_type='str'):
    h = html.lstrip('#')
    rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    if return_type == 'str':
        return 'QColor(' +",".join(rgb) +"')"
    else:
        return rgb

def rgb_to_hex(r,g,b,a=None):
    return '#%02x%02x%02x' % (r,g,b)

# does not run in debug mode
def getPaletteInfo(fn=None):
    palette = QPalette()
    #build a dict with all the colors
    result = {}

    for role in color_role:
        for group in color_state:
            group_text = str(group).split(".")[1]
            role_text = str(role).split(".")[1]
            try:
                result[f'{group_text}_{role_text}'] = palette.color(group, role).name()
            except:
                print("failed ", group, role)
    if fn is not None:
        with open("default.json", mode='w+') as fh:
            json.dump(result, fh, indent=4)
    print("finished")
    return result


def chosen_palette(colorScheme):
            
    newPalette = QPalette()
    if 'Active_Window' not in colorScheme or 'Active_Text' not in colorScheme:
        raise KeyError("Require to have at minimum active window and active text color")

    for role in color_role:
        for group in color_state:
            group_text = str(group).split(".")[1]
            role_text = str(role).split(".")[1]
            dic_item = f'{group_text}_{str(role_text)}'
            if dic_item in colorScheme.keys():
                newPalette.setColor(group, role, colorScheme[dic_item])
            elif f'Active_{role_text}' in color_role.keys():
                newPalette.setColor(group, role, colorScheme[f'Active_{role_text}'])
            elif 'Text' in role_text:
                if f'{group_text}_Text' in colorScheme.keys():
                    newPalette.setColor(group, role, colorScheme[f'{group_text}_Text'])
                else:
                    newPalette.setColor(group, role, colorScheme['Active_Text'])
            else:
                newPalette.setColor(group, role, colorScheme['Active_Window'])


    return newPalette

def color_scheme(name, base_color, item_returned, prefix='Active_'):
    # https://thingsgrow.me/2020/01/02/navigating-through-000000-and-ffffff-color-theory-in-python/
    base = Color(base_color)
    num_ = len(item_returned)
    if name == 'complement':
        base.hue = base.hue + 0.5 if base.hue < 0.5 else base.hue - 0.5
        base.luminance = base.luminance + 0.5 if base.luminance < 0.5 else base.luminance - 0.5
        return {f'{prefix}{v}': base.hex for v in item_returned}
    elif name == 'analog':
        # default 60
        color_1 = color_2 = base
        color_1.hue = (color_1.hue + 1/6.0) % 1
        color_2.hue = (color_2.hue - 1/6.0) % 1
        return [color_1.hex, color_2.hex]
    elif name == 'triadic':
        color_1 = color_2 = base
        color_1.hue = (color_1.hue + 1/3.0) % 1
        color_2.hue = (color_2.hue + 2/3.0) % 1
        return [color_1.hex, color_2.hex]
    elif name == 'shades':
        newColor = list(base.range_to(Color('black'), num_ + 1))
        return {f'{prefix}{v}': newColor[i].hex for i, v in enumerate(item_returned)}
    elif name == 'tints':
        newColor = list(base.range_to(Color('white'), num_ + 2))
        return {f'{prefix}{v}': newColor[i].hex for i, v in enumerate(item_returned)}
    elif name == 'monochromatic':
        newColor = {}
        for i in range(len(item_returned)):
            base.hue = max(base.saturation - 0.1, 0)
            newColor[f'{prefix}{item_returned[i]}'] = base.hex
        return newColor
    else:
        return {f'{prefix}{v}': base_color for v in item_returned}

def create_palette(window, text, alternate):
    cur_theme = {}
    groups = {'same':{
        window: ['Window', 'Base', 'ToolTipBase', 'Button'],
        alternate: ['HighlightedText'],
        text: ['WindowText', 'Text', 'ButtonText', 'ToolTipText']
    },
        'monochromatic': {text: ['PlaceholderText']},
        'triadic': {text: ['BrightText', 'Link']},
        'tints': {window: ['Light', 'AlternateBase','Midlight']},
        'shades': {window: ['Shadow', 'Mid', 'LinkVisited', 'Dark']},
        'complement': {
            alternate: ['Highlight']
        }}

    # from group
    for scheme_name, item_dic in groups.items():
        for baseColor, lists in item_dic.items():
            colors = color_scheme(scheme_name, baseColor, lists, 'Active_')
            if type(colors) == dict:
                cur_theme.update(colors)
            else:
                for i, v in enumerate(lists):
                    cur_theme[f'Active_{v}'] = colors[(i + 1) % len(colors)]

    # from active to inactive
    # inactive equals to disabled
    # reduce saturation
    new_dic = {}
    for c, v in cur_theme.items():
        new_color_2 = Color(v)
        new_color_1 = Color(v)
        new_color_1.saturation = max(0, new_color_1.saturation - 0.15)
        new_color_2.saturation = max(0, new_color_2.saturation - 0.5)
        new_dic[c.replace("Active","Inactive")] = new_color_1.hex
        new_dic[c.replace("Active","Disabled")] = new_color_2.hex

    cur_theme.update(new_dic)

    return cur_theme