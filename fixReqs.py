def Fix(good,bad,new):
    final = []
    good_lines = open(good,'r').readlines()
#    print(good_lines)
    bad_lines = open(bad,'r').readlines()
#    print(bad_lines)
    new_lines = open(new,'r').readlines()
#    print(new_lines)
    for line in new_lines:
        if line in good_lines and line in bad_lines:
            final.append(line.strip())
        elif line in good_lines and line not in bad_lines:
            final.append(line.strip())
        elif line not in good_lines and line not in bad_lines:
            final.append(line.strip())
    print("\n".join(final))

Fix("requirements-latest.txt", "requirements-bad.txt", "requirements.txt")
