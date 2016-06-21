FILES :=                              \
    Netflix.py                        \
    RunNetflix.py                     \
    RunNetflix.in                     \
    RunNetflix.out                    \
    TestNetflix.py                    \
    #TestNetflix.out                   \
    #Netflix.html                      \
    #Netflix.log

ifeq ($(CI), true)
    COVERAGE := coverage
    PYLINT   := pylint
else
    COVERAGE := coverage-3.5
	PYLINT   := pylint
endif

.pylintrc:
	$(PYLINT) --disable=bad-whitespace,missing-docstring,pointless-string-statement,global-statement,too-many-branches,trailing-whitespace,too-many-statements,no-name-in-module --reports=n --generate-rcfile > $@

Netflix-tests:
	git clone https://github.com/cs373-summer-2016/netflix-tests.git

Netflix.html: Netflix.py
	pydoc3 -w Netflix

Netflix.log:
	git log > Netflix.log

RunNetflix.tmp: .pylintrc RunNetflix.in RunNetflix.out RunNetflix.py
	-$(PYLINT) Netflix.py
	-$(PYLINT) RunNetflix.py
	./RunNetflix.py < RunNetflix.in > RunNetflix.tmp
	diff RunNetflix.tmp RunNetflix.out
	python3 -m cProfile RunNetflix.py < RunNetflix.in > RunNetflix.tmp
	#python3 -m cProfile RunNetflix.py < /u/downing/cs/netflix/probe.txt > RunNetflix.tmp
	cat RunNetflix.tmp

TestNetflix.tmp: .pylintrc TestNetflix.py
	-$(PYLINT) Netflix.py
	-$(PYLINT) TestNetflix.py
	$(COVERAGE) run --omit='*requests*,*numpy*' --branch TestNetflix.py 
	$(COVERAGE) report -m                      >> TestNetflix.tmp
	cat TestNetflix.tmp

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  .pylintrc
	rm -f  *.pyc
	rm -f  Netflix.html
	rm -f  Netflix.log
	rm -f  RunNetflix.tmp
	rm -f  TestNetflix.tmp
	rm -rf __pycache__
	rm -rf netflix-tests

config:
	git config -l

format:
	autopep8 -i Netflix.py
	autopep8 -i RunNetflix.py
	autopep8 -i TestNetflix.py

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

test: Netflix.html Netflix.log Netflix-tests TestNetflix.tmp RunNetflix.tmp check