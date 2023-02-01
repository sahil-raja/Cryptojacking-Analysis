import os

import psutil
from psutil import Process
from awaits.awaitable import awaitable
import asyncio
from pywinauto import Application
from win10toast import ToastNotifier

# os.system("start cmd")

@awaitable
def _worker(p: Process):
    try:
        return {
            'name': p.name(),
            'pid': p.pid,
            'cpu_usage': ((p.cpu_percent(interval=0.5)/psutil.cpu_count())/100) * psutil.cpu_freq().max,
            'memory': p.memory_full_info().uss
        }
    except Exception as e:
        # print('ERROR:', e)
        return None


async def get_proc_info(p: Process):
    return await _worker(p)


async def scan_processes():
    tasks = []
    results = []

    for p in psutil.process_iter(attrs=None, ad_value=None):
        tasks.append(asyncio.create_task(get_proc_info(p)))

    for task in tasks:
        results.append(await task)
    return [i for i in results if i]


while True:
    procs = asyncio.run(scan_processes())
    browser_procs = list()
    for i in range(len(procs)):
        if procs[i]['name'] == 'chrome.exe' or procs[i]['name'] == 'firefox.exe' or procs[i]['name'] == 'opera.exe' or procs[i]['name'] == 'edge.exe':
            print(procs[i]['pid'], ' ', procs[i]['cpu_usage'])
            browser_procs.append(procs[i])

    if browser_procs:
        max_cpu_proc = max(browser_procs, key=lambda i: i['cpu_usage'])
        max_mem_proc = max(browser_procs, key=lambda p: p['memory'])
    else:
        continue

    print('\nHighest CPU load Process is:')
    process_id = max_cpu_proc['pid']
    cpu_usage = max_cpu_proc['cpu_usage']
    process_name = max_cpu_proc['name']
    print(max_cpu_proc['name'] + f' [{max_cpu_proc["pid"]}]', max_cpu_proc['cpu_usage'])
    alerted_list = list()
    if cpu_usage > 500:
        url = ''
        try:
            app = Application(backend='uia')
            app.connect(title_re=".*Chrome.*")
            element_name = "Address and search bar"
            dlg = app.top_window()
            url = dlg.child_window(title=element_name, control_type="Edit").get_value()
            print('\nCurrent URL in browser: ', url)
        except Exception as e:
            print(e)

        # if process_id not in alerted_list:
        n = ToastNotifier()
        n.show_toast("Cryptoblocker", f"Alert: {process_name[:-4]} tab with url '{url}' and process ID '{process_id}' may be running a cryptojacker ", duration=10)
        alerted_list.append(process_id)

    print('\nHighest RAM Usage Process is:')
    print(max_mem_proc['name'] + f' [{max_mem_proc["pid"]}]', max_mem_proc['memory'])
