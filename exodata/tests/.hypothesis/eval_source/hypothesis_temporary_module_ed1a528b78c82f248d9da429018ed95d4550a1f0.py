from hypothesis.utils.conventions import not_set

def accept(f):
    def test_works(self, T_eff=not_set, mu=not_set, g=not_set, H=not_set):
        return f(self=self, T_eff=T_eff, mu=mu, g=g, H=H)
    return test_works
