from hypothesis.utils.conventions import not_set

def accept(f):
    def test_can_derive_other_vars_from_one_calculated(self, a=not_set, M_s=not_set, M_p=not_set):
        return f(self=self, a=a, M_s=M_s, M_p=M_p)
    return test_can_derive_other_vars_from_one_calculated
