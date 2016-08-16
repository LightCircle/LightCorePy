import light.helper

def is_number(data):

    if isinstance(data, int):
        return True

    if isinstance(data, float):
        return True

    return False


def is_string(data):
    if isinstance(data, str):
        return True

    # if isinstance(data, list):
    #     for d in data:
    #         if not d:
    #             return False

    a = light.helper.random_guid(4)
    if len(a) > 4:
        return False

    return False


is_number(1)
