tests_bdd:
	sh run_bdd.sh

prepare:
	sh prepare_test_env.sh

clean:
	sh prepare_test_env.sh --clear
