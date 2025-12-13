# ai-agent-lab

A hands-on lab for building and experimenting with AI agents — from scratch and using frameworks such as `LangChain`, `LangGraph`, `CrewAI`, and `AutoGen`.

**Why this repo**: This collection of notebooks and helpers is designed for learning and prototyping autonomous agents, agent architectures, and integrations with popular agent frameworks. It is lightweight, examplar-driven, and intended for interactive exploration.

**Highlights**
- **Interactive notebooks**: Guided examples exploring planning, tool use, and reflection patterns.
- **Framework experiments**: Small demos and comparisons using multiple agent frameworks.
- **Reusable helpers**: Utility code (see `Scratch/helper.py`) to speed up experiments.

**Quick Start**

- **Prerequisites**: Python 3.10+ and `pip`.
- **Install dependencies**:

```bash
python -m pip install -r requirements.txt
```

- **Open the notebooks** (recommended):

```bash
jupyter lab
# or
jupyter notebook
```

- Notebooks are in the `Scratch/` folder. Useful starting points:
	- `Scratch/1_Reflection_pattern.ipynb` — reflection-based agent patterns
	- `Scratch/2_Tool_use_pattern.ipynb` — tool invocation workflows
	- `Scratch/3_Planning_pattern.ipynb` — planning and decomposition

**Repository Layout**
- `Scratch/` : example notebooks and `helper.py` utilities.
- `requirements.txt` : Python dependencies used by the notebooks.
- `README.md` : this file.

**Usage Tips**
- Use a virtual environment to keep dependencies isolated:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```
- If a notebook needs API keys (LLM providers, vector DBs), set them in your shell or a `.env` file and load them in the notebook before running cells.

**Contributing**
- Suggestions, bug reports, and PRs are welcome. For small improvements (typos, README edits), open a PR directly.
- For larger changes (new experiments, refactors), open an issue first to discuss the design.

**License & Contact**
- This project does not include a license file — add one if you plan to publish or share broadly.
- Questions or comments: open an issue or contact the repository owner.

Enjoy exploring agent design and experimentation! Pull requests and improvements welcome.
