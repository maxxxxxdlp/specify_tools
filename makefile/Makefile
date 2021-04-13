# make run   VERSION=6_8_00/6_8_00_L10N/6_7_01/6_7_04 RUN=S/S1/W/D/B
# make pull  BRANCH=develop # will update local specify build from GitHub # can select any branch
# make build BRNACH=develop UPDATE=y INSTALL=y # runs make pull and then builds it

# RUN values:
#  S  - Specify4GB
#  S1 - Specify
#  W  - SpWizard
#  D  - DataExporter
#  B  - SpBackupRestore

ANT_LOCATION=~/

ifeq (${VERSION},)

else ifeq (${VERSION},6_8_00)
	EXEC_PATH=~/Specify_6_8_00/bin/
else ifeq (${VERSION},6_8_00_L10N)
	EXEC_PATH=~/Specify_6_8_00_L10N/bin/
else ifeq (${VERSION},6_7_01)
	EXEC_PATH=~/Specify_6_7_01/bin/
else ifeq (${VERSION},6_7_04)
	EXEC_PATH=~/Specify/bin/
endif

ifeq (${RUN},)

else ifeq (${RUN},S)
	RUN_PATH=Specify4GB
else ifeq (${RUN},S1)
	RUN_PATH=Specfify
else ifeq (${RUN},W)
	RUN_PATH=SpWizard
else ifeq (${RUN},D)
	RUN_PATH=DataExporter
else ifeq (${RUN},B)
	RUN_PATH=SpBackupRestore
endif

run:
	${EXEC_PATH}${RUN_PATH}

pull:
	curl -sS https://codeload.github.com/specify/specify6/zip/${BRANCH} > ${CURDIR}/specify6-${BRANCH}.zip
	unzip -o ${CURDIR}/specify6-${BRANCH}.zip
	rm ${CURDIR}/specify6-${BRANCH}.zip

build:
	if [ "$(UPDATE)" != "n" ]; then \
		make pull BRANCH=${BRANCH}; \
	fi
	${ANT_LOCATION}apache-ant-1.10.7/bin/./ant package-internal-nonmac -Dinstall4j.dir=${HOME}/install4j7 -f ${HOME}/Downloads/specify6-${BRANCH}/build.xml
	chmod 777 ${CURDIR}/specify6-${BRANCH}/packages/internal/*
	if [ "$(INSTALL)" != "n" ]; then \
		${CURDIR}/specify6-${BRANCH}/packages/internal/./Specify_unix_6_8_00_Beta_64.sh; \
	fi
