from hypothesis.utils.conventions import not_set

def accept(f):
    def test_can_derive_other_vars_from_one_calculated(self, T_eff=not_set, mu=not_set, g=not_set):
        return f(self=self, T_eff=T_eff, mu=mu, g=g)
    return test_can_derive_other_vars_from_one_calculated
