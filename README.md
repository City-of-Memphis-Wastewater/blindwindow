# Blindwindow

Render console stderr and stdout to a TKinter based REPL widget masquerading as a log pange.

Use Case: When calling a CLI packaged inside of a MSIX that has been delivered via the Microsoft Store. This use case typically does not allow prints. 
Example: `pdflinkcheck.exe serve --help`


## Helptree

See the `blindwindow` Typer CLI structure.

```bash
blindwindow helptree
```
<p align="center">
  <img src="https://raw.githubusercontent.com/City-of-Memphis-Wastewater/blindwindow/main/assets/blindwindow_v0.1.4_helptree.svg" width="100%" alt="SVG of the CLI helptree">
</p>
