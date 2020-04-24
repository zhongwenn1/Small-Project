
# contains types and file name path
types = {'type2': ['C:/Users/wzhong/Documents/temp/logfiles/AnalogicStandaloneType2_20190620.log',
                   'C:/Users/wzhong/Documents/temp/logfiles/AnalogicStandaloneType2_20190621.log',
                   'C:/Users/wzhong/Documents/temp/logfiles/AnalogicStandaloneType2_20190622.log',
                   'C:/Users/wzhong/Documents/temp/logfiles/AnalogicStandaloneType2_20190623.log',
                   'C:/Users/wzhong/Documents/temp/logfiles/AnalogicStandaloneType2_20190624.log'],
         'type5': 'C:/Users/wzhong/Documents/temp/logfiles/AnalogicStandaloneType5_20200312.log',
         'test': 'C:/Users/wzhong/Documents/temp/2-4/files/runtime_.txt'}

beam_diff = {'type2': [0, 150],
             'type5': [-20, 150]}


type2 = {'linked': [0, 150],
         'slipping': [151, 200],
         'pushed': [-50, -1],
         'index': 4}

type5 = {'linked': [-20, 150],
         'slipping': [151, 200],
         'pushed': [-50, -1],
         'index': 5}


files = {'inWindow': 'in_window_logfile.csv',
         'machineDec': 'machine_decision_logfile.csv',
         'notInWindow': 'not_in_window_logfile.csv',
         'stopRunTime': 'runtime_.txt',
         'simulation': 'simulation delay.txt',
         'pattern': 'AnalogicStandaloneType'}
