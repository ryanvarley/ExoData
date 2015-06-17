from hypothesis.utils.conventions import not_set

def accept(f):
    def test_can_derive_other_vars_from_one_calculated(self, A, T_s=not_set, R_s=not_set, a=not_set, epsilon=not_set):
        return f(self=self, A=A, T_s=T_s, R_s=R_s, a=a, epsilon=epsilon)
    return test_can_derive_other_vars_from_one_calculated
