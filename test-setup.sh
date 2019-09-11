
# run some basic exec-tests

# check if all listing are ok
python3 -m tptp local list-solvers
python3 -m tptp system-on-tptp list-solvers

# run some basic proves
python3 -m tptp local run --solver-name "leo3" --problem "problems/SYN001+1.p" --timeout 60
python3 -m tptp local request --solver-name "leo3" --solver-command "leo3 %s -t %d" --problem "problems/SYN001+1.p" --timeout 60
python3 -m tptp system-on-tptp request --solver-name "Leo-III---1.4" --solver-command "run_Leo-III %s %d" --problem "problems/SYN001+1.p" --timeout 60
