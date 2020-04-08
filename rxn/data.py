
GASES = {"O2", "F2", "H2", "N2", "CO", "CO2", "H2O"}
GAS_RELEASE = {'O2', 'CO', 'CO2', 'H2O'}

# THERMODYNAMIC DATA COMPILED FROM BARIN THERMOCHEMICAL TABLES AND NBS THERMOCHEMICAL TABLES
ST = {"O2":  {0: 0, 298 : 0.3170 , 300 : 0.3192 , 400 : 0.4433 , 500 : 0.5718 , 600 : 0.7041 , 700 : 0.8396 ,
              800 : 0.9781 , 900 : 1.1190 , 1000 : 1.2623 , 1100 : 1.4075 , 1200 : 1.5547 , 1300 : 1.7036 ,
              1400 : 1.8541 , 1500 : 2.0060 , 1600 : 2.1594 , 1700 : 2.3141 , 1800 : 2.4700 , 1900 : 2.6271 ,
              2000 : 2.7854 },
      "H2":  {0: 0, 298: 0.2019, 300: 0.2034, 400: 0.2886, 500: 0.3776, 600: 0.4697, 700: 0.5645, 800: 0.6614,
              900: 0.7605, 1000: 0.8614, 1100: 0.9640, 1200: 1.0683, 1300: 1.1741, 1400: 1.2815, 1500: 1.3902,
              1600: 1.5003, 1700: 1.6116, 1800: 1.7242, 1900: 1.8380, 2000: 1.9528	},
      "CO":  {0: 0, 298 : 0.3054, 300 : 0.3076, 400 : 0.4275, 500 : 0.5515, 600 : 0.6788, 700 : 0.8092,
              800 : 0.9423, 900 : 1.0778, 1000 : 1.2155, 1100 : 1.3552, 1200 : 1.4967, 1300 : 1.6400, 1400 : 1.7848,
              1500 : 1.9311, 1600 : 2.0788, 1700 : 2.2277, 1800 : 2.3779, 1900 : 2.5291, 2000 : 2.6815 },
      "CO2": {0: 0, 298 : 0.2202, 300 : 0.2218, 400 : 0.3113, 500 : 0.4057, 600 : 0.5042, 700 : 0.6064, 800 : 0.7116,
              900 : 0.8197, 1000 : 0.9303, 1100 : 1.0432, 1200 : 1.1582, 1300 : 1.2751, 1400 : 1.3938, 1500 : 1.5141,
              1600 : 1.6360, 1700 : 1.7593, 1800 : 1.8839, 1900 : 2.0098, 2000 : 2.1369},
      "H2O": {0: 0, 298 : 0.1946, 300 : 0.1961, 400 : 0.2749, 500 : 0.3570, 600 : 0.4419, 700 : 0.5293, 800 : 0.6189,
              900 : 0.7107, 1000 : 0.8045, 1100 : 0.9001, 1200 : 0.9975, 1300 : 1.0966, 1400 : 1.1972, 1500 : 1.2994,
              1600 : 1.4030, 1700 : 1.5079, 1800 : 1.6142, 1900 : 1.7216, 2000 : 1.8303 }
      }

H = {"CO": -0.5897, "CO2": -1.3583, "H2O": -0.82547}

DEFAULT_GAS_PRESSURES = {'O2': 0.2095, 'CO2': 0.000394737, 'N2': 0.7809, 'H2': 0.1, 'H2O': 0.1, 'F2': 0.1}

