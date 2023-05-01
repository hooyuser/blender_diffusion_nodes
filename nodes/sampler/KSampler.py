import bpy

from ...base_types.base_node import BaseNode

from ComfyUI.nodes import common_ksampler


class KSampler:
    SCHEDULERS = ["karras", "normal", "simple", "ddim_uniform"]
    SAMPLERS = ["euler", "euler_ancestral", "heun", "dpm_2",
                "dpm_2_ancestral", "lms", "dpm_fast", "dpm_adaptive",
                "dpmpp_2s_ancestral", "dpmpp_sde", "dpmpp_2m", "ddim",
                "uni_pc", "uni_pc_bh2"]


def to_pascal_case(s):
    return ''.join(word.capitalize() for word in s.split('_'))


SAMPLER_ITEMS = [(str(idx), to_pascal_case(s), to_pascal_case(s))
                 for idx, s in enumerate(KSampler.SAMPLERS)]

SCHEDULER_ITEMS = [(str(idx), to_pascal_case(s), to_pascal_case(s))
                   for idx, s in enumerate(KSampler.SCHEDULERS)]


class KSamplerNode(bpy.types.Node, BaseNode):
    '''A simple sampler node'''

    bl_idname = 'KSampler'
    bl_label = 'KSampler'
    bl_icon = 'FILE_FONT'

    sampler_enum: bpy.props.EnumProperty(name="Sampler",
                                         default="0",
                                         items=SAMPLER_ITEMS,
                                         update=lambda self, context: 1)

    scheduler_enum: bpy.props.EnumProperty(name="Scheduler",
                                           default="1",
                                           items=SCHEDULER_ITEMS,
                                           update=lambda self, context: 1)

    def init(self, context):
        BaseNode.base_init(self, context)
        self.index = -3
        self.inputs.new('DiffusionSocketModel', "Model")
        '''
        "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                    "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
                    "cfg": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 100.0}),
                    "sampler_name": (comfy.samplers.KSampler.SAMPLERS, ),
                    "scheduler": (comfy.samplers.KSampler.SCHEDULERS, ),
                    "positive": ("CONDITIONING", ),
                    "negative": ("CONDITIONING", ),
                    "latent_image": ("LATENT", ),
                    "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                    '''
        self.inputs.new('DiffusionSocketPositiveInt', "Seed")
        self.inputs.new('DiffusionSocketPositiveInt', "Steps")
        self.inputs["Steps"].default_value = 20
        self.inputs.new('DiffusionSocketFloat', "CFG")
        self.inputs["CFG"].default_value = 8.0
        # self.inputs.new('DiffusionSocketSampler', "Sampler")
        # self.inputs.new('DiffusionSocketScheduler', "Scheduler")
        self.inputs.new('DiffusionSocketConditioning', "Positive")
        self.inputs.new('DiffusionSocketConditioning', "Negative")
        self.inputs.new('DiffusionSocketImage', "Latent Image")
        self.inputs.new('DiffusionSocketFloat', "Denoise").default_value = 1.0
        self.inputs["Denoise"].min_value = 0.0
        self.inputs["Denoise"].max_value = 1.0
        self.inputs["Denoise"].step = 0.01
        self.outputs.new('DiffusionSocketImage', "Latent Image")

    def draw_buttons(self, context, layout):
        # create a slider for int values
        layout.prop(self, 'sampler_enum', text='')
        layout.prop(self, 'scheduler_enum', text='')

    def compute(
        self, model, seed, steps, cfg, positive, negative, latent,
            denoise):
        return common_ksampler(
            model=model,
            seed=seed,
            steps=steps,
            cfg=cfg,
            sampler_name=KSampler.SAMPLERS[int(self.sampler_enum)],
            scheduler=KSampler.SCHEDULERS[int(self.scheduler_enum)],
            positive=positive,
            negative=negative,
            latent=latent,
            denoise=denoise
        )
