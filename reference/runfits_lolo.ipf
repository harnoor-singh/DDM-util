#pragma rtGlobals=3		// Use modern global access method and strict wave access.
#include <KBColorizeTraces>

Function ApplyColorTableToTopGraph(ctabname)
	String ctabname

	String graphName = WinName(0, 1)
	if (strlen(graphName) == 0)
		return -1
	endif

	Variable numTraces = ItemsInList(TraceNameList(graphName,";",3))

	if (numTraces <= 0)
		return -1
	endif
	
	Variable denominator= numTraces-1
	if( denominator < 1 )
		denominator= 1    // avoid divide by zero, use just the first color for 1 trace
	endif

	ColorTab2Wave $ctabname	// creates M_colors
	Wave M_colors
	Variable numRows= DimSize(M_colors,0)
	Variable red, green, blue
	Variable i, index
	for(i=0; i<numTraces; i+=1)
		index = round(i/denominator * (numRows-1))	// spread entire color range over all traces.
		ModifyGraph/W=$graphName rgb[i]=(M_colors[index][0], M_colors[index][1], M_colors[index][2])
	endfor
	return 0
End

Function biexp(w,t) : FitFunc
	Wave w
	Variable t

	//CurveFitDialog/ These comments were created by the Curve Fitting dialog. Altering them will
	//CurveFitDialog/ make the function less convenient to work with in the Curve Fitting dialog.
	//CurveFitDialog/ Equation:
	//CurveFitDialog/ f(t) = a*(p*exp(-t/T1) + (1 - p)*exp(-t/T2)) + y0
	//CurveFitDialog/ End of Equation
	//CurveFitDialog/ Independent Variables 1
	//CurveFitDialog/ t
	//CurveFitDialog/ Coefficients 5
	//CurveFitDialog/ w[0] = y0
	//CurveFitDialog/ w[1] = a
	//CurveFitDialog/ w[2] = T1
	//CurveFitDialog/ w[3] = T2
	//CurveFitDialog/ w[4] = p

	return w[1]*(w[4]*exp(-t/w[2]) + (1 - w[4])*exp(-t/w[3])) + w[0]
End


Function monoexpraw(w,t) : FitFunc
	Wave w
	Variable t

	//CurveFitDialog/ These comments were created by the Curve Fitting dialog. Altering them will
	//CurveFitDialog/ make the function less convenient to work with in the Curve Fitting dialog.
	//CurveFitDialog/ Equation:
	//CurveFitDialog/ f(t) = y0*(1 - sqrt(a*a)*exp(-t/T1))
	//CurveFitDialog/ End of Equation
	//CurveFitDialog/ Independent Variables 1
	//CurveFitDialog/ t
	//CurveFitDialog/ Coefficients 3
	//CurveFitDialog/ w[0] = y0
	//CurveFitDialog/ w[1] = a
	//CurveFitDialog/ w[2] = T1

	return w[0]*(1 - sqrt(w[1]*w[1])*exp(-t/w[2]))
End

Function WaterVisc(T_integer)
	Variable T_integer
	//source: https://wiki.anton-paar.com/en/water/
	make/N=41/O viscarr={0,0,1.6735,1.619,1.5673,1.5182,1.4715,1.4271,1.3847,1.3444,1.3059,1.2692,1.234,1.2005,1.1683,1.1375,1.1081,1.0798,1.0526,1.0266,1.0016,0.9775,0.9544,0.9321,0.9107,0.89,0.8701,0.8509,0.8324,0.8145,0.7972,0.7805,0.7644,0.7488,0.7337,0.7191,0.705,0.6913,0.678,0.6652,0.6527}
	//print viscarr[T_integer]
	return viscarr[T_integer]
End

Function CalcDiameter(diff,errdiff)
	Variable diff, errdiff	//um^2/s
	Variable eta_w, T, T_inCelsius, kB
	Variable  Rh, errRh	
	diff*=1e-12	//mks
	errdiff*=1e-12
	kB = 1.3806503e-23
	T_inCelsius = 24
	T = 273.15 + T_inCelsius
	eta_w = WaterVisc(T_inCelsius)//0.9107//1.0016 at 20C, 0.9107 at 24C, 0.89 at 25C, 0.7972 at 30C
	//eta_w=2.1
	eta_w/=1000
	Rh = kB*T/(6*pi*eta_w*diff)
	//error bars
	errRh = Rh*(errdiff/diff)
	//print "Diffusion coefficient in m^2/s", diff
	print "Rh in nanometers", Rh*1e9, "particle diameter in nm", 2*Rh*1e9, "+/-", 2*errRh*1e9
	return 2*Rh*1e9
End

Function biexpraw(w,t) : FitFunc
	Wave w
	Variable t

	//CurveFitDialog/ These comments were created by the Curve Fitting dialog. Altering them will
	//CurveFitDialog/ make the function less convenient to work with in the Curve Fitting dialog.
	//CurveFitDialog/ Equation:
	//CurveFitDialog/ f(t) = y0*(1 - sqrt(a*a)*(p*exp(-t/T1) + (1 - p)*exp(-t/T2)))
	//CurveFitDialog/ End of Equation
	//CurveFitDialog/ Independent Variables 1
	//CurveFitDialog/ t
	//CurveFitDialog/ Coefficients 5
	//CurveFitDialog/ w[0] = y0
	//CurveFitDialog/ w[1] = a
	//CurveFitDialog/ w[2] = T1
	//CurveFitDialog/ w[3] = T2
	//CurveFitDialog/ w[4] = p

	return w[0]*(1 - sqrt(w[1]*w[1])*(w[4]*exp(-t/w[2]) + (1 - w[4])*exp(-t/w[3])))
End

Macro DisplayandRenameWaves()

variable i=1, imax=128
string basename,newname, oldname
basename = "PS60 63X 40sec a"//"PS200_white2_2000frames_23p5s_reg02_"
Rename wave0, $(basename + "0")
do
	oldname = "wave" + num2str(i)
	newname = basename + num2str(i)
	Rename $(oldname) $(newname)
	if(5*floor(i/5)==i)
		if(i == 5)
			Display $(newname) vs $(basename + "0")
		else
			AppendtoGraph $(newname) vs $(basename + "0")
		endif
		ModifyGraph log(bottom)=1
	endif
	i+=1
while(i <= imax)
End

Macro runrawfits()
Silent 1

variable i, ibegin, iend
Variable halfboxsize=225//64//240
variable imax = 100//200
string wname = "PS60 63X 40sec a"//"PS200_white2_2000frames_23p5s_reg02_" //default is "wave"
iend = 45//85//32//70//50 //imax
ibegin = 5//3//10//4 //0
i = ibegin
//identify the plateau region, and set these values
variable p_begin = 30//29//46//41//45
variable p_end = 50//40//43//65//60//80

//fitting parameters
//Make/D/N=5/O W_coef, W2_coef
Make/D/N=3/O W_coef
variable freq=1// already done this in DDM_stack.py//10620/40//9731/40.
variable micron_per_pixel = 6.5/63//0.023255// 6.5/63 
variable aguess =0.8, pguess=0.95
variable T1guess = 1/freq, T2guess
string sig, fit //, inv

T2guess=5*T1guess
//W_coef[0] = 0; W_coef[1] = aguess; W_coef[2] = T1guess; W_coef[3] = T2guess; W_coef[4] = pguess
Make/O/N=(imax) q_arr, a_arr=Nan, tau1_arr=Nan//, tau2_arr=Nan, p_arr=Nan
Make/O/N=(imax) errinvtau1_arr=Nan//, errinvtau2_arr=Nan
Make/O/T/N=2 T_Constraints
//define q based on the experiment
//q_arr=0.5*(x+1)/200			//in units of inverse pixels
q_arr=2*pi*0.5*(x+1)/halfboxsize/micron_per_pixel
//run one fit manually, print W_coef, and override the above defaults
sig = wname +num2str(0)
duplicate/O $sig delta_t
delta_t = $sig/freq
//delta_t = wave0/freq //units of seconds, needed if not done in DDM code
do
	//sig = "wave" +num2str(i)
	sig = wname +num2str(i)
	//sig2 = "wav2_" + num2str(i)
	//inv = "inv" + num2str(i)
	fit = "fit_" + sig
	//duplicate/O $sig $inv
	WaveStats/Q/R=[p_begin,p_end] $sig
	//$inv = 1 - $sig/V_max
	//W_coef=W2_coef 		//use initial guess for all waves
	if (i == ibegin)
		display $sig vs delta_t; 
		ModifyGraph log = 1; ModifyGraph width=500,height={Aspect,0.66}
		ModifyGraph mode($sig)=3, marker($sig) =8; SetAxis left 10,50; SetAxis left 10,1000
		DoWindow/C grafitraw4
		//T_Constraints[0] = {"K4 > 0","K4 < 1"}
		FuncFit/Q/H="000"/NTHR=0 monoexpraw W_coef  $sig[0,p_end] /X=delta_t /D ///C=T_Constraints 
		ModifyGraph mode($fit)=0
	else
		appendtograph $sig vs delta_t
		//T_Constraints[0] = {"K4 > 0","K4 < 1"}
		//FuncFit/Q/H="00011"/NTHR=0 monoexpraw W_coef  $sig[0,p_end] /X=delta_t /D ///C=T_Constraints 
		FuncFit/Q/H="00011"/NTHR=0 monoexpraw W_coef  $sig[0,p_end] /X=delta_t /D ///C=T_Constraints 
		if (i == 3*floor(i/3.))
			ModifyGraph mode($sig)=3, marker($sig) =8
			ModifyGraph mode($fit)=0
		else
			RemoveFromGraph $sig, $fit
		endif
	endif
	SetAxis/A
	a_arr[i] = W_coef[1]
	tau1_arr[i] = W_coef[2]
	errinvtau1_arr[i]=abs(W_sigma[2]/W_coef[2])
	//tau2_arr[i] = W_coef[3]
	//errinvtau2_arr[i]=abs(W_sigma[3]/W_coef[3])
	//p_arr[i] = W_coef[4]
	sleep/s 0.1
	i+=1
while (i < iend)	
//calculate quantities for final graph
	duplicate/o tau1_arr inv_tau1_arr; inv_tau1_arr= 1/tau1_arr
	//duplicate/o tau2_arr inv_tau2_arr; inv_tau2_arr= 1/tau2_arr
	duplicate/o q_arr qsqd_arr; qsqd_arr=q_arr^2
	errinvtau1_arr*=inv_tau1_arr
	//errinvtau2_arr*=inv_tau2_arr
//display settings
ApplyColorTableToTopGraph("ColdWarm")
//display a_arr vs q_arr
//display tau1_arr vs q_arr; appendtograph tau2_arr vs q_arr
//display p_arr vs q_arr
//Edit q_arr,a_arr,tau1_arr,tau2_arr,p_arr
//appendtotable inv_tau1_arr, errinvtau1_arr, inv_tau2_arr, errinvtau2_arr, qsqd_arr
//DisplayFinalGraph()
End

Macro RenameOutputWaves()
string addstr = "_e"
Rename a_arr, $("a_arr" + addstr)
Rename delta_t,$("delta_t" + addstr)
Rename errinvtau1_arr, $("errinvtau1_arr" + addstr)
Rename errinvtau2_arr,$("errinvtau2_arr" + addstr)
Rename inv_tau1_arr,$("inv_tau1_arr" + addstr)
Rename inv_tau2_arr,$("inv_tau2_arr" + addstr)
Rename p_arr,$("p_arr"+ addstr)
Rename qsqd_arr,$("qsqd_arr"+ addstr)
Rename q_arr,$("q_arr"+ addstr)
Rename tau1_arr,$("tau1_arr"+ addstr)
Rename tau2_arr,$("tau2_arr"+ addstr)

Macro DisplayFinalGraph()


Variable invtau_max	
	Wavestats inv_tau1_arr
	invtau_max = 10*ceil(V_max/10)
	display inv_tau1_arr vs qsqd_arr; //appendtograph  inv_tau2_arr vs qsqd_arr; ShowInfo
	ModifyGraph mode=3,marker=19,rgb(inv_tau1_arr)=(0,0,0)
	SetAxis left 0.001,invtau_max; SetAxis bottom 0.001,100
	ModifyGraph width=340.157,height={Aspect,1}; 
	Label left "\\Z18τ\\S-1\\M\\F'Arial'\\Z18 (1/s)"
	//Label left "\Z18\F'Symbol't\S-1\M\F'Arial'\Z18 (1/s)"; Label bottom "\\f00\\Z18\\F'Arial'q\\S2\\M\\Z18(\\F'Symbol'm\\F'Arial'm\\S-2\\M\\Z18)"
	Label bottom "\\f00\\Z18\\F'Arial'q\\S2\\M\\Z18(μm\\S-2\\M\\Z18)"
	ErrorBars inv_tau1_arr Y,wave=(errinvtau1_arr,errinvtau1_arr)
	//ErrorBars inv_tau2_arr Y,wave=(errinvtau2_arr,errinvtau2_arr)
End

Macro runfitsnorm()
Silent 1

variable i, ibegin, iend
variable imax = 128//200
iend = 40//70//50 //imax
ibegin = 10//10//4 //0
i = ibegin
// clean up
//KillWindow grafit

//identify the plateau region, and set these values
variable p_begin = 51//41//45
variable p_end = 65//60//80

//fitting parameters
Make/D/N=5/O W2_coef, W_coef
variable freq=1// already done this in DDM_stack.py//10620/40//9731/40.
variable micron_per_pixel = 0.85/14.67//6.5/63 
variable aguess =0.8, pguess=0.95
variable T1guess = 1/freq, T2guess
T2guess=5*T1guess
W_coef[0] = 0; W_coef[1] = aguess; W_coef[2] = T1guess; W_coef[3] = T2guess; W_coef[4] = pguess
Make/O/N=(imax) q_arr, a_arr=Nan, tau1_arr=Nan, tau2_arr=Nan, p_arr=Nan
Make/O/T/N=2 T_Constraints
//define q based on the experiment
//q_arr=0.5*(x+1)/200			//in units of inverse pixels
q_arr=2*pi*0.5*(x+1)/halfboxsize/micron_per_pixel
//run one fit manually, print W_coef, and override the above defaults
//W_coef= {0,0.446376,0.151746,1.53018,0.791045}
//W_coef= {0,0.844,0.049,0.58,0.35}
//W_coef={0,0.38,0.08,1.2, 0.62}
//W_coef={0,0.45,0.1,1.2,0.65}
//W_coef={0,0.54,0.08,1.3,0.45}
//W_coef={0,0.9,0.25,1.0,0.95}
W2_coef={0,0.69,0.01,0.13,0.25}
 
  //
string sig, inv, fit
duplicate/O wave0 delta_t
delta_t = wave0/freq
//delta_t = wave0/freq //units of seconds, needed if not done in DDM code
do
	sig = "wave" +num2str(i)
	//sig2 = "wav2_" + num2str(i)
	inv = "inv" + num2str(i)
	fit = "fit_" + inv
	duplicate/O $sig $inv
	WaveStats/Q/R=[p_begin,p_end] $sig
	$inv = 1 - $sig/V_max
	//W_coef=W2_coef
	if (i == ibegin)
		W_coef=W2_coef
		display $inv vs delta_t
		ModifyGraph log = 1; ModifyGraph width=500,height={Aspect,0.66}
		ModifyGraph mode($inv)=3, marker($inv) =8; SetAxis left 1e-04,1.1
		DoWindow/C grafit5
		T_Constraints[0] = {"K4 > 0","K4 < 1"}
		FuncFit/Q/H="10000"/NTHR=0 biexp W_coef  $inv[0,p_end] /X=delta_t /D /C=T_Constraints 
		ModifyGraph mode($fit)=0
	else
		appendtograph $inv vs delta_t
		T_Constraints[0] = {"K4 > 0","K4 < 1"}
		FuncFit/Q/H="10000"/NTHR=0 biexp W_coef  $inv[0,p_end] /X=delta_t /D /C=T_Constraints 
		if (i == 5*floor(i/5.))
			ModifyGraph mode($inv)=3, marker($inv) =8
			ModifyGraph mode($fit)=0
		else
			RemoveFromGraph $inv, $fit
		endif
	endif
	a_arr[i] = W_coef[1]*W_coef[0]
	tau1_arr[i] = W_coef[2]
	tau2_arr[i] = W_coef[3]
	p_arr[i] = W_coef[4]
	sleep/s 0.3
	i+=1
while (i < iend)	
//display settings
ApplyColorTableToTopGraph("ColdWarm")
//display a_arr vs q_arr
//display tau1_arr vs q_arr; appendtograph tau2_arr vs q_arr
//display p_arr vs q_arr
//Edit q_arr,a_arr,tau1_arr,tau2_arr,p_arr
//DisplayFinalGraph()
End


Macro testfit()
Variable i=1, imax=60
String str0=""
make/O/N=(imax) AA
display test0; //SetAxis left 0,1.5
do
	str0 = num2str(i)
	test0 = $("wave" + str0); Wavestats/Q test0; test0/=V_max
	WaveStats/Q/R=[20,35] test0; test0/=V_max
	AA[i] = V_max	
	Sleep/S 1	
	print i
	i+=2
while(i < imax)
//display AA vs q_arr
End

Macro RenameWaves()
variable ibegin=0, i
variable iend=240
string sig, sig2
i = ibegin
do
	sig2 = "wave" +num2str(i)
	sig = "PS0p49_green_reg01_" + num2str(i)
//	inv = "inv" + num2str(i)
//	inv2 = "inv256a2" + num2str(i)
	print sig, sig2
	rename $sig, $sig2
//	rename $inv, $inv2
	i+=1
while(i < iend)

End

Macro RescaleWaves()
variable, i=1, iend=128
//i=130;iend=257
string sig
	do
		sig = "wave" +num2str(i)
		$sig /= 1e10
		i +=1
	while (i <= iend)	
	
End

