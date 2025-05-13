alpha = '4E6nQpOkBcWmIfXorxGhg_z81qC3sv79DlRSN5PHeUZAwVYuat0TF2djJbKLyMi'
print(len(alpha), ''.join(sorted(alpha)))
check = 'lScv9oQ6VgELTPBdHnxp9dND'

dec = []
for c in check:
    dec += [alpha.index(c)]

print(dec)