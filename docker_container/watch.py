from common import *


send_notification("Watching...", "Watching...")


def run_command():
    command = "docker logs --tail 0 --follow " + container_name
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
    if "Hash" in l or "compiled successfully" in l:
        send_notification("SUCCESS!!!", "Specify 7 Updated!", "Glass")
    if "ERROR" in l:
        send_notification(
            "ERROR!!!",
            "Error occurred while updating Specify 7!",
            "Hero",
        )
    if "Killed" in l:
        send_notification(
            "Webpack Died(((, again", "Wepback container quit", "Sosumi"
        )
    print(l, end="", flush=True)
