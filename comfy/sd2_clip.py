from comfy import sd1_clip
import torch
import os

class SD2ClipModel(sd1_clip.SD1ClipModel):
    def __init__(self, arch="ViT-H-14", device="cpu", max_length=77, freeze=True, layer="penultimate", layer_idx=None):
        textmodel_json_config = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sd2_clip_config.json")
        super().__init__(device=device, freeze=freeze, textmodel_json_config=textmodel_json_config)
        self.empty_tokens = [[49406] + [49407] + [0] * 75]
        if layer == "last":
            pass
        elif layer == "penultimate":
            layer_idx = -1
            self.clip_layer(layer_idx)
        elif self.layer == "hidden":
            assert layer_idx is not None
            assert abs(layer_idx) < 24
            self.clip_layer(layer_idx)
        else:
            raise NotImplementedError()

    def clip_layer(self, layer_idx):
        if layer_idx < 0:
            layer_idx -= 1 #The real last layer of SD2.x clip is the penultimate one. The last one might contain garbage.
        if abs(layer_idx) >= 24:
            self.layer = "hidden"
            self.layer_idx = -2
        else:
            self.layer = "hidden"
            self.layer_idx = layer_idx

class SD2Tokenizer(sd1_clip.SD1Tokenizer):
    def __init__(self, tokenizer_path=None, embedding_directory=None):
        super().__init__(tokenizer_path, pad_with_end=False, embedding_directory=embedding_directory)
