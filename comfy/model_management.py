
CPU = 0
NO_VRAM = 1
LOW_VRAM = 2
NORMAL_VRAM = 3
HIGH_VRAM = 4
MPS = 5

accelerate_enabled = False
vram_state = NORMAL_VRAM

total_vram = 0
total_vram_available_mb = -1

import sys
import psutil

forced_cpu = "--cpu" in sys.argv

set_vram_to = NORMAL_VRAM

try:
    import torch
    total_vram = torch.cuda.mem_get_info(torch.cuda.current_device())[1] / (1024 * 1024)
    total_ram = psutil.virtual_memory().total / (1024 * 1024)
    forced_normal_vram = "--normalvram" in sys.argv
    if not forced_normal_vram and not forced_cpu:
        if total_vram <= 4096:
            print("Trying to enable lowvram mode because your GPU seems to have 4GB or less. If you don't want this use: --normalvram")
            set_vram_to = LOW_VRAM
        elif total_vram > total_ram * 1.1 and total_vram > 14336:
            print("Enabling highvram mode because your GPU has more vram than your computer has ram. If you don't want this use: --normalvram")
            vram_state = HIGH_VRAM
except:
    pass

try:
    OOM_EXCEPTION = torch.cuda.OutOfMemoryError
except:
    OOM_EXCEPTION = Exception

if "--disable-xformers" in sys.argv:
    XFORMERS_IS_AVAILBLE = False
else:
    try:
        import xformers
        import xformers.ops
        XFORMERS_IS_AVAILBLE = True
    except:
        XFORMERS_IS_AVAILBLE = False

ENABLE_PYTORCH_ATTENTION = False
if "--use-pytorch-cross-attention" in sys.argv:
    torch.backends.cuda.enable_math_sdp(True)
    torch.backends.cuda.enable_flash_sdp(True)
    torch.backends.cuda.enable_mem_efficient_sdp(True)
    ENABLE_PYTORCH_ATTENTION = True
    XFORMERS_IS_AVAILBLE = False


if "--lowvram" in sys.argv:
    set_vram_to = LOW_VRAM
if "--novram" in sys.argv:
    set_vram_to = NO_VRAM
if "--highvram" in sys.argv:
    vram_state = HIGH_VRAM


if set_vram_to == LOW_VRAM or set_vram_to == NO_VRAM:
    try:
        import accelerate
        accelerate_enabled = True
        vram_state = set_vram_to
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        print("ERROR: COULD NOT ENABLE LOW VRAM MODE.")

    total_vram_available_mb = (total_vram - 1024) // 2
    total_vram_available_mb = int(max(256, total_vram_available_mb))

try:
    if torch.backends.mps.is_available():
        vram_state = MPS
except:
    pass

if forced_cpu:
    vram_state = CPU

print("Set vram state to:", ["CPU", "NO VRAM", "LOW VRAM", "NORMAL VRAM", "HIGH VRAM", "MPS"][vram_state])


current_loaded_model = None
current_gpu_controlnets = []

model_accelerated = False


def unload_model():
    global current_loaded_model
    global model_accelerated
    global current_gpu_controlnets
    global vram_state

    if current_loaded_model is not None:
        if model_accelerated:
            accelerate.hooks.remove_hook_from_submodules(current_loaded_model.model)
            model_accelerated = False

        #never unload models from GPU on high vram
        if vram_state != HIGH_VRAM:
            current_loaded_model.model.cpu()
        current_loaded_model.unpatch_model()
        current_loaded_model = None

    if vram_state != HIGH_VRAM:
        if len(current_gpu_controlnets) > 0:
            for n in current_gpu_controlnets:
                n.cpu()
            current_gpu_controlnets = []


def load_model_gpu(model):
    global current_loaded_model
    global vram_state
    global model_accelerated

    if model is current_loaded_model:
        return
    unload_model()
    try:
        real_model = model.patch_model()
    except Exception as e:
        model.unpatch_model()
        raise e
    current_loaded_model = model
    if vram_state == CPU:
        pass
    elif vram_state == MPS:
        mps_device = torch.device("mps")
        real_model.to(mps_device)
        pass
    elif vram_state == NORMAL_VRAM or vram_state == HIGH_VRAM:
        model_accelerated = False
        real_model.cuda()
    else:
        if vram_state == NO_VRAM:
            device_map = accelerate.infer_auto_device_map(real_model, max_memory={0: "256MiB", "cpu": "16GiB"})
        elif vram_state == LOW_VRAM:
            device_map = accelerate.infer_auto_device_map(real_model, max_memory={0: "{}MiB".format(total_vram_available_mb), "cpu": "16GiB"})

        accelerate.dispatch_model(real_model, device_map=device_map, main_device="cuda")
        model_accelerated = True
    return current_loaded_model

def load_controlnet_gpu(models):
    global current_gpu_controlnets
    global vram_state
    if vram_state == CPU:
        return

    if vram_state == LOW_VRAM or vram_state == NO_VRAM:
        #don't load controlnets like this if low vram because they will be loaded right before running and unloaded right after
        return

    for m in current_gpu_controlnets:
        if m not in models:
            m.cpu()

    device = get_torch_device()
    current_gpu_controlnets = []
    for m in models:
        current_gpu_controlnets.append(m.to(device))


def load_if_low_vram(model):
    global vram_state
    if vram_state == LOW_VRAM or vram_state == NO_VRAM:
        return model.cuda()
    return model

def unload_if_low_vram(model):
    global vram_state
    if vram_state == LOW_VRAM or vram_state == NO_VRAM:
        return model.cpu()
    return model

def get_torch_device():
    if vram_state == MPS:
        return torch.device("mps")
    if vram_state == CPU:
        return torch.device("cpu")
    else:
        return torch.cuda.current_device()

def get_autocast_device(dev):
    if hasattr(dev, 'type'):
        return dev.type
    return "cuda"

def xformers_enabled():
    if vram_state == CPU:
        return False
    return XFORMERS_IS_AVAILBLE

def pytorch_attention_enabled():
    return ENABLE_PYTORCH_ATTENTION

def get_free_memory(dev=None, torch_free_too=False):
    if dev is None:
        dev = get_torch_device()

    if hasattr(dev, 'type') and (dev.type == 'cpu' or dev.type == 'mps'):
        mem_free_total = psutil.virtual_memory().available
        mem_free_torch = mem_free_total
    else:
        stats = torch.cuda.memory_stats(dev)
        mem_active = stats['active_bytes.all.current']
        mem_reserved = stats['reserved_bytes.all.current']
        mem_free_cuda, _ = torch.cuda.mem_get_info(dev)
        mem_free_torch = mem_reserved - mem_active
        mem_free_total = mem_free_cuda + mem_free_torch

    if torch_free_too:
        return (mem_free_total, mem_free_torch)
    else:
        return mem_free_total

def maximum_batch_area():
    global vram_state
    if vram_state == NO_VRAM:
        return 0

    memory_free = get_free_memory() / (1024 * 1024)
    area = ((memory_free - 1024) * 0.9) / (0.6)
    return int(max(area, 0))

def cpu_mode():
    global vram_state
    return vram_state == CPU

def mps_mode():
    global vram_state
    return vram_state == MPS

def should_use_fp16():
    if cpu_mode() or mps_mode():
        return False #TODO ?

    if torch.cuda.is_bf16_supported():
        return True

    props = torch.cuda.get_device_properties("cuda")
    if props.major < 7:
        return False

    #FP32 is faster on those cards?
    nvidia_16_series = ["1660", "1650", "1630", "T500", "T550", "T600"]
    for x in nvidia_16_series:
        if x in props.name:
            return False

    return True

#TODO: might be cleaner to put this somewhere else
import threading

class InterruptProcessingException(Exception):
    pass

interrupt_processing_mutex = threading.RLock()

interrupt_processing = False
def interrupt_current_processing(value=True):
    global interrupt_processing
    global interrupt_processing_mutex
    with interrupt_processing_mutex:
        interrupt_processing = value

def processing_interrupted():
    global interrupt_processing
    global interrupt_processing_mutex
    with interrupt_processing_mutex:
        return interrupt_processing

def throw_exception_if_processing_interrupted():
    global interrupt_processing
    global interrupt_processing_mutex
    with interrupt_processing_mutex:
        if interrupt_processing:
            interrupt_processing = False
            raise InterruptProcessingException()
