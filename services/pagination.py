def paginate(
    items,
    page,
    size=5
):

    start = page * size

    end = start + size


    return items[start:end]



def pages_count(
    items,
    size=5
):

    return (
        len(items) + size - 1
    ) // size