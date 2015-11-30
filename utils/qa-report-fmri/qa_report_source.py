#!/usr/bin/env python
#
# @author:  Bob Dougherty
#

import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import nibabel as nb
import os
import numpy as np
from glob import glob
from nipy.algorithms.registration import affine,Realign4d
from dipy.segment.mask import median_otsu
import sys
import json
import argparse
import time
import shutil

qa_version = 1.0

def add_subplot_axes(fig, ax, rect, axisbg='w'):
    box = ax.get_position()
    width = box.width
    height = box.height
    inax_position  = ax.transAxes.transform(rect[0:2])
    transFigure = fig.transFigure.inverted()
    infig_position = transFigure.transform(inax_position)
    x = infig_position[0]
    y = infig_position[1]
    width *= rect[2]
    height *= rect[3]  # <= Typo was here
    subax = fig.add_axes([x,y,width,height],axisbg=axisbg)
    x_labelsize = subax.get_xticklabels()[0].get_size()
    y_labelsize = subax.get_yticklabels()[0].get_size()
    x_labelsize *= rect[2]**0.5
    y_labelsize *= rect[3]**0.5
    subax.xaxis.set_tick_params(labelsize=x_labelsize)
    subax.yaxis.set_tick_params(labelsize=y_labelsize)
    return subax

def plot_data(ts_z, abs_md, rel_md, tsnr, num_spikes, spike_thresh, outfile):
    import matplotlib.pyplot as plt
    '''Plot the per-slice z-score timeseries represented by t_z.'''
    c = np.vstack((np.linspace(0,1.,ts_z.shape[0]), np.linspace(1,0,ts_z.shape[0]), np.ones((2,ts_z.shape[0])))).T
    sl_num = np.tile(range(ts_z.shape[0]), (ts_z.shape[1], 1)).T
    fig = plt.figure(figsize=(16,8))
    ax1 = fig.add_subplot(211)
    t = np.arange(0,len(abs_md))
    ax1.plot(t, abs_md, 'k-')
    ax1.plot(t, rel_md, 'gray')
    ax1.set_xlabel('Time (frame #)')
    ax1.set_ylabel('Mean Displacement (mm)')
    ax1.axis('tight')
    ax1.grid()
    ax1.set_title('Subject Motion')
    ax1.legend(('absolute', 'relative'), loc='best', prop={'size':10})
    ax2 = fig.add_subplot(212)
    for sl in range(ts_z.shape[0]):
        ax2.plot(ts_z[sl,:], color=c[sl,:])
    ax2.plot((0,ts_z.shape[1]),(-spike_thresh,-spike_thresh),'k:')
    ax2.plot((0,ts_z.shape[1]),(spike_thresh,spike_thresh),'k:')
    ax2.set_xlabel('time (frame #)')
    ax2.set_ylabel('Signal Intensity (z-score)')
    ax2.axis('tight')
    ax2.grid()
    if num_spikes==1:
        ax2.set_title('Spike Plot (%d spike, tSNR=%0.2f)' % (num_spikes, tsnr))
    else:
        ax2.set_title('Spike Plot (%d spikes, tSNR=%0.2f)' % (num_spikes, tsnr))
    cbax = add_subplot_axes(fig, ax2, [.85,1.11, 0.25,0.05])
    plt.imshow(np.tile(c,(2,1,1)).transpose((0,1,2)), axes=cbax)
    cbax.set_yticks([])
    cbax.set_xlabel('Slice number')
    plt.tight_layout()
    plt.savefig(outfile, bbox_inches='tight')

def mask(d, raw_d=None, nskip=3, mask_bad_end_vols=True):
    mn = d[:,:,:,nskip:].mean(3)
    masked_data, mask = median_otsu(mn, 3, 2)
    mask = np.concatenate((np.tile(True, (d.shape[0], d.shape[1], d.shape[2], nskip)),
                           np.tile(np.expand_dims(mask==False, 3), (1,1,1,d.shape[3]-nskip))),
                           axis=3)
    if mask_bad_end_vols:
        # Some runs have corrupt volumes at the end (e.g., mux scans that are stopped prematurely). Mask those too.
        # But... motion correction might have interpolated the empty slices such that they aren't exactly zero.
        # So use the raw data to find these bad volumes.
        # 2015.10.29 RFD: this caused problems with some non-mux EPI scans that (inexplicably)
        # have empty slices at the top of the brain. So we'll disable it for now.
        if raw_d!=None:
            slice_max = raw_d.max(0).max(0)
        else:
            slice_max = d.max(0).max(0)
        bad = np.any(slice_max==0, axis=0)
        # We don't want to miss a bad volume somewhere in the middle, as that could be a valid artifact.
        # So, only mask bad vols that are contiguous to the end.
        mask_vols = np.array([np.all(bad[i:]) for i in range(bad.shape[0])])
    # Mask out the skip volumes at the beginning
    mask_vols[0:nskip] = True
    mask[:,:,:,mask_vols] = True
    brain = np.ma.masked_array(d, mask=mask)
    good_vols = np.logical_not(mask_vols)
    return brain,good_vols

def find_spikes(d, spike_thresh):
    slice_mean = d.mean(axis=0).mean(axis=0)
    t_z = (slice_mean - np.atleast_2d(slice_mean.mean(axis=1)).T) / np.atleast_2d(slice_mean.std(axis=1)).T
    spikes = np.abs(t_z)>spike_thresh
    spike_inds = np.transpose(spikes.nonzero())
    # mask out the spikes and recompute z-scores using variance uncontaminated with spikes.
    # This will catch smaller spikes that may have been swamped by big ones.
    d.mask[:,:,spike_inds[:,0],spike_inds[:,1]] = True
    slice_mean2 = d.mean(axis=0).mean(axis=0)
    t_z = (slice_mean - np.atleast_2d(slice_mean.mean(axis=1)).T) / np.atleast_2d(slice_mean2.std(axis=1)).T
    spikes = np.logical_or(spikes, np.abs(t_z)>spike_thresh)
    spike_inds = np.transpose(spikes.nonzero())
    return((spike_inds, t_z))

def estimate_motion(nifti_image):
    # BEGIN STDOUT SUPRESSION
    actualstdout = sys.stdout
    sys.stdout = open(os.devnull,'w')
    # We want to use the middle time point as the reference. But the algorithm does't allow that, so fake it.
    ref_vol = nifti_image.shape[3]/2 + 1
    ims = nb.four_to_three(nifti_image)
    reg = Realign4d(nb.concat_images([ims[ref_vol]] + ims)) # in the next release, we'll need to add tr=1.

    reg.estimate(loops=3) # default: loops=5
    aligned = reg.resample(0)[:,:,:,1:]
    sys.stdout = actualstdout
    # END STDOUT SUPRESSION
    abs_disp = []
    rel_disp = []
    transrot = []
    prev_T = None
    # skip the first one, since it's the reference volume
    for T in reg._transforms[0][1:]:
        # get the full affine for this volume by pre-multiplying by the reference affine
        #mc_affine = np.dot(ni.get_affine(), T.as_affine())
        transrot.append(T.translation.tolist()+T.rotation.tolist())
        # Compute the mean displacement
        # See http://www.fmrib.ox.ac.uk/analysis/techrep/tr99mj1/tr99mj1/node5.html
        # radius of the spherical head assumption (in mm):
        R = 80.
        # The center of the volume. Assume 0,0,0 in world coordinates.
        # Note: it might be better to use the center of mass of the brain mask.
        xc = np.matrix((0,0,0)).T
        T_error = T.as_affine() - np.eye(4)
        A = np.matrix(T_error[0:3,0:3])
        t = np.matrix(T_error[0:3,3]).T
        abs_disp.append(np.sqrt( R**2. / 5 * np.trace(A.T * A) + (t + A*xc).T * (t + A*xc) ).item())
        if prev_T!=None:
            T_error = T.as_affine() - prev_T.as_affine() # - np.eye(4)
            A = np.matrix(T_error[0:3,0:3])
            t = np.matrix(T_error[0:3,3]).T
            rel_disp.append(np.sqrt( R**2. / 5 * np.trace(A.T * A) + (t + A*xc).T * (t + A*xc) ).item())
        else:
            rel_disp.append(0.0)
        prev_T = T
    return aligned,np.array(abs_disp),np.array(rel_disp),np.array(transrot)

def compute_qa(ni, tr, spike_thresh=6., nskip=4):
    brain,good_vols = mask(ni.get_data(), nskip=nskip)
    t = np.arange(0.,brain.shape[3]) * tr
    # Get the global mean signal and subtract it out for spike detection
    global_ts = brain.mean(0).mean(0).mean(0)
    # Simple z-score-based spike detection
    spike_inds,t_z = find_spikes(brain - global_ts, spike_thresh)
    # Compute temporal snr on motion-corrected data,
    aligned,abs_disp,rel_disp,transrot = estimate_motion(ni)
    brain_aligned = np.ma.masked_array(aligned.get_data(), brain.mask)
    # Remove slow-drift (3rd-order polynomial) from the variance
    global_ts_aligned = brain_aligned.mean(0).mean(0).mean(0)
    global_trend = np.poly1d(np.polyfit(t[good_vols], global_ts_aligned[good_vols], 3))(t)
    tsnr = brain_aligned.mean(axis=3) / (brain_aligned - global_trend).std(axis=3)
    # convert rotations to degrees
    transrot[:,3:] *= 180./np.pi
    return transrot,abs_disp,rel_disp,tsnr,global_ts,t_z,spike_inds

def generate_qa_report(epoch_id, nimspath, force=False, spike_thresh=6., nskip=4):
    import transaction
    import sqlalchemy
    from nimsgears.model import *
    # Note: the caller may have locked the db, so we should be sure to commit the transaction asap.
    start_secs = time.time()
    epoch = Epoch.get(epoch_id)
    if force or epoch.qa_status==u'pending' or epoch.qa_status==u'rerun':
        epoch.qa_status = u'running'
        transaction.commit()
        DBSession.add(epoch)
    else:
        if epoch.qa_status==u'running':
            print('%s epoch id %d (%s) QA: appears to be running; aborting.' % (time.asctime(), epoch_id, str(epoch)))
        else:
            print('%s epoch id %d (%s) QA: appears to be done already; aborting. Use "--force" to redo it.' % (time.asctime(), epoch_id, str(epoch)))
        transaction.commit()
        return

    print('%s epoch id %d (%s) QA: Starting QA report...' % (time.asctime(), epoch_id, str(epoch)))
    # FIXME: use ds.kind==u'qa'
    qa_ds = [ds for ds in epoch.datasets if ds.filetype==u'json' and ds.label==u'QA']
    if len(qa_ds)>0:
        if force:
            for ds in qa_ds:
                if os.path.isdir(os.path.join(nimspath, ds.relpath)):
                    shutil.rmtree(os.path.join(nimspath, ds.relpath))
                ds.delete()
            transaction.commit()
            DBSession.add(epoch)
    ni_ds = [ds for ds in epoch.datasets if ds.filetype==u'nifti']
    if len(ni_ds)<1:
        # Keep it pending, since the nifti might be being generated.
        print("%s epoch id %d (%s) QA: Epoch has no nifti; aborting." % (time.asctime(), epoch_id, str(epoch)))
        epoch.qa_status = u'pending'
    else:
        ni_fname = os.path.join(nimspath, ni_ds[0].relpath, ni_ds[0].filenames[0])
        ni = nb.load(ni_fname)
        tr = ni.get_header().get_zooms()[3]
        dims = ni.get_shape()
        if len(dims)<4 or dims[3]<nskip+3:
            print("%s epoch id %d (%s) QA: not enough timepoints in nifti; aborting." % (time.asctime(), epoch_id, str(epoch)))
            epoch.qa_status = u'abandoned'
        else:
            qa_file_name = epoch.name + u'_qa'
            print("%s epoch id %d (%s) QA: computing report..." % (time.asctime(), epoch_id, str(epoch)))
            transrot,abs_disp,rel_disp,tsnr,global_ts,t_z,spike_inds = compute_qa(ni, tr, spike_thresh, nskip)
            median_tsnr = np.ma.median(tsnr)[0]
            qa_ds = Dataset.at_path(nimspath, u'json')
            qa_ds.filenames = [qa_file_name + u'.json', qa_file_name + u'.png']
            qa_ds.kind = u'qa'
            qa_ds.container = epoch
            json_file = os.path.join(nimspath, qa_ds.relpath, qa_ds.filenames[0])
            print("%s epoch id %d (%s) QA: writing report to %s..." % (time.asctime(), epoch_id, str(epoch), json_file))
            with open(json_file, 'w') as fp:
                json.dump({ 'version': qa_version,
                            'dataset': ni_fname, 'tr': tr.tolist(),
                            'frame #': range(0,brain.shape[3]),
                            'transrot': transrot.round(4).tolist(),
                            'mean displacement': abs_disp.round(2).tolist(),
                            'relative displacement': rel_disp.round(2).tolist(),
                            'max md': rel_disp.max().round(3).astype(float),
                            'median md': np.median(rel_disp).round(3).astype(float),
                            'temporal SNR (median)': median_tsnr.round(3).astype(float),
                            'global mean signal': global_ts.round(3).tolist(fill_value=round(global_ts.mean(),3)),
                            'timeseries zscore': t_z.round(1).tolist(fill_value=0),
                            'spikes': spike_inds.tolist(),
                            'spike thresh': spike_thresh},
                          fp)
            img_file = os.path.join(nimspath, qa_ds.relpath, qa_ds.filenames[1])
            print("%s epoch id %d (%s) QA: writing image to %s..." % (time.asctime(), epoch_id, str(epoch), img_file))
            plot_data(t_z, abs_disp, rel_disp, median_tsnr, spike_inds.shape[0], spike_thresh, img_file)
        # the state may have changed while we were processing...
        if epoch.qa_status!=u'rerun':
            epoch.qa_status = u'done'
    print("%s epoch id %d (%s) QA: Finished in %0.2f minutes." % (time.asctime(), epoch_id, str(epoch), (time.time()-start_secs)/60.))
    transaction.commit()
    return

def clean_up(nims_path):
    import transaction
    import sqlalchemy
    from nimsgears.model import *
    ep = Epoch.query.filter((Epoch.qa_status==u'done')).filter(Epoch.scan_type==scan_type).order_by(Epoch.timestamp.desc()).all()
    eids = [e.id for e in ep]
    for eid in eids:
        epoch = Epoch.get(eid)
        qa_ds = [ds for ds in epoch.datasets if ds.filetype==u'json' and ds.label==u'QA']
        if len(qa_ds)==0:
            epoch.qa_status=u'rerun'
        else:
            n = len(qa_ds)
            for ds in qa_ds:
                if not os.path.exists(os.path.join(nimspath, ds.relpath, ds.filenames[0])):
                    if os.path.isdir(os.path.join(nimspath, ds.relpath)):
                        shutil.rmtree(os.path.join(nimspath, ds.relpath))
                    ds.delete()
                    n -= 1
            if n==0:
                epoch.qa_status=u'rerun'
        transaction.commit()
    return

def run_a_job(nims_path, scan_type, spike_thresh, nskip, lock=True):
    import transaction
    import sqlalchemy
    from nimsgears.model import *
    # Get the latest functional epoch without qa and try it. (.desc() means descending order)
    # We need to lock the column so that another process doesn't pick this one up before we have a chance to
    # commit the transaction that marks it as 'running'.
    epoch = (Epoch.query.join(Dataset)
                        .filter((Epoch.qa_status==u'pending') | (Epoch.qa_status==u'rerun'))
                        .filter(Epoch.scan_type==scan_type)
                        .filter(Epoch.trashtime==None)
                        .filter(Dataset.filetype==u'nifti')
                        .order_by(Epoch.timestamp.desc()))
    if lock:
        epoch = epoch.with_lockmode('update').first()
    else:
        epoch = epoch.first()
    if epoch:
        epoch_id = epoch.id
        # Set force=True here so that any old QA files will be cleaned up. We've already filtered by
        # qs_status. Force a rerun of the qa by simply resetting the qa_status flag to 'rerun'.
        try:
            generate_qa_report(epoch_id, nims_path, force=True, spike_thresh=spike_thresh, nskip=nskip)
        except Exception as e:
            print e
            Epoch.get(epoch_id).qa_status=u'failed'
            transaction.commit()
    else:
        time.sleep(10)

class ArgumentParser(argparse.ArgumentParser):
    def __init__(self):
        super(ArgumentParser, self).__init__()
        self.description = """Run CNI quality assurance metrics and save the qa report in the NIMS database."""
        self.add_argument('db_uri', metavar='URI', help='NIMS database URI')
        self.add_argument('nims_path', metavar='DATA_PATH', help='NIMS data location (must be writable)')
        self.add_argument('-f', '--force', default=False, action='store_true', help='force qa to run even it exists.')
        self.add_argument('-s', '--session_id', type=int, help='To run QA metrics on all epochs in a session, pass the session id (here) or exam # (below).')
        self.add_argument('-x', '--exam_num', type=int, help='To run QA metrics on all epochs in a session, pass the exam # (here) or session id (above).')
        self.add_argument('-e', '--epoch_id', type=int, help='Run QA metrics on just this epoch.')
        self.add_argument('-t', '--spike_thresh', type=float, default=6., metavar='[6.0]', help='z-score threshold for spike detector.')
        self.add_argument('-n', '--nskip', type=int, default=6, metavar='[6]', help='number of initial timepoints to skip.')
        self.add_argument('-j', '--jobs', type=int, default=4, metavar='[4]', help='Number of jobs to run in parallel.')

if __name__ == '__main__':
    import multiprocessing
    args = ArgumentParser().parse_args()
    init_model(sqlalchemy.create_engine(args.db_uri))
    scan_type = u'functional'
    if args.epoch_id:
        epochs = [args.epoch_id]
        generate_qa_report(args.epoch_id, args.nims_path, force=args.force, spike_thresh=args.spike_thresh, nskip=args.nskip)
    elif args.session_id or args.exam_num:
        if args.session_id:
            sessions = [Session.get(args.session_id)]
        else:
            sessions = Session.query.filter(Session.exam==args.exam_num).all()
        epoch_ids = [e.id for s in sessions for e in s.epochs if e.scan_type==scan_type]
        for eid in epoch_ids:
            generate_qa_report(eid, args.nims_path, force=args.force, spike_thresh=args.spike_thresh, nskip=args.nskip)
    else:
        # Run continuously, doing QA on the latest epoch without QA.
        while True:
            if args.jobs==1:
                run_a_job(args.nims_path, scan_type=scan_type, spike_thresh=args.spike_thresh, nskip=args.nskip, lock=False)
            else:
                if len(multiprocessing.active_children())<args.jobs:
                    t = multiprocessing.Process(target=run_a_job, args=(args.nims_path, scan_type, args.spike_thresh, args.nskip))
                    t.start()
                time.sleep(1)



# nims_path = '/net/cnifs/cnifs/nims'
# dsets=[d.id for d in Dataset.query.filter(Dataset.label==u'QA').all()]
# epochs = []
# for d in dsets:
#    ds = Dataset.get(d)
#    if len(ds.filenames)<2:
#        epochs.append(ds.container_id)

