import gradio as gr

configuraciones = {
    "image-blend": {
        "input1": gr.Image(label="Source Image", type="filepath"),
        "input2": gr.Image(label="Destination Image", type="filepath"),
        "result": gr.Image(label="Result"),
    }
}