COVID 19 (my data analysis)
===========================

Introduction
------------
Thanks to the COVID19 data made available by the Johns Hopkins University (https://systems.jhu.edu/research/public-health/ncov/) in the github repository (https://github.com/CSSEGISandData/COVID-19) it is possible to make your own analysis and create your own plots. 

I made some analysis to see how the number of cases and deaths are growing still in an exponential way, but the rate should decrease hopefully soon.

In a logarithmic plot, an exponential curve looks as a straigh line. The pendent of the straight line gives you the increase rate. It can be shown that the data is not fully linear but the slope is changing towards to an horizontal (stabilization). For example this plot compares the situation of Spain with Italy, considering a delay of 7 days (Spain behind Italy): 

.. image:: https://github.com/srio/COVID19/blob/master/figures/italy_vs_spain.png

In the following anaysis, I make a plot per country (Spain, France, Italy and US) displaying the situation up to now, make a fit of the last days to calculate the increasing ratio (number of days in which it doubles) and extrapolate for tomorrow. Hopefully, because we are at home #quedateencasa the ratio will be reduced in the next days so we will approach the stabilization. 

We must act together to flatten the curves!! 


Evolution of the time for doubling the cases/deaths
---------------------------------------------------

.. image:: https://github.com/srio/COVID19/blob/master/figures/Spain_x2.png
.. image:: https://github.com/srio/COVID19/blob/master/figures/France_x2.png
.. image:: https://github.com/srio/COVID19/blob/master/figures/Italy_x2.png
.. image:: https://github.com/srio/COVID19/blob/master/figures/US_x2.png

New cases/deaths
----------------

.. image:: https://github.com/srio/COVID19/blob/master/figures/Spain_new_cases.png
.. image:: https://github.com/srio/COVID19/blob/master/figures/France_new_cases.png
.. image:: https://github.com/srio/COVID19/blob/master/figures/Italy_new_cases.png
.. image:: https://github.com/srio/COVID19/blob/master/figures/US_new_cases.png


Situation on 2020-04-05
-----------------------

.. image:: https://github.com/srio/COVID19/blob/master/figures/Spain_2020-04-05.png
.. image:: https://github.com/srio/COVID19/blob/master/figures/Italy_2020-04-05.png
.. image:: https://github.com/srio/COVID19/blob/master/figures/US_2020-04-05.png

Situation on 2020-04-04
-----------------------

.. image:: https://github.com/srio/COVID19/blob/master/figures/Spain_2020-04-04.png
.. image:: https://github.com/srio/COVID19/blob/master/figures/France_2020-04-04.png
.. image:: https://github.com/srio/COVID19/blob/master/figures/Italy_2020-04-04.png
.. image:: https://github.com/srio/COVID19/blob/master/figures/US_2020-04-04.png

Situation on 2020-04-03
-----------------------

.. image:: https://github.com/srio/COVID19/blob/master/figures/Spain_2020-04-03.png
.. image:: https://github.com/srio/COVID19/blob/master/figures/France_2020-04-03.png
.. image:: https://github.com/srio/COVID19/blob/master/figures/Italy_2020-04-03.png
.. image:: https://github.com/srio/COVID19/blob/master/figures/US_2020-04-03.png














