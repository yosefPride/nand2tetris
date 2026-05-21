# Bugs
## Arrays:
    For an expression like 'let a[i] = x;', I'll advance right past the '['.
    Which means arrays won't be handled when assigned to.
