from common import *


send_notification("Rebuilding...", "Rebuilding...")


def run_command():
    command = "(cd /Users/mambo/site/python/specify7 && docker-compose up --build -d)"
    print(command)
    p = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=False,
        shell=True,
    )

    nice_stdout = open(os.dup(p.stdout.fileno()), newline="")
    for line in nice_stdout:
        yield line, p.poll()

    yield "", p.wait()


for l, rc in run_command():
    # if 'Running' in l:
    #        send_notification('SUCCESS!!!','Specify 7 Updated!','Glass')
    # if 'ERROR' in l:
    # 	send_notification('ERROR!!!','Error occurred while updating Specify 7!','Hero')
    print(l, end="", flush=True)

run_process(
    "docker exec specify7_specify7_1 mkdir -p '/volumes/static-files/frontend-static/'"
)
run_process(
    "docker cp /Users/mambo/site/python/specify7/specifyweb/frontend/static/img specify7_specify7_1:/volumes/static-files/frontend-static/img"
)
run_process(
    "docker exec specify7_specify7_1 bash -c './ve/bin/python manage.py migrate auth && ./ve/bin/python manage.py migrate contenttypes && ./ve/bin/python manage.py migrate sessions && ./ve/bin/python manage.py migrate workbench && ./ve/bin/python manage.py migrate notifications'"
)
send_notification("Rebuilt...", "Rebuilt...", "Glass")
