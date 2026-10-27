"""Tiny helpers for the notebook builders (markdown and code cells, four-part explanation blocks)."""
import nbformat as nbf


def md(t): return nbf.v4.new_markdown_cell(t.strip("\n"))
def code(t): return nbf.v4.new_code_cell(t.strip("\n"))


def explain(title, why, alts, how, read):
    """alts: list of strings. Returns one markdown cell with the four required parts."""
    a = "\n".join(f"   - {x}" for x in alts)
    return md(f"**{title}**\n\n1. **Why this method.** {why}\n2. **Alternatives considered.**\n{a}\n3. **How it works.** {how}\n4. **How to read the output.** {read}")


def save(cells, path):
    nb = nbf.v4.new_notebook(); nb.cells = cells
    nb.metadata["kernelspec"] = {"name": "portfolio", "display_name": "portfolio", "language": "python"}
    nbf.write(nb, path)
