import uuid
from abc import ABC, abstractmethod

from loguru import logger
from batchrl.utils.exp import init_exp_logger


class BasePolicy(ABC):
    def __init__(self, args):
        logger.info('Init AlgoTrainer')
        if "exp_name" not in args.keys():
            exp_name = str(uuid.uuid1()).replace("-","")
        else:
            exp_name = args["exp_name"]

        self.exp_logger = init_exp_logger(experiment_name = exp_name)
        self.exp_logger.set_params(args, name='hparams')

    
    def log_res(self, epoch, result):
        logger.info('Epoch : {}', epoch)
        for k,v in result.items():
            logger.info('{} : {}',k, v)
            self.exp_logger.track(v, name=k.split(" ")[0], epoch=epoch,)
            
    
    @abstractmethod
    def train(self, 
              history_buffer,
              eval_fn=None,):
        pass
    
    def _sync_weight(self, net_target, net, soft_target_tau = 5e-3):
        for o, n in zip(net_target.parameters(), net.parameters()):
            o.data.copy_(o.data * (1.0 - soft_target_tau) + n.data * soft_target_tau)
    
    
    @abstractmethod
    def save_model(self,):
        pass
    
    @abstractmethod
    def get_policy(self,):
        pass
    
    
