import os

path = "/tmp/all_env_vars.txt"
envs = sorted(os.environ.items())

for k, v in envs:
    print(f"{k}={v}")

with open(path, "w") as f:
    for k, v in envs:
        f.write(f"{k}={v}\n")

print(len(envs))
