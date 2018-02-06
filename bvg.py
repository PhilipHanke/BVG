import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Jahreseinkommen/Gehalt


# Objekt model
# Beinhaltet: vier Beitragssätze (vier Altersstufen), Zinssatz, Umwandlungssatz
# Beispiel: model = [0.07, 0.10, 0.15, 0.18, 0.01, 0.07]

legalminimum = [0.07, 0.10, 0.15, 0.18, 0.01, 0.068]
#examplesalary = list(range(40000, 80000, 1000))


def contribution(salary, year, model):
    #Berechnet die BVG-Beiträge pro Jahr auf Basis des Jahreseinkommens
    koordinationsabzug = 24675
    versicherterLohn = max(min(84600, salary - koordinationsabzug), 0)
    contribution = versicherterLohn * contributionRate(year, model)
    return contribution

def contributionRate(year, model):
    #Berechnet die Beitragsrate entsprechend dem Alter
    #Problem: Je nach Plan unterschiedlich. Plan wird in Form der Liste model geliefert.
    age = year+20

    if age < 25:
        contributionRate = 0
    elif age >= 25 & age < 34:
        contributionRate = model[0]
    elif age >= 35 & age < 45:
        contributionRate = model[1]
    elif age >= 45 & age < 55:
        contributionRate = model[2]   
    elif age >= 55:
        contributionRate = model[3]
    return contributionRate

def contributions(model, salary):
    #Erstellt eine Liste mit den Beiträgen pro Jahr
    contributions = []
    for year in range(0,40):
        contributions.append(contribution(salary[year], year, model))
    return contributions

def pensionCapital(contributions, model):
    #contributions muss eine Liste sein (Beiträge pro Jahr für eine bestimmte Person)
    interestRate = model[4]
    contributionWithInterest = 0
    for annualcontribution in contributions:
        contributionWithInterest = contributionWithInterest + annualcontribution * (1+interestRate)**(40-contributions.index(annualcontribution))
    return contributionWithInterest


def pension(model, salary):
    #Berechnet die jährliche Pension (Kapital x Umwandlungssatz)
    umwandlungssatz = model[5]
    pension = pensionCapital(contributions(model, salary), model) * umwandlungssatz
    return int(pension)


def BVGModel(model):
    # Erstellt eine Liste (allSalaries) aus unterschiedlichen Gehältern (salary)
    allSalaries = []
    alphas = []
    betas = []
    for alpha in range(0,100000, 1000):
        for beta in range(0, 5000, 100):
            salary = [alpha + beta * year if (alpha+beta*year) > 0 else 1 for year in range(0,40)]
            for i in range(0, 15):
                salary.append(pension(model, salary))           # Fügt dem Einkommen noch 15 Jahre Pension hinzu
            coverage = pension(model, salary) / salary[39]      # Berechnet den Deckungsgrad (Pension in Prozent des letzten Gehalts)
            salary.append(round(coverage, 4))
            allSalaries.append(salary)
            alphas.append(alpha)
            betas.append(beta)
    summary = []

    # Für jede Person: Anfangs- und Endgehalt, Pension (2 Mal), Deckungsgrad
    for salary in allSalaries:
        individualSummary =[salary[0], salary[39], salary[40], salary[41], salary[55]]
        summary.append(individualSummary)

    #print(summary)

    #Liste mit allen Endgehältern
    endSalaries=[salary[39] for salary in allSalaries]
    
    #Liste mit allen Deckungsgraden
    coverages=[salary[55] for salary in allSalaries]

    # Pandas-DataFrame zur graphischen Darstellung
    df = pd.DataFrame({'endsalary': endSalaries, 'coverage':coverages, 'alpha':alphas, 'beta':betas})
    
    #plt.scatter(df.endsalary, df.coverage)
    #plt.title(model)

    print(df[df.coverage > 0.16])
    print(df[df.beta == 0])
    #print(df.endsalary, df.coverage, df.alpha, df.beta)

    #for i, label in enumerate(df.alpha): 
     #   plt.text(df.endsalary[i], df.coverage[i], df.alpha)

    #plt.text(df.endsalary, df.coverage, df.alpha)
    #plt.savefig(str(model)+'.jpg')
    #plt.show()
    return df

collectionOfModels = [
    legalminimum,
    [0.07, 0.10, 0.15, 0.18, 0.02, 0.068],
    [0.07, 0.10, 0.15, 0.18, 0.03, 0.068],
    [0.07, 0.10, 0.15, 0.18, 0.04, 0.068],
    [0.07, 0.10, 0.15, 0.18, 0.05, 0.068],
    [0.07, 0.10, 0.15, 0.18, 0.15, 0.18]
]

#for model in collectionOfModels:
#    BVGModel(model)

BVGModel(legalminimum)

plt.show()




# Nur Endgehalt und Deckungsgrad
#endSalaryAndCoverage = [[salary[1], salary[4]] for salary in summary]





#Berechnet die Versicherungsabdeckung für jedes Einkommen



#Berechne Lebenseinkommen pro Person mit allen Kombinationen aus alpha und beta
