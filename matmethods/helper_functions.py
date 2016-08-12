import os
import json

from pymongo import MongoClient, DESCENDING
import gridfs

import zlib

from pymatgen.electronic_structure.bandstructure import BandStructureSymmLine
from pymatgen.electronic_structure.dos import Dos

from matmethods.vasp.vasp_powerups import use_fake_vasp

import matplotlib.pyplot as plt


__author__ = 'Kiran Mathew <kmathew@lbl.gov>'


def get_db(db_file):
    """
    connect to the database and return the connection
    """    
    with open(db_file) as f:
        creds = json.loads(f.read())
        conn = MongoClient(creds["host"], creds["port"])
        db = conn[creds["database"]]
        return db


def get_task_collection(db_file):
    """
    connect to the database and return task collection
    """
    db = get_db(db_file)
    with open(db_file) as f:
        creds = json.loads(f.read())
        return db[creds["collection"]]


def get_collections(db_file):
    d1 = get_task_collection(db_file).find_one({"task_label": "structure optimization"}, 
                                           sort=[("_id", DESCENDING)])
    d2 = get_task_collection(db_file).find_one({"task_label": "static"}, 
                                           sort=[("_id", DESCENDING)])
    d3 = get_task_collection(db_file).find_one({"task_label": "nscf line"}, 
                                           sort=[("_id", DESCENDING)])
    d4 = get_task_collection(db_file).find_one({"task_label": "nscf uniform"}, 
                                           sort=[("_id", DESCENDING)])
    return (d1, d2, d3, d4)


def get_bs(db_file):
    """ return bandstructure object from the database """
    d1, d2, d3, d4 = get_collections(db_file)
    db = get_db(db_file)
    fs = gridfs.GridFS(db, 'bandstructure_fs')
    bs_fs_id = d3["calcs_reversed"][0]["bandstructure_fs_id"]
    bs_json = zlib.decompress(fs.get(bs_fs_id).read())
    bs_dict = json.loads(bs_json.decode())
    return BandStructureSymmLine.from_dict(bs_dict)


def get_dos(db_file):
    """ return density of states object from the database """    
    d1, d2, d3, d4 = get_collections(db_file)
    db = get_db(db_file)
    fs = gridfs.GridFS(db, 'dos_fs')
    dos_fs_id = d4["calcs_reversed"][0]["dos_fs_id"]
    dos_json = zlib.decompress(fs.get(dos_fs_id).read())
    dos_dict = json.loads(dos_json.decode())
    return Dos.from_dict(dos_dict)


def simulate_bandstructure_vasprun(wf, ref_dir="/wkshp_shared"):
    reference_dir = os.path.join(ref_dir, "Si_bandstructure_runs")
    si_ref_dirs = {"structure optimization": os.path.join(reference_dir, "Si_structure_optimization"),
                   "static": os.path.join(reference_dir, "Si_static"),
                   "nscf uniform": os.path.join(reference_dir, "Si_nscf_uniform"),
                   "nscf line": os.path.join(reference_dir, "Si_nscf_line")}
    return use_fake_vasp(wf, si_ref_dirs)


def simulate_elasticity_vasprun(wf, deformations, ref_dir="/wkshp_shared"):
    reference_dir = os.path.join(ref_dir, "Si_elastic_runs")
    si_ref_dirs = {"structure optimization": os.path.join(reference_dir,
                                                          "Si-structure_optimization")}
    for i, deformation in enumerate(deformations):
        si_ref_dirs["elastic_deformation_"+str(i+1)] = os.path.join(reference_dir,
                                                                    "Si-elastic_deformation-"+str(i+1))
    return use_fake_vasp(wf, si_ref_dirs, params_to_check=["ENCUT"])


def plot_wf(wf, depth_factor=1.0, breadth_factor=2.0, style='rD--', markersize=10,
            markerfacecolor='blue', fontsize=12, labels_on=True,
            numerical_label=False, text_loc_factor=1.0,save_as=None):
    """ generate a visual representation of the workflow """
    keys = sorted(wf.links.keys(), reverse=True)
    points_map = {}
    points_map.update({keys[0]:(-0.5*breadth_factor, (keys[0]+1)*depth_factor)})
    for k in keys:
        if wf.links[k]:
            for i, j in enumerate(wf.links[k]):
                if not points_map.get(j, None):
                    points_map[j] = ((i-len(wf.links[k])/2.0)*breadth_factor, k*depth_factor)
    # plot lines
    for k in keys:
        for i in wf.links[k]:
            plt.plot([points_map[k][0], points_map[i][0]],
                     [points_map[k][1], points_map[i][1]],
                     style, markersize=markersize, markerfacecolor=markerfacecolor)
            if labels_on:
                if numerical_label:
                    plt.text(points_map[k][0]*text_loc_factor, points_map[k][1]*text_loc_factor,
                            str(k), fontsize=fontsize)
                    plt.text(points_map[i][0]*text_loc_factor, points_map[i][1]*text_loc_factor,
                            str(i), fontsize=fontsize)
                else:
                    plt.text(points_map[k][0]*text_loc_factor, points_map[k][1]*text_loc_factor,
                            wf.id_fw[k].name, fontsize=fontsize)
                    plt.text(points_map[i][0]*text_loc_factor, points_map[i][1]*text_loc_factor,
                            wf.id_fw[i].name, fontsize=fontsize)
    plt.axis('scaled')
    plt.axis('off')
    if save_as:
        plt.savefig(save_as)
