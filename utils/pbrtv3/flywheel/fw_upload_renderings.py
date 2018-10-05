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
    import flywheel

    api_key = sys.argv[1]
    input_directory = sys.argv[2]
    upload_project = sys.argv[3]
    acquisition_label = sys.argv[4]

    # 0. Initialize Flywheel
    fw = flywheel.Flywheel(api_key)

    # 1. UPLOAD all INPUT files that are .dat or .txt
    upload_files = list(glob.glob(os.path.join(input_directory, '*.dat')))
    upload_files.extend(glob.glob(os.path.join(input_directory, '*.txt')))

    # Create the acquisition in the session to upload.
    session_label = acquisition_label.split("_")[0]
    session_id = fw.add_session(flywheel.Session(project=upload_project, label=session_label))
    acquisition_id = fw.add_acquisition(flywheel.Acquisition(session=session_id, label=acquisition_label))
    print('Uploading files...')
    for f in upload_files:
        print('\t%s...' % (f))
        fw.upload_file_to_acquisition(acquisition_id, f)
    print('Done!')
