from django import template

register = template.Library()


TABLE_HEAD = '''
             <table class="table table-dark table-hover">
                <tbody>
             '''

TABLE_TAIL = '''
             </tbody>
                </table>
             '''

TABLE_CONTENT = '''
             <tr>
                <td>{name}</td>
                <td>{value}</td>
             </tr>
                '''

PRODUCT_SPEC = {
    'notebook': {
        'Diagonal': 'diagonal',
        'Display type': 'display_type',
        'Processor freq': 'processor_freq',
        'RAM': 'ram',
        'Video': 'video',
        'Work withouth charge': 'time_without_charge'
    },
    'smartphone': {
        'Diagonal': 'diagonal',
        'Display type': 'display_type',
        'Resolution': 'resolution',
        'Accum': 'accum_volume',
        'RAM': 'ram',
        'Slot for sd': 'sd',
        'Max SD volume': 'sd_max_volume',
        'Camera (MP)': 'main_cam',
        'Frontal camera (MP)': 'front_cam'
    }
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    return TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL