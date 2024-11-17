import gradio as gr

configuraciones = {
    "image-blend": {
        "input1": gr.Image(label="Source", type="filepath"),
        "input2": gr.Image(label="Destination", type="filepath"),
        "result": gr.Image(label="Result"),
    }
}