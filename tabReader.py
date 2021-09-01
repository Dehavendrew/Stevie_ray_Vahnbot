import guitarpro
import numpy as np
song = guitarpro.parse('stevieTabs/Stevie Ray Vaughan - Rude Mood.gp3')
#song = guitarpro.parse('test2.gp5')

print(song.title)
#
# for track in song.tracks:
#     if len(track.strings) == 6:
#         print(track.name)
#         for measure in track.measures:
#             #print(vars(measure))
#             for voice in measure.voices:
#                 #print(voice)
#                 #print(vars(voice))
#                 for beat in voice.beats:
#                     print(vars(beat))
#                     for note in beat.notes:
#                         pass
#                         #print(vars(note))
#                         #print(note.value, note.durationPercent, note.velocity, note.effect)


measures = []

for track in song.tracks:

    if len(track.strings) == 6:
        print(track.name)
        for m in range(len(track.measures)):
            print(m)
            measure = track.measures[m]
            voice = measure.voices[0]

            print(vars(voice))

            noteBlock = np.ones((len(voice.beats),6,2), dtype=np.int8) * -2
            for i in range(len(voice.beats)):
                for note in voice.beats[i].notes:
                    #print(vars(note))
                    if(note.type==guitarpro.models.NoteType.dead):
                        noteBlock[i,note.string - 1,0] = -1
                        noteBlock[i,note.string - 1,1] = note.velocity
                    else:
                        noteBlock[i,note.string - 1,0] = note.value
                        noteBlock[i,note.string - 1,1] = note.velocity
                #print(vars(beat))
            measures.append(noteBlock)



print(measures)
new_song = guitarpro.models.Song()

new_song.tracks[0].useRSE = True

time = 960
for m in range(len(measures)):
    print(m)
    print(new_song.tracks[0].measures)
    beat2 = guitarpro.models.Beat(new_song.tracks[0].measures[m].voices[0], start=960)
    new_song.tracks[0].measures[m].voices[1].beats.append(beat2)

    for j in range(measures[m].shape[0]):
        durat = guitarpro.models.Duration(value=8)
        rest = True
        for i in range(6):
            if measures[m][j,i,0] != -2:
                rest = False
        if rest:
            beat = guitarpro.models.Beat(new_song.tracks[0].measures[m].voices[0], start=time, duration=durat, status=guitarpro.models.BeatStatus.rest)
        else:
            beat = guitarpro.models.Beat(new_song.tracks[0].measures[m].voices[0], start=time, duration=durat, status=guitarpro.models.BeatStatus.normal)


        new_song.tracks[0].measures[m].voices[0].beats.append(beat)
        #print(vars(beat))
        for i in range(6):
            val = measures[m][j,i,0]
            velo = measures[m][j,i,1]
            if val == -2:
                continue
            if val == -1:
                note = guitarpro.models.Note(new_song.tracks[0].measures[m].voices[0].beats[j], value=0, string=i + 1, velocity=velo, type=guitarpro.models.NoteType.dead)
                new_song.tracks[0].measures[m].voices[0].beats[j].notes.append(note)
            else:
                print(j, len(new_song.tracks[0].measures[m].voices[0].beats))
                note = guitarpro.models.Note(new_song.tracks[0].measures[m].voices[0].beats[j], value=val, string=i + 1,velocity=velo, type=guitarpro.models.NoteType.normal)
                new_song.tracks[0].measures[m].voices[0].beats[j].notes.append(note)
        time = time + 480

    head = guitarpro.models.MeasureHeader(number = m + 1)
    meas = guitarpro.models.Measure(new_song.tracks[0], header=head)


    voc = guitarpro.models.Voice(meas)
    new_song.tracks[0].measures.append(meas)
    new_song.tracks[0].measures[m + 1].voices.append(voc)

for track in new_song.tracks:
    #print(vars(track))
    for measure in track.measures:
        for voice in measure.voices:
            for beat in voice.beats:
                pass
                #print(beat)

# for track in new_song.tracks:
#     if len(track.strings) == 6:
#         print(track.name)
#         for measure in track.measures:
#             #print(vars(measure))
#             for voice in measure.voices:
#                 #print(vars(voice))
#                 for beat in voice.beats:
#                     print(vars(beat))
#                     #print(beat.duration, beat.effect)
#                     for note in beat.notes:
#                         pass
#                         #print(vars(note))
#                         #print(note.value, note.durationPercent, note.velocity, note.effect)




guitarpro.write(new_song, "Test.gp5")
