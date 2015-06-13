""" Tests new style equations using hypothesis
"""
#
# from .. import astroquantities as aq
# import hypothesis
#
# def eqn_tester(eqn, precision=0.01, **kwargs):
#     """
#     :param eqn:
#     :param input_dict: {'var': (hypothesis.strategies, unit),}
#     :type: dict
#     :return:
#     """
#
#     keys = kwargs.keys()
#
#     for k in keys:
#         v = kwargs[k]
#         kwargs[k] = None  # set key to None
#
#         # get the value of this key from the other variables
#         result = eval('eqn(**kwargs).{}'.format(k))
#
#         # Now given the result, test we can recover each other combination
#         for k2 in keys:
#             v2 = kwargs[k2]
#             kwargs[k2] = None
#
#             result2 = eval('eqn(**kwargs).{}'.format(k2))
#
#             # TODO test result2 == v2 within tolerance
#
#             kwargs[k2] = v2
#
#         kwargs[k] = v  # replace key value