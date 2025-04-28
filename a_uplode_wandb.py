import os
import wandb
from tqdm import tqdm

# 1. 初始化wandb
wandb.init(
    project="End2End-5-lines_1",  # 你的wandb项目名
    name="upload_all_images",  # 新的一个run名字
    job_type="upload",
)

# 2. 设置实验目录
exp_name = "0428-194856-End2End-5-lines-XiJu"  # 你的exp_name
result_dir = f"./results/{exp_name}"

# 3. 收集所有epoch的layout、render、recover图
layout_pngs = sorted([f for f in os.listdir(result_dir) if f.endswith(".png") and f.startswith("epoch")])

for layout_file in tqdm(layout_pngs, desc="Uploading images for each Epoch"):
    epoch_idx = layout_file.replace(".png", "")  # 如 epoch0, epoch1

    # 找到对应的渲染图和复原图
    render_file = f"img1_render_{epoch_idx}.png"
    recover_file = f"img1_rec_{epoch_idx}.png"

    layout_path = os.path.join(result_dir, layout_file)
    render_path = os.path.join(result_dir, render_file)
    recover_path = os.path.join(result_dir, recover_file)

    log_data = {}

    # 镜片layout图
    if os.path.exists(layout_path):
        log_data[f"lens_layout/{epoch_idx}"] = wandb.Image(layout_path)

    # 渲染图（失真图）
    if os.path.exists(render_path):
        log_data[f"rendered_image/{epoch_idx}"] = wandb.Image(render_path)

    # 复原图（修复图）
    if os.path.exists(recover_path):
        log_data[f"recovered_image/{epoch_idx}"] = wandb.Image(recover_path)

    if log_data:
        wandb.log(log_data)

wandb.finish()
