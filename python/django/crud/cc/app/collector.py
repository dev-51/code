def createJSON(**kwargs):
    ob = []
    keys = []
    data = {}

    keys = [str(key) for key in kwargs]

    if "arguments" in keys:
        ob = kwargs["arguments"]
        keys = [str(key) for key in ob]
    elif "request" in keys:
        request = kwargs["request"]

        if request.method == 'POST':
            keys = [str(key) for key in request.POST.iterkeys()]
            ob = request.POST
        elif request.method == 'GET':
            keys = [str(key) for key in request.GET.iterkeys()]
            ob = request.GET

    for key in keys:
        data[key] = ob[key]

    return data