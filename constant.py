import numpy as np

si_ability = [0.12404439355108413, 0.2924749852195381, 0.6273255944092082, 0.5872160267629065, 0.36279514420134534,
              0.38752683367941704, 0.5298506762490425, 0.3695002883810033, 0.05745553220095449, 0.2012815051373862,
              0.6320905130034038, 0.45692974966724925, 0.0, 0.5993554655626938, 0.6059474994052593, 0.23348393408691423,
              0.5827101685905265, 0.6873859803117867, 0.6053710021529646, 0.2902943262585678, 0.34484560141783654,
              0.447512600887913, 0.37214398475297683, 0.3939773318217345, 0.3650801548852223, 0.2662674378710574,
              0.41500139462115315, 0.6294776706587127, 0.5264451852738044, 0.29778439925655403, 0.4365943218393177,
              0.46465812302236953, 0.6881853479565414, 0.33382666153719065, 0.47050643987541246, 0.5943102245977125,
              0.3855727565015592, 0.4713468995387961, 0.3283709790787016, 0.3919289278047941, 0.7384682862452697,
              0.45186437979287447, 0.8081923388712169, 0.49018599094551063, 0.08050845114726717, 0.6719618856914068,
              0.3937518184077501, 0.4573482920734295, 0.34415658079868433, 0.8831706804438464, 0.6290341758171156,
              0.42012398736372597, 0.7169136343675286, 0.13905551946546246, 0.46524151997545377, 0.47432668834127384,
              0.6012773210385776, 0.41237720689674284, 0.6320758419631968, 0.9680696885646034, 0.745108196655414,
              0.39167885610702163, 0.19338191264337468, 0.4604068543634966, 0.8809821326077418, 1.0, 0.4125001070124247,
              0.36179036059490494, 0.10979398586857596, 0.5107719329766204, 0.4876769335376264, 0.32770447820225435,
              0.6665929606344732, 0.6258078673077618, 0.6246245583892479, 0.8493827569728569, 0.5854447910971603,
              0.03410575294225908, 0.07127388796953085, 0.9029031065925074, 0.6140564749229892, 0.6110051430078786,
              0.29901319954970657, 0.7649338429157049, 0.6552020429342729, 0.4224547839508524, 0.4208870239192877,
              0.23596201339170167, 0.47250995422660685, 0.2566056948313268, 0.6488415288955522, 0.1950586644492456,
              0.37370843774358403, 0.7740615738511644, 0.6579864280720422, 0.32808307867845804, 0.4400968038118285,
              0.38107173782574794, 0.39659334138475644, 0.10111781913481499]

# 工人的真实个人能力

# co_ability = [1.915266613333476, 2.3339695931052225, 3.542867169321302, -1.0139880627014133, 1.083943835659414, 0.2222255509956622, 0.4164984720114431, 1.6428710867933103, 1.934096249512415, 1.187709254137948, -0.5413287843332606, -0.6092362483042026, 1.4694023404344714, 0.5673575163375425, -0.3764683517057985, 1.902397221149269, 1.1093191719077442, 0.2706262878107323, 1.3561585941995837, 3.2050019374795653, 0.3814892318058596, 0.5430463748661486, -0.29519463935690426, -0.142554577109403, -0.8471551127187258, 1.5279570458183243, -0.20133245683934997, 0.6658469646585563, 1.998837699682435, 2.458767268941849, -0.22618764568770944, 0.005572195388371393, 0.33621017519282836, 1.1492180109881354, 0.882948450884381, 0.45664452474714234, 1.4748975709987546, 1.9647999792516986, 1.282078609987961, 2.4374827576616793, 1.0953224588215176, 1.8114337890250067, 2.770299749854451, -0.6158034736798961, 2.6024506937428846, 1.2033113962181998, 1.897509257912271, 2.594292018917726, 0.9123532259676446, 1.2738643773325213, 0.39141610787798475, 1.2193071482165432, -0.1031205816136107, -0.5171264772673458, 1.4241445607407188, 0.9418338500981162, 0.7842209834371391, 2.2585379338199614, -0.5038005000974497, 1.7532135368605304, 1.9482775871294218, 0.1886826757820118, 1.2354836407623926, 1.3537265098907465, 1.744987951909939, 2.246186868385748, 1.012946776998573, 0.8143708403932206, 1.2695449888888053, 1.1015211799312359, -0.2595600060807435, 0.39711020726937174, -0.3994688446836636, 0.07698148885465106, 0.7107263461387421, 0.6570696269809597, 3.41341984054521, 0.6812295136313202, 1.5392976243287777, 0.7697821241269585, 1.5899988392589117, 2.143443725526839, 1.570803633531913, 1.3395250554807194, -0.431652781007674, 1.2794047199671994, 0.697885661798648, 0.6414268891790615, 1.9206302739752203, 1.0818632091392733, 1.9084237964633126, 0.8909153928729983, -1.3537934713304645, 0.4127246543768921, 0.48559409780366936, 2.3332515659776876, 0.840687506705823, 1.2758989094068924, 0.5811077489961602, -0.3761783017981426]
co_ability = [0.4086887203030975, 2.956855651844556, 2.796317522976212, 0.5999866725775841, 0.11206195545755902,
              1.6465394816471797, 0.2816231574273841, 0.5160199622550448, 1.0308369401070527, 0.703159606947294,
              0.2882930776796865, 1.9576662413678685, 0.5347474534005484, 0.11888361298357632, 0.6130846503551768,
              1.1709491018606908, 0.3828081949483261, 9.87867234609066, 0.6700421680409605, 0.7091503259885353,
              0.39547153485868475, 0.5482484808592786, 0.6926678269473857, 0.8778054654361442, 0.3231953147961451,
              0.23019824781342693, 1.153625829093327, 1.3492410676868818, 2.2613118068999465, 1.093847132864601,
              1.160068102116186, 0.35764310464778143, 0.172374734133921, 0.6548503413179799, 0.9813160682506273,
              2.9763809970793607, 1.066735034568483, 0.36594600279213635, 0.4129718275978048, 1.2816222837315847,
              0.7163037576195689, 0.39980290706199, 0.8466517129434364, 0.43625867336320745, 1.6501095109233577,
              0.2760372311375777, 2.918476789451282, 7.821186213040928, 1.1070485673839447, 0.1783252076686486,
              0.3114322311675599, 0.20930952371063932, 0.378905749342928, 0.6774133618301592, 0.6178811971800865,
              1.12413646252708, 0.20671543049819974, 0.9828020415762497, 0.7499054016189585, 3.2037480358681747,
              0.21792605147809904, 0.18168774077127975, 0.5375446053066956, 0.18715682633312, 1.1824186614702494,
              0.15447716008928425, 0.2512909178446912, 0.7328870048420083, 0.3046186460954641, 0.9623787340497062,
              1.0312861210778308, 0.11634188929585182, 2.407138859177722, 0.784915789954388, 1.47423916770169,
              0.29202308487369527, 0.7741644128474753, 0.11743625537588405, 1.1439383310223492, 0.3362590746832703,
              0.23671431208422847, 0.5382383256698684, 0.13816017875951767, 3.4271585629457357, 2.2561345945332563,
              1.087937427822521, 0.9824797011891864, 0.4892082534224963, 0.9302734671542158, 0.15881047385306973,
              1.2132954303677987, 0.26690730022667575, 2.4692547333660353, 3.240360728578718, 0.5308099234034848,
              3.789733519585693, 0.34548268539798416, 2.5991181524976468, 0.3094890045156665, 1.359456673350892]

# 工人的真实协作能力

num_of_system = 100
co_ability_var = float(np.var(co_ability))
si_ability_var = float(np.var(si_ability))
