
import numpy as np
import onnx
import onnxruntime as ort

from onnx import helper, TensorProto

# Create a simple ONNX model: Y = X + X
X = helper.make_tensor_value_info(
    "X", TensorProto.FLOAT, [2]
)

Y = helper.make_tensor_value_info(
    "Y", TensorProto.FLOAT, [2]
)

node = helper.make_node(
    "Add",
    inputs=["X", "X"],
    outputs=["Y"]
)

graph = helper.make_graph(
    [node],
    "test_graph",
    [X],
    [Y]
)

model = helper.make_model(
    graph,
    opset_imports=[
        helper.make_opsetid("", 13)
    ]
)

# Use a broadly supported ONNX IR version
model.ir_version = 9

session = ort.InferenceSession(
    model.SerializeToString(),
    providers=["CPUExecutionProvider"]
)

input_data = np.array(
    [2.0, 3.0],
    dtype=np.float32
)

result = session.run(
    None,
    {"X": input_data}
)

print("ONNX execution successful!")
print("Input:", input_data)
print("Output:", result[0])
