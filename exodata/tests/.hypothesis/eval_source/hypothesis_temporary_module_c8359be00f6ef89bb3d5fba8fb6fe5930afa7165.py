from hypothesis.utils.conventions import not_set

def accept(f):
    def test_can_derive_other_vars_from_one_calculated(self, T=not_set, R=not_set):
        return f(self=self, T=T, R=R)
    return test_can_derive_other_vars_from_one_calculated
