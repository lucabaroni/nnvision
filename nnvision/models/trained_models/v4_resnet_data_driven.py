import torch
import os

import nnvision
import nnfabrik
from nnfabrik.builder import get_model

# full model key

keys = [{'model_fn': 'nnvision.models.ptrmodels.task_core_gauss_readout',
  'model_hash': '4987765ae5e80eebc01a4bc60d9253f0',
  'dataset_fn': 'nnvision.datasets.monkey_loaders.monkey_static_loader_combined',
  'dataset_hash': '9ef1991a6c99e7d5af6e2a51c3a537a6',
  'trainer_fn': 'nnvision.training.trainers.nnvision_trainer',
  'trainer_hash': 'e67767f0f592b14b0bebe7d4a96c442d',
  'seed': 1000},
 {'model_fn': 'nnvision.models.ptrmodels.task_core_gauss_readout',
  'model_hash': '4987765ae5e80eebc01a4bc60d9253f0',
  'dataset_fn': 'nnvision.datasets.monkey_loaders.monkey_static_loader_combined',
  'dataset_hash': '9ef1991a6c99e7d5af6e2a51c3a537a6',
  'trainer_fn': 'nnvision.training.trainers.nnvision_trainer',
  'trainer_hash': 'e67767f0f592b14b0bebe7d4a96c442d',
  'seed': 3000},
 {'model_fn': 'nnvision.models.ptrmodels.task_core_gauss_readout',
  'model_hash': '4987765ae5e80eebc01a4bc60d9253f0',
  'dataset_fn': 'nnvision.datasets.monkey_loaders.monkey_static_loader_combined',
  'dataset_hash': '9ef1991a6c99e7d5af6e2a51c3a537a6',
  'trainer_fn': 'nnvision.training.trainers.nnvision_trainer',
  'trainer_hash': 'e67767f0f592b14b0bebe7d4a96c442d',
  'seed': 7000},
 {'model_fn': 'nnvision.models.ptrmodels.task_core_gauss_readout',
  'model_hash': '4987765ae5e80eebc01a4bc60d9253f0',
  'dataset_fn': 'nnvision.datasets.monkey_loaders.monkey_static_loader_combined',
  'dataset_hash': '9ef1991a6c99e7d5af6e2a51c3a537a6',
  'trainer_fn': 'nnvision.training.trainers.nnvision_trainer',
  'trainer_hash': 'e67767f0f592b14b0bebe7d4a96c442d',
  'seed': 8000},
 {'model_fn': 'nnvision.models.ptrmodels.task_core_gauss_readout',
  'model_hash': '4987765ae5e80eebc01a4bc60d9253f0',
  'dataset_fn': 'nnvision.datasets.monkey_loaders.monkey_static_loader_combined',
  'dataset_hash': '9ef1991a6c99e7d5af6e2a51c3a537a6',
  'trainer_fn': 'nnvision.training.trainers.nnvision_trainer',
  'trainer_hash': 'e67767f0f592b14b0bebe7d4a96c442d',
  'seed': 2000}]


model_fn = 'nnvision.models.ptrmodels.task_core_gauss_readout'
model_config =  {'input_channels': 1,
  'model_name': 'resnet50_l2_eps0_1',
  'layer_name': 'layer3.0',
  'pretrained': False,
  'bias': False,
  'final_batchnorm': True,
  'final_nonlinearity': True,
  'momentum': 0.1,
  'fine_tune': True,
  'init_mu_range': 0.4,
  'init_sigma_range': 0.6,
  'readout_bias': True,
  'gamma_readout': 3.0,
  'gauss_type': 'isotropic',
  'elu_offset': -1,}

data_info = {
    "all_sessions": {
        "input_dimensions": torch.Size([64, 1, 100, 100]),
        "input_channels": 1,
        "output_dimension": 1244,
        "img_mean": 124.54466,
        "img_std": 70.28,
    },
}

current_dir = os.path.dirname(__file__)
filename = os.path.join(current_dir, '../../data/model_weights/v4_resnet_data_driven/resnet_data_driven_1.pth.tar')
state_dict = torch.load(filename)

# load single model
v4_resnet_data_driven = get_model(
    model_fn, model_config, seed=10, data_info=data_info, state_dict=state_dict
)

# load ensemble model
from mei.modules import EnsembleModel

# fill the list ensemble names with task driven 01 - 10
ensemble_names = ['resnet_data_driven_1.pth.tar',
    'resnet_data_driven_2.pth.tar',
    'resnet_data_driven_3.pth.tar',
    'resnet_data_driven_4.pth.tar',
    'resnet_data_driven_5.pth.tar',]

base_dir = os.path.dirname(filename)
ensemble_models = []

for f in ensemble_names:
    ensemble_filename = os.path.join(base_dir, f)
    ensemble_state_dict = torch.load(ensemble_filename)
    ensemble_model = get_model(
        model_fn, model_config, seed=10, data_info=data_info, state_dict=ensemble_state_dict
    )
    ensemble_models.append(ensemble_model)

v4_resnet_data_driven_ensemble = EnsembleModel(*ensemble_models)
