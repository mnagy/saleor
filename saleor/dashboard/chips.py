from django.utils.translation import gettext

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

PATTERN = '%s: %s'


def build_query(request, param, value=None):
    request_get = request.GET.copy()
    if value:
        value_list = request_get.getlist(param)
        value_list.pop(value_list.index(value))
        request_get[param] = value_list
    else:
        del request_get[param]
    return '?' + urlencode(request_get, True)


def handle_default(request, field, chips_list):
    chips = chips_list[:]
    chips.append({'content': PATTERN % (field.label, field.value()),
                  'link': build_query(request, field.name,
                                      field.value())})
    return chips


def handle_multiplechoice(request, field, chips_list, context):
    chips = chips_list[:]
    for partial_value in [f for f in field.value() if f]:
        value = context[partial_value]
        chips.append({'content': PATTERN % (field.label, value),
                      'link': build_query(request, field.name,
                                          partial_value)})
    return chips


def handle_nullboolean(request, field, chips_list):
    chips = chips_list[:]
    values = [
        gettext('No'),
        gettext('Yes')
    ]
    value = values[1] if field.value() else values[0]
    chips.append({'content': PATTERN % (field.label, value),
                  'link': build_query(request, field.name,
                                      1 if field.value() else 0)})
    return chips


def handle_range(request, field, chips_list):
    chips = chips_list[:]
    values = [f if f else None for f in field.value()]
    text = [gettext('From'), gettext('To')]
    for i, value in enumerate(values):
        if value:
            chips.append(
                {'content': PATTERN % (field.label, text[i] + ' ' + value),
                 'link': build_query(request, '%s_%i' % (field.name, i),
                                     field.value()[i])})
    return chips


def handle_choice(request, field, chips_list):
    chips = chips_list[:]
    value = list(filter(lambda x: x[0] == field.value(),
                        field.field._choices))[0][1]
    chips.append({'content': PATTERN % (field.label, value),
                  'link': build_query(request, field.name, field.value())})
    return chips
