import requests
from django.shortcuts import render

def alert(request):
    import os
    os.system("notify-send 'Django Works' 'Check your results.' -u normal -t 7500 -i checkbox-checked-symbolic")
    item = {'ok':'its ok'}
    print(item)
    return render(request, 'core/home.html', item)
