tests_bdd: prepare
	sh run_bdd.sh

prepare:
	sh prepare_test_env.sh

clean:
	sh prepare_test_env.sh --clear
