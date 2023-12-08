def ext_euclid(a: int, b :int) -> tuple[int, int, int]:
    """
    Returns (d, x, y) such that d = gcd(a, b) = ax + by
    """
    if b == 0:
        return a, 1, 0
    q = a // b
    r = a % b
    d, x, y = ext_euclid(b, r)
    return d, y, x - q * y


def crt(a1: int, m1: int, a2: int, m2: int) -> tuple[int, int]:
    """
    Returns (x, m) such that x = a1 (mod m1) and x = a2 (mod m2) and m = m1 * m2 // gcd(m1, m2).
    Usually m1 and m2 are coprime and m = m1 * m2.
    """
    d, x, y = ext_euclid(m1, m2)
    if (a1 - a2) % d != 0:
        raise ValueError("No solution")
    m = m1 * m2 // d
    x = (a1 * y * m2 + a2 * x * m1) // d
    return x % m, m


def list_crt(rems: list[int], mods: list[int]) -> tuple[int, int]:
    """
    Returns (x, m) such that x = rems[i] (mod mods[i]) for all i and m = lcm(mods).
    Usually mods are coprime and m = prod(mods).
    """
    if len(rems) != len(mods):
        raise ValueError("Lengths of rems and mods must be equal")
    x = rems[0]
    m = mods[0]
    for i in range(1, len(rems)):
        x, m = crt(x, m, rems[i], mods[i])
    return x, m
