from functools import reduce
import re


colours = [
    120, 34, 39, 5, 4, 210, 94, 80, 162, 124, 190, 230,
    2, 1, 100, 6, 189, 57, 21, 7, 3, 231
]


def highlight_nan_or_inf(str, pad_to=0):
    str_len = len(str)
    if re.search('(?:nan|inf)', str):
        str = f'\033[38;5;9m\033[1m{str}\033[0m'

    extra_spaces = max(0, pad_to - str_len)
    str += ' ' * extra_spaces
    return str


def print_tensor_row(name, value, sizes, max_name_len, max_shape_len, search, invert_search):
    shape = tuple(value.shape)
    shape_str = '(' + ', '.join(f'\033[38;5;{colours[sizes.index(v) % len(colours)]}m{v}\033[0m' for v in shape) + ')'
    if len(shape) == 1:
        shape_str = shape_str[:-1] + ',)'
    shape_str += ' ' * (max_shape_len - len(str(shape)))

    shape = str(tuple(value.shape))
    base_type = value.__class__.__name__
    dtype = str(value.dtype).split('.')[-1]

    if hasattr(value, 'numel'):
        size = value.numel()
    else:
        size = value.size
    if size > 0:
        val_min = highlight_nan_or_inf(f'{float(value.min()):.02g}', pad_to=10)
        val_max = highlight_nan_or_inf(f'{float(value.max()):.02g}')
    else:
        val_min = ' ' * 10
        val_max = ''

    if hasattr(value, 'device'):
        device = value.device.type
    else:
        device = 'cpu'

    line = f'{name: <{max_name_len}}{shape_str}{base_type: <10}{dtype: <12}{device: <9}{val_min}{val_max}'

    if search is None:
        print(line)
    else:
        search_result = (re.search(f'(?i){search}', line) is not None)
        if invert_search != search_result:
            print(line)


def filter_attribute(name, value):
    valid = not name.startswith('_')
    valid = valid and hasattr(value, 'dtype')
    valid = valid and hasattr(value, 'shape') and value.shape.__class__.__name__ in ['tuple', 'Size']
    return valid


def tensorinfo(search=None, invert_search=False, breakpoint=False):
    import inspect
    frame = inspect.currentframe()
    try:
        locals = frame.f_back.f_locals
        attributes = {}
        buffers = {}
        params = {}
        if 'self' in locals:
            attributes = vars(locals['self'])
            if '_buffers' in attributes:
                buffers = attributes['_buffers']
                buffers = {f'self.{k} (buffer)': v for k, v in buffers.items() if filter_attribute(k, v)}
            if '_parameters' in attributes:
                params = attributes['_parameters']
                params = {f'self.{k}': v for k, v in params.items() if filter_attribute(k, v)}
            attributes = {f'self.{k}': v for k, v in attributes.items() if filter_attribute(k, v)}
        locals = {k: v for k, v in locals.items() if filter_attribute(k, v)}

        locals.update(attributes)
        locals.update(buffers)
        locals.update(params)

        name_strs = ['Name'] + list(locals.keys())
        max_name_len = 4 + max(map(len, name_strs))

        shapes = [tuple(v.shape) for v in locals.values()]
        if len(shapes) == 0:
            sizes = []
        else:
            sizes = list(reduce(set.union, map(set, shapes)))
        shape_strs = ['Shape'] + list(map(str, shapes))
        max_shape_len = 4 + max(map(len, shape_strs))

        title_row = f'\n{"Name": <{max_name_len}}{"Shape": <{max_shape_len}}{"Type": <10}{"dtype": <12}{"Device": <9}{"Min": <10}{"Max": <5}'
        print(title_row)
        print('=' * len(title_row))

        for name, value in locals.items():
            print_tensor_row(name, value, sizes, max_name_len, max_shape_len, search, invert_search)
        print()

        if breakpoint:
            input('Press return to continue execution.')
    finally:
        del frame