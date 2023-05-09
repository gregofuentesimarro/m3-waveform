import yaml

with open("C:/Users/grego/Box/Cornell Spring 2023/ADVANCED LAB/SKILL/pftl/examples/experiment.yml", 'r') as f:
    e = yaml.load(f, Loader=yaml.FullLoader)

print(e['Experiment'])
for k in e['Experiment']:
    print(k)
    print(e['Experiment'][k])
    print(10*'-')