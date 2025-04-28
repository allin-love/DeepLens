import imageio
import os
from tqdm import tqdm
import wandb

# 1. 实验目录
exp_name = "0427-185039-End2End-5-lines-Q6w4"  # <-- 填你的exp_name
result_dir = f"./results/{exp_name}"

# 2. 收集所有epoch的layout图
epoch_pngs = sorted([f for f in os.listdir(result_dir) if f.endswith(".png") and f.startswith("epoch")])

layout_images = []
for png_file in tqdm(epoch_pngs, desc="Collecting Layout Images"):
    img = imageio.imread(os.path.join(result_dir, png_file))
    layout_images.append(img)

# 3. 保存成GIF
gif_path = os.path.join(result_dir, "lens_evolution.gif")
imageio.mimsave(gif_path, layout_images, duration=1)  # 每帧0.5秒，可调

print(f"GIF saved to {gif_path}")

# 4. 上传GIF到wandb
wandb.init(
    project="End2End-5-lines",
    name="upload_lens_evolution_gif",
    job_type="upload_gif",
)

wandb.log({
    "lens_evolution": wandb.Video(gif_path, fps=2, format="gif")
})

wandb.finish()
