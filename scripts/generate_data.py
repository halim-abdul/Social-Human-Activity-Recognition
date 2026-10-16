from pathlib import Path
from socialhar.synthetic import generate

target = Path("data/synthetic/activities.csv")
target.parent.mkdir(parents=True, exist_ok=True)
generate().to_csv(target, index=False)
print(target)
