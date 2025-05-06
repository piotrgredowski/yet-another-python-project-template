# Yet Another Python Project Template

## Additional dependencies

You need to have Python packages installed:

- `copier`
- `copier-templates-extensions`

You can install them with the following command:

```bash
pip install "copier==9.4.1" copier-templates-extensions
# or
uv tool install "copier==9.4.1" --with copier-templates-extensions
```

## Run copier

```bash
copier copy --vsc-ref HEAD https://github.com/piotrgredowski/yet-another-python-project-template <name_of_output_dir>
```
or
```bash
uv tool run copier copy --vsc-ref HEAD https://github.com/piotrgredowski/yet-another-python-project-template <name_of_output_dir>
```

## Creating a new project using this template

You need to run below command to start the project creation process:

```bash
copier copy https://github.com/piotrgredowski/yet-another-python-project-template.git /path/to/parent/directory/of/your/project
```
or 
```bash
uv tool run copier copy https://github.com/piotrgredowski/yet-another-python-project-template.git /path/to/parent/directory/of/your/project
```

You will be asked with many different questions. Answer them thoroughly.
