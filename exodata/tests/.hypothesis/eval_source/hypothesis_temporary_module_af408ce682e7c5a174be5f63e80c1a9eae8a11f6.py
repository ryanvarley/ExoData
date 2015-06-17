from hypothesis.utils.conventions import not_set

def accept(f):
    def test_can_derive_other_vars_from_one_calculated(self, M=not_set, R=not_set):
        return f(self=self, M=M, R=R)
    return test_can_derive_other_vars_from_one_calculated
