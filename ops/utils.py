import torch
import numpy as np
from sklearn.metrics import confusion_matrix
import sys

log_file = "spatial.log"
log_stream = open("spatial.log", "a")

def get_grad_hook(name):
    def hook(m, grad_in, grad_out):
        log((name, grad_out[0].data.abs().mean(), grad_in[0].data.abs().mean()))
        log((grad_out[0].size()))
        log((grad_in[0].size()))

        log((grad_out[0]))
        log((grad_in[0]))

    return hook


def softmax(scores):
    es = np.exp(scores - scores.max(axis=-1)[..., None])
    return es / es.sum(axis=-1)[..., None]


def log_add(log_a, log_b):
    return log_a + np.log(1 + np.exp(log_b - log_a))


def class_accuracy(prediction, label):
    cf = confusion_matrix(prediction, label)
    cls_cnt = cf.sum(axis=1)
    cls_hit = np.diag(cf)

    cls_acc = cls_hit / cls_cnt.astype(float)

    mean_cls_acc = cls_acc.mean()

    return cls_acc, mean_cls_acc

def log(*args, file=log_stream):
    """log to a file and console"""
    if file:
        print(*args, file=file)
        file.flush()
    print(*args)
    sys.stdout.flush()
