from basic_pitch import ICASSP_2022_MODEL_PATH
from basic_pitch.inference import Model, predict

from helper_function import fixing_duration, adjusting_notes
from send_data import sending_data

model = Model(ICASSP_2022_MODEL_PATH)

INPUT_SOURCE = "test/Not Pianika Bella Ciao OST Money Heist La Casa De Papel.mp3"
nada_dasar=60
model_output, midi_data, note_events = predict(INPUT_SOURCE, model)
note_events = [(item[0], item[1], item[2], round(item[3]*32767)) for item in note_events]
confidence = [item for item in note_events if ((item[2] - nada_dasar<= 24 and item[2] - nada_dasar >= 0) and (item[1] - item[0] > 0.3))]
basic_notes = [(item[0], item[1], item[2] - nada_dasar, item[3]) for item in confidence]
base_note = sorted(basic_notes, key=lambda x: x[0])
fix_duration = fixing_duration.non_negative(basic_notes)
data_to_send = adjusting_notes.adjust_notes(basic_notes)

print(data_to_send)