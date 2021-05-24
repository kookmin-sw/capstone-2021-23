
_base_ = ['./slowfast_r50_4x16x1_256e_kinetics400_rgb.py']

model = dict(
    backbone=dict(
        resample_rate=8,  # tau
        speed_ratio=8,  # alpha
        channel_ratio=8  # beta_inv
    ),
    cls_head=dict(
    num_classes=2
    )
    )

# dataset settings
# tree_path='data_center'
data_root = 'assult/train/'
data_root_val = 'assult/val/'
ann_file_train = 'assult/train.txt'
ann_file_val = 'assult/val.txt'
ann_file_test = 'assult/val.txt'
test_cfg = dict(average_clips='prob')
dataset_type = 'VideoDataset'
# model.cls_head.num_classes = 2
# data_root = 'data/kinetics400/videos_train'
# data_root_val = 'data/kinetics400/videos_val'
# ann_file_train = 'data/kinetics400/kinetics400_train_list_videos.txt'
# ann_file_val = 'data/kinetics400/kinetics400_val_list_videos.txt'
# ann_file_test = 'data/kinetics400/kinetics400_val_list_videos.txt'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_bgr=False)
train_pipeline = [
    dict(type='DecordInit'),
    dict(type='SampleFrames', clip_len=32, frame_interval=2, num_clips=1),
    dict(type='DecordDecode'),
    dict(type='Resize', scale=(-1, 256)),
    dict(type='RandomResizedCrop'),
    dict(type='Resize', scale=(224, 224), keep_ratio=False),
    dict(type='Flip', flip_ratio=0.5),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='FormatShape', input_format='NCTHW'),
    dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
    dict(type='ToTensor', keys=['imgs', 'label'])
]
val_pipeline = [
    dict(type='DecordInit'),
    dict(
        type='SampleFrames',
        clip_len=32,
        frame_interval=2,
        num_clips=1,
        test_mode=True),
    dict(type='DecordDecode'),
    dict(type='Resize', scale=(-1, 256)),
    dict(type='CenterCrop', crop_size=224),
    dict(type='Flip', flip_ratio=0),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='FormatShape', input_format='NCTHW'),
    dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
    dict(type='ToTensor', keys=['imgs'])
]
test_pipeline = [
    dict(type='DecordInit'),
    dict(
        type='SampleFrames',
        clip_len=32,
        frame_interval=2,
        num_clips=5,
        test_mode=True),
    dict(type='DecordDecode'),
    dict(type='Resize', scale=(-1, 256)),
    dict(type='ThreeCrop', crop_size=256),
    dict(type='Flip', flip_ratio=0),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='FormatShape', input_format='NCTHW'),
    dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
    dict(type='ToTensor', keys=['imgs'])
]
data = dict(
    videos_per_gpu=8,
    workers_per_gpu=4,
    train=dict(
        type=dataset_type,
        ann_file=ann_file_train,
        data_prefix=data_root,
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        ann_file=ann_file_val,
        data_prefix=data_root_val,
        pipeline=val_pipeline),
    test=dict(
        type=dataset_type,
        ann_file=ann_file_test,
        data_prefix=data_root_val,
        pipeline=test_pipeline))

# runtime settings
# cfg.setdefault('omnisource', False)
# # Modify num classes of the model in cls_head
# cfg.model.cls_head.num_classes = 2
# # We can use the pre-trained TSN model
# cfg.load_from = './checkpoints/slowfast_r50_video_4x16x1_256e_kinetics400_rgb_20200826-f85b90c5.pth'
#
# # Set up working dir to save files and logs.
# cfg.work_dir = './yoonseok1'
#
# # The original learning rate (LR) is set for 8-GPU training.
# # We divide it by 8 since we only use one GPU.
# # cfg.data.videos_per_gpu = cfg.data.videos_per_gpu // 1
# cfg.data.videos_per_gpu = 1
# cfg.optimizer.lr = cfg.optimizer.lr / 8 / 16
# cfg.total_epochs = 10
#
# # We can set the checkpoint saving interval to reduce the storage cost
# cfg.checkpoint_config.interval = 10
# # We can set the log print interval to reduce the the times of printing log
# cfg.log_config.interval = 5
#
# # Set seed thus the results are more reproducible
# cfg.seed = 0
# set_random_seed(0, deterministic=False)
# cfg.gpu_ids = range(1)

# work_dir = './work_dirs/slowfast_r50_video_3d_4x16x1_256e_kinetics400_rgb'
work_dir = './assult'
