#from music21 import clef, converter, stream, note, chord, metadata, dynamics, spanner, environment
from music21 import *

def extract_measures_with_detailed_notes(file_path):
    measure_data = []
    score = converter.parse(file_path)
    parts = score.parts
    first_part = parts[0]

    ts_changes,ks_changes = detect_signature_changes(first_part)
    measures = list(first_part.getElementsByClass(stream.Measure))

    title = score.metadata.title if score.metadata and score.metadata.title else "Unknown Title"
    slurs = first_part.spannerBundle.getByClass(spanner.Slur)

    key_sig = score.recurse().getElementsByClass('KeySignature').first()
    time_sig = score.recurse().getElementsByClass('TimeSignature').first()

    key_str = key_sig.asKey().name if key_sig else None
    time_str = time_sig.ratioString if time_sig else None

    for i, m in enumerate(measures, start=1):
        meas = '<h3>Measure ' + str(i) +'</h3>'
        exp_str = get_text_in_measure(m)
        if exp_str != '':
            meas += '<p>'+ exp_str + '</p>'
        # Get any dynamic Symbols in the measure
        measure_dynamics = m.recurse().getElementsByClass(dynamics.Dynamic)
        for dyn in measure_dynamics:
            meas += '<p>Dynamic: ' + str(dyn.value) + '</p>'
        dynamic_spanners = [s for s in m.getSpannerSites() if isinstance(s, (spanner.Crescendo, spanner.Diminuendo))]
        
        has_repeat,rep_str = check_repeats_in_measure(m)
        if has_repeat:
            meas += '<p>' + rep_str + '</p>'

        for el in m.notesAndRests:
            if isinstance(el, note.Note):
                pitch = el.pitch
                duration = el.quarterLength
                note_type = el.duration.type

                #Check Ties
                tie = "Tie: " + el.tie.type if el.tie else ""
                
                #Check Articulations
                ats = ''
                if el.articulations:
                    for art in el.articulations:
                        ats += f"{art.classes[0]} " #({type(art).__name__}) "


                #Check Dynamics
                active_dynamics = []
                dyn_str = ''
                for dyn in dynamic_spanners:
                    if el in dyn:
                        active_dynamics.append(dyn)

                for dyn in active_dynamics:
                    kind = "Crescendo" if isinstance(dyn, spanner.Crescendo) else "Diminuendo"
                    start_note = dyn.getFirst()
                    end_note = dyn.getLast()

                    if el is start_note:
                        dyn_str += f"{kind} Start"
                        print('asdf')
                    elif el is end_note:
                        dyn_str += f"{kind} End"
                    else:
                        dyn_str += f"{kind} Continue"
                        print('asdf')
                
                #Check Slurs
                slur_data = ''
                for slur in slurs:
                    if el in slur:
                        if el is slur.getFirst():
                            slur_data += f"Start Slur"
                        elif el is slur.getLast():
                            slur_data += f"Stop Slur"
                        else:
                            slur_data += f"Continue Slur"

                meas += f"<p>Note: {pitch}, Type: {note_type}, Duration: {duration}, {tie} {slur_data} {ats} {dyn_str}</p>"

            elif isinstance(el, chord.Chord):
                pitches = ', '.join(str(p) for p in el.pitches)
                note_type = el.duration.type
                meas += f"<p>Chord: [{pitches}], Type: {note_type}, Duration: {el.quarterLength}, {ats} {dyn_str}</p>"

            elif el.isRest:
                note_type = el.duration.type
                meas+= f"<p>Rest: Type: {note_type}, Duration: {el.quarterLength}</p>"
        measure_data.append(meas)
    return measure_data, key_str, time_str, title, ts_changes, ks_changes

def check_repeats_in_measure(measure):
    repeat_found = False
    repeat_str = 'Repeat At '
    # Check for left (start) barline
    if measure.leftBarline and isinstance(measure.leftBarline, bar.Repeat):
        if measure.leftBarline.direction == 'start':
            repeat_str += f"Start, "
            repeat_found = True

    # Check for right (end) barline
    if measure.rightBarline and isinstance(measure.rightBarline, bar.Repeat):
        if measure.rightBarline.direction == 'end':
            repeat_str += f"End, "
            repeat_found = True
 
    return repeat_found, repeat_str

def get_text_in_measure(measure):
    exp_str = ''
    for el in measure.recurse():
        if isinstance(el, expressions.Expression):
            exp_str += f" Expression: '{el}'"
        elif hasattr(el, 'style') and hasattr(el.style, 'text') and el.style.text:
            exp_str += f" Styled Text: '{el.style.text}'"
        elif isinstance(el, tempo.MetronomeMark) and el.text:
            exp_str += f" Tempo Text: '{el.text}'"
    return exp_str

def detect_signature_changes(part):
    previous_time = None
    previous_key = None

    ks_changes = {}
    ts_changes = {}



    for measure in part.getElementsByClass(stream.Measure):
        m_num = measure.measureNumber

        # Check for time signature change
        ts = measure.getElementsByClass(meter.TimeSignature)
        if ts:
            ts = ts[0]  # In case of multiple, take the first
            if previous_time is None or ts.ratioString != previous_time.ratioString:
                ts_changes[m_num] = ts.ratioString
                previous_time = ts

        # Check for key signature change
        ks = measure.getElementsByClass(key.KeySignature)
        if ks:
            ks = ks[0]  # In case of multiple, take the first
            if previous_key is None or ks.sharps != previous_key.sharps:
                ks_changes[m_num] = ks.asKey().name
                previous_key = ks
    return ts_changes, ks_changes                