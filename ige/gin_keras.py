"""
Importing this makes `tf.keras` submodules configurable.

Exported modules are
* activations
* layers
* losses
* metrics
* optimizers
* regularizers
* constraints
* callbacks

Members are available under gin modules with the same name.

Example usage:
```gin
import ige.gin_keras

@my_model_fn.loss = @tf.keras.losses.CategoricalCrossentropy()
@my_model_fn.kernel_regularizer = @tf.keras.regularizers.l2()
tf.keras.regularizers.l2.l = 4e-5
tf.keras.losses.CategoricalCrossentropy.from_logits = True
```
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from gin import config


def _register_callables(package, module, blacklist):
    for k in dir(package):
        if k not in blacklist:
            v = getattr(package, k)
            if callable(v):
                config.external_configurable(v, name=k, module=module)


blacklist = set(('serialize', 'deserialize', 'get'))
# These may end up moving into gin-config proper
for package, module in (
    (tf.keras.activations, 'tf.keras.activations'),
    (tf.keras.layers, 'tf.keras.layers'),
    (tf.keras.losses, 'tf.keras.losses'),
    (tf.keras.metrics, 'tf.keras.metrics'),
    (tf.keras.optimizers, 'tf.keras.optimizers'),
    (tf.keras.regularizers, 'tf.keras.regularizers'),
    (tf.keras.constraints, 'tf.keras.constraints'),
    (tf.keras.callbacks, 'tf.keras.callbacks'),
      ):
    _register_callables(package, module, blacklist)


# clean up namespace
del package, module, blacklist, _register_callables
