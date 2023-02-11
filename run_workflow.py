import subprocess
import json
import pathlib
import collections


def submit_run():
    command = ['gh', 'workflow', 'run']
    subprocess.run(' '.join(command), shell=True)


def get_workflow_runs(workflow_name: str):
    command = [
        'gh', 'run', 'list',
        f'--workflow={workflow_name}',
        '--json', 'databaseId',
    ]
    output = subprocess.check_output(' '.join(command), shell=True, encoding='utf-8')
    return json.loads(output)


def get_run_logs(run_id: int):
    command = [
        'gh', 'run', 'view',
        str(run_id),
        '--log',
    ]
    output = subprocess.check_output(' '.join(command), shell=True, encoding='utf-8')
    return output


# submit_run()


content = collections.defaultdict(list)
for run in get_workflow_runs('channels.yaml'):
    log = get_run_logs(run['databaseId'])
    for line in log.split('\n'):
        tokens = line.split('\t', 2)
        if len(tokens) != 3:
            continue
        content[(str(run['databaseId']), tokens[0], tokens[1])].append(tokens[2])


directory = pathlib.Path('logs')
for (database_id, job_name, step), logs in content.items():
    (directory / database_id / job_name).mkdir(exist_ok=True, parents=True)
    with (directory / database_id / job_name / f"{step.replace('/', '-')}.txt").open('w') as f:
        f.write('\n'.join(logs))
