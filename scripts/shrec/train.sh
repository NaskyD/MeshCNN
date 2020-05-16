#!/usr/bin/env bash

## run the training
python train.py --dataroot datasets/shrec_16 --name shrec16 --ncf 64 128 256 256 --pool_res 600 450 300 180 --norm group --resblocks 1 --flip_edges 0.2 --slide_verts 0.2 --num_aug 20 --niter_decay 100

#python train.py --dataroot datasets/#####_DataSet_##### --name #####_NAME_##### --ncf 64 128 256 256 --pool_res 1600 1300 1000 700 --norm group --resblocks 1 --flip_edges 0.2 --slide_verts 0.2 --num_aug 20 --niter_decay 100 --ninput_edges 2200 --dataset_mode classification --gpu_ids 0 --export_folder ./meshes