tests_bdd:
	cd tests/bdd && ../../test_env/bin/python3 -m behave

prepare:
	sh prepare_test_env.sh 

clean:
	sh prepare_test_env.sh --clear
