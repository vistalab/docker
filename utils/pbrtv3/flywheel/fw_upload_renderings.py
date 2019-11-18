#!/usr/bin/env python


if __name__ == "__main__":

    """
    INPUTS:
        api_key:            Flywheel API Key
        input_directory:    Directory in which to save the inputs + assets
        upload_acquisition: Acquisition ID in which to upload results
    """

    import os
    import sys
    import glob
    import pytz
    import datetime
    import tzlocal
    import flywheel

    api_key = sys.argv[1]
    input_directory = sys.argv[2]
    upload_project = sys.argv[3]
    acquisition_label = sys.argv[4]
    session_label = sys.argv[5]
    subject_label = sys.argv[6]

    # If the session_label was not passed into fwrender.sh, then we will have
    # received a 'null' string here. Thus we check and if 'null' is the label,
    # we will fall back to using the acquistiion label to set the session label.
    if session_label == 'null':
        session_label = acquisition_label.split("_")[0]

    # If the subject_label was not passed into fwrender.sh, then we will have
    # received a 'null' string here. Thus we check and if 'null' is the label,
    # we will fall back to using 'renderings' as the session label.
    if subject_label == 'null':
        subject_label = 'renderings'


    # 0. Initialize Flywheel Object
    fw = flywheel.Flywheel(api_key)

    # 1. UPLOAD all INPUT files that are .dat or .txt
    upload_files = list(glob.glob(os.path.join(input_directory, '*.dat')))
    upload_files.extend(glob.glob(os.path.join(input_directory, '*.txt')))

    # Find the session if it already exists. If the session does not exist we create it.
    project_sessions = fw.get_project_sessions(upload_project)
    this_session = [ x for x in project_sessions if x['label'] == session_label and x['subject']['label'] == subject_label ]

    if this_session and len(this_session) == 1:
        session_id = this_session[0]['_id']
        print('Using existing session...')
    else:
        session_id = fw.add_session(flywheel.Session(project=upload_project, label=session_label, subject={'code': subject_label, 'label': subject_label}, timestamp=datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('America/Los_Angeles')).isoformat()))

    acquisition_id = fw.add_acquisition(flywheel.Acquisition(session=session_id, label=acquisition_label, timestamp=datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('America/Los_Angeles')).isoformat()))
    print('Uploading files...')
    for f in upload_files:
        print('\t%s...' % (f))
        fw.upload_file_to_acquisition(acquisition_id, f)
    print('Done!')
