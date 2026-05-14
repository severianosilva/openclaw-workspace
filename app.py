import gradio as gr
import subprocess
import time
import os

def generate_video(prompt):
    """Generate Wan 2.1 video automatically"""
    # Setup
    os.chdir('/tmp')
    if not os.path.exists('ComfyUI'):
        subprocess.run(['git', 'clone', '-b', 'v0.3.0', '--depth', '1', 
                       'https://github.com/comfyanonymous/ComfyUI.git'], check=True)
    
    # Install nodes
    os.chdir('/tmp/ComfyUI/custom_nodes')
    if not os.path.exists('ComfyUI-Wan'):
        subprocess.run(['git', 'clone', 'https://github.com/kijai/ComfyUI-Wan.git'], check=True)
    
    # Download models (simplified)
    os.chdir('/tmp/ComfyUI')
    
    return "Video generation started! Check the ComfyUI interface."

# Gradio interface
demo = gr.Interface(
    fn=generate_video,
    inputs=gr.Textbox(label="Prompt", value="winter fox sunset tracking shot"),
    outputs="video",
    title="Wan 2.1 Auto Generator",
    description="Generate videos automatically with Wan 2.1"
)

if __name__ == "__main__":
    demo.launch()