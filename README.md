# lark-performance-tests

This is a mess. Was created for lark PR [#949](https://github.com/lark-parser/lark/pull/949).

These scripts made sense to me at the time. Not sure how about now.

In general:

-  `performance_tests.py` uses a second implementation of the rule generation to tests a lot of different scenarios on how splitting up the `N` into `a`s and `b`s performs.
-  `performance_tests_2.py` varied the actual Thresholds inside of lark to check for the actual effects on the implementation.
-  `best_factors.py` just tests which 'factorizations' of `a`s and `b`s gets the best 'factor_sums'.
