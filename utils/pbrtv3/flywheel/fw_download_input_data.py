#!/usr/bin/env python


def download_input_data(input_acq_id, input_directory):
    """
    1. Download all INPUT files in the acquisition with ID=$2
    """
    print('Downloading acquisition files...')
    acquisition_files = fw.get_acquisition(input_acquisition_id)['files']
    for f in acquisition_files:
        print('\t%s ...' % (f['name']))
        fw.download_file_from_acquisition(input_acquisition_id, f['name'], os.path.join(input_directory, f['name']))


def download_assets(asset_string, dl_directory, input_dir):
    """
    2. Download all files in assets (contianing the ids and filenames)
    3. Unzip all cgresource files and rsync to input_dir
    """
    import tempfile
    import shutil
    assets = asset_string.split(' ')
    assets_dict = dict(zip(assets[::2], assets[1::2]))
    print('Downloading assets...')

    for a_id, f_name in assets_dict.items():

        print('\t%s/%s ...' % (a_id, f_name))
        output_file = os.path.join(dl_directory, f_name)
        fw.download_file_from_acquisition(a_id, f_name, output_file)

        # Make a temp dir and unzip there
        temp_dir = os.path.join(tempfile.gettempdir(), f_name.strip('.zip'))
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)
        cmd = 'unzip %s -d %s' % (output_file, temp_dir)
        print(cmd)
        os.system(cmd)

        # Rsync to input_dir
        cmd = 'rsync -a %s/* %s/' % (temp_dir, input_dir)
        print(cmd)
        os.system(cmd)

        # Remove tempdir
        shutil.rmtree(temp_dir)

if __name__ == "__main__":

    """
    INPUTS:
        api_key:            Flywheel API Key
        input_acq_id:       Acquisition ID containing input PBRT asset
        asset_string:       Space-seperated pairs of acquisition_id/filename for input assets
        input_directory:    Directory in which to save the inputs + assets
    """

    import os
    import sys
    import flywheel

    api_key = sys.argv[1]
    input_acq_id = sys.argv[2]
    asset_string = sys.argv[3]
    input_directory = sys.argv[4]

    # 0. Initialize Flywheel
    fw = flywheel.Flywheel(api_key)

    # 1. Download all INPUT files in the acquisition with ID=$2
    download_input_data(input_acq_id, input_directory)

    # 2. Download all files in assets (contianing the ids and filenames)
    # 3. Unzip all cgresource files to the INPUT_DIRECTORY
    # 4. Resulting in $INPUT_DIRECTORY/scene & $INPUT_DIRECTORY/textures AND $INPUT_DIRECTORY/*.pbrt
    download_assets(asset_string, '/tmp', input_dir)
