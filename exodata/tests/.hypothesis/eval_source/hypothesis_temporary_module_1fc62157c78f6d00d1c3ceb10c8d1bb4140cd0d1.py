from hypothesis.utils.conventions import not_set

def accept(f):
    def test_can_derive_other_vars_from_one_calculated(self, R_p=not_set, R_s=not_set):
        return f(self=self, R_p=R_p, R_s=R_s)
    return test_can_derive_other_vars_from_one_calculated
