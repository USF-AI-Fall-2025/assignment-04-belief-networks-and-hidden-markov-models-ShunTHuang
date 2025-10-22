from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete import TabularCPD


def bayesian_network(step = "step_2"):
    edges = [
            ("Battery", "Radio"),
            ("Battery", "Ignition"),
            ("Ignition","Starts"),
            ("Gas","Starts"),
            ("Starts","Moves"),
    ]
    if step == "step_3": edges.append(("KeyPresent","Starts"))

    car_model = BayesianNetwork(edges)

    # Defining the parameters using CPT


    cpd_battery = TabularCPD(
        variable="Battery", variable_card=2, values=[[0.70], [0.30]],
        state_names={"Battery":['Works',"Doesn't work"]},
    )

    cpd_gas = TabularCPD(
        variable="Gas", variable_card=2, values=[[0.40], [0.60]],
        state_names={"Gas":['Full',"Empty"]},
    )

    cpd_radio = TabularCPD(
        variable=  "Radio", variable_card=2,
        values=[[0.75, 0.01],[0.25, 0.99]],
        evidence=["Battery"],
        evidence_card=[2],
        state_names={"Radio": ["turns on", "Doesn't turn on"],
                     "Battery": ['Works',"Doesn't work"]}
    )

    cpd_ignition = TabularCPD(
        variable=  "Ignition", variable_card=2,
        values=[[0.75, 0.01],[0.25, 0.99]],
        evidence=["Battery"],
        evidence_card=[2],
        state_names={"Ignition": ["Works", "Doesn't work"],
                     "Battery": ['Works',"Doesn't work"]}
    )

    cpd_moves = TabularCPD(
        variable="Moves", variable_card=2,
        values=[[0.8, 0.01], [0.2, 0.99]],
        evidence=["Starts"],
        evidence_card=[2],
        state_names={"Moves": ["yes", "no"],
                     "Starts": ['yes', 'no']}
    )

    if step == "step_2":
        cpd_starts = TabularCPD(
            variable="Starts",
            variable_card=2,
            values=[[0.95, 0.05, 0.05, 0.001], [0.05, 0.95, 0.95, 0.9999]],
            evidence=["Ignition", "Gas"],
            evidence_card=[2, 2],
            state_names={"Starts":['yes','no'], "Ignition":["Works", "Doesn't work"], "Gas":['Full',"Empty"]},
        )

        car_model.add_cpds(cpd_starts, cpd_ignition, cpd_gas, cpd_radio, cpd_battery, cpd_moves)

    # step_3
    if step == "step_3":
        cpd_starts = TabularCPD(
            variable="Starts",
            variable_card=2,
            values=[[0.99, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01], [0.01, 0.99, 0.99, 0.99, 0.99, 0.99, 0.99, 0.99]],
            evidence=["Ignition", "Gas", "KeyPresent"],
            evidence_card=[2, 2, 2],
            state_names={"Starts":['yes','no'], "Ignition":["Works", "Doesn't work"], "Gas":['Full',"Empty"], "KeyPresent": ["yes", "no"]},
        )

        cpd_key = TabularCPD(
            variable="KeyPresent", variable_card=2,
            values=[[0.7], [0.3]],
            state_names={"KeyPresent": ["yes", "no"]},
        )

        car_model.add_cpds(cpd_starts, cpd_ignition, cpd_gas, cpd_radio, cpd_battery, cpd_moves, cpd_key)

    return VariableElimination(car_model)

def step_2(car_infer):
    # Q1: Given that the car will not move, what is the probability that the battery is not working?
    q1 = car_infer.query(variables=["Battery"], evidence={"Moves": "no"})
    print(q1)
    print(f"[Q1] P(Battery='Doesn't work' | Moves='no') = {float(q1.values[1])} \n")

    # Given that the radio is not working, what is the probability that the car will not start?
    q2 = car_infer.query(variables=["Starts"], evidence={"Radio": "Doesn't turn on"})
    print(q2)
    print(f"[Q2] P(Starts='no' | Radio='Doesn't turn on') = {float(q2.values[1])} \n")

    # Q3: Given that the battery is working, does radio change if gas is known?
    q3a = car_infer.query(variables=["Radio"], evidence={"Battery": "Works"})
    q3b = car_infer.query(variables=["Radio"], evidence={"Battery": "Works", "Gas": "Full"})
    print(q3a)
    print(q3b)
    print(f"[Q3a] P(Radio='turns on' | Battery='Works') = {float(q3a.values[0])}")
    print(f"[Q3b] P(Radio='turns on' | Battery='Works', Gas='Full') = {float(q3b.values[0])}\n")

    # Q4: Given that the car doesn't move, how does ignition failure change with Gas='Empty'?
    q4a = car_infer.query(variables=["Ignition"], evidence={"Moves": "no"})
    q4b = car_infer.query(variables=["Ignition"], evidence={"Moves": "no", "Gas": "Empty"})
    print(q4a)
    print(q4b)
    print(f"[Q4a] P(Ignition='Doesn't work' | Moves='no') = {float(q4a.values[1])}")
    print(f"[Q4b] P(Ignition='Doesn't work' | Moves='no', Gas='Empty') = {float(q4b.values[1])}\n")

    # Q5: What is the probability the car starts if radio works and gas is full?
    q5 = car_infer.query(variables=["Starts"], evidence={"Radio": "turns on", "Gas": "Full"})
    print(q5)
    print(f"[Q5] P(Starts='yes' | Radio='turns on', Gas='Full') = {float(q5.values[0])}")

def step_3(car_infer):
    q = car_infer.query(variables=["KeyPresent"], evidence={"Moves": "no"})
    print("[Step3] P(KeyPresent| Moves='no')")
    print(q)
    print(f"P(KeyPresent='no' | Moves='no') = {float(q.values[1])}")


def main():
    # Associating the parameters with the model structure

    # step_2
    # car_model.add_cpds(cpd_starts, cpd_ignition, cpd_gas, cpd_radio, cpd_battery, cpd_moves)

    # step_3
    # car_model.add_cpds( cpd_starts, cpd_ignition, cpd_gas, cpd_radio, cpd_battery, cpd_moves, cpd_key)

    # car_infer = VariableElimination(car_model)

    # print(car_infer.query(variables=["Moves"],evidence={"Radio":"turns on", "Starts":"yes"}))
    # step_2(car_infer)
    print("[Step2]")
    step_2(bayesian_network())
    print("\n[Step3]")
    step_3(bayesian_network("step_3"))


if __name__ == "__main__":
    main()