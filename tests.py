#Exercise the MTK Command Script
from __future__ import print_function
import mtk

# Static Sentences
print('Set Default Sentence Updating:', mtk.default_sentences)
print('Do a Hot Start:', mtk.hot_start)
print('Do a Warm Start:', mtk.warm_start)
print('Do a cold start:', mtk.cold_start)
print('Do a full reset and cold start:', mtk.full_cold_start)
print('Go into Standby:', mtk.standby)

# Baudrate Sentences
print('Valid Baudrate Strings')
for test in mtk.__valid_baudrates:
    test_string = mtk.update_baudrate(test)
    print('Baudrate:', test)
    print('Required String:', test_string)

nmea_rates = [1.0, 5.0, 10.0, 3.5]
for rate in nmea_rates:
    nmea_sentence = mtk.update_nmea_rate(rate)
    print(nmea_sentence)

enable_string = mtk.update_sentences(gsv_int=5)
print(enable_string)
