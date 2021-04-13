# Makefile

This is a tool that helps quickly build and run any version of Specify

```sh
make run   VERSION=6_8_00/6_8_00_L10N/6_7_01/6_7_04 RUN=S/S1/W/D/B
make pull  BRANCH=develop # will update local specify build from GitHub # can select any branch
make build BRNACH=develop UPDATE=y INSTALL=y # runs make pull and then builds it

# RUN values:
#  S  - Specify4GB
#  S1 - Specify
#  W  - SpWizard
#  D  - DataExporter
#  B  - SpBackupRestore
```
