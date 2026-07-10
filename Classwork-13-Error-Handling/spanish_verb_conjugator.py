#Required structure
pronouns = ["Yo", "Tú", "Él", "Nosotros", "Vosotros", "Ellos"]

endings = {
    'ar': ['o', 'as', 'a', 'amos', 'ais', 'an'],
    'er': ['o', 'es', 'e', 'emos', 'eis', 'en'],
    'ir': ['o', 'es', 'e', 'imos', 'is', 'en']
}

#INPUT
verb = input("Write a spanish verb (ar/er/ir): ")

#PROCESS
stem = verb[:-2]
ending = verb[-2:]

conjugations = endings[ending]

#OUTPUT
for index, pronoun in enumerate(pronouns):
    termination = conjugations[index]
    print(f"{pronoun} {stem}{termination}")