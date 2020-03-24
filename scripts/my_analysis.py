
import numpy
from srxraylib.plot.gol import set_qt, plot
import matplotlib.pylab as plt
from datetime import date
from scipy.optimize import curve_fit
set_qt()


urlCases = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
urlDeaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

def get_country(name="Spain",number_of_past_days=29):

     a = numpy.genfromtxt(urlCases,delimiter=' ,',dtype=str)
     b = numpy.genfromtxt(urlDeaths,delimiter=' ,',dtype=str)

     ifound = -1
     for i in range(len(a)):
          country1 = (a[i].split(","))[1]
          if country1 == name:
               ifound = i
               # break

     if ifound < 0:
          raise Exception("country key not found")

     spain=a[ifound].split(",")
     spainD=b[ifound].split(",")

     s = numpy.array(spain[-number_of_past_days:],dtype=float).copy()
     sD = numpy.array(spainD[-number_of_past_days:],dtype=float).copy()
     uptoday = numpy.linspace(-len(spain), 0, len(spain) + 1)
     t = uptoday[-number_of_past_days:]
     return t,s,sD

def italy_vs_spain():

     country1 = "Italy"
     country2 = "Spain"
     t1,c1,d1 = get_country(country1)
     t2,c2,d2 = get_country(country2)

     shift=7
     p=plot(t1,c1,
          t1,d1,
          t2-shift,c2,
          t2-shift,d2,
          xtitle="Days from today (%s)"%date.today(),
          legend=["Cases %s"%country1,"Deaths %s"%country1,
                  "Cases %s" % country2, "Deaths %s" % country2,],
          title="%s vs %s shifted by -%d"%(country1,country2,shift),
          ylog=1,
          marker=['o','o','x','x'],
          ytitle="cases/deaths",
          show=0)

     plt.grid(b=True,which="major")
     plt.grid(b=True,which="minor")
     filepng = "../figures/italy_vs_spain_%s.png"%date.today()
     plt.savefig(filepng)
     print("File %s written to file."%filepng)
     plt.show()



# italy_vs_spain()

def expo2(x,t0,a0):
     y4 = 2 ** (x / t0)

     y4 = y4 * a0

     return y4

def analyze_country(country1):
     # country1 = "Spain"
     t1,c1,d1 = get_country(country1)


     # t = t1
     # y4 = 2**(t/4)
     # y4 = y4 / y4[-1] * c1[-1]

     ndays=7
     poptC, pcov = curve_fit(expo2, t1[-ndays:], c1[-ndays:], p0=[3,c1[-1]])
     poptD, pcov = curve_fit(expo2, t1[-ndays:], d1[-ndays:], p0=[3,d1[-1]])

     print(">>>>>>>>",poptC,poptD)

     t11 = numpy.concatenate((t1,numpy.array([1,2])))

     todayC = expo2(0,poptC[0], poptC[1])
     todayD = expo2(0,poptD[0], poptD[1])
     tomorrowC = expo2(1,poptC[0], poptC[1])
     tomorrowD = expo2(1,poptD[0], poptD[1])


     plot(t1,c1,
          t1,d1,
          t11,expo2(t11,poptC[0],poptC[1]),
          t11,expo2(t11,poptD[0],poptD[1]),
          ylog=1,
          legend=["Cases","Deaths",
                  "Cases doble in %2.1f days"%poptC[0],"Deaths doble in %2.1f days"%poptD[0],],
          xtitle="Days from today (%s)" % date.today(),
          title="%s (%s): %d cases %d deaths, \n prediction tomorrow: %d cases (+%d) %d deaths (+%d)"%\
                (country1,date.today(),
                 todayC,todayD,
                 tomorrowC,tomorrowC-todayC,
                 tomorrowD,tomorrowD-todayD),
          ytitle="cases/deaths",
          linestyle=["solid","solid","dashed","dashed"],
          show=0)

     plt.grid(b=True, which="major")
     plt.grid(b=True, which="minor")
     filepng = "../figures/%s_%s.png" % (country1,date.today())
     plt.savefig(filepng)
     print("File %s written to file." % filepng)
     plt.show()

if __name__ == "__main__":
     italy_vs_spain()
     analyze_country("Spain")
     analyze_country("France")
     analyze_country("Italy")
     analyze_country("US")
     
