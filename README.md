# Yet Another Python Project Template

## Additional dependencies

You need to have Python packages installed:

- `copier==9.4.1`
- `copier-templates-extensions`

You can install them with the following command:

```bash
pip install "copier==9.4.1" copier-templates-extensions
# or
uv tool install "copier==9.4.1" --with copier-templates-extensions
```

## Run copier

```bash
copier copy --vcs-ref HEAD https://github.com/piotrgredowski/yet-another-python-project-template <name_of_output_dir>
```

or

```bash
uv tool run copier copy --vcs-ref HEAD https://github.com/piotrgredowski/yet-another-python-project-template <name_of_output_dir>
```

You will be asked with many different questions. Answer them thoroughly.
