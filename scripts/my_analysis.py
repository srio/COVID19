
import numpy
from srxraylib.plot.gol import set_qt, plot
import matplotlib.pylab as plt
from datetime import date
from scipy.optimize import curve_fit
set_qt()


urlCases = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
urlDeaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

def get_country(name="Spain",number_of_past_days=29,day=0):

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

     if day == 0:
         s = numpy.array(spain[(-number_of_past_days+day):],dtype=float).copy()
         sD = numpy.array(spainD[(-number_of_past_days+day):],dtype=float).copy()
     else:
         s = numpy.array(spain[(-number_of_past_days+day):day],dtype=float).copy()
         sD = numpy.array(spainD[(-number_of_past_days+day):day],dtype=float).copy()

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
     filepng = "../figures/italy_vs_spain.png"
     plt.savefig(filepng)
     print("File %s written to file."%filepng)
     plt.show()


def expo2(x,t0,a0):
     y4 = 2 ** (x / t0)
     y4 = y4 * a0
     return y4

def analyze_country(country1,day=0,do_plot=True):
     t1,c1,d1 = get_country(country1,day=day)

     ndays=7
     poptC, pcov = curve_fit(expo2, t1[-ndays:], c1[-ndays:], p0=[3,c1[-1]])
     poptD, pcov = curve_fit(expo2, t1[-ndays:], d1[-ndays:], p0=[3,d1[-1]])

     t11 = numpy.concatenate((t1,numpy.array([1,2])))


     todayC = c1[-1]
     todayD = d1[-1]
     yesterdayC = c1[-2]
     yesterdayD = d1[-2]
     tomorrowC = expo2(1,poptC[0], poptC[1])
     tomorrowD = expo2(1,poptD[0], poptD[1])

     if do_plot:
         plot(t1,c1,
              t1,d1,
              t11,expo2(t11,poptC[0],poptC[1]),
              t11,expo2(t11,poptD[0],poptD[1]),
              ylog=1,
              legend=["Cases","Deaths",
                      "Cases double in %2.1f days"%poptC[0],"Deaths double in %2.1f days"%poptD[0],],
              xtitle="Days from today (%s)" % date.today(),
              title="%s (%s): %d cases (+%d); %d (+%d) deaths, \n prediction tomorrow: +%d cases;  +%d deaths "%\
                    (country1,date.today(),
                     todayC,todayD,
                     todayC-yesterdayC, todayD-yesterdayD,
                     expo2(1,poptC[0], poptC[1])-expo2(0,poptC[0], poptC[1]),
                     expo2(1,poptD[0], poptD[1])-expo2(0,poptD[0], poptD[1])),
              ytitle="cases/deaths",
              linestyle=["solid","solid","dashed","dashed"],
              show=0)

         plt.grid(b=True, which="major")
         plt.grid(b=True, which="minor")
         filepng = "../figures/%s_%s.png" % (country1,date.today())
         plt.savefig(filepng)
         print("File %s written to file." % filepng)
         plt.show()

     return tomorrowC, tomorrowD, todayC, todayD, poptC[0], poptD[0]


def model_analysis(country1):


     print("day   tomorrowC    tomorrowD      todayC        todayD    real-prevision   real-prevision  coeC coeD")

     tomorrowC_old, tomorrowD_old, todayC_old, todayD_old = 0,0,0,0
     ndays = 15
     out = numpy.zeros((15,9))
     for i,day in enumerate(range(0,-ndays,-1)):
         tomorrowC, tomorrowD, todayC, todayD, poptC,poptD = analyze_country(country1,do_plot=False,day=day)
         print("%2d   %d         %d         %d      %d     %d    %d   %2.1f  %2.1f"%\
               (day,tomorrowC, tomorrowD, todayC, todayD,todayC_old-tomorrowC,todayD_old-tomorrowD,poptC,poptD))

         out[i,0] = day
         out[i,1] = tomorrowC
         out[i,2] = tomorrowD
         out[i,3] = todayC
         out[i,4] = todayD
         out[i,5] = poptC
         out[i,6] = poptD
         out[i,7] = todayC_old-tomorrowC
         out[i,8] = todayD_old-tomorrowD

         if i==0:
             out[i, 7] = numpy.nan
             out[i, 8] = numpy.nan

         tomorrowC_old, tomorrowD_old, todayC_old, todayD_old = tomorrowC, tomorrowD, todayC, todayD


     plot(out[:, 0]+1, out[:, 1],
          out[:, 0]+1, out[:, 2],
          out[:, 0], out[:, 3],
          out[:, 0], out[:, 4],
          legend=["Prevision Cases","Prevision Deaths","Cases","Deaths"],ylog=1,
          title=country1,
          xtitle="Days from today %s"%date.today(),
          yrange=[10**1,10**5],
          show=0)
     # plt.savefig(country1+"_1.png")
     plt.show()

     plot(out[:, 0], out[:, 5],
          out[:, 0], out[:, 6],
          legend=["Double-days Cases", "Double-days Deaths"],marker=['o','o'],
          title=country1,
          xtitle="Days from today %s" % date.today(),
          yrange=[1,9],
          show=0)
     plt.grid(True)
     filepng = "../figures/%s_x2.png"%country1
     plt.savefig(filepng)
     print("File %s written to disk"%filepng)
     plt.show()

     plot(out[:, 0], out[:, 7] / out[:, 3],
          out[:, 0], out[:, 8] / out[:, 4],
          legend=["Error Cases/Cases", "Error Deaths/Deaths"],marker=['o','o'],
          title=country1,
          xtitle="Days from today %s" % date.today(),
          yrange=[-0.75,0.75],
          show=0)
     # plt.savefig(country1+"_3.png")
     plt.show()

def new_cases(country1):
    t1, c1, d1 = get_country(country1, day=0, number_of_past_days=15)

    # plot(t1[1:], c1[1:]-c1[0:-1], t1[1:], d1[1:]-d1[0:-1],
    #      xtitle="Days from today %s" % date.today(),
    #      ytitle="Cases/deaths per day",
    #      title=country1,
    #      legend=["New cases","New deaths"])

    plt.bar(t1[1:], c1[1:]-c1[0:-1])
    plt.bar(t1[1:], d1[1:] - d1[0:-1], )
    plt.title(country1)
    plt.xlabel("Days from today %s" % date.today())
    plt.ylabel("Cases/deaths per day")
    plt.legend(labels=['Cases', 'Deaths'])
    # plt.grid(True)
    filepng = "../figures/%s_new_cases.png" % country1
    plt.savefig(filepng)
    print("File %s written to disk" % filepng)
    plt.show()



if __name__ == "__main__":


    for country1 in ["Spain","Italy","France","US"]:
        new_cases(country1)

    for country1 in ["Spain","Italy","France","US"]:
        analyze_country(country1)

    italy_vs_spain()

    for country1 in ["Spain","Italy","France","US"]:
        model_analysis(country1)
     
