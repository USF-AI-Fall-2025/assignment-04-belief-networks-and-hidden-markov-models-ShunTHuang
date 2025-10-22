from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination

alarm_model = BayesianNetwork(
    [
        ("Burglary", "Alarm"),
        ("Earthquake", "Alarm"),
        ("Alarm", "JohnCalls"),
        ("Alarm", "MaryCalls"),
    ]
)

# Defining the parameters using CPT
from pgmpy.factors.discrete import TabularCPD

cpd_burglary = TabularCPD(
    variable="Burglary", variable_card=2, values=[[0.999], [0.001]],
    state_names={"Burglary":['no','yes']},
)
cpd_earthquake = TabularCPD(
    variable="Earthquake", variable_card=2, values=[[0.998], [0.002]],
    state_names={"Earthquake":["no","yes"]},
)
cpd_alarm = TabularCPD(
    variable="Alarm",
    variable_card=2,
    values=[[0.999, 0.71, 0.06, 0.05], [0.001, 0.29, 0.94, 0.95]],
    evidence=["Burglary", "Earthquake"],
    evidence_card=[2, 2],
    state_names={"Burglary":['no','yes'], "Earthquake":['no','yes'], 'Alarm':['yes','no']},
)
cpd_johncalls = TabularCPD(
    variable="JohnCalls",
    variable_card=2,
    values=[[0.95, 0.1], [0.05, 0.9]],
    evidence=["Alarm"],
    evidence_card=[2],
    state_names={"Alarm":['yes','no'], "JohnCalls":['yes', 'no']},
)
cpd_marycalls = TabularCPD(
    variable="MaryCalls",
    variable_card=2,
    values=[[0.1, 0.7], [0.9, 0.3]],
    evidence=["Alarm"],
    evidence_card=[2],
state_names={"Alarm":['yes','no'], "MaryCalls":['yes', 'no']},
)

# Associating the parameters with the model structure
alarm_model.add_cpds(
    cpd_burglary, cpd_earthquake, cpd_alarm, cpd_johncalls, cpd_marycalls)

alarm_infer = VariableElimination(alarm_model)

# print(alarm_infer.query(variables=["JohnCalls"],evidence={"Earthquake":"yes"}))
#
#the probability of Mary Calling given that John called

# q = alarm_infer.query(variables=["Alarm", "Burglary"],evidence={"MaryCalls":"yes"})
# print(q)


def main():
    q1 = alarm_infer.query(variables=["MaryCalls"], evidence={"JohnCalls": "yes"})
    print("P(MaryCalls | JohnCalls='yes'):")
    print(q1)
    print(f"P(MaryCalls='yes' | JohnCalls='yes') = {float(q1.values[0])} \n")

    q2 = alarm_infer.query(variables=["JohnCalls", "MaryCalls"], evidence={"Alarm": "yes"})
    print("P(JohnCalls, MaryCalls | Alarm='yes'):")
    print(q2)
    print(f"P(JohnCalls='yes', MaryCalls='yes' | Alarm='yes') = {float(q2.values[0, 0])} \n")

    q3 = alarm_infer.query(variables=["Alarm"], evidence={"MaryCalls": "yes"})
    print("P(Alarm | MaryCalls='yes'):")
    print(q3)
    print(f"P(Alarm='yes' | MaryCalls='yes') = {float(q3.values[0])}")

if __name__ == "__main__":
    main()