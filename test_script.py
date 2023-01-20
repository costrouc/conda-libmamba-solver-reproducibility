import re
import subprocess

cmd = 'conda create --experimental-solver libmamba -n testtesttest -c conda-forge --override-channels python=3.8 bokeh hvplot --dry-run'
pattern = r'\/(.+)::bokeh-(\d+.\d+.\d+)'

for _ in range(10):
    result = subprocess.run(cmd.split(' '), capture_output=True, text=True)
    print(re.findall(pattern, result.stdout))
