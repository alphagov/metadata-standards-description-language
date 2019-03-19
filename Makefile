.PHONY: help prepare prepare-prereq odfpy clean mrproper run

# User configuration
export GDS_PREFIX=/Users/andybennett/git/odf-prototype


# No more user configuration below this line!
export GDS_PYTHON_MODULES=${GDS_PREFIX}/lib
export PYTHONPATH=${GDS_PYTHON_MODULES}/lib/python2.7/site-packages

help:
	@echo "Edit the user configuration in the Makefile and then run \`make prepare\`"
	@echo "to install the dependencies."
	@echo "Use \`make run\` to invoke the tool with the correct environment."

prepare: prepare-prereq odfpy

prepare-prereq:
	if [ -d ${GDS_PREFIX} ]; then \
		exit 0;               \
	else                          \
	        echo "\n\nERROR: ${GDS_PREFIX}/ does not exist!";           \
		echo "ERROR: Please configure the Makefile and try again!\n"; \
		exit 1;               \
	fi

${GDS_PYTHON_MODULES}:
	mkdir $@/

${PYTHONPATH}: ${GDS_PYTHON_MODULES}
	mkdir -p ${PYTHONPATH}/
 
odfpy: prepare-prereq ${PYTHONPATH}
	if [ -d tmp.prepare/ ]; then   \
		echo "\n\nERROR: tmp.prepare/ already exists!\n"; \
		exit 1;                \
	else                           \
		mkdir tmp.prepare/;    \
		cd tmp.prepare/;       \
		git clone http://github.com/eea/odfpy.git; \
		cd odfpy/ ;            \
		python setup.py build; \
		python setup.py install --prefix=${GDS_PYTHON_MODULES}; \
		mkdir manual/out/;        \
		cd manual/out;            \
		python ../buildmanual.py; \
		python ../htmlmanual.py;  \
		cd -;                     \
		mv manual/out        ${GDS_PYTHON_MODULES}/odfpy.manual ; \
		mv examples          ${GDS_PYTHON_MODULES}/odfpy.manual/; \
		mv doc               ${GDS_PYTHON_MODULES}/odfpy.manual/; \
		mv api-for-odfpy.odt ${GDS_PYTHON_MODULES}/odfpy.manual/; \
		cd ../../ ;            \
		rm -fr tmp.prepare/;   \
	fi

clean:

mrproper: clean
	rm -fr *~
	rm -fr tmp.prepare/
	rm -fr ${GDS_PYTHON_MODULES}/

run:
	python poc.py

