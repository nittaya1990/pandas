tseries: pandas/_libs/lib.pyx pandas/_libs/tslib.pyx pandas/_libs/hashtable.pyx
	python setup.py build_ext --inplace

.PHONY : develop build clean clean_pyc tseries doc

clean:
	-python setup.py clean

clean_pyc:
	-find . -name '*.py[co]' -exec rm {} \;

build: clean_pyc
	python setup.py build_ext --inplace

lint-diff:
	git diff upstream/master --name-only -- "*.py" | xargs flake8

develop: build
	-python setup.py develop

doc:
	-rm -rf doc/build doc/source/generated
	cd doc; \
	python make.py clean; \
	python make.py html
	python make.py spellcheck


json: pandas/_libs/src/ujson/python/objToJSON.c
	clang -Wno-unused-result -Wsign-compare -Wunreachable-code -fno-common -dynamic -g -fwrapv   -Wall -I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.14.sdk/System/Library/Frameworks/Tk.framework/Versions/8.5/Headers -Ipandas/_libs/src/ujson/python -Ipandas/_libs/src/ujson/lib -Ipandas/_libs/src/datetime -I/Users/taugspurger/sandbox/numpy/numpy/core/include -I/usr/local/include -I/usr/local/opt/openssl/include -I/usr/local/opt/sqlite/include -I/Users/taugspurger/Envs/pandas-dev/include -I/usr/local/Cellar/python/3.7.1/Frameworks/Python.framework/Versions/3.7/include/python3.7m -c pandas/_libs/src/ujson/python/ujson.c -o build/temp.macosx-10.13-x86_64-3.7/pandas/_libs/src/ujson/python/ujson.o
	clang -Wno-unused-result -Wsign-compare -Wunreachable-code -fno-common -dynamic -g -fwrapv   -Wall -I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.14.sdk/System/Library/Frameworks/Tk.framework/Versions/8.5/Headers -Ipandas/_libs/src/ujson/python -Ipandas/_libs/src/ujson/lib -Ipandas/_libs/src/datetime -I/Users/taugspurger/sandbox/numpy/numpy/core/include -I/usr/local/include -I/usr/local/opt/openssl/include -I/usr/local/opt/sqlite/include -I/Users/taugspurger/Envs/pandas-dev/include -I/usr/local/Cellar/python/3.7.1/Frameworks/Python.framework/Versions/3.7/include/python3.7m -c pandas/_libs/src/ujson/python/objToJSON.c -o build/temp.macosx-10.13-x86_64-3.7/pandas/_libs/src/ujson/python/objToJSON.o
	clang -Wno-unused-result -Wsign-compare -Wunreachable-code -fno-common -dynamic -g -fwrapv   -Wall -I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.14.sdk/System/Library/Frameworks/Tk.framework/Versions/8.5/Headers -Ipandas/_libs/src/ujson/python -Ipandas/_libs/src/ujson/lib -Ipandas/_libs/src/datetime -I/Users/taugspurger/sandbox/numpy/numpy/core/include -I/usr/local/include -I/usr/local/opt/openssl/include -I/usr/local/opt/sqlite/include -I/Users/taugspurger/Envs/pandas-dev/include -I/usr/local/Cellar/python/3.7.1/Frameworks/Python.framework/Versions/3.7/include/python3.7m -c pandas/_libs/src/ujson/python/JSONtoObj.c -o build/temp.macosx-10.13-x86_64-3.7/pandas/_libs/src/ujson/python/JSONtoObj.o
	clang -Wno-unused-result -Wsign-compare -Wunreachable-code -fno-common -dynamic -g -fwrapv   -Wall -I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.14.sdk/System/Library/Frameworks/Tk.framework/Versions/8.5/Headers -Ipandas/_libs/src/ujson/python -Ipandas/_libs/src/ujson/lib -Ipandas/_libs/src/datetime -I/Users/taugspurger/sandbox/numpy/numpy/core/include -I/usr/local/include -I/usr/local/opt/openssl/include -I/usr/local/opt/sqlite/include -I/Users/taugspurger/Envs/pandas-dev/include -I/usr/local/Cellar/python/3.7.1/Frameworks/Python.framework/Versions/3.7/include/python3.7m -c pandas/_libs/src/ujson/lib/ultrajsonenc.c -o build/temp.macosx-10.13-x86_64-3.7/pandas/_libs/src/ujson/lib/ultrajsonenc.o
	clang -Wno-unused-result -Wsign-compare -Wunreachable-code -fno-common -dynamic -g -fwrapv   -Wall -I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.14.sdk/System/Library/Frameworks/Tk.framework/Versions/8.5/Headers -Ipandas/_libs/src/ujson/python -Ipandas/_libs/src/ujson/lib -Ipandas/_libs/src/datetime -I/Users/taugspurger/sandbox/numpy/numpy/core/include -I/usr/local/include -I/usr/local/opt/openssl/include -I/usr/local/opt/sqlite/include -I/Users/taugspurger/Envs/pandas-dev/include -I/usr/local/Cellar/python/3.7.1/Frameworks/Python.framework/Versions/3.7/include/python3.7m -c pandas/_libs/src/ujson/lib/ultrajsondec.c -o build/temp.macosx-10.13-x86_64-3.7/pandas/_libs/src/ujson/lib/ultrajsondec.o
	clang -Wno-unused-result -Wsign-compare -Wunreachable-code -fno-common -dynamic -g -fwrapv   -Wall -I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.14.sdk/System/Library/Frameworks/Tk.framework/Versions/8.5/Headers -Ipandas/_libs/src/ujson/python -Ipandas/_libs/src/ujson/lib -Ipandas/_libs/src/datetime -I/Users/taugspurger/sandbox/numpy/numpy/core/include -I/usr/local/include -I/usr/local/opt/openssl/include -I/usr/local/opt/sqlite/include -I/Users/taugspurger/Envs/pandas-dev/include -I/usr/local/Cellar/python/3.7.1/Frameworks/Python.framework/Versions/3.7/include/python3.7m -c pandas/_libs/tslibs/src/datetime/np_datetime.c -o build/temp.macosx-10.13-x86_64-3.7/pandas/_libs/tslibs/src/datetime/np_datetime.o
	clang -Wno-unused-result -Wsign-compare -Wunreachable-code -fno-common -dynamic -g -fwrapv   -Wall -I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.14.sdk/System/Library/Frameworks/Tk.framework/Versions/8.5/Headers -Ipandas/_libs/src/ujson/python -Ipandas/_libs/src/ujson/lib -Ipandas/_libs/src/datetime -I/Users/taugspurger/sandbox/numpy/numpy/core/include -I/usr/local/include -I/usr/local/opt/openssl/include -I/usr/local/opt/sqlite/include -I/Users/taugspurger/Envs/pandas-dev/include -I/usr/local/Cellar/python/3.7.1/Frameworks/Python.framework/Versions/3.7/include/python3.7m -c pandas/_libs/tslibs/src/datetime/np_datetime_strings.c -o build/temp.macosx-10.13-x86_64-3.7/pandas/_libs/tslibs/src/datetime/np_datetime_strings.o
	clang -bundle -undefined dynamic_lookup build/temp.macosx-10.13-x86_64-3.7/pandas/_libs/src/ujson/python/ujson.o build/temp.macosx-10.13-x86_64-3.7/pandas/_libs/src/ujson/python/objToJSON.o build/temp.macosx-10.13-x86_64-3.7/pandas/_libs/src/ujson/python/JSONtoObj.o build/temp.macosx-10.13-x86_64-3.7/pandas/_libs/src/ujson/lib/ultrajsonenc.o build/temp.macosx-10.13-x86_64-3.7/pandas/_libs/src/ujson/lib/ultrajsondec.o build/temp.macosx-10.13-x86_64-3.7/pandas/_libs/tslibs/src/datetime/np_datetime.o build/temp.macosx-10.13-x86_64-3.7/pandas/_libs/tslibs/src/datetime/np_datetime_strings.o -L/usr/local/lib -L/usr/local/opt/openssl/lib -L/usr/local/opt/sqlite/lib -o /Users/taugspurger/sandbox/pandas/pandas/_libs/json.cpython-37m-darwin.so

bug: bug.py
	gdb python
