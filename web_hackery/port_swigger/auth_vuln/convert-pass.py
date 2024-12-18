print("[", end='')

with open('passwordlist', 'r') as f:
    lines = f.readlines()

# Remove any trailing newline characters and print passwords
formatted_passwords = []
for pwd in lines:
    formatted_passwords.append(f'"{pwd.rstrip()}"')

# Join the formatted passwords with commas and print
print(", ".join(formatted_passwords), end='')

print(", \"random\"]")
